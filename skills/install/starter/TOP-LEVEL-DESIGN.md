# THE TOP-LEVEL DESIGN — the explained table of contents of everything this AIOS holds

## READ ORDER

**What this is.** The top of this AIOS: the explained table of contents of every project in its workspace. Each
numbered section below is a short bridge plus the links to the `DESIGN.md` documents it bridges; read in order, the
bridges explain the whole, and the master map's line for this folder names this document.

**How to read it.** Read it top to bottom when the work is wired into this top — when a section here names the work's
folder — then follow only the links the work needs, and read each document you follow whole. Work this document does
not name reads only its own project's canon: its `CLAUDE.md`, its `DESIGN.md` and its board.

**How to change it.** Read the whole document, find every place a change touches, rewrite each so it states the
architecture and nothing else, re-read the affected sections, run the top-level-design gate bare, and add what changed
and why to the `CHANGELOG.md` beside this file. A new project gets its bridge in the section that owns its kind, with a
link to its `DESIGN.md`.

**Where progress lives.** In each project's own board, in its `.claude/rules/`, and in the top-level states doc the
installation binds; every detail lives in the documents the sections link.

- ARCHIVE AND PROGRAM FOLDERS: none

## 1. THE AIOS

This folder is the AIOS: its `CLAUDE.md` is the boot config, and its `.claude/rules/` holds the rules every session
here loads, `user_info.md` among them as the one file that names the user and binds the roles. The skills reach every
session here from the plugin the folder turns on.

## 2. THE PROJECTS

Every project lives in this AIOS's workspace, `workspace/`, one folder each, and everything the AI does here happens
in one of them; each gets one bridge here: what it is, how it relates to the others, and a link to its `DESIGN.md`.

AND THAT'S THE ARCHITECTURE.
