# 22-seq — WRITE (OR REWRITE) A GOAL: a run commissioned → a /goal prompt to complete a table of stages + its goal file, merged, runnable

<docsys kind="dev-flow" role="instance"/>

TRIGGER:[*USER* says "set up the goal" / "make the goal" / "big goal" · a multi-hour run commissioned · any goal
file written or rewritten by its writer — a row a run adds to the table, or a condition it adds with `goal_check.py
--add`, is the run's own work, proven and shipped with it, and fires nothing here] · a PROCEDURE flow: every stage runs every time · the form is the `setup-goal`
skill; this rule is how that form gets made, shipped and proven.

## RETRIEVE (in this order)

| what | where |
|---|---|
| FIRST: the repo's open PRs — land your own on this work (finish, hand off, see it MERGED by the CI/CD agent, or by your queue by hand while its runner starts no job) before new work | `gh pr list --state open` |
| the model and its checker, from disk | the `setup-goal` skill's `SKILL.md` whole + `goal_check.py` beside it, at the seat a live session loads them from (the skill's base directory, which Claude Code names when it loads the skill) · the template's copies (`HOST_AIOS/skills/setup-goal/`) too; a change lands in the template's, and reaches the live one in a new release where [[user_info]] binds THE AIOS RELEASES (a release assembled from its sources takes it from the template), else in both |
| the spec the run builds | the next planned release version — the sections of the project's `DESIGN.md`, and of every child design its READ ORDER names, that state what it holds (a design that plans no versions gets them first); every step the design states for it — a part the design places in a later version (HELD, with the reason it waits) excepted — and every board row of it short of its last state becomes a row of the table |
| the state it moves | the owning `_states.md`, whole · the top-level states doc's row + the monorepo board's row (found by name) |
| the dev flows it follows | every owning `22-seq-<feature>.md` the work touches |
| the architecture map | the owning `21-architecture-diagrams.md` — where a new dev flow the run makes will be placed |
| the rules the runner is injected with NOW | `ls -la` of the AIOS's rules (current names) — the release in use's `rules/` where THE AIOS RELEASES is bound, else `~/.claude/rules/` · `00-the-work-loop` · `28-distributed-state` · `top-level-session-worktree` · the scratchpads (the project's own, a committed rule, and the host's top one with its ref) |
| the project's OPEN list | the `## OPEN` table on the project's board (rule 28) |
| every path the goal will name | `ls` each |

## THE CHANGE (obligations, in order)

1. Fill the skill's MODEL. **The prompt is to complete a table of stages, and lists no condition:** it names the goal
   file and orders its table completed — every row through every stage, a row added for whatever the spec requires
   that the table lacks — the table, the checksums and the boards kept as the run goes, the design followed. The goal is the
   most specific current instruction: the file's §3 names its own read list and nothing else — the only-the-
   required context, and the run's whole read (the top-level design and states doc only when the task needs
   them). No design in the goal · no note and no pointer at the goal in any state file.
2. Name by ROLE anything the run or a parallel session can move (the board, the scratchpad rule, a gate); a
   path only for what cannot move.
3. Write §2 as the skill's model has it: THE STAGES the task's deliverables move through, each defined by what its
   proof shows; THE TABLE, with a ROW for EVERY deliverable the next planned version holds and the design does not mark HELD — exhaustive, walked section
   by section, each row saying what each of its cells reflects, a `—` only where the row has no such stage, and a row for
   every bridge that closes a loop a left-out part would have closed ([[a-version-closes-every-loop]]); and the
   six CONDITIONS about the table, each proven by a file the run will record with its checksum. A row is never scoped
   to what is convenient, and once merged no row, stage, `—` or condition is dropped or reworded; the table only grows. A question for *USER* is
   asked with the AskUserQuestion tool AND listed OPEN in the project's OPEN list — never guessed; only work that
   does not depend on it proceeds; when every open condition waits on *USER*, the run puts every open question in
   one AskUserQuestion call at once, never a text reply to its Stop hook.
4. Give every deliverable the run moves its own board row (split a lane the run moves only part of); its row in the
   table names that board row, and C3 its target phase.
5. Run `goal_check.py <goal>` bare and read it: every condition open, no REFUSED line; and every cell of the table
   blank or `—`.
5b. Run THE PROOF's fresh-reader dry run BEFORE the goal is committed anywhere a push can carry it — on the default
   branch a row or a condition can only be added, never reworded, so a cell no run can fill or a condition no run can
   meet must be found and rewritten first. Verify each finding against the code and the design before acting on it; a fact the run needs goes into
   the DESIGN.md, never into the goal. A goal that reached the default branch before its dry run, holding a condition
   no run can meet, is REPLACED: a new goal file whose conditions carry every old condition's intent, the old file
   removed in the same commit, the mapping old → new in the project's `CHANGELOG.md`. A goal on the default branch in
   the earlier form — its deliverables written as prose conditions — runs as written; a rewrite of it into a table
   is a replacement by this same step.
