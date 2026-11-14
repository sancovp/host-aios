#!/usr/bin/env python3
"""check_reachable — every document is reached from the top (rule every-level-describes-and-breadcrumbs-below ·
rule 26-canonical-design · rule 24).

THE LAW IT CHECKS: every document is a design document, wired upward — a top-level design reaches every `DESIGN.md`
beneath it, a `DESIGN.md` reaches every document under it, each by a one-line summary and a link — so a document
nothing reaches is lost, and a ruling written there does not bind.

WHAT IT DOES: from one start document (a top-level design or a `DESIGN.md`) it follows every link and every named path
to a file or a folder, from each `.md` file it reaches, and lists every `.md` file under the start document's folder
that nothing reaches — the files git tracks or would track (never one git ignores), or every `.md` file where the
folder is in no git checkout. Exit 1 when any is listed.

    a link            `[text](path)` · a path in backticks · a bare path with a `/` or ending in `.md` — each counted
                      only when it resolves, from the folder of the file that names it (`~/` and absolute paths too)
    a reached folder  its `CLAUDE.md`, and every `.md` file under its `.claude/rules/` and `.claude/skills/`, are
                      reached with it: Claude Code loads or lists them when a session works there — and a reached
                      `DESIGN.md` reaches its folder, since a design is read inside the folder it designs
    exempt            the files inside every folder named on the line `ARCHIVE AND PROGRAM FOLDERS:` of the start
                      document's READ ORDER, or of any `DESIGN.md` beneath it outside such a folder — evidence,
                      generated output, a program's source — each folder counted as reached by that line; a link from
                      inside such a folder reaches nothing

    python3 check_reachable.py <start document>          the list; exit 1 when a document is unreached
    python3 check_reachable.py <start document> --json   the same as a record

A gate adds DETECTION, never authority (rule 24): the law binds whether or not this runs. Its blind spot: a document
named only in prose that is no path (its bare title) is not counted as reached — give it a link.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

ARCHIVE_LINE = "ARCHIVE AND PROGRAM FOLDERS:"
_LINK = re.compile(r"\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
_TICKS = re.compile(r"`([^`\n]+)`")
_BARE = re.compile(r"(?<![\w`(\[])(~?[\w.@+-]*[\w@+-]/[\w./@+-]*|[\w.@+-]+\.md)\b/?")
_HEADING2 = re.compile(r"^##\s+(.*?)\s*$")
_TRAIL = ".,;:)]}>'\"*"


def candidates(root: str) -> list[str]:
    """Every `.md` file under root that git does not ignore — absolute paths. Outside git, every `.md` file under root
    outside a dot-folder other than `.claude`."""
    r = subprocess.run(["git", "-C", root, "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", "."],
                       capture_output=True, text=True)
    if r.returncode == 0:
        out = {os.path.normpath(os.path.join(root, p)) for p in r.stdout.split("\0") if p.endswith(".md")}
        return sorted(p for p in out if os.path.isfile(p))
    found = []
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if not d.startswith(".") or d == ".claude"]
        found += [os.path.join(dp, f) for f in fns if f.endswith(".md")]
    return sorted(found)


def read_order_archive(text: str) -> list[str] | None:
    """The folders the READ ORDER's `ARCHIVE AND PROGRAM FOLDERS:` line names, or None when the text has no such line."""
    for line in text.splitlines():
        head = line.replace(f"`{ARCHIVE_LINE}`", ARCHIVE_LINE).replace(f"**{ARCHIVE_LINE}**", ARCHIVE_LINE)
        head = head.strip().lstrip("-*· ")
        if head.startswith(ARCHIVE_LINE):
            rest = head[len(ARCHIVE_LINE):]
            names = [t.strip() for t in _TICKS.findall(rest)] or [t for t in re.split(r"[\s·,]+", rest) if t]
            return [n.rstrip("/") for n in names if n.strip("`").lower() not in ("none", "—", "-", "")]
    return None


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
        t = t.split("#", 1)[0]
        t = re.sub(r":\d+(?:[-–]\d+)?$", "", t)                       # a file:line citation names the file
        if t:
            cleaned.add(t)
    return cleaned


def resolve(token: str, base: str) -> str | None:
    p = os.path.expanduser(token) if token.startswith("~") else token
    p = p if os.path.isabs(p) else os.path.join(base, p)
    p = os.path.normpath(p)
    return p if os.path.exists(p) else None


