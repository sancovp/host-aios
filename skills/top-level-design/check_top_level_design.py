#!/usr/bin/env python3
"""check_top_level_design — THE TOP-LEVEL-DESIGN GATE (rule 00-top-level-design-is-an-lfp-rollup · rule 24).

THE SHAPE IT CHECKS:

    THE TOP-LEVEL DESIGN is the book about the tree of `DESIGN.md` documents. Every section is a
    BRIDGING explanation plus the links into the `DESIGN.md` documents it bridges; read top to
    bottom, the bridges explain the whole system, and the document CLOSES on its last line,
    `AND THAT'S THE ARCHITECTURE.` It states only the design — what must be constructed, which is
    what is constructed — and nothing else: no previous or wrong design, no state of
    construction, no history, no date, no quote.

WHAT IT REFUSES (each finding names its line, its kind and why):

    structure       a `##` number repeated or descending · a `###` number outside its parent or
                    out of order
    no_close        the last line is not `AND THAT'S THE ARCHITECTURE.`
    opening         the opening section does not say what the document is, how to read it, how
                    to change it, and where progress lives
    date            a date or a year
    quote           the user's name · a quotation · "verbatim"
    superseded      a replaced, superseded, corrected, retired or renamed reading · strikethrough
    history         the document's or the system's history: moves, evictions, rulings, sessions,
                    commits, incidents
    patch_block     ADDENDUM · UPDATED · "additive only" · a changelog or errata block
    moved_stub      a section that only says it moved
    status          a state-of-construction word or mark (BUILT, LIVE, INTENDED, PLANNED, ✅ …)
    inlined_detail  a section grown past a bridge — over the word budget, or carrying code-grain
                    detail (file:line, ports, line/test counts)

The opening section states the law, so it names the forbidden forms; the lexical kinds
(superseded · history · patch_block · status) skip it. Dates, quotes and structure are checked
everywhere.

WHERE THE DOCUMENTS ARE: each top is named by THE MASTER MAP (rule 00-canonical-doc-paths), the global rule at
`<global home>/rules/master-map.md` — the global home being --global-home, else CLAUDE_CONFIG_DIR, else the home
folder's `.claude`. Where no map is there, the one top is the ROLE THE TOP-LEVEL DESIGN, bound per installation in
`user_info.md`, read from the nearest `.claude/rules/user_info.md` above the document or the working directory, else
the template's own. An installation with neither has nothing to check: the gate says so and exits 1, which is not a
pass.

THE MAP CHECK (`--map`): the map opens with its title line (a `# ` heading); every other line that is not blank is one
map line, `- <what the top is> — [<its name>](<its top-level design>)`. It refuses: no title line · a map line with no
link, or more than one · a link that resolves to nothing (absolute, `~/`, or relative to the map's folder) · a line
over 200 characters · two lines naming one top · any text that is not a line.

    python3 check_top_level_design.py              # every top the map names, else the bound one; exit 1 if deformed
    python3 check_top_level_design.py <path>       # any document of this shape
    python3 check_top_level_design.py --map        # the map at the global home
    python3 check_top_level_design.py --map <map>  # the map at that path
    python3 check_top_level_design.py --json       # findings as machine-readable records

A gate adds DETECTION, never authority (rule 24): the law binds whether or not this runs. Red
means fix the edit, never the gate. `hook.py` beside this file runs the same check on every
Edit/Write to every top the map names (else the bound one), and the map check on every edit of the
map, and refuses an edit that adds a finding.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass

CLOSING_LINE = "AND THAT'S THE ARCHITECTURE."

# A bridge is short: a section's own prose (its heading to the next heading) past this many
# words has grown into the detail its DESIGN.md holds.
BRIDGE_WORDS = 450

_HEADING = re.compile(r"^(#{2,3}) (.*)$")
_NUMBERED = re.compile(r"^(\d+(?:\.\d+)*)([a-z]?)[.)]?\s")
_LETTERED = re.compile(r"^([A-Z])[.)]\s")


@dataclass(frozen=True)
class Finding:
    line: int
    kind: str
    snippet: str
    why: str

    @property
    def key(self) -> tuple[str, str]:
        """Identity independent of line number — what the hook compares before and after an edit."""
        return (self.kind, " ".join(self.snippet.split()).lower())


# ── the lexicons ────────────────────────────────────────────────────────────────────────────
# Each entry: (compiled pattern, why). Case-sensitive where the WORD is only a status in caps.

def _ci(p: str) -> re.Pattern:
    return re.compile(p, re.I)


DATE = [
    (re.compile(r"\b(?:19|20)\d\d-(?:0[1-9]|1[0-2])(?:-(?:0[1-9]|[12]\d|3[01]))?\b"), "an ISO date"),
    (re.compile(r"(?<![\w.§/:-])(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])(?![\w-]|\.\d)"), "a month-day date"),
    (_ci(r"\b(?:jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.? \d{1,2}(?:st|nd|rd|th)?\b"), "a named date"),
    (re.compile(r"(?<![\w.:/-])(?:19[5-9]\d|20[0-4]\d)(?![\w.:/-])"), "a year"),
]

PATCH = [
    (re.compile(r"\bADDENDUM\b|\bAddendum\b"), "an appended block — integrate the decision where it belongs"),
    (_ci(r"\badditive[ -]only\b"), "the phrase that makes appending feel safe — it IS the violation"),
    (_ci(r"\bchange ?log\b|\bupdate log\b|\berrata\b"), "a change record — git holds the versions"),
    (re.compile(r"\bUPDATED\b|\bUPDATE:|\bAMENDED\b|\bAMENDMENT\b|\bERRATUM\b"), "a patch marker"),
    (_ci(r"\[same day|\bnote added\b"), "a patch marker"),
]

SUPERSEDED = [
    (_ci(r"supersed\w*"), "a superseded reading"),
    (re.compile(r"~~"), "strikethrough — a replaced reading kept in view"),
    (_ci(r"\bpreviously\b|\bformerly\b|\bno longer\b|\bused to (?:be|say|read|mean|run|live)\b"), "a replaced reading"),
    (_ci(r"\b(?:was|were|been|now|is) replaced\b|\breplaced (?:by|with)\b"), "a replaced reading"),
    (_ci(r"\bcorrect(?:ed|ion|ions)\b|\bmis-?read(?:ing)?\b|\bconfabulat\w*"), "a correction — state the right design, never the fix"),
    (_ci(r"\bretired\b|\bdeprecated\b|\breverted\b|\bstruck\b|\brenamed\b|\bre-?scoped\b|\bre-?based\b|\bre-?homed\b"), "a replaced reading"),
    (_ci(r"\b(?:old|earlier|original|prior|previous|pre-\S+) (?:reading|version|framing|claim|wording|picture|plan)\b"), "a replaced reading"),
    (_ci(r"\bkept(?::| at its| inline| as (?:one|an) inline)\b|\(kept\b"), "a kept reading"),
]

HISTORY = [
    (_ci(r"\bevict\w*|\bmoved (?:to|into|out|whole)\b|\bhas moved\b|\bnow lives\b|\blifted (?:out|into)\b"), "a move — say where the thing IS"),
    (_ci(r"\bappended\b|\bappending\b"), "an append — the document's own history"),
    (_ci(r"\bruled\b|\brulings?\b|\bhis (?:word|call|stamp|ruling|order)\b|\bstamped\b|\bdecided\b"), "a ruling event — state the design it fixed"),
    (_ci(r"\b(?:for )?the first time\b|\boriginally\b|\bat the time\b|\bsince then\b|\bincident\b|\bpost-?mortem\b|\bautopsy\b|\bprovenance\b|\binoculat\w*"), "history"),
    (_ci(r"\b(?:prior|later|earlier|previous|past|another|parallel|fresh) sessions?\b|\bthis session\b|"
         r"\bsessions? (?:found|read|wrote|built|made|reported|believed)\b"), "a session's work — the system's history"),
    (_ci(r"\bcommit(?:s|ted)?\b|\bPR #\d+|\bmerged\b|\bpushed\b|`[0-9a-f]{7,12}`"), "a commit — git holds the history"),
    (_ci(r"\bthe repair\b|\brepair pass\b|\bthe roll-?up repair\b|\bwas written\b|\bhas been\b|\bhad been\b"), "the document's own history"),
    (_ci(r"\blanded\b|\bbanked\b|\b(?:was|were|has been|have been|got) (?:captured|recorded)\b"), "an event — state the design itself"),
]

STATUS = [
    (re.compile(r"\b(?:BUILT|UNBUILT|LIVE|DORMANT|INTENDED|ASPIRATIONAL|SHIPPED|PROPOSED|PENDING|TODO|WIP|"
                r"DONE|STUB|PLANNED|DESIGNED|OUTSTANDING|QUEUED|PARKED|DEFERRED|VERIFIED|UNVERIFIED|"
                r"CONTRACTED|IMPLEMENTED|BLOCKED|NOT BUILT|NOT YET|IN PROGRESS|WORK IN PROGRESS|"
                r"PUBLISHED|UNMERGED|SPEC'D|SPECIFIED)\b"), "a state-of-construction word"),
    (_ci(r"\bnot yet\b|\bnot built\b|\bnever built\b|\bunbuilt\b|\bhalf-built\b|\bzero code\b|"
         r"\bdoes(?:n't| not) exist yet\b|\bstill (?:open|owed|unbuilt|missing)\b|\bis owed\b|\bowed\b"), "a state of construction"),
    (_ci(r"\bcurrently\b|\bas built\b|\bas of\b|\btoday\b|\bright now\b|\bfor now\b|\bso far\b|\bat present\b|"
         r"\bis live\b|\bgoes live\b|\bproven live\b|\blive-proven\b|\bbrowser-(?:proven|verified)\b"), "a state of construction"),
    (re.compile(r"[✅⏸☐◐🚧]"), "a status mark"),
    (_ci(r"\b\d+\s*/\s*\d+\s+(?:green|pass(?:ed|ing)?|tests?|OK)\b"), "a test count — a measurement of construction"),
]

DETAIL = [
    (re.compile(r"[\w./-]+\.(?:py|ts|tsx|js|mjs|cjs|sh|json|toml|ya?ml|css|html|pl|rs|go):\d+"), "a file:line citation — code detail belongs below the bridge"),
    (re.compile(r"(?:localhost|127\.0\.0\.1)?:\d{4,5}\b(?!\.\d)"), "a port — code detail belongs below the bridge"),
    (_ci(r"\b\d[\d,]*\s*(?:lines|L|tris|commits|files|tokens|LOC)\b"), "a measurement — code detail belongs below the bridge"),
]

MOVED_HEADING = _ci(r"\b(?:moved|evicted|retired|removed|relocated)\b")

# A month-day after a counting noun is a range ("rounds 10-25"), not a date.
_COUNTED = _ci(r"\b(?:lines?|rounds?|steps?|rungs?|stations?|items?|rows?|pages?|pp\.?|chapters?|"
               r"volumes?|levels?|phases?|acts?|sections?|§+|L)\s*$")

# A quotation = an opening quote mark, then at least QUOTE_WORDS words, then the closing mark.
QUOTE_WORDS = 6
_QUOTED = re.compile(r"[\"“]([^\"”\n]+)[\"”]")


# ── the binding ────────────────────────────────────────────────────────────────────────────

def _user_info_path(start: str | None = None) -> str:
    """The installation's `user_info.md`: the nearest `.claude/rules/user_info.md` above `start` (the file
    being checked) or above the working directory — where an installation's rules are loaded from — and
    else the one beside this skill's own `rules/`, the template's."""
    for base in (start, os.getcwd()):
        if not base:
            continue
        d = os.path.realpath(os.path.expanduser(base))
        if not os.path.isdir(d):
            d = os.path.dirname(d)
        while True:
            found = os.path.join(d, ".claude", "rules", "user_info.md")
            if os.path.isfile(found):
                return found
            if os.path.dirname(d) == d:
                break
            d = os.path.dirname(d)
    here = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(here, "..", "..", "rules", "user_info.md")


def read_binding(user_info: str | None = None, start: str | None = None) -> dict:
    """The installation's bindings this gate reads: the user's NAME, THE TOP-LEVEL DESIGN, and
    THE TOP-LEVEL STATES DOC. A role the file does not bind is absent from the result."""
    path = user_info or _user_info_path(start)
    out: dict = {}
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return out
    m = re.search(r"\{NAME\}`?\s*=\s*([A-Za-z][\w-]*)", text)
    if m:
        out["name"] = m.group(1)
    for role, key in (("THE TOP-LEVEL DESIGN", "design"), ("THE TOP-LEVEL STATES DOC", "states")):
        for line in text.splitlines():
            if line.lstrip().startswith("|") and f"**{role}**" in line:
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                tick = re.search(r"`([^`]+)`", cells[-1]) if cells else None
                if tick:
                    out[key] = os.path.expanduser(tick.group(1))
                break
    return out


# ── the master map ─────────────────────────────────────────────────────────────────────────

MAP_LINE_MAX = 200
_MAP_LINK = re.compile(r"\[([^\]]+)\]\(\s*<?([^)\s>]+)>?\s*\)")


def global_home(given: str | None = None) -> str:
    """Claude Code's configuration folder: the one named, else CLAUDE_CONFIG_DIR, else the home folder's `.claude`."""
    if given:
        return os.path.realpath(os.path.expanduser(given))
    if os.environ.get("CLAUDE_CONFIG_DIR"):
        return os.path.realpath(os.path.expanduser(os.environ["CLAUDE_CONFIG_DIR"]))
    return os.path.realpath(os.path.expanduser("~/.claude"))


def map_path(home: str | None = None) -> str:
    return os.path.join(global_home(home), "rules", "master-map.md")


def _link_target(target: str, base: str) -> str:
    p = os.path.expanduser(target) if target.startswith("~") else target
    return os.path.realpath(p if os.path.isabs(p) else os.path.join(base, p))


def check_map(text: str, base: str) -> list[Finding]:
    """THE MAP CHECK — every finding about the master map's text; `base` is the map's folder."""
    out: list[Finding] = []
    lines = text.splitlines()
    seen: dict[str, int] = {}
    titled = False
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        if not titled:
            titled = True
            if not line.startswith("# "):
                out.append(Finding(i + 1, "map_title", line[:60], "the map opens with its title line, a `# ` heading"))
            continue
        if len(line) > MAP_LINE_MAX:
            out.append(Finding(i + 1, "map_long", line[:60], f"{len(line)} characters — a map line holds at most "
                                                              f"{MAP_LINE_MAX}: what the top is, and one link"))
        if not line.startswith("- "):
            out.append(Finding(i + 1, "map_text", line[:60], "text that is not a map line — the map holds its title "
                                                              "and one line per top-level design, nothing more"))
            continue
        links = _MAP_LINK.findall(line)
        if len(links) != 1:
            out.append(Finding(i + 1, "map_link", line[:60], "a map line holds exactly one link, to its top-level "
                                                              f"design — this one holds {len(links)}"))
            continue
        target = _link_target(links[0][1], base)
        if not os.path.isfile(target):
            out.append(Finding(i + 1, "map_dead_link", links[0][1][:60], "the link resolves to nothing"))
            continue
        if target in seen:
            out.append(Finding(i + 1, "map_duplicate", links[0][1][:60], f"a second line naming the top line "
                                                                          f"{seen[target]} names"))
        seen.setdefault(target, i + 1)
    if not titled:
        out.append(Finding(1, "map_title", "<empty>", "the map is empty — it opens with its title line"))
    return out


def tops_from_map(path: str) -> list[str]:
    """The top-level design each map line links, where its link resolves to a file — in the map's order."""
    base, out = os.path.dirname(path), []
    for line in open(path, encoding="utf-8", errors="replace").read().splitlines():
        if line.startswith("- "):
            links = _MAP_LINK.findall(line)
            if len(links) == 1:
                t = _link_target(links[0][1], base)
                if os.path.isfile(t) and t not in out:
                    out.append(t)
    return out


