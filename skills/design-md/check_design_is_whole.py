#!/usr/bin/env python3
"""check_design_is_whole — the design is the whole of a project's writing and accounts for every line of its code
(rule 00-samaya §V · rule 26-canonical-design · rule 24).

THE LAW IT CHECKS: the ground-truth process ends only when every line of the code is accounted for in a design page,
and nothing is left in the project but design documents, code and the AIOS's own files.

WHAT IT DOES: it lists
    every code file no page accounts for from line 1 to its last line with no gap, and
    every written file that is not the design, the code or the AIOS's own files.
Exit 1 when either list holds anything.

    a code file       as the coverage gate counts one (check_design_covers_code.py, beside this file)
    accounted for     a page — DESIGN.md or a .md under design/ — holds the heading
                          ## `<the file's path from the project folder>` — N lines
                      with N the file's line count, followed by table rows whose first cell is a line range `a-b`;
                      the ranges are in order, the first starts at 1, each starts one after the one before ends, and
                      the last ends at N
    a written file    a file with a prose extension (.md .markdown .txt .rst .adoc .org) that is not code
    allowed           DESIGN.md · the pages under design/ (never one named *.vision.md, a gathering file the factoring
                      removes) · a CLAUDE.md · anything under a .claude folder · the root CHANGELOG.md · a README
                      beside a build file · a licence or a requirements file · the files of a child project (a folder
                      beneath with a DESIGN.md of its own) · build output · and the files under each folder the READ
                      ORDER names on one of these lines:
                          OUTPUTS OF USE:   folders of the project's workspace holding what using it made
                          PROGRAM TEXT:     folders whose written files are the program itself — prompts, templates,
                                            the skills it ships, fixtures
                      Never a folder of documents that say what the project is, does or is meant to be.
    not read          a code file the owner ruled is not to be read is named, in backticks, on a READ ORDER line
                      `NOT READ BY RULING:` and owes no line ranges

    python3 check_design_is_whole.py <project folder, or its DESIGN.md>
    python3 check_design_is_whole.py <project> --json     the same as a record

A gate adds DETECTION, never authority (rule 24). Its blind spot: it tells that a range is written, never that the
row beside it says what those lines do, and never that every statement of a deleted document was placed — both are
judged by a reader who built nothing.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_design_covers_code as cov  # noqa: E402

WRITTEN_EXT = {".md", ".markdown", ".txt", ".rst", ".adoc", ".org"}
BUILD_MARKERS = {"pyproject.toml", "setup.py", "setup.cfg", "package.json", "Cargo.toml", "go.mod", "pom.xml",
                 "build.gradle", "Gemfile", ".claude-plugin"}
NOT_READ_LINE = "NOT READ BY RULING:"
OUTPUTS_LINE = "OUTPUTS OF USE:"
PROGRAM_TEXT_LINE = "PROGRAM TEXT:"
_HEAD = re.compile(r"^## `([^`]+)` — ([\d,]+) lines\s*$")
_ROW = re.compile(r"^\|\s*(\d+)\s*-\s*(\d+)\s*\|")
_TICKS = re.compile(r"`([^`\n]+)`")


def is_code(root: str, rel: str) -> bool:
    parts = rel.split("/")
    if any(p in cov.BUILD_OUTPUT for p in parts):
        return False
    base = parts[-1]
    ext = os.path.splitext(base)[1].lower()
    if ext in cov.SOURCE_EXT or base in cov.BUILD_FILES:
        return True
    if not ext:
        try:
            with open(os.path.join(root, rel), "rb") as fh:
                return fh.read(2) == b"#!"
        except OSError:
            return False
    return False


def line_counts(path: str) -> set[int]:
    """The line counts a page may state for a file: the newlines in it, and one more when its last line has none."""
    with open(path, "rb") as fh:
        data = fh.read()
    n = data.count(b"\n")
    return {n, n + 1} if data and not data.endswith(b"\n") else {n}


def named_on(design_text: str, label: str) -> list[str]:
    """Every backticked name on the lines of the design that carry the label, as folder or file paths."""
    names: list[str] = []
    for line in design_text.splitlines():
        if label in line:
            names += [t.strip().rstrip("/") for t in _TICKS.findall(line.split(label, 1)[1])]
    return [n for n in names if n and n != "none"]


def under(rel: str, folders: list[str]) -> bool:
    return any(rel == f or rel.startswith(f + "/") for f in folders)


def read_pages(root: str, files: list[str]) -> dict[str, tuple[int, list[tuple[int, int]], str]]:
    """file path → (the N its heading states, its ranges in the order written, the page that holds them)."""
    found: dict[str, tuple[int, list[tuple[int, int]], str]] = {}
    pages = [p for p in files if p == "DESIGN.md" or (p.startswith("design/") and p.endswith(".md"))]
    for page in pages:
        try:
            with open(os.path.join(root, page), encoding="utf-8", errors="replace") as fh:
                lines = fh.read().splitlines()
        except OSError:
            continue
        current = None
        for line in lines:
            head = _HEAD.match(line)
            if head:
                current = head.group(1).strip()
                found[current] = (int(head.group(2).replace(",", "")), [], page)
                continue
            if line.startswith("## "):
                current = None
                continue
            row = _ROW.match(line)
            if row and current:
                found[current][1].append((int(row.group(1)), int(row.group(2))))
    return found


def check(root: str) -> dict:
    design = os.path.join(root, "DESIGN.md")
    if not os.path.isfile(design):
        return {"refused": f"no DESIGN.md at {root}"}
    with open(design, encoding="utf-8", errors="replace") as fh:
        design_text = fh.read()
    files = cov.tracked(root)
    children = sorted({os.path.dirname(p) for p in files if os.path.basename(p) == "DESIGN.md" and os.path.dirname(p)})
    not_read = named_on(design_text, NOT_READ_LINE)
    not_code = named_on(design_text, cov.NOT_CODE_LINE)
    outputs = named_on(design_text, OUTPUTS_LINE)
    program_text = named_on(design_text, PROGRAM_TEXT_LINE)
    pages = read_pages(root, files)
    folders_with_build = {os.path.dirname(p) for p in files if os.path.basename(p) in BUILD_MARKERS
                          or ".claude-plugin" in p.split("/")}

    unaccounted: list[dict] = []
    code_checked = 0
    for rel in files:
        if not is_code(root, rel) or rel.startswith("workspace/") or under(rel, children) or under(rel, not_code):
            continue
        if under(rel, not_read):
            continue
        code_checked += 1
        counts = line_counts(os.path.join(root, rel))
        if rel not in pages:
            unaccounted.append({"file": rel, "why": "no page holds its heading and its line ranges"})
            continue
        stated, ranges, page = pages[rel]
        if stated not in counts:
            unaccounted.append({"file": rel, "why": f"{page} states {stated} lines; the file has {min(counts)}"})
            continue
        if stated == 0:
            continue
        if not ranges:
            unaccounted.append({"file": rel, "why": f"{page} holds its heading and no line range"})
            continue
        expect = 1
        fault = None
        for a, b in ranges:
            if a != expect or b < a:
                fault = f"{page}: the range {a}-{b} does not start at line {expect}"
                break
            expect = b + 1
        if fault is None and expect - 1 != stated:
            fault = f"{page}: the ranges end at line {expect - 1} of {stated}"
        if fault:
            unaccounted.append({"file": rel, "why": fault})

    stray: list[dict] = []
    for rel in files:
        parts = rel.split("/")
        base = parts[-1]
        low = base.lower()
        ext = os.path.splitext(base)[1].lower()
        if ext not in WRITTEN_EXT or is_code(root, rel):
            continue
        if any(p in cov.BUILD_OUTPUT or p.endswith(".egg-info") for p in parts):
            continue
        if rel.startswith("design/") and low.endswith(".vision.md"):
            stray.append({"file": rel, "why": "a gathering file: the factoring absorbs it and removes it"})
            continue
        if rel == "DESIGN.md" or rel.startswith("design/") or base == "CLAUDE.md" or ".claude" in parts:
            continue
        if rel == "CHANGELOG.md" or low.startswith(("license", "licence", "copying", "notice")):
            continue
        if low.startswith("requirements") and ext == ".txt":
            continue
        if low.startswith("readme") and os.path.dirname(rel) in folders_with_build:
            continue
        if under(rel, children) or under(rel, outputs) or under(rel, program_text):
            continue
        stray.append({"file": rel, "why": "says something outside the design: absorb every statement, then delete it"})

    return {"design": design, "code_checked": code_checked, "pages": len({v[2] for v in pages.values()}),
            "unaccounted": unaccounted, "stray": stray}


def main() -> int:
    ap = argparse.ArgumentParser(description="the design is the whole of the project's writing and code")
    ap.add_argument("project", nargs="?", help="the project folder, or its DESIGN.md")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if not args.project:
        print("NOTHING WAS CHECKED — no project given")
        return 1
    root = os.path.abspath(args.project)
    if os.path.isfile(root):
        root = os.path.dirname(root)
    result = check(root)
    if args.json:
        print(json.dumps(result, indent=1))
        return 1 if result.get("refused") or result["unaccounted"] or result["stray"] else 0
    if result.get("refused"):
        print(f"NOTHING WAS CHECKED — {result['refused']}")
        return 1
    bad = result["unaccounted"]
    stray = result["stray"]
    if bad:
        print(f"✗ {len(bad)} code file(s) with lines no page accounts for:")
        for item in bad:
            print(f"    {item['file']} — {item['why']}")
    if stray:
        print(f"✗ {len(stray)} written file(s) outside the design, the code and the AIOS's own files:")
        for item in stray:
            print(f"    {item['file']} — {item['why']}")
    if bad or stray:
        print(f"NOT WHOLE — {result['design']}: {result['code_checked']} code files checked, "
              f"{len(bad)} unaccounted, {len(stray)} written files to absorb")
        return 1
    print(f"✔ WHOLE — {result['design']}: every line of {result['code_checked']} code files is accounted for in "
          f"{result['pages']} page(s), and no written file stands outside the design")
    return 0


if __name__ == "__main__":
    sys.exit(main())
