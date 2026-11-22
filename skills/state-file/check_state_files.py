#!/usr/bin/env python3
"""check_state_files — THE GATE for states files, `*states.md` (rule 28 · rule 24).

THE SHAPE IT CHECKS:

    DESIGN.md holds prose, section by section, where a section is a feature.
    A feature may have its own DESIGN.md in its own dir.
    Every dir with a DESIGN.md has one `_states` rule per identity: its DEV board
      (`<project>_dev_states.md`, or the one board it has today) and, once it has work
      to track, its WORK board (`<project>_work_states.md`).
    A `_states` rule is N TABLES, each the process by which one type of deliverable is produced:
      columns = that process's general states, stated once in its dev flow; rows = the deliverables,
      every state a row has reached marked; a row is never removed for having reached its last state.
    The architecture map, the dev flows and the design each live in their own
      rule or document, and every DESIGN.md is cohered into the top-level design.

A `_states.md` holds workflow tables and nothing else. Prose has homes —
`DESIGN.md`, the diagram rules, the top-level design — and none of them is this file.

A gate adds DETECTION, never authority (rule 24): the law binds whether or not this
runs; this is what catches a file drifting from it.

    python3 <the state-file skill's folder>/check_state_files.py [paths…]   # exit 1 if deformed; a pass names every file
    python3 <the state-file skill's folder>/check_state_files.py --json     # machine-readable

Paths may be relative or absolute — every argument is made absolute first. Point it at
the board you mean: the per-dir laws depend on which dir the board sits in.

Zero files checked is NOT a pass: with nothing to check it says so and exits 1.

It checks SHAPE. Whether each row's pointer resolves (rule 29) is not checked here.

THIS FILE SHIPS INSIDE THE AIOS, beside the skill that authors the files it checks:
rules 28 and 28b and every dev flow bind to it, so a runner never reaches outside the
AIOS to satisfy the AIOS.

ITS LOCATION IS LOAD-BEARING: `--root` defaults RELATIVE TO THIS FILE — three levels up
from a project's copy (`<project>/.claude/skills/<this skill>/`), two up from the host AIOS's
`<aios>/skills/state-file/`. Move this file and the default scans the wrong tree; fix the
default and run it from an unrelated cwd before trusting it.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

# A HEADER + a leading BANNER (what the table is, its law, its pointer) is the
# only prose a states file may carry. These are the budgets, deliberately tight.
MAX_PREAMBLE_CHARS = 1_500     # everything before the first table row
MAX_CELL_CHARS = 300           # a cell is a STATE or a POINTER, never a narrative
                               # (a `## ` heading that OWNS a table is a workflow header,
                               # not prose — see _heading_owns_table below)
MAX_TRAILING_CHARS = 400       # a short residue/pointer footer, nothing more

_ROW = re.compile(r"^\s*\|")
_SEPARATOR = re.compile(r"^\s*\|(\s*:?-+:?\s*\|)+\s*$")
_SECTION = re.compile(r"^#{2,3} ")
_NOTE_HEADERS = {"note", "notes", "comment", "comments", "remarks"}
_PHASE_HOLDER_HEADERS = {"phase", "phases", "state", "status", "stage"}


def _heading_owns_table(lines: list[str], idx: int) -> bool:
    """A `## ` heading is a WORKFLOW HEADER if a table follows it before the next
    heading. A state file is N tables — one per workflow type, rows = tasks,
    columns = that workflow's phases. Only a heading with no
    table under it is appended prose."""
    for l in lines[idx + 1:]:
        if _SECTION.match(l):
            return False
        if _ROW.match(l):
            return True
    return False


def _cell_count(line: str) -> int:
    """How many cells a table row holds, as Markdown splits it: a `|` inside a backtick code span, or escaped as `\\|`,
    is text and splits nothing; the leading and trailing pipes bound the row."""
    count, code, i, s = 0, False, 0, line.strip()
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            i += 2
            continue
        if c == "`":
            code = not code
        elif c == "|" and not code:
            count += 1
        i += 1
    if not s.startswith("|"):
        count += 1
    if not s.endswith("|") or s.endswith("\\|"):
        count += 1
    return count - 1


def _has_stack(proj: str) -> bool:
    """Rule 23: a project with a DESIGN.md owes its stack — a mermaid flowchart with at least one
    dependency arrow — in `.claude/rules/21-architecture-diagrams.md`. A lone placeholder box is no stack."""
    try:
        with open(os.path.join(proj, ".claude", "rules", "21-architecture-diagrams.md")) as fh:
            text = fh.read()
    except OSError:
        return False
    return "```mermaid" in text and "flowchart" in text and "-->" in text


def check(path: str) -> list[dict]:
    try:
        with open(path) as fh:
            lines = fh.read().splitlines()
    except OSError as e:
        return [{"kind": "unreadable", "detail": str(e)}]

    first_row = next((i for i, l in enumerate(lines) if _ROW.match(l)), None)
    out: list[dict] = []

    if first_row is None:
        return [{"kind": "no_table",
                 "detail": "a _states file IS one table; this one has no table at all"}]

    preamble = sum(len(l) + 1 for l in lines[:first_row])
    if preamble > MAX_PREAMBLE_CHARS:
        out.append({"kind": "preamble_too_long",
                    "detail": f"{preamble:,} chars before the first row "
                              f"(max {MAX_PREAMBLE_CHARS:,}) — the header states what the "
                              f"table is and points at the design; it does not explain it"})

    last_row = max(i for i, l in enumerate(lines) if _ROW.match(l))
    sections = [(i + 1, l) for i, l in enumerate(lines)
                if _SECTION.match(l) and i > first_row and not _heading_owns_table(lines, i)]
    if sections:
        out.append({"kind": "appended_prose",
                    "detail": f"{len(sections)} prose section(s) with no table under them — "
                              f"first at line {sections[0][0]}: {sections[0][1][:70]!r}. "
                              f"A `## ` heading in a states file introduces a WORKFLOW TABLE; "
                              f"prose belongs in DESIGN.md / the diagram rules / the top-level design",
                    "sections": len(sections)})

    trailing = sum(len(l) + 1 for l in lines[last_row + 1:] if l.strip())
    if trailing > MAX_TRAILING_CHARS and not sections:
        out.append({"kind": "trailing_prose",
                    "detail": f"{trailing:,} chars of prose after the last row "
                              f"(max {MAX_TRAILING_CHARS:,})"})

    # THE COLUMNS ARE THE PHASES (rule 28b: rows = tasks · columns = phases · `●` = reached). A header
    # cell NAMED like a phase-holder means the phase lives in a cell as a word, not across the columns;
    # a header cell named like a note means notes are being kept in the board (rule 28: never a note).
    for i in range(len(lines) - 1):
        if not (_ROW.match(lines[i]) and _SEPARATOR.match(lines[i + 1])):
            continue
        header = [c.strip().strip("*`").lower() for c in lines[i].split("|")[1:-1]]
        if any(h in _NOTE_HEADERS for h in header):
            out.append({"kind": "notes_column",
                        "detail": f"the table at line {i + 1} has a notes column — a board shows "
                                  f"deliverables moving through phases and nothing else; notes go "
                                  f"to the project's scratchpad rule"})
        if any(h in _PHASE_HOLDER_HEADERS for h in header):
            out.append({"kind": "phase_as_value",
                        "detail": f"the table at line {i + 1} keeps the state as a WORD in one "
                                  f"column — the COLUMNS are the states, one per state, and every "
                                  f"state a row has reached is marked `●` (rule 28)"})
        # EVERY ROW HAS ITS HEADER'S CELLS: a row with fewer cells reads its marks under the wrong states, and one
        # with more holds marks under no state at all — either way the board says something false about that row.
        width = _cell_count(lines[i])
        j = i + 2
        while j < len(lines) and _ROW.match(lines[j]):
            n = _cell_count(lines[j])
            if n != width:
                out.append({"kind": "cell_count",
                            "detail": f"line {j + 1} has {n} cells where its table's header (line {i + 1}) has "
                                      f"{width} — every row carries one cell per column, so each mark sits under "
                                      f"the state it reached (rule 28)"})
            j += 1

    worst = 0
    worst_line = 0
    for i, l in enumerate(lines):
        if not _ROW.match(l):
            continue
        for cell in l.split("|")[1:-1] or l.split("|")[1:]:
            if len(cell) > worst:
                worst, worst_line = len(cell), i + 1
    if worst > MAX_CELL_CHARS:
        out.append({"kind": "essay_cell",
                    "detail": f"a cell on line {worst_line} is {worst:,} chars "
                              f"(max {MAX_CELL_CHARS}) — evidence is a POINTER "
                              f"(a path, a commit, a doc), never a paragraph (rule 29)",
                    "chars": worst})
    return out


def findings_for_backlog(rows: list[tuple[str, list[dict]]], base: str) -> list[dict]:
    """Shape them as a machine-readable backlog — stable ids, and TEXT you can copy
    straight at an agent."""
    out = []
    for path, probs in rows:
        rel = os.path.relpath(path, base)
        for p in probs:
            out.append({
                "id": f"state_file_{p['kind']}:{rel}",
                "kind": f"state_file_{p['kind']}",
                "title": f"{os.path.basename(path)}: {p['kind'].replace('_', ' ')}",
                "text": (
                    f"{rel} violates rule 28: {p['detail']}.\n\n"
                    f"A `_states` rule is N TABLES, each the process by which one type of "
                    f"deliverable is produced: its columns that process's general states, stated "
                    f"once in its dev flow; its rows the deliverables, every state each has "
                    f"reached marked, a row never removed for having reached its last state. "
                    f"Re-shape it: keep the tables, "
                    f"move prose to the DESIGN.md that owns the feature (or the diagram "
                    f"rules), and replace every essay cell with a POINTER. Then re-run "
                    f"`python3 <the state-file skill's folder>/check_state_files.py <board>`."),
                "detail": {"path": rel, **{k: v for k, v in p.items() if k != "detail"}},
            })
    return out


def _shown(path: str, base: str) -> str:
    """A checked path as the output names it: relative to the root when it sits under it, else absolute."""
    rel = os.path.relpath(path, base)
    return os.path.abspath(path) if rel.startswith("..") else rel


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--json", action="store_true", help="emit backlog findings")
    # a project's copy, `<project>/.claude/skills/<this skill>/` → three up is `<project>/`; the host AIOS keeps its
    # real copy at `<aios>/skills/state-file/` (no `.claude`) → two up. See the docstring's
    # location clause: this default is why the shipped copy works at all.
    _here = os.path.dirname(os.path.realpath(__file__))
    _up = 3 if os.path.basename(os.path.dirname(os.path.dirname(_here))) == ".claude" else 2
    ap.add_argument("--root", default=os.path.join(_here, *[".."] * _up))
    a = ap.parse_args()
    base = os.path.realpath(a.root)

    # ⛔ ABSOLUTE, ALWAYS. `dirname("board_states.md")` is "", which breaks the per-dir DESIGN.md
    # check and makes the verdict depend on the cwd.
    targets = [os.path.abspath(p) for p in a.paths] or [
        os.path.join(dp, f)
        for dp, dns, fns in os.walk(base)
        if not any(s in dp for s in ("node_modules", "/.git", "/.venv", "/dist", "__pycache__"))
        for f in fns if f.endswith("states.md")       # `x_states.md`, and the bare `states.md` too
    ]

    # ⛔⛔ ZERO FILES IS NOT A PASS. A gate that checked nothing must never print the same line as
    # a gate that checked everything and found it clean — that FALSE GREEN is how a wrong --root
    # certifies an unexamined tree.
    if not targets:
        print(f"⛔ check_state_files: NOTHING WAS CHECKED — 0 `*states.md` under {base}\n"
              f"   This is not a pass. Either the root is wrong (pass one explicitly with --root, "
              f"or name the board's path), or this project owes a board (rule 28: every "
              f"dir with a DESIGN.md has one).")
        return 1
    # ── THE PER-DIR LAWS (rule 28): one states file per identity per project dir — at most
    # one WORK board (`*_work_states.md`) and one DEV board (any other) — and only where that
    # dir has a DESIGN.md. These are properties of a DIRECTORY, not of a file, so they are
    # checked over the whole target set.
    by_dir: dict[str, list[str]] = {}
    for p in targets:
        d = os.path.dirname(p)
        proj = d[: -len("/.claude/rules")] if d.endswith("/.claude/rules") else d
        by_dir.setdefault(proj, []).append(p)

    extra: dict[str, list[dict]] = {}
    for proj, files in by_dir.items():
        work = [f for f in files if os.path.basename(f).endswith("_work_states.md")]
        dev = [f for f in files if f not in work]
        if len(work) > 1 or len(dev) > 1:
            names = ", ".join(sorted(os.path.basename(f) for f in files))
            for f in files:
                extra.setdefault(f, []).append({
                    "kind": "many_per_dir",
                    "detail": f"{len(files)} state files in {_shown(proj, base)} "
                              f"({names}) — a dir gets one per identity: its DEV board "
                              f"(`<project>_dev_states.md`, or the one board it has) and its WORK "
                              f"board (`<project>_work_states.md`). Fold the rest into those "
                              f"two, whose ROWS are the lanes; each lane's detail hangs off by pointer"})
        if not os.path.exists(os.path.join(proj, "DESIGN.md")):
            for f in files:
                extra.setdefault(f, []).append({
                    "kind": "no_design",
                    "detail": f"{_shown(proj, base)} has no DESIGN.md — a dir with no "
                              f"design has no state to keep. Write the DESIGN.md, or this is "
                              f"notes and does not belong in rules/"})
        elif not _has_stack(proj):
            for f in files:
                extra.setdefault(f, []).append({
                    "kind": "no_stack",
                    "detail": f"{_shown(proj, base)} has a DESIGN.md and no stack — rule 23: "
                              f"`.claude/rules/21-architecture-diagrams.md` holds a mermaid "
                              f"flowchart of the design's layers with its dependency arrows, "
                              f"drawn the same turn as the design (no code needed), never a "
                              f"placeholder"})

    rows = [(p, probs) for p in sorted(targets)
            if (probs := check(p) + extra.get(p, []))]

    if a.json:
        print(json.dumps(findings_for_backlog(rows, base), indent=2))
        return 0

    if not rows:
        print(f"check_state_files: {len(targets)} file(s), all workflow tables ✔")
        for path in sorted(targets):
            print(f"   ✔ {_shown(path, base)}")
        return 0
    for path, probs in rows:
        print(f"\n⛔ {_shown(path, base)}")
        for p in probs:
            print(f"   · {p['kind']}: {p['detail']}")
    print(f"\n{len(rows)} of {len(targets)} state file(s) deformed. "
          f"A _states rule is N TABLES — one per WORKFLOW TYPE (rule 28).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
