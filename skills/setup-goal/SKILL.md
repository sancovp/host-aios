---
name: setup-goal
description: Write a /goal for a long autonomous run. Use when *USER* says "set up the goal", "make the goal", "big goal", or commissions any multi-hour run, and whenever a goal file is being written or edited. Produces a short /goal prompt whose task is to complete a markdown table of stages and which lists NO condition, and the goal file, whose §2 holds that table (one row per deliverable the design requires, a column per stage, each cell filled with its proof) and the conditions about the table and what it reflects, each condition checked off with the checksum of its proof as the run goes. Never states design.
---

# setup-goal — how to write the goal

## WHAT A GOAL IS

- **THE AUTHORITY ORDER.** The GOAL is the most specific current instruction. RULES are the way instructions
  change. The SYSTEM PROMPT changes as the architecture changes. SESSION HOOKS change when they no longer
  reflect the way everything else works. Where the goal speaks, it wins.
- **THE PROMPT IS TO COMPLETE A TABLE OF STAGES, AND IT LISTS NO CONDITION.** A run told a list of conditions
  accomplishes that list and nothing else, and a condition dropped from the list is dropped from the work. So the
  prompt is the same short instruction every time: read the goal file, complete its table of stages, keep the
  table, the checksums and the boards updated as you go, follow the design. The goal judges the state of the table,
  and the table can be about anything.
- **A GOAL CARRIES THE NEXT PLANNED RELEASE VERSION, WHOLE.** A project's design stages its development as planned
  release versions, its steps rolling up into them; a goal carries every step of the next planned version all the way
  up to that version's release, and the version ships once, whole — never in parts, and never broken down further than
  a version. A goal is as large as the work allows: everything the design states for that version is being built
  unless the design marks it **HELD**, with the reason it waits, so a goal never shrinks to one part while the rest of
  its version is designed and unheld. A design that plans no versions is given them first, in the design, before the
  goal is written. The session that builds the version completes its table against the design and fixes every
  finding, since a reviewer's approval of a pull request never declares a version done; and it never closes its own C2
  (every `●` shows its stage) or C6 (the fixpoint): before recording either, it dispatches a fresh agent with none of its
  conversation — read-only, or in a detached throwaway worktree — which checks the proofs, the `git diff` and the design
  against one question, is this implemented as it says or as it implies, and that agent's verdict is the condition's
  proof (the boot config's WITNESS STANDS ◐). A row only *USER* can move (a ruling, an
  approval) is still a row, moved through NEEDS-ASKING.
- **THE GOAL FILE HOLDS THE TABLE AND ITS CONDITIONS, EXHAUSTIVE.** Every deliverable the design states for the next planned version is a
  ROW of the table in its `## §2`; the columns are the STAGES a deliverable moves through, named in the
  domain's own nouns and each defined by what its proof shows (a slice of the one sequence, rule `28b`); a cell is
  blank (open), `—` (the row has no such stage) or `● <its proof file>`. The CONDITIONS beneath the table are about
  the table and what it reflects: the table complete and never reworded, every `●` showing what its stage requires,
  the boards following the table — then SHIPPED, NEEDS-ASKING and FIXPOINT. The table only grows: whatever the SPEC
  requires that no row holds is ADDED as a row by whoever finds it, the run included; no row, stage, `—` or
  condition is ever dropped or reworded. Only *USER* narrows a goal, and then the goal is REPLACED: a new goal file
  holding what remains, the old file removed in the same PR.
