---
name: design-toc
description: Open at ANY edit of a project's DESIGN.md — keep the READ ORDER at its head naming every child DESIGN.md, regenerate its table of contents (its `.claude/rules/design_toc.md`) in the same commit, create the TOC with --init when a DESIGN.md passes ~500 lines, and run --check before trusting a line number and before a version leaves. Fire the moment a DESIGN.md changes or grows large.
---

# design-toc — every DESIGN.md opens with its READ ORDER; a big one keeps a table of contents

## THE READ ORDER — every DESIGN.md, big or small

Every `DESIGN.md` opens with its READ ORDER (the rule `26-canonical-design`): its first `##` heading is `## READ ORDER`,
and under it, what this level is, then for which work which child design and which procedure to read, then one line
naming the folders the checks skip:

```
## READ ORDER

<what this level is, in a line or two>

- for <which work> → `<child>/DESIGN.md` · <its procedure: a dev flow, a skill>
- for <which work> → §<n> · <its procedure>
- ARCHIVE AND PROGRAM FOLDERS: `<folder>/` · `<folder>/`
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
of contents too: `STALE` means regenerate first. `CURRENT` means both hold; a project with no TOC rule passes or fails
on its READ ORDER alone. Exit 1 names each finding.

## NEXT

- the check refuses the READ ORDER → rewrite it so it names each child design it lists, then run the check again
- the design has documents beneath it → the `top-level-design` skill's `check_reachable.py`, from this `DESIGN.md`
