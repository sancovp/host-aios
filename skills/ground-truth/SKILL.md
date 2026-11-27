---
name: ground-truth
description: WHEN a project that exists has a DESIGN.md that is wrong, mangled or absent, or holds other written files that still say what it is, does or is meant to be, run this process on it before any other work there — gather the REALITY from every line of its code and the fully resolved VISION from every document anywhere that ever spoke about it, factor the two into one design system with every stage of every transformation written as a design, put every true status on the boards, and leave nothing in the project but design documents and code — never on a new project, never keeping an old document.
---

# ground-truth — the process that resolves everything a project's code and documents say into one design

The law is the rule `00-samaya` §V. Ground truth is a PROCESS: it is run, and it ends with one design system that
holds everything, written through the `design-md` skill. It is never a kind of document, and it leaves no record file
and no findings folder behind it.

## THE TWO THINGS IT GATHERS — never confuse them

- **REALITY** is what the code does. It is gathered from the code alone, every line of every module. The code is the
  reality and never the truth of what is meant: nothing about what the project should be is concluded from it.
- **THE VISION** is the entire, fully resolved idea and design. It is gathered from EVERY document anywhere that ever
  spoke about the project — inside its folder and outside it — every statement, resolved in date order against every
  other, every supersession accounted for.

From the two it makes: the whole vision FACTORED into designs about the code, one design file per group of modules
that makes sense to group; the TRUE STATUS of every part, as rows of the board; every STAGE of every transformation
from the code as it is to the highest version the vision holds, each stage a design of its own, written completely
and solved end to end; and ONE top-level `DESIGN.md` that directs all thinking about the project.

## WHEN IT RUNS, AND WHEN IT NEVER DOES

It runs when a project ALREADY EXISTS and its `DESIGN.md` is wrong, mangled or absent, or when written files beside
the design still say what the project is, does or is meant to be. A new project takes no ground truth: its design is
written from the stated intent, by the `aios-artifacts` skillchain. Where the project has a HALO SEEM map, the agents
keep it open: it says where the features' boundaries are.

## DONE ONLY WHEN — every one of these, and a design is never a summary

1. Every line of code of every module has been read, and is accounted for in its group's page, range by range.
2. Every document anywhere that spoke about the project has been read whole, and every statement of it is placed.
3. Every line of code is mapped against every line of design, prose and ideas.
4. Each group of modules that makes sense to group has ONE design file.
5. Every supersession is accounted for: the design holds what stands, `CHANGELOG.md` holds what it replaced.
6. The final design is figured out and all information is resolved.
7. Every stage of every transformation is written as a design, solved end to end, through the highest version.
8. Every true status is a row of the board.
9. It is rolled up into ONE `DESIGN.md`.
10. Nothing is left in the project but design documents, code and the AIOS's own files. Every other written file that
    says anything about the project is absorbed, statement by statement, and deleted. None is kept as archive,
    record, pointer or reference.
