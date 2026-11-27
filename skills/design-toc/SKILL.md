---
name: design-toc
description: Open at ANY edit of a project's DESIGN.md — keep the READ ORDER at its head naming every child DESIGN.md, regenerate its table of contents (its `.claude/rules/design_toc.md`) in the same commit, create the TOC with --init when a DESIGN.md passes ~500 lines, and run --check before trusting a line number and before a version leaves. Fire the moment a DESIGN.md changes or grows large.
---

# design-toc — every DESIGN.md opens with its READ ORDER; a big one keeps a table of contents

## THE READ ORDER — every DESIGN.md, big or small

Every `DESIGN.md` opens with its READ ORDER (the rule `26-canonical-design`): its first `##` heading is `## READ ORDER`,
and under it, what this level is, then for which work which section, which page, which child design and which procedure
to read, then the line naming the folders this check and the reachability check skip, and, where the project holds code
that is a copy, generated output or run evidence, the line naming the folders the coverage gate leaves unchecked:

```
## READ ORDER

<what this level is, in a line or two>

- for <which work> → `<child>/DESIGN.md` · <its procedure: a dev flow, a skill>
- for <which work> → §<n> · <its procedure>
- ARCHIVE AND PROGRAM FOLDERS: `<folder>/` · `<folder>/`
- COPIES, GENERATED OUTPUT AND RUN EVIDENCE: `<folder>/`
```

It names every child `DESIGN.md` beneath it — the nearest `DESIGN.md` down each folder, outside the folders its
`ARCHIVE AND PROGRAM FOLDERS:` line names: run evidence, records, goals and their proofs, forks, generated output, a
program's source such as a template (`none` when there are none). Every `DESIGN.md` it names resolves.

WHEN a child design is added, renamed or removed: rewrite the READ ORDER in the same commit.

## THE TABLE OF CONTENTS — a DESIGN.md past ~500 lines

WHEN a project's DESIGN.md passes ~500 lines and has no TOC rule: run
`python3 "${CLAUDE_SKILL_DIR}/design_toc.py" <project_dir> --init`, then fill the hand-written
"WHERE THE CURRENT ANSWER IS" table with the questions that keep coming up.

WHEN DESIGN.md changes: run `python3 "${CLAUDE_SKILL_DIR}/design_toc.py" <project_dir>` in the
same turn and the same commit as the edit.

The script writes only the block between the TOC markers; the hand-written table above it is never
touched. The law is the rule `design-docs-keep-a-toc`.

## THE CHECK — before trusting a line number, and before a version leaves

`python3 "${CLAUDE_SKILL_DIR}/design_toc.py" <project_dir> --check`, run bare, and read what it says. It checks the
READ ORDER of the project's `DESIGN.md` — refusing one with no READ ORDER at its head, one that does not name a child
`DESIGN.md` on disk, and one that names a `DESIGN.md` that is gone — and, where the project keeps a TOC rule, the table
of contents too: `STALE` means regenerate first. It also reads the design's state. A design found holding state has each
passage of it fenced where it stands (rule `26-canonical-design`), between the fence's opening line
`> **WARNING: STATE MENTIONED IN DESIGN.MD -- NOT ALLOWED IN DESIGN. THIS MUST MOVE TO STATE FILE WHEN WORKED ON. DO NOT
REMOVE THIS FENCE UNTIL THE STATE IS RECONCILED AND EVERY INTENDED THING IS BUILT AS INTENDED. DO NOT SKIP THIS.**`, written
as one line, and its closing line `> **END OF STATE FENCE**`. The check admits every line from an opening line to its
closing line, and `CURRENT` names how many lines the fences hold that are still to be moved into the boards. It refuses
a state mark — an `ASPIRATIONAL` mark, an `as built` statement, a `✅ MEASURED` or `⏳ AS OF` claim — outside every
fence, naming each line, and an opening line with no closing line after it, naming where it opens. Lines inside a code
block are not read for any of it. `CURRENT` means all of
it holds; a project with no TOC rule passes or fails on its READ ORDER and its state alone. Exit 1 names each finding.

## NEXT

- the check refuses the READ ORDER → rewrite it so it names each child design it lists, then run the check again
- the check refuses a state mark outside every fence → fence the whole passage that holds it where it stands, every word
  unchanged, then run the check again; it refuses a fence left open → write its closing line where its passage ends
- the check names fenced state still to move, and the project is being worked on → the `state-file` skill: each fenced
  passage written as rows of its board, any state it needs defined with its dev flow; the fence is removed only once the
  state is reconciled and every intended thing is built as intended
- the design has documents beneath it → the `top-level-design` skill's `check_reachable.py`, from this `DESIGN.md`
- the project has code → the `design-md` skill's `check_design_covers_code.py`, on the project: every code file named in
  the design or a page it reaches
