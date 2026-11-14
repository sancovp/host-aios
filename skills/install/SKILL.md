---
name: install
description: Install the host AIOS for this machine's user — a folder of its own holding its boot config, its rules, a starter top-level design and its workspace of projects, the plugin turned on for that folder, one line in the global Claude folder pointing down to it, and that folder's line on the master map — or bring an install up to the plugin's version. Use when asked to install, set up or update the host AIOS.
---

# Install the host AIOS

The host AIOS is a configuration a Claude takes on by reading it: a boot config (`CLAUDE.md`) and a set of rules. A
plugin install loads no `CLAUDE.md`, so this skill puts them where Claude Code loads them by itself: in a folder of
their own. The global Claude folder — which every session on the machine loads, so nothing in it can change safely —
gets only one line, pointing down to that folder. What it makes:

| made | what it is |
|---|---|
| `<folder>/CLAUDE.md` | the boot config |
| `<folder>/.claude/rules/` | the rules, the blank `user_info.md` among them (the one file the installer fills out with their bindings) |
| `<folder>/TOP-LEVEL-DESIGN.md` | the starter top-level design — the folder's own top, placed only while absent, so it is the installer's to write as projects are made |
| `<folder>/workspace/` | the AIOS's workspace — THE WORKSPACE, where every project the AI works in is a folder: its index `workspace/CLAUDE.md`, one line per project, placed only while absent, and its `.claude/` scaffold empty |
| `<folder>/.claude/skills/` · `<folder>/.claude/agents/` | empty: the skills come from this plugin, turned on for the folder |
| `<folder>/.claude/settings.json` | turns this plugin on for every session in the folder |
| `<folder>/.claude/host-aios-install.json` | the record of every file placed, with its checksum |
| `<global home>/CLAUDE.md` | one line: read the folder's `CLAUDE.md` before anything else — left as it is when it already points to another folder that holds an install |
| `<global home>/rules/master-map.md` | THE MASTER MAP, a rule every session loads: its title line, then one line linking each installed folder's top-level design — written with this folder's line, or this folder's line added |

## 1. Get the answers

Take each answer from the task when it gives them; ask the installer only for what it does not.

- **the folder** — where the AIOS lives: a folder of its own, which the installer works in or under
- **the global home** — Claude Code's configuration folder; give it only when the task names one. Otherwise the script
  uses `CLAUDE_CONFIG_DIR`, else the home folder's `.claude`

## 2. Run the installer

```
python3 "${CLAUDE_SKILL_DIR}/install.py" --folder "<folder>" [--global-home "<global home>"]
```

It refuses first, changing nothing and naming each file, when it would overwrite a file it did not write, or a file it
placed that has been changed since — a file at the map's place without the map's title line among them. A second run at the same version changes nothing; a run at a newer version of the
plugin replaces only the files it placed that are still as it placed them, and keeps the installer's `user_info.md`, top-level design and workspace index.

## 3. Read its report

It prints one JSON report: `"ok": true` with the files `placed`, `replaced`, `removed` and `kept`, or `"ok": false` with
each file `refused` and why. Report a refusal as it stands — never move, delete or overwrite the file it names to get
past it; that is the installer's choice to make.

## 4. Tell the installer

What was placed and where, that sessions started in the folder (or under it) load the host AIOS, that
`<folder>/.claude/rules/user_info.md` is theirs to fill out with their name and their bindings — THE WORKSPACE bound
to `<folder>/workspace/` among them — that every project goes in that workspace, one folder each, and that
`<folder>/TOP-LEVEL-DESIGN.md` is the folder's top, named on the master map, which each project in the workspace is
bridged into.