def inside(path: str, folder: str) -> bool:
    return path == folder or path.startswith(folder.rstrip(os.sep) + os.sep)


def archive_of(start: str, root: str, pool: list[str]) -> set[str]:
    """Every folder the `ARCHIVE AND PROGRAM FOLDERS:` lines name — the start document's, then each `DESIGN.md`'s
    beneath it, shallowest first, a design inside a folder already named skipped."""
    found: set[str] = set()
    designs = [start] + sorted((p for p in pool if os.path.basename(p) == "DESIGN.md" and p != start),
                               key=lambda p: p.count(os.sep))
    for d in designs:
        if any(inside(d, a) for a in found):
            continue
        try:
            names = read_order_archive(open(d, encoding="utf-8", errors="replace").read())
        except OSError:
            continue
        for n in names or []:
            p = resolve(n, os.path.dirname(d))
            if p and os.path.isdir(p) and inside(os.path.realpath(p), root):
                found.add(os.path.realpath(p))
    return found


def check(start: str) -> dict:
    start = os.path.realpath(start)
    root = os.path.dirname(start)
    pool = candidates(root)
    reached: set[str] = set()
    archive = archive_of(start, root, pool)
    folders: set[str] = set(archive)
    queue = [start]

    def reach_file(p: str) -> None:
        if p not in reached:
            reached.add(p)
            if p.endswith(".md") and not any(inside(p, a) for a in archive):
                queue.append(p)
                if os.path.basename(p) == "DESIGN.md":
                    reach_folder(os.path.dirname(p))

    def reach_folder(d: str) -> None:
        if d in folders:
            return
        folders.add(d)
        if os.path.isfile(os.path.join(d, "CLAUDE.md")):
            reach_file(os.path.join(d, "CLAUDE.md"))
        for sub in (".claude/rules", ".claude/skills"):
            top = os.path.join(d, sub)
            for p in pool:
                if inside(p, top):
                    reach_file(p)

    reach_folder(root)
    while queue:
        f = queue.pop()
        try:
            text = open(f, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        base = os.path.dirname(f)
        for t in tokens(text):
            p = resolve(t, base)
            if not p:
                continue
            p = os.path.realpath(p)
            if not inside(p, root):
                continue
            if os.path.isdir(p):
                if not any(inside(p, a) for a in archive):
                    reach_folder(p)
            else:
                reach_file(p)
    exempt = [p for p in pool if any(inside(p, a) for a in archive)]
    unreached = [p for p in pool if p not in reached and p not in exempt]
    rel = lambda p: os.path.relpath(p, root)
    return {"start": start, "root": root, "documents": len(pool), "reached": len([p for p in pool if p in reached]),
            "exempt": len(exempt), "archive_folders": sorted(rel(a) for a in archive),
            "unreached": [rel(p) for p in unreached]}


def main() -> int:
    ap = argparse.ArgumentParser(description="list every document nothing reaches from a start document")
    ap.add_argument("start", help="a top-level design or a DESIGN.md")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not os.path.isfile(a.start):
        print(f"⛔ check_reachable: no document at {a.start} — NOTHING WAS CHECKED; this is not a pass.")
        return 1
    r = check(a.start)
    if a.json:
        print(json.dumps(r, indent=1, ensure_ascii=False))
        return 1 if r["unreached"] else 0
    if not r["unreached"]:
        print(f"check_reachable: ✔ every document under {r['root']} is reached from {os.path.basename(r['start'])} — "
              f"{r['documents']} documents: {r['reached']} reached, {r['exempt']} exempt in "
              f"{len(r['archive_folders'])} archive and program folder(s)")
        return 0
    print(f"⛔ {len(r['unreached'])} document(s) under {r['root']} that nothing reaches from "
          f"{os.path.basename(r['start'])} ({r['documents']} documents: {r['reached']} reached, {r['exempt']} exempt):")
    for p in r["unreached"]:
        print(f"   {p}")
    print("\nGive each its one-line summary and link in the parent that owns its topic — the design section, or its "
          "folder's CLAUDE.md — or name the folder it sits in on the READ ORDER's `ARCHIVE AND PROGRAM FOLDERS:` line "
          "when it is evidence, generated output or a program's source (law: rule every-level-describes-and-"
          "breadcrumbs-below).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