6. The goal file is WORK, a document: commit it by its own path on the default branch of the copy in use and push it
   the same turn ([[top-level-session-worktree]] point 2) — no worktree, no pull request. Any rule change the goal
   depends on is CODE and lands first as a version, by the repository's own git loop: where it has a merge queue, in
   your own worktree on its own branch, pushed and PR'd READY, merged by the CI/CD agent (its reviewer and merge
   queue) — while its runner starts no job, by the writer as the CI through the CI design's queue by hand (point 3:
   the merge alone in its call, the branch deleted in a call of its own; a PR the harness will not let the writer
   merge is landed by the next session that holds the CI, and the reply waits for it); where its own rules put work
   straight on its default branch, committed and pushed there. *USER* does not do git, and nothing about a merge or a
   stopped queue is put to *USER*; while the CI runs neither the writer nor the run merges code into a merge-queue
   repository.
7. Reply in the skill's RESPONSE FORMAT only once the goal is on the default branch — the run starts from there,
   and the checker compares the run's goal file against that copy.

## COHERENCE SET

§0 = the prompt byte-for-byte · the prompt's task is the table, and it lists no condition · §2's table holds a row for
every deliverable the spec requires, its stages defined, and the six conditions beneath it ·
every board row the goal names exists at its current phase · every dev flow the read list names exists · the OPEN
list carries every question the run may ask · the scratchpad rule named by role · a rule PR the goal depends on
merged first · a goal *USER* widens is rewritten and re-merged, its conditions only growing · a goal *USER* narrows is
replaced: a new goal file holding what remains, the old file removed in the same commit · a goal found unrunnable after
it reached the default branch is replaced the same way, every condition's intent carried and the mapping recorded

## THE PROOF

- `python3 <the deployed setup-goal skill>/goal_check.py <goal>` bare → EXIT=2, every condition `open`, no REFUSED
  line (it refuses a condition in the prompt, a missing SHIPPED · NEEDS-ASKING · FIXPOINT, a malformed line) ·
  `grep -c '^| R[0-9]' <goal>` → the number of deliverables the spec requires, every cell blank or `—`
- `awk '/^```$/{f=!f;next} f' <goal> | wc -c` → under 4000 · `grep -c 'injected rules order' <goal>` → 0
  · `grep -c '^Read the goal at' <goal>` → 1
- every relative path → `ls` exists; every `~/` path → `ls -la` exists now
- the board: `check_state_files <absolute board path>` bare → EXIT=0 and it names the file (the SHAPE only —
  it passes a board full of notes) · the no-note grep over the board and both top-level rows → 0
- the goal file saved as work: `git log origin/<default>..<default>` in the copy in use → empty · each rule PR the goal
  depends on MERGED first (`gh pr view <n> --json state,mergedBy,labels` → MERGED — by the CI/CD agent, or while its
  runner starts no job by the writer's queue by hand or, when the harness keeps the writer from merging it, by the next
  session that holds the CI, labelled for the late review)
- the default branch's goal blob = the one you wrote: `git show origin/<default>:<goal> | diff - <goal>` → empty
- a fresh-reader dry run, run at step 5b before the goal is committed: given only the prompt + the injected rules,
  it says what it reads first (the goal file, then its §3), which dev flows it follows, where every note goes, how a
  cell is filled (its proof file named in it) and how a condition is checked off (its proof file and that file's
  checksum, through the checker), that it adds a row for any deliverable the spec requires and the table lacks, and
  who merges — every answer matches the model — and it names every cell or condition no action at the runner's seat
  can meet, every `—` the spec contradicts, every proof two readers would record differently, and every part of the
  spec no row covers; each one it names is verified, then fixed in the design or the goal

NOT:[hand *USER* a merge, a rebase, any git step or a word about a stopped queue · send the goal file through a worktree or a pull request (it is work) · merge a merge-queue repository's rule PR yourself while its CI runs · hand over a goal that is not on
the default branch · list a condition in the prompt · write a deliverable as a prose condition instead of a row ·
scope the table to less than the next planned version holds · write a goal smaller than a planned version, or ship a version in parts · take a reviewer's verdict as the judgment that the version is done · drop or reword a row, a stage, a `—` or a condition once merged · name a movable thing by its path · put a note, a date or a goal pointer in any state file ·
write a READ line that defers to a hook or to what the injected rules order · put a quote, a date or a history
note in the goal]