def tops(home: str | None = None, start: str | None = None) -> tuple[list[str], str | None]:
    """Every top to check, and the map they came from: the map's tops where a map is at the global home, else the
    one THE TOP-LEVEL DESIGN binding names (and no map)."""
    m = map_path(home)
    if os.path.isfile(m):
        return tops_from_map(m), m
    bound = read_binding(start=start).get("design")
    return ([os.path.realpath(bound)] if bound else []), None


# ── the check ──────────────────────────────────────────────────────────────────────────────

def _headings(lines: list[str]) -> list[tuple[int, int, str]]:
    """(index, level, title) for every `##`/`###` heading outside fenced blocks."""
    out, fence = [], False
    for i, l in enumerate(lines):
        if l.lstrip().startswith("```"):
            fence = not fence
            continue
        m = _HEADING.match(l)
        if m and not fence:
            out.append((i, len(m.group(1)), m.group(2).strip()))
    return out


def _snip(line: str, m: re.Match) -> str:
    a, b = max(0, m.start() - 30), min(len(line), m.end() + 30)
    return line[a:b].strip()


def check_text(text: str, binding: dict | None = None) -> list[Finding]:
    binding = binding or {}
    lines = text.splitlines()
    out: list[Finding] = []
    heads = _headings(lines)

    # THE OPENING = everything before the first numbered `##` section.
    first_num = next((i for i, lvl, t in heads if lvl == 2 and _NUMBERED.match(t)), len(lines))
    opening = "\n".join(lines[:first_num]).lower()
    needs = [("what this is", "WHAT the document is"),
             ("how to read", "HOW to read it"),
             ("how to change", "HOW to change it (the one legal write)")]
    states = binding.get("states")
    if states:
        needs.append((os.path.basename(states).lower(), "WHERE progress lives (the top-level states doc)"))
    for needle, what in needs:
        if needle not in opening:
            out.append(Finding(1, "opening", needle, f"the opening does not state {what} — an agent could still ask"))

    # STRUCTURE — `##` unique and ascending; `###` inside its parent and ascending.
    seen: dict[int, int] = {}
    last_top, parent, last_sub = None, None, None
    for i, lvl, title in heads:
        m = _NUMBERED.match(title)
        if lvl == 2:
            last_sub = None
            if not m or "." in m.group(1):
                parent = None
                continue
            n = int(m.group(1))
            if n in seen:
                out.append(Finding(i + 1, "structure", title[:60], f"§{n} repeats (first at line {seen[n]})"))
            elif last_top is not None and n < last_top:
                out.append(Finding(i + 1, "structure", title[:60], f"§{n} follows §{last_top} — numbers ascend"))
            seen.setdefault(n, i + 1)
            last_top, parent = n, n
            continue
        if m:
            parts = [int(x) for x in m.group(1).split(".")]
            key = (tuple(parts), m.group(2))
            if parent is None or parts[0] != parent or len(parts) < 2:
                out.append(Finding(i + 1, "structure", title[:60], f"§{m.group(1)}{m.group(2)} sits outside its parent §{parent}"))
            elif last_sub is not None and key <= last_sub:
                out.append(Finding(i + 1, "structure", title[:60], f"§{m.group(1)}{m.group(2)} does not ascend"))
            last_sub = key
        elif _LETTERED.match(title):
            key = ((ord(title[0]),), "")
            if last_sub is not None and key <= last_sub:
                out.append(Finding(i + 1, "structure", title[:60], f"§{title[0]} does not ascend"))
            last_sub = key

    # THE CLOSE.
    tail = [l.strip() for l in lines if l.strip()]
    if not tail or tail[-1] != CLOSING_LINE:
        out.append(Finding(len(lines), "no_close", (tail[-1] if tail else "<empty>")[:60],
                           f"the last line must be exactly `{CLOSING_LINE}`"))

    # MOVED STUBS — a heading that says the section moved.
    for i, lvl, title in heads:
        if MOVED_HEADING.search(title):
            out.append(Finding(i + 1, "moved_stub", title[:60], "a section that says it moved — the section goes, and so does the stub"))

    # THE LEXICAL KINDS, line by line.
    name = binding.get("name")
    name_re = re.compile(rf"\b{re.escape(name)}\b") if name else None
    fence = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if not line.strip():
            continue
        in_opening = i < first_num
        for rx, why in DATE:
            for m in rx.finditer(line):
                if why == "a month-day date" and _COUNTED.search(line[:m.start()]):
                    continue
                out.append(Finding(i + 1, "date", _snip(line, m), why))
        if name_re:
            for m in name_re.finditer(line):
                out.append(Finding(i + 1, "quote", _snip(line, m), "the user named — a document of the design names no one"))
        for m in re.finditer(r"\bverbatim\b|(?<!\*)\*[\"“]", line, re.I):   # *"…  opens a quotation; **"term" is emphasis
            out.append(Finding(i + 1, "quote", _snip(line, m), "a quotation"))
        if not fence:   # a diagram's labels are quoted strings, not quotations
            for m in _QUOTED.finditer(line):
                if len(m.group(1).split()) >= QUOTE_WORDS:
                    out.append(Finding(i + 1, "quote", _snip(line, m), "a quotation"))
        if in_opening:
            continue
        for kind, table in (("patch_block", PATCH), ("superseded", SUPERSEDED), ("history", HISTORY),
                            ("status", STATUS), ("inlined_detail", DETAIL)):
            for rx, why in table:
                for m in rx.finditer(line):
                    if kind == "history" and rx.pattern.startswith(r"\bappended") and "append-only" in line.lower():
                        continue
                    out.append(Finding(i + 1, kind, _snip(line, m), why))

    # INLINED DETAIL — a section's own prose past the bridge budget.
    bounds = [i for i, _, _ in heads] + [len(lines)]
    for k, (i, lvl, title) in enumerate(heads):
        if i < first_num:
            continue
        body = lines[i + 1:bounds[k + 1]]
        words = sum(len(re.findall(r"\S+", l)) for l in body if not l.lstrip().startswith(("```", "|---")))
        if words > BRIDGE_WORDS:
            out.append(Finding(i + 1, "inlined_detail", title[:60],
                               f"{words} words under this heading (budget {BRIDGE_WORDS}) — keep the bridge, "
                               f"link the DESIGN.md that holds the detail"))
    return sorted(out, key=lambda f: (f.line, f.kind))