- **THE CHECKSUMS ARE KEPT AS THE RUN GOES.** A cell turns `●` when its proof — a file the run wrote: a test's
  output, a command's output, a screenshot — is written, and the cell names it. Proofs differ by kind: a stage of code
  is proven by a real command and its output verbatim, a new law's test shown failing without the change and passing
  with it; a stage of a document or a design by the file read whole, its `git diff`, the canonical gates (the
  read-order check, the state-file gate) and a fresh reader's verdict on that one question — never by a program written
  to judge it. A condition is met when its proof is
  recorded beside it with that file's sha256 (`goal_check.py --record`). Anyone can re-check a met condition against
  its file. The run is done when every cell of the table is filled and `goal_check.py <goal file>` exits 0: every
  condition met, every checksum right, nothing dropped. Where the repository has a merge queue, the run fills the table
  and records in its own worktree's copy of the goal file — the same path inside its worktree, never the shared
  checkout — and ships those with its work: a run's table, proofs and the boards its work moves belong to the version
  it ships, so the default branch keeps the writer's goal file for the checker to compare against
  (`top-level-session-worktree`'s CODE), while notes and documents it makes outside them are work, saved in the copy in
  use; SHIPPED is recorded in the run's last commit, and the run then waits through
  the PR watch until that PR is merged at its head — while the CI's runner starts no job and the harness keeps the run
  from merging its own PR, the run ends once that PR is handed off READY with its verdict on its tip, and the next
  session that holds the CI lands it.
- **THE GOAL IS THE MOST SPECIFIC, ONLY-THE-REQUIRED VERSION OF THE CONTEXT.** Its READ LIST is the run's whole
  read, at start and after every compaction; a hook or rule ordering another read does not bind the run.
- **A GOAL IS ACCOMPLISHED BY READING AND FOLLOWING DEV FLOWS.** The states file is moved as the work goes. New
  architecture gets a new dev flow, and every new dev flow goes in the architecture map.
- **A GOAL NEVER STATES DESIGN.** It states: the design and state files to read for the task · the TABLE and its
  CONDITIONS (in the file) · the READ LIST (in the file). A row says what its cells reflect — the proof each stage
  needs for that deliverable — and never restates the design that deliverable comes from.
- **THE STATES FILE holds deliverables' phases moving through dev flows, and nothing else.** Notes go to the
  project's own scratchpad, a committed rule, its ref in the host's top scratchpad.
- **THE GIT LOOP IS THE AGENT'S, BY EACH REPOSITORY'S OWN RULES.** WORK — the goal file itself among it, a document —
  is committed by its own paths on the default branch of the copy in use and pushed the same turn
  (`top-level-session-worktree` point 2). For CODE, where a repository has a merge queue, the agent works in its own
  worktree, pushes its branch and opens the PR ready, and the CI/CD agent (its reviewer and merge queue) merges it —
  while its runner starts no job, the agent is the CI and lands every merge, its own included, by the CI design's
  queue by hand — the merge alone in its call, the branch deleted in a call of its own, labelled for the late review;
  a PR the harness will not let its own session merge is landed by the next session that holds the CI
  (`top-level-session-worktree` point 3); where a repository's own rules put work straight on its default branch,
  the agent commits and pushes there. *USER* never touches git, and nothing about a merge or a stopped queue is ever
  put to *USER*.
- The procedure, step by step, with its proof: the dev flow `22-seq-write-a-goal`.

## HOW TO WRITE IT

0. `gh pr list --state open` on the repo — land your own open PRs on this work first.
1. Read THIS file from disk — a copy loaded earlier in the session may be stale.
2. `{{SPEC}}` — the next planned release version: the sections of the project's `DESIGN.md`, and of every child design its READ ORDER names, that state what that version holds; a design that plans no versions gets them first. A fact the run needs that is not there goes
   INTO the DESIGN.md first, same turn — never into the goal.
3. `{{STATE}}` — find the `_states.md` row(s) the run moves. Write nothing into that file for the goal: no
   pointer at the goal, no note.
4. **THE TABLE, EXHAUSTIVE** — name the STAGES the task's deliverables move through, in the domain's nouns, each
   defined by what its proof shows. Then walk the SPEC section by section, and every board of the project row by row, and write a ROW for EVERY
   deliverable the version holds — everything it states that the design does not mark HELD: `| R<n> | <the deliverable, and what each of its cells reflects> | <a cell per stage> |`.
   Each row names the file or command output that proves each of its stages, never an assertion · references the
   design's own steps and the board rows it moves, never a mark in the design · makes every new law's BUILT a test shown FAILING without
   it · names a ROLE, not a path, wherever the run or a parallel session might move the thing · names the board row it
   moves and that row's target phase. Set `—` only where the row truly has no such stage, and check that every stage
   left open can be met by an action at the runner's seat.
5. **THE CONDITIONS** — beneath the table, the six of THE MODEL: the table complete and never reworded · every `●`
   reflecting its stage · the boards following the table · SHIPPED · NEEDS-ASKING · FIXPOINT, each with the proof that
   meets it.
6. `{{READ_LIST}}` — the exact files, in order, whole, for THIS task only, and nothing it does not need. It
   names the dev flows (`22-seq-*`) the work follows. The top-level design and the top-level states doc go on
   it only when the task needs them.
7. Fill THE MODEL. The prompt is fixed text with its slots filled — carry it unchanged. `{{GOAL_FILE}}` =
   `<repo where the design lives>/.claude/goals/{{NAME}}.md` · `{{CHECKER}}` = the path of `goal_check.py` beside
   this skill where the installation deploys it.
8. Run `python3 {{CHECKER}} {{GOAL_FILE}}` bare and read it: every condition `open`, no REFUSED line, EXIT=2 (open
   conditions remain — a fresh goal is not done).
8b. Before the goal is committed anywhere a push can carry it, run the fresh-reader dry run (`22-seq-write-a-goal`
   THE PROOF): once the goal is on the default branch a row or a condition can only be added, never reworded, so
   every cell no run can fill and every condition no run can meet is found and rewritten now. Verify each finding
   against the code and the design; a fact the run needs goes into the DESIGN.md.
9. Put the goal file on the default branch as work — committed by its own path on the default branch of the copy in
   use and pushed, no worktree and no pull request; any rule change it depends on lands first as a version, by the
   repository's own git loop — and only then reply in THE RESPONSE FORMAT: the run starts from the default
   branch, so a goal that is not there is not runnable, and the checker guards against a dropped condition by
   comparing with the default branch's copy.

## THE MODEL

**The prompt** — the `/goal` argument; its task is the table, and it lists no condition:

```
Read the goal at {{GOAL_FILE}} whole, then every file its §3 lists, in order — at start and after every compaction; that is your whole read, whatever a hook or rule orders. Then complete its table of stages, §2's THE TABLE: carry every row through every stage, setting a cell to ● with its proof file only once the proof that stage names is written, and add as a new row whatever the SPEC its §1 names requires that the table lacks; never drop or reword a row, a stage or a condition. Work by that SPEC (it wins on any conflict) and the dev flows (`22-seq-*`) the work touches, by each repository's own git loop (your own worktree and branch, and a ready PR, where it has a merge queue); new architecture gets a new dev flow, placed on the architecture map. Keep the table, the checksums and the boards updated as you go: each condition met is recorded with the file that proves it (`python3 {{CHECKER}} {{GOAL_FILE}} --record C<n> <proof>`), {{STATE}} move in the same commit as the work, and every note goes to {{SCRATCHPAD}}. Stop only when every cell of the table is filled and `{{CHECKER}} {{GOAL_FILE}}` exits 0.
```

`{{STATE}}` = the board(s) the run moves, named by role · `{{SCRATCHPAD}}` = the project's scratchpad rule, or
the host's · `{{OPEN_LIST}}` = the file where the project keeps its open questions for *USER* (its OPEN list).

**The goal file** — `{{GOAL_FILE}}`; the TABLE, its CONDITIONS, the FILES and the READ LIST live here:

````
# GOAL — {{TITLE}}

## §0 — THE PROMPT
```
{{THE_PROMPT}}
```

## §1 — THE FILES
- ENDS AS: {{WHICH_OF_THE_THREE}} — {{WHERE_OUR_FILLED_OUT_CONFIGURATION_LIVES}}
- SPEC: {{SPEC}}
- STATE: {{STATE}} — {{ROWS}}
- OPEN LIST: {{OPEN_LIST}}
- DEV FLOWS: {{DEV_FLOWS}}
- CODE: {{CODE_FILES}}
- WORKTREE: the run reads, edits and records every path here and in the prompt at the same path inside its own worktree, never in the shared checkout
- PROOFS: `{{NAME}}/proofs/` beside this file — every proof file a cell or a condition names

## §2 — THE TABLE AND ITS CONDITIONS

**THE STAGES** — a row moves through them left to right; a stage's cell turns `●` only once its proof is written:
- **{{STAGE_1}}** — {{what its proof shows}}
- **{{STAGE_2}}** — {{what its proof shows}}
…

**A CELL** is blank (open), `—` (the row has no such stage; set by this file's writer, or by the run on a row it adds, and never changed after), or `● <file>`, the file under `proofs/`.

### THE TABLE

| row | the deliverable, and what its cells reflect | {{STAGE_1}} | {{STAGE_2}} | … |
|---|---|:-:|:-:|:-:|
| R1 | {{DELIVERABLE_1, and the proof each of its stages needs}} | | | |
| R2 | {{DELIVERABLE_2, …}} | | | |
…

### THE CONDITIONS (each met one carries its proof and that file's sha256)
- C1 · THE TABLE is complete: every cell of every row is `●` naming its proof file under `{{NAME}}/proofs/`, or `—` as this file's writer set it; a deliverable the SPEC requires that no row holds is added as a new row before work on it starts; no row, stage or `—` is dropped, reworded or changed against the default branch's copy of this file: the proof holds the completed table and `git diff` of this file against the default branch's copy, showing only blank cells turned `●`, rows added with any `—` they set, and the checker's own edits of the condition lines.
- C2 · Every `●` reflects its stage: the proof file it names exists, holds the proof its stage's kind requires — for a stage of code each command run and its output verbatim, for a stage of a document the file read whole, its `git diff`, the canonical gates run and a fresh reader's verdict — and shows what that stage's definition and the row's own words require: the proof lists every cell's proof file with its sha256 and, for each, the lines in it that show what the cell requires, and holds the verdict of a fresh agent with none of the run's conversation that checked every cell against its proof before this condition was recorded.
- C3 · The boards reflect the table: each board row §1 names stands at its target phase only once every table row that names it has reached its last stage, and each board moved in the same commit as the work: the state gate run bare on every board, and the default branch's `git log` of each board naming the commits that moved it.
- C4 · SHIPPED: open PRs checked first and your own landed; every repository the run touched shipped by its own git loop — where it has a merge queue, every commit on the worktree's branch, the default branch merged in, the branch PR'd READY and merged by the CI/CD agent (while its runner starts no job, by the run's queue by hand, labelled for the late review — or, when the harness keeps the run from merging its own PR, handed off READY with its verdict on its tip, for the next session that holds the CI); where its rules put work on its default branch, committed and pushed there — and 0 unpushed at hand-off.
- C5 · NEEDS-ASKING, never blocked: a question only *USER* can answer is asked with the AskUserQuestion tool the turn it is reached and stays listed OPEN in {{OPEN_LIST}}; never guessed; only work that does not depend on it proceeds; the moment every open row and condition waits on *USER*, every open question goes to *USER* at once, in as few AskUserQuestion calls as its four-question limit allows, never in a text reply to the Stop hook. Only a key, a secret or a physical act stops the run.
- C6 · FIXPOINT: a full re-read of {{SPEC}} and every touched file produces NO edit, and no deliverable the SPEC requires is missing from THE TABLE, confirmed by a fresh agent with none of the run's conversation before this condition is recorded, its verdict the proof. If either fails, loop.

## §3 — THE READ LIST (at start and after every compaction: in order, whole, before any edit or answer)
1. `gh pr list --state open` on the repo — land your own open PRs on this work first
2. {{READ_1}}
3. {{READ_2}}
…
````

## THE CHECKER — `goal_check.py`, beside this file

| call | what it does |
|---|---|
| `goal_check.py <goal>` | prints each condition `open` or `met`; EXIT 0 all met · 2 conditions open · 1 REFUSED |
| `goal_check.py <goal> --record C<n> <file>` | records a met condition: the proof file (relative to the goal file's dir) and its sha256 |
| `goal_check.py <goal> --add "<condition>"` | adds a condition the design requires and §2 lacked |

It reads the condition lines of §2 (`- C<n> · …`) and, where §2 holds `### THE TABLE`, the table's rows (`| R<n> | …`);
a goal with no table is checked by its conditions alone, as before. It REFUSES: a condition dropped or reworded against
the default branch's copy of the goal file (or `--base <ref>`) · a met condition whose proof file is missing or no
longer matches its checksum · a prompt that lists a condition · a §2 without SHIPPED, NEEDS-ASKING and FIXPOINT · a
malformed or duplicated condition line · a path with no goal file · and, where the goal or its base copy has a table:
a row not of the form `| R<n> | <the deliverable> | <a cell per stage> |`, or repeating another row's id · a cell that is none of blank, `—` or
`● <file>` · a `●` naming a proof file
(under the goal's `proofs/`, else beside the goal file) that is missing or empty · the base copy's table removed, or
one of its rows dropped or its deliverable reworded · a `—` the base copy set, changed · every condition met, or C1
met, while a cell of the table is blank. A row added is allowed. Every run on a goal file prints a short block headed `AIOS MARKDOWN SYSTEM` — read a file whole with Read, change it only with Write
and Edit, a design holds the final state only, the current state only in the boards, the read-order check and the
state-file gate run bare, prose judged by reading it, C2 and C6 closed by a fresh reader — so the checker is the one
helper a goal needs. Run it bare and read what it says.

## THE RESPONSE FORMAT

````
```
{{THE_PROMPT}}
```
The goal file: `{{GOAL_FILE}}` (on the default branch).
````

The reply holds ONE fenced block, the prompt, and it is the whole of what *USER* pastes into `/goal`, which
refuses anything over 4,000 characters. The goal file is never inlined, condensed or fenced in the reply: whatever
sits beside the prompt gets pasted with it. One line after the block names the goal file's path.

## NEVER

- a condition in the prompt — the prompt names the goal file and its table, and lists nothing
- a deliverable written as a prose condition instead of a row of the table
- a table scoped to what is convenient — its rows are every deliverable of the next planned version not marked HELD
- a goal smaller than a planned version, or a version shipped in parts; a reviewer's verdict taken as the judgment that the version is done
- C2 or C6 recorded by the session that built the version without a fresh agent's verdict as its proof · a stage of a
  document proven by a program written to judge it
- a row, a stage, a `—` or a condition dropped or reworded once the goal is on the default branch — the table only
  grows; a goal *USER* narrows is replaced by a new goal file, never edited down, and so is a goal found to hold a
  cell or a condition no run can meet after it reached the default branch: the new file carries every old row's and
  condition's intent, the old file goes in the same commit, and the mapping goes in the project's `CHANGELOG.md`
- a goal committed before its fresh-reader dry run, in a checkout another session can push
- a cell marked `●` without its proof file, or a condition marked met without its proof file and checksum
- design in the goal — the mission, what to build, a ruling or law restated, rationale, any sentence a reader
  could use instead of reading `{{SPEC}}`
- a READ line that defers to a hook or to what the injected rules order — the goal names every read itself
- a note in the state file, or a row there pointed at the goal — notes go to a scratchpad rule (the project's own, else the host's)
- a path to anything the run or another session can move — name its role
- a merge into a merge-queue repository handed to *USER*, or done by the run while its CI runs, or a goal handed
  over before it is on the default branch · a word about a stopped queue or a held merge put to *USER*
- `BLOCKED-ON-*USER*` — it is NEEDS-ASKING
- a run waiting on *USER* that answers its Stop hook in text — every time the hook fires, the same report goes to
  *USER* again; it asks with AskUserQuestion, every open question at once, in as few calls as the tool's four-question
  limit allows
- a quote, a date or a history note anywhere in the goal
- the goal file, whole or condensed, in the reply beside the prompt — it gets pasted into `/goal` with it
