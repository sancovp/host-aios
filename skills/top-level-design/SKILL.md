---
name: top-level-design
description: Check or repair a TOP-LEVEL DESIGN so it is the book about the tree of DESIGN.md documents — every section a bridge plus its links, closing on its last line, stating only the design — check THE MASTER MAP that names every top, and check that every document is reached from the top. Use before and after any write to a top-level design or the map, before a version leaves, and to install the gate that fires on every write. THE LAWS are rules 00-top-level-design-is-an-lfp-rollup, 00-canonical-doc-paths and every-level-describes-and-breadcrumbs-below
---

# top-level-design — the gates that keep each top a pure bridge document, the map whole, and every document reached

Each top AIOS has a top-level design, and THE MASTER MAP names every one: a global rule at
`<global home>/rules/master-map.md`, its title line, then one line and one link per top-level design (rule
`00-canonical-doc-paths`). Where no map is there, THE TOP-LEVEL DESIGN is the ROLE `user_info.md` binds to a file.
This skill carries the gates those rules bind to, so an installation never reaches outside the AIOS to check its
own tops.

## THE GATE — `check_top_level_design.py`, beside this file

```
python3 "${CLAUDE_SKILL_DIR}/check_top_level_design.py"              # every top the map names, else the bound one
python3 "${CLAUDE_SKILL_DIR}/check_top_level_design.py" <path>       # any document of the shape
python3 "${CLAUDE_SKILL_DIR}/check_top_level_design.py" --map        # the map at the global home
python3 "${CLAUDE_SKILL_DIR}/check_top_level_design.py" --map <map>  # a map at that path
```

On a top-level design it REFUSES, naming the line, the kind and the reason: a section number repeated or out of order ·
a last line that is not `AND THAT'S THE ARCHITECTURE.` · an opening that does not say what the document is, how to
read it, how to change it and where progress lives · a date · a quote or the user's name · a replaced, superseded or
corrected reading · the document's or the system's history · a patch block · a moved stub · a state-of-construction
word · a section grown past a bridge (over its word budget, or carrying file:line, ports and counts).

On the map it REFUSES: no title line · a map line with no link, or more than one · a link that resolves to nothing · a
line over 200 characters · two lines naming one top · any text that is not a line.

⛔ **RUN IT BARE AND READ WHAT IT SAYS.** A pass names the file it checked; no map, no binding and no path is NOTHING
CHECKED, exit 1, never a pass. Red means fix the document, never the gate.

## THE REACHABILITY CHECK — `check_reachable.py`, beside this file

```
python3 "${CLAUDE_SKILL_DIR}/check_reachable.py" <a top-level design or a DESIGN.md>
```

From the start document it follows every link and every named path to a file or a folder, counts a reached folder's
`CLAUDE.md`, `.claude/rules/` and `.claude/skills/` as reached, skips the folders a READ ORDER names on its line
`ARCHIVE AND PROGRAM FOLDERS:`, and lists every `.md` file under the start document's folder that nothing reaches —
exit 1 when any. Give each listed document its one-line summary and link in the parent that owns its topic, or name
its folder on that line when it is evidence, generated output or a program's source; run it again until it exits 0.

## THE HOOK — `hook.py`, beside this file

The same check on every Edit / MultiEdit / Write to any top the map names (else the bound one), and the map check on
every edit of the map, before the write lands: an edit that adds a finding is refused; an edit that only removes
findings passes, so a deformed document is repaired one edit at a time and a clean one stays clean. Install it in the
project settings of the repository that holds a top-level design (the snippet is in `hook.py`'s docstring). It
recognizes the same file in every worktree of that repository.

## HOW TO REPAIR A FINDING — the one legal write

Read the whole document · find every place the change touches · rewrite each so it states the design and nothing
else, the replaced reading leaving no trace · re-read the affected sections · run the gate bare. A finding is removed
and replaced with NOTHING: no note that it was removed, anywhere. Detail cut from a bridge belongs in the `DESIGN.md`
of the part it describes — check it is there before cutting it.

## NEXT

- a new top made — an island the canonical home's top-level design does not cover → its top-level design, then its
  line on the map, then `--map` run bare
- a `DESIGN.md` changed → the `design-toc` skill, for its READ ORDER and its table of contents
