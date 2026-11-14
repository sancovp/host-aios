---
name: skillmap
description: Turn a flat folder of skills (or any markdown) into a navigable, coordinate-addressed map so you can do progressive disclosure instead of loading the whole pile. Use when a .claude/skills or docs folder is a big flat list you can't navigate, when you have too many skills to hold in context, when context is melting from too many files at once, or the user says "map my skills", "organize my skills", "index my skills", "too many skills", "make a navigation map", "progressive disclosure".
---

# skillmap

Your skills (or any folder of markdown) load as a **flat list** — the platform auto-loads a folder and its direct children, never deeper. Past a handful, you can't navigate them: you either load everything (context melts) or guess. `skillmap` fixes that in one command.

## What it does

Point it at a folder. It gives every skill a **hierarchical coordinate** (`0.1`, `0.2.1`, …), reads each one's description, and writes a single `CLAUDE.md` with:
- a **Folder Map** (the tree, with coordinates + descriptions),
- an **addressable Index** (coord → skill → what it does → path),
- **branch summaries** (what each branch opens to).

Now you can **open a branch and descend to the coordinate you need** — progressive disclosure — instead of holding the whole pile in context.

## How to use it

```bash
# print the map
python3 "${CLAUDE_SKILL_DIR}/skillmap.py" <folder>

# write CLAUDE.md into the folder (so it auto-loads next time)
python3 "${CLAUDE_SKILL_DIR}/skillmap.py" <folder> --write
```

Examples:
- `python3 "${CLAUDE_SKILL_DIR}/skillmap.py" <project>/.claude/skills --write` — map the skills of the project you are
  working on.
- Point it at any docs/ folder to get an instant navigable index.
- Never `--write` into the home folder's `.claude/skills/`: a `CLAUDE.md` written there loads into every session on the
  machine. Print that map without `--write` instead.

Zero dependencies (Python stdlib). Non-destructive — it only writes `CLAUDE.md`.

## When to reach for it

- A skills/docs folder has grown past what you can scan at a glance.
- You're about to load many files "just in case" — map first, then load only the coordinate you need.
- The user wants an index, a map, or a navigable structure over a pile of markdown.
