# the-host-aios-scratchpad

The TOP scratchpad: one ref per project scratchpad that has open work. Every window has it in context and
every window shares it — change it with the Edit tool only, one line at a time, never rewrite it whole.

## HOW EVERY SCRATCHPAD WORKS — THE SHAPE NEVER CHANGES

1. **EVERY PROJECT HAS ITS OWN SCRATCHPAD, AND IT IS A RULE:** `<project>/.claude/rules/<project>_scratchpad.md`,
   committed in git like every other rule — never excluded, never ignored — so it is injected into every window
   that works in that project, in every worktree. A sub-dir with work of its own has its own scratchpad the same
   way, and its parent's scratchpad carries the ref to it. A project whose folder is PUBLISHED — mirrored to a public
   repository, so everything inside it publishes — keeps no scratchpad inside that folder: its notes live in a
   holding file in its own `workspace/` once its publisher leaves that folder out, and beside its folder until then
   (`how-to-save-work`), and its ref in this file names that file.
2. **A PROJECT SCRATCHPAD HAS THREE PARTS:** a first line naming this file as its law · THE REFS — one line per
   undone, rolled-up task or sub-scratchpad with open work · a CURRENT TASK section for each piece of work in
   progress, headed by that piece and not rolled up, where the window working on it keeps what it needs to do
   it — each line a command with the moment it fires (`WHEN … → …`), pointing at the board row that holds where that
   work stands; a state the window finds — built or not, measured, missing — is written as a row of the board, never
   here; a later finding edits the earlier line; no window writes in another's section while its task is in
   progress. The section's first line is the window's MODE LINE — `MODE: DEV or WORK · <the project> · <where it
   works: its worktree in the dev space, or the project's workspace> · GOAL: <the goal file, or the request in one
   line>` — written into the scratchpad with the Write or Edit tool, since a line said only in a reply is not there to
   be read again; this file loads in every window, so the window reads it again after every compaction. The section
   stays, its mode line first, through the task's last turn, and leaves only by rule 4's roll-up — by its own window
   before that window's next task, or by any window that finds its task done, since a done task's section holds
   nothing a roll-up loses.
3. **THIS TOP SCRATCHPAD HAS ONLY THESE INSTRUCTIONS AND THE REFS** — one line per project scratchpad with open
   work: `WHEN <the moment it matters> → <that scratchpad's path> — <what you will find there>`. Working in that
   project injects its scratchpad, so the ref expands by itself.
4. **ROLL UP BEFORE THE NEXT TASK.** Before a window starts another task, it rolls up its own CURRENT TASK section:
   every note moved under the next-highest thing it belongs to — the document that owns it, a sub-dir's scratchpad,
   or one ref line in its scratchpad's REFS (`WHEN … → where it expands — what you will find`) — until the section
   is empty and removed; then it opens the new task's section. A window rolls up its own section, and another
   window's only once that section's task is done (rule 2).
5. **EVERYTHING ON A SCRATCHPAD GETS DONE. DONE THINGS DO NOT REMAIN** — no line, no ref. When a project
   scratchpad has no open work left, its ref leaves this file; the history goes to the project's `CHANGELOG.md`.
6. **BEFORE ANY WORK IN A PROJECT, MAKE ITS SCRATCHPAD TRUE:** it exists, it is committed, it has this shape, and
   this file carries its ref. A scratchpad that is untracked or excluded from git is lifted in as work, by its own paths — its
   exclude line removed, its content committed, the untracked original removed once its content is in. Notes of
   that project waiting anywhere else — a holding file named in a ref below, an old list — move into it, and the
   holding file is deleted; then the ref below is rewritten to name only the scratchpad. A published project (rule 1)
   keeps its holding file instead, where rule 1 places it: its notes stay there while it has open work, and the ref
   names that file.
7. **NEVER OVER 20KB**, this file or any scratchpad (`wc -c`). Over it means a roll-up is owed — do it first.
8. **NOTES GO ON A SCRATCHPAD AND NOWHERE ELSE** — never in a `_states` file, a `DESIGN.md`, a `CLAUDE.md` or any
   other rule; and a scratchpad holds no state, which is a row of a board and is written nowhere else.

---

## THE REFS

None yet — one line per project scratchpad with open work.
