#!/usr/bin/env python3
"""check_design_covers_code — the design names every file of the code (rule 26-canonical-design · rule 24).

THE LAW IT CHECKS: a project's design covers every file that exists in its code — why the file exists and how it
connects to everything else — in `DESIGN.md` itself or in a page `DESIGN.md` links, so a question about the project is
answered from the design and never by reading the code again.

WHAT IT DOES: it lists the code files under the project folder, reads `DESIGN.md` and every page it reaches, and lists
every code file whose name appears in none of them. Exit 1 when any is listed.

    a code file       a file git tracks or would track (never one git ignores) with a source extension, a build file
                      named below, or no extension and a `#!` first line; outside git, every such file outside a
                      dot-folder
    a page            a `.md` file inside the project folder that `DESIGN.md` reaches by a link or a named path, and
                      every page such a page reaches. Never counted, and never followed: a board (`*_states.md`), a
                      scratchpad, a `CHANGELOG.md`, a dated `GROUND_TRUTH_*` record, the generated `design_toc.md`, a
                      `CLAUDE.md`, another `DESIGN.md`, and every file inside a folder the READ ORDER names on its
                      line `ARCHIVE AND PROGRAM FOLDERS:` — a record or a program's own file is not a design page
    named             a page writes the file's path from the project folder, or an end of that path no other code
                      file shares — `core.py` when the project has one `core.py`, `pkg/core.py` when it has two. A
                      file written only by an end other files share is listed apart: a reader cannot tell which
                      file the line is about. A name with no extension and no folder counts only in backticks
    not checked       the files of build output (`__pycache__`, `node_modules`, `dist`, `build`, …) · the files of
                      the project's own `workspace/`, which holds what using the project made and never its program ·
                      the files under a folder beneath the project that has a `DESIGN.md` of its own, which that
                      design covers · the files inside every folder the READ ORDER names on its line
                      `COPIES, GENERATED OUTPUT AND RUN EVIDENCE:` — each such folder is printed with the number of
                      code files left unchecked in it, on a pass too. The code of a folder named on the line
                      `ARCHIVE AND PROGRAM FOLDERS:` is checked like any other: that line is about documents

    python3 check_design_covers_code.py <project folder, or its DESIGN.md>
    python3 check_design_covers_code.py <project> --ext .proto a source extension added (repeatable)
    python3 check_design_covers_code.py <project> --json       the same as a record

A gate adds DETECTION, never authority (rule 24): the law binds whether or not this runs. Its blind spot: it tells that
a file is named, never that the line beside the name says why the file exists and what it connects to — that is judged
by reading the page.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys

ARCHIVE_LINE = "ARCHIVE AND PROGRAM FOLDERS:"
NOT_CODE_LINE = "COPIES, GENERATED OUTPUT AND RUN EVIDENCE:"
SOURCE_EXT = {
    ".py", ".pyi", ".pyx", ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".sh", ".bash", ".zsh", ".fish", ".pl",
    ".pro", ".prolog", ".rb", ".go", ".rs", ".java", ".kt", ".kts", ".scala", ".swift", ".c", ".h", ".cc", ".cpp",
    ".cxx", ".hpp", ".hh", ".m", ".mm", ".cs", ".fs", ".php", ".lua", ".r", ".jl", ".ex", ".exs", ".erl", ".hs",
    ".ml", ".clj", ".lisp", ".el", ".sql", ".graphql", ".proto", ".html", ".htm", ".css", ".scss", ".sass", ".less",
    ".vue", ".svelte", ".astro", ".tf", ".hcl", ".nix", ".cmake", ".gradle", ".owl", ".ttl",
}
BUILD_FILES = {"Dockerfile", "Makefile", "Justfile", "Rakefile", "Procfile", "Containerfile"}
BUILD_OUTPUT = {"__pycache__", "node_modules", ".venv", "venv", "dist", "build", "target", ".tox", ".next",
                ".mypy_cache", ".pytest_cache", ".ruff_cache"}
NOT_A_PAGE = ("*_states.md", "*_scratchpad.md", "CHANGELOG.md", "GROUND_TRUTH_*", "design_toc.md", "CLAUDE.md",
              "DESIGN.md")
_LINK = re.compile(r"\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
_TICKS = re.compile(r"`([^`\n]+)`")
_BARE = re.compile(r"(?<![\w`(\[])(~?[\w.@+-]*[\w@+-]/[\w./@+-]*|[\w.@+-]+\.md)\b/?")
_TRAIL = ".,;:)]}>'\"*"


def inside(path: str, folder: str) -> bool:
    return path == folder or path.startswith(folder.rstrip(os.sep) + os.sep)


def tracked(root: str) -> list[str]:
    """Every file under root that git does not ignore, as paths from root. Outside git, every file outside a
    dot-folder."""
    r = subprocess.run(["git", "-C", root, "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", "."],
                       capture_output=True, text=True)
    if r.returncode == 0:
        return sorted(p for p in set(r.stdout.split("\0")) if p and os.path.isfile(os.path.join(root, p)))
    found = []
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if not d.startswith(".")]
        found += [os.path.relpath(os.path.join(dp, f), root) for f in fns]
    return sorted(found)


def is_code(root: str, rel: str, extensions: set[str]) -> bool:
    name = os.path.basename(rel)
    ext = os.path.splitext(name)[1].lower()
    if ext in extensions or name in BUILD_FILES:
        return True
    if ext or name.startswith("."):
        return False
    try:
        with open(os.path.join(root, rel), "rb") as f:
            return f.read(2) == b"#!"
    except OSError:
        return False


def build_output(rel: str) -> bool:
    parts = rel.split(os.sep)[:-1]
    return any(p in BUILD_OUTPUT or p.endswith(".egg-info") for p in parts)


def folders_on(design: str, root: str, label: str) -> list[str]:
    """The folders the design names on the line that opens with label, as real paths inside root."""
    try:
        text = open(design, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    for line in text.splitlines():
        head = line.replace(f"`{label}`", label).replace(f"**{label}**", label)
        head = head.strip().lstrip("-*· ")
        if head.startswith(label):
            rest = head[len(label):]
            names = [t.strip() for t in _TICKS.findall(rest)] or [t for t in re.split(r"[\s·,]+", rest) if t]
            out = []
            for n in names:
                if n.strip("`").lower() in ("none", "—", "-", ""):
                    continue
                p = os.path.realpath(os.path.join(root, n.rstrip("/")))
                if os.path.isdir(p) and inside(p, root):
                    out.append(p)
            return sorted(set(out))
    return []


def tokens(text: str) -> set[str]:
    """Every string in the text that could name a path: link targets, backticked spans and their words, bare paths."""
    out: set[str] = set()
    for m in _LINK.finditer(text):
        out.add(m.group(1))
    for m in _TICKS.finditer(text):
        span = m.group(1).strip()
        out.add(span)
        out.update(span.split())
    for m in _BARE.finditer(text):
        out.add(m.group(1))
    cleaned = set()
    for t in out:
        t = t.strip().lstrip("([{<'\"*").rstrip(_TRAIL)
        if not t or "://" in t or t.startswith(("mailto:", "#", "$")):
            continue
        t = re.sub(r":\d+(?:[-–]\d+)?$", "", t.split("#", 1)[0])
        if t:
            cleaned.add(t)
    return cleaned


def a_page(path: str) -> bool:
    name = os.path.basename(path)
    return path.endswith(".md") and not any(fnmatch.fnmatch(name, pat) for pat in NOT_A_PAGE)


def pages_of(design: str, root: str, archive: list[str]) -> list[str]:
    """`DESIGN.md` and every page it reaches inside root, each a real path, the design first."""
    seen = [design]
    queue = [design]
    while queue:
        f = queue.pop()
        try:
            text = open(f, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        base = os.path.dirname(f)
        for t in tokens(text):
            p = os.path.expanduser(t) if t.startswith("~") else t
            p = os.path.realpath(p if os.path.isabs(p) else os.path.join(base, p))
            if (p in seen or not os.path.isfile(p) or not a_page(p) or not inside(p, root)
                    or any(inside(p, a) for a in archive)):
                continue
            seen.append(p)
            queue.append(p)
    return seen


def mentioned(form: str, text: str, ticks: set[str]) -> bool:
    """Whether the text writes form as a path of its own — never as the tail of a longer name or a longer path. A
    name with no extension and no folder counts only in backticks."""
    if "/" not in form and not os.path.splitext(form)[1]:
        return form in ticks or ("./" + form) in ticks
    return re.search(r"(?:(?<![\w./-])|(?<=(?<![\w.])\./)|(?<=\.\./))" + re.escape(form) + r"(?!\w)", text) is not None


def named(rel: str, text: str, ticks: set[str], shared: dict[str, int]) -> str:
    """How the pages' text names the code file at rel: `yes` by its whole path, or by an end of it no other code file
    shares; `shared` only by an end of its path other code files share; `` not at all."""
    parts = rel.split(os.sep)
    only_shared = False
    for k in range(len(parts), 0, -1):
        form = "/".join(parts[-k:])
        if mentioned(form, text, ticks):
            if k == len(parts) or shared[form] == 1:
                return "yes"
            only_shared = True
    return "shared" if only_shared else ""


def check(project: str, extensions: set[str]) -> dict:
    design = os.path.realpath(project if os.path.isfile(project) else os.path.join(project, "DESIGN.md"))
    root = os.path.dirname(design)
    files = tracked(root)
    archive = folders_on(design, root, ARCHIVE_LINE)
    declared = folders_on(design, root, NOT_CODE_LINE)
    workspace = os.path.join(root, "workspace")
    children = sorted({os.path.dirname(os.path.join(root, f)) for f in files
                       if os.path.basename(f) == "DESIGN.md" and os.path.dirname(f)
                       and not any(inside(os.path.join(root, f), a) for a in archive)})
    code, built, by_declared, by_child, in_workspace = [], {}, {}, {}, 0
    for f in files:
        if not is_code(root, f, extensions):
            continue
        full = os.path.join(root, f)
        if build_output(f):
            top = f.split(os.sep)[0]
            built[top] = built.get(top, 0) + 1
            continue
        child = next((c for c in children if inside(full, c)), None)
        skip = next((d for d in declared if inside(os.path.realpath(full), d)), None)
        if skip:
            key = os.path.relpath(skip, root)
            by_declared[key] = by_declared.get(key, 0) + 1
        elif inside(full, workspace):
            in_workspace += 1
        elif child:
            key = os.path.relpath(child, root)
            by_child[key] = by_child.get(key, 0) + 1
        else:
            code.append(f)
    pages = pages_of(design, root, archive)
    text = "\n".join(open(p, encoding="utf-8", errors="replace").read() for p in pages)
    ticks = {w for span in _TICKS.findall(text) for w in [span.strip(), *span.split()]}
    ends: dict[str, int] = {}
    for f in code:
        parts = f.split(os.sep)
        for k in range(1, len(parts) + 1):
            ends["/".join(parts[-k:])] = ends.get("/".join(parts[-k:]), 0) + 1
    uncovered, shared = [], []
    for f in code:
        how = named(f, text, ticks, ends)
        if how != "yes":
            (shared if how == "shared" else uncovered).append(f)
    return {"design": design, "root": root, "code_files": len(code), "pages": [os.path.relpath(p, root) for p in pages],
            "uncovered": uncovered, "shared_name": shared, "declared_folders": by_declared, "workspace": in_workspace, "child_designs": by_child,
            "build_output": built}


def notes(r: dict) -> list[str]:
    out = []
    for folder, n in sorted(r["declared_folders"].items()):
        out.append(f"   not checked: {n} code file(s) in {folder}/ — named on the READ ORDER's `{NOT_CODE_LINE}` line")
    if r["workspace"]:
        out.append(f"   not checked: {r['workspace']} code file(s) in workspace/ — what using the project made, never "
                   f"its program")
    for folder, n in sorted(r["child_designs"].items()):
        out.append(f"   not checked: {n} code file(s) in {folder}/ — it has its own DESIGN.md; run this check there")
    for folder, n in sorted(r["build_output"].items()):
        out.append(f"   not checked: {n} code file(s) of build output under {folder}/")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="list every code file the design does not name")
    ap.add_argument("project", help="a project folder holding a DESIGN.md, or that DESIGN.md")
    ap.add_argument("--ext", action="append", default=[], help="a source extension to add, e.g. .proto")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    design = a.project if os.path.isfile(a.project) else os.path.join(a.project, "DESIGN.md")
    if not os.path.isfile(design) or os.path.basename(design) != "DESIGN.md":
        print(f"⛔ check_design_covers_code: no DESIGN.md at {design} — NOTHING WAS CHECKED; this is not a pass.")
        return 1
    extensions = SOURCE_EXT | {e if e.startswith(".") else "." + e for e in (x.lower() for x in a.ext)}
    r = check(design, extensions)
    if a.json:
        print(json.dumps(r, indent=1, ensure_ascii=False))
        return 1 if r["uncovered"] or r["shared_name"] else 0
    read = f"DESIGN.md and {len(r['pages']) - 1} page(s) it reaches"
    if not r["uncovered"] and not r["shared_name"]:
        if r["code_files"]:
            print(f"check_design_covers_code: ✔ every code file under {r['root']} is named in {r['design']} or a page "
                  f"it reaches — {r['code_files']} code file(s), {read}")
        else:
            print(f"check_design_covers_code: ∅ no code file found under {r['root']} for {r['design']} to cover — "
                  f"0 code files, {read}")
        for line in notes(r):
            print(line)
        return 0
    missing = len(r["uncovered"]) + len(r["shared_name"])
    print(f"⛔ {missing} of {r['code_files']} code file(s) under {r['root']} are not named by {r['design']} or a page "
          f"it reaches ({read}).")
    if r["uncovered"]:
        print(f"\n{len(r['uncovered'])} named nowhere:")
        for f in r["uncovered"]:
            print(f"   {f}")
    if r["shared_name"]:
        print(f"\n{len(r['shared_name'])} named only by a name other code files share — a reader cannot tell which "
              f"file the line is about; write each with its folder:")
        for f in r["shared_name"]:
            print(f"   {f}")
    for line in notes(r):
        print(line)
    print("\nGive each file its line — why it exists and what it connects to — in the design section that owns its "
          "topic, or in a page of the `design/` folder that section links (law: rule 26-canonical-design; how: the "
          "`design-md` skill).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