11. The gates pass, each run bare and read: the wholeness gate (the `design-md` skill's `check_design_is_whole.py`),
    the coverage gate, the read-order check, the reachability check and the state-file gate on each board.

The test that it is done: could every old document be deleted now, with no question about the project left that only
an old document answers? If not, it is not done, whatever the gates print.

## WHO READS — the planner and the agents

Measure first (the rule `00-size-the-corpus-before-generating-into-it`). Where the code and every document together
fit one window, the session runs every stage itself. Where they do not, the session is THE PLANNER: it measures, cuts,
writes each brief, sends agents on the model the installation binds for them (the rule `the-subagent-model`), and
checks what returns. The planner reads none of the code and none of the documents itself, and writes no findings, no
map and no report of what they say. The agents read, and the agents write the design.

## THE SENDINGS — the record of every agent

The planner keeps a table `## THE SENDINGS` on the project's board (the `state-file` skill), one row per agent, the
row written BEFORE the agent is sent: which stage, which share or which sources, which model. Its phases: SENT →
RETURNED → PROVEN (a program finds nothing left out, and a fresh agent that built nothing checks it) → COMMITTED. What
a returned agent says remains goes in its row. An agent with no row was not sent, and after a compaction that table
is how the planner knows where the work stands. The project's scratchpad carries one line, DO NEXT, rewritten in the
same commit as every step that moves, so no window repeats a finished step.

## THE STAGES — in order

1. **DEPRECATE.** The broken `DESIGN.md` stops being canonical the moment the process starts. It is one of the
   documents the process absorbs: read as a claim, never as a source.
2. **SIZE AND CUT.** By program, never by reading: list every code file with its lines; cut the code into SHARES, each
   a group of modules that makes sense to group and small enough for one reader to hold whole (about 250 KB of
   source), a group too large for one reader cut into parts that are groups of their own. List every other written
   file in the project with its size and its date — the date it first entered git, a date the file states winning
   over it. Then locate every document OUTSIDE the project that speaks about it, by a bounded search of the
   installation for the project's names, and list those with their dates too. Record the shares and the counts in the
   scratchpad, so no later window measures again.
3. **GATHER REALITY — the code pass.** One agent per share, all at once, each writing only its own page
   `design/<share>.md`, in the form the `design-md` skill's THE GROUP PAGES gives: per file a heading
   `## <path in backticks> — N lines`, why the file exists, then a table whose first column is a line range `a-b`,
   running from 1 to N with no gap — what the range is, what it does, what calls it, what it calls. It reads at most
   400 lines at a time and writes their rows before reading on. What it finds wrong it lists at the end of its page,
   for the board.
4. **GATHER THE VISION — the document pass.** One agent at a time, oldest documents first, each given a share of
   sources it can read whole. It reads the current `DESIGN.md` and the owner's recorded rulings first, since a ruling
   of the owner's outranks every older statement. Then it reads each source whole and places EVERY statement of
   design, prose or idea in `design/<share>.vision.md`, under the file, function or topic it is about — every
   statement, not only the ones that conflict. A statement counts as already placed only when the page says the same
   thing in full; any difference of condition, number, name, reason or example is added. Where a later statement
   replaces an earlier one, the page gets what stands and `CHANGELOG.md` gets what it replaced, with both dates. A
   statement about nothing in the code is vision with no code yet, and is kept as that. A statement about the project
   as a whole goes in `design/the-whole.vision.md`. The agent deletes one of the project's own documents only when
   every statement of it is placed, and appends one `CHANGELOG.md` entry per deleted file saying where its statements
   went. A document outside the project is read, its statements placed, and left where it is. Stages 3 and 4 write
   different files, so they run at the same time.
5. **FACTOR — per group, by a fresh agent.** With the group's reality page and its vision page both whole in front of
   it, it writes the group's design at the head of `design/<share>.md`: the whole vision for the group, resolved, in
   its highest version. For every part of that design it works out the TRUE STATUS — the code does it, the code
   differs, or no code holds it — and lists each one that is not simply done as a row for the board. For every line
   range it says which part of the design the range carries, or that no design asks for it. Then it deletes the
   vision page.
6. **WRITE THE STAGES — per group, then across groups.** Every stage of every transformation from the code as it is
   to the highest version, in order. Each stage is a design: what the group is at the end of that stage, what changes
   in which files, what proves it — complete, everything in it solved end to end. A stage that is a name or one line
   is not written.
7. **ROLL UP.** One agent writes the single `DESIGN.md` from the group pages: what the project is, the final design,
   the stages across groups in the order they are done, and, for every kind of work, which group page to read. Its
   READ ORDER names no folder of old documents.
8. **PROVE — by fresh agents that built nothing.** Per code file: every line range is in its group's page and its
   row says what those lines do. Per deleted document, read from git: every statement of it is in the design or, as
   replaced, in `CHANGELOG.md`. The stage that missed is run again, until both lists are empty. Then the gates of
   DONE ONLY WHEN 11, each run bare. Then the owner is told, with the counts.

## WHAT EVERY BRIEF SAYS — whichever stage

A brief is the only context its agent has. It states the goal in the owner's terms, names the exact files the agent
reads and the ONE file it writes, gives the form of that file, and carries these, in these words:

> Read every file on your list whole, with the Read tool — no sampling, no searching in place of reading; a search
> only locates. Write as you go, so nothing depends on memory. Write only the file named. Never edit code, tests, a
> board, a rule or a skill. Never run a test, a daemon or a network call. Never run a git command that changes
> anything except, where your brief says so, removing a document all of whose statements you have placed. State only
> what you read. Write no date, no quote, no person's name, no history and nothing about where anything stands into
> a design page: history goes to `CHANGELOG.md`, and what you find wrong goes in your page's last section, for the
> board. When done, answer only: the file written, the count of what you read against what you were given, and what
> you could not do.

## CHECKING WHAT RETURNS

By program first: the wholeness gate lists every code file whose ranges do not run from 1 to its last line, and
every written file still outside the design. Then by a fresh agent, never by the planner reading the page and never
by the agent that wrote it. A page with a gap is sent again. After each agent: the gates bare, the row on the board
marked, the work saved and pushed by its own paths (the rule `top-level-session-worktree`).

## NEVER

- take the code for the truth of what is meant, or write a design from the code alone
- write the design from a reduction — a summary, a map of contradictions, a list of topics, a reader's findings
- keep an old document, as archive, record, pointer or reference, or leave a dated record or a findings folder
- delete a document before every statement of it is placed
- leave a stage of the way to the final design as a name
- let the planner read the code or the documents, or check a page by reading it itself
- send an agent with no row on the board, or leave the scratchpad's DO NEXT line saying a finished step
- write a state into a design page
- run it on a new project, or leave two canonical documents

## THE ORDER OF ATTENTION

```rune
[Deprecate] ⇒ [SizeAndCut] ⇒ [GatherRealityFromTheCode] ⇒ [GatherTheVisionFromEveryDocument] ⇒ [FactorTheVisionOntoTheCode] ⇒ [WriteEveryStageAsADesign] ⇒ [RollUpIntoOneDesign] ⇒ [ProveByThoseWhoBuiltNothing] ⇒ |OneDesignThatHoldsEverythingAndNothingElseLeft|
```

## NEXT

- stages 3 to 7 → the `design-md` skill: every page is written through it, and its wholeness gate closes the run
- a true status was found → the `state-file` skill: a row of the board
- the new `DESIGN.md` stands → the `design-toc` skill (its READ ORDER and table of contents), the `archi-diagram`
  skill (the stack drawn from the new design), the `top-level-design` skill (the reachability check; the project's
  line in the top-level design that holds it)
- a question only the owner can answer was found → the `how-to-settle-a-question-for-the-owner` skill, and only when
  no statement in the documents or the owner's recorded rulings settles it