def _report(path: str, found: list[Finding], n_lines: int, as_json: bool, map_: bool = False) -> int:
    if as_json:
        print(json.dumps({"path": path, "findings": [f.__dict__ for f in found]}, ensure_ascii=False, indent=1))
        return 1 if found else 0
    if not found:
        what = ("the master map: a title line, then one line and one link per top-level design, each link resolving"
                if map_ else "one continuous bridge document · closes · states only the design")
        print(f"check_top_level_design: ✔ {path}\n   {n_lines} lines · {what}")
        return 0
    print(f"⛔ {path}  ({n_lines} lines)")
    for f in found:
        print(f"   line {f.line:>5} · {f.kind:<14} · {f.snippet}  — {f.why}")
    kinds = Counter(f.kind for f in found)
    print(f"\n{len(found)} finding(s): " + " · ".join(f"{k} {v}" for k, v in kinds.most_common()))
    law = "rule 00-canonical-doc-paths" if map_ else "rule 00-top-level-design-is-an-lfp-rollup"
    print(("The master map holds its title and one line per top." if map_ else
           "The top-level design states only the design.") + f" Fix the document, never the gate (law: {law}).")
    return 1


def _read(path: str) -> str | None:
    try:
        return open(path, encoding="utf-8", errors="replace").read()
    except OSError as e:
        print(f"⛔ check_top_level_design: cannot read {path}: {e}\n   NOTHING WAS CHECKED — this is not a pass.")
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("path", nargs="?")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--user-info", help="read the bindings from this user_info.md instead of the AIOS's own")
    ap.add_argument("--map", nargs="?", const="", default=None, metavar="MAP",
                    help="check the master map — the one at this path, or the global home's")
    ap.add_argument("--global-home", help="Claude Code's configuration folder (default: CLAUDE_CONFIG_DIR, else ~/.claude)")
    a = ap.parse_args()

    if a.map is not None:
        path = os.path.abspath(os.path.expanduser(a.map)) if a.map else map_path(a.global_home)
        text = _read(path)
        if text is None:
            return 1
        return _report(path, check_map(text, os.path.dirname(path)), len(text.splitlines()), a.json, map_=True)

    if a.path:
        paths, the_map = [os.path.abspath(os.path.expanduser(a.path))], None
    elif a.user_info:
        bound = read_binding(a.user_info).get("design")
        paths, the_map = ([os.path.abspath(bound)] if bound else []), None
    else:
        paths, the_map = tops(a.global_home)
    if not paths:
        where = (f"the master map at {the_map} names no top-level design that exists" if the_map else
                 "no master map is at the global home, and this installation's user_info.md binds no THE TOP-LEVEL "
                 "DESIGN")
        print(f"⛔ check_top_level_design: NOTHING WAS CHECKED — no path given, and {where}.\n   This is not a pass. "
              "Write the map's line, bind the role, or name the document.")
        return 1
    code = 0
    if the_map and not a.json:
        print(f"check_top_level_design: {len(paths)} top(s) found through the master map at {the_map}")
    for path in paths:
        text = _read(path)
        if text is None:
            code = 1
            continue
        binding = read_binding(a.user_info, path)
        code |= _report(path, check_text(text, binding), len(text.splitlines()), a.json)
    return code


if __name__ == "__main__":
    sys.exit(main())
