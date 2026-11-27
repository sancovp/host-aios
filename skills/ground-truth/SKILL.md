---
name: ground-truth
description: WHEN a project that exists has a DESIGN.md that is wrong, mangled or absent, run this process on it before any other work there — deprecate the design, go through everything that exists as it is at this datetime, establish every line by reading or measuring, then output the design system through the `design-md` skill, its top page and the pages that cover every file of the code, with the boards carrying what was found and a dated GROUND_TRUTH record left — never on a new project, never leaving two canonical documents.
---

# ground-truth — the process that gives a project back a design it can be read from

The law is the rule `00-samaya` §V. Ground truth is a PROCESS: it is run, it outputs a corrected design system, and it
leaves a dated record. It is never a kind of document, never a standing "current state" page, and nothing in it turns
into the design: the design is written, through the `design-md` skill, from what the process found.

## WHEN IT RUNS, AND WHEN IT NEVER DOES

It runs when a project ALREADY EXISTS and its `DESIGN.md` is wrong, mangled or absent. A new project takes no ground
truth: its design is written from the stated intent, by the `aios-artifacts` skillchain. Before starting, read the
project's HALO SEEM map where it has one, and keep it open during the run: it says where the features' boundaries are.

## WHAT IT OUTPUTS — and the run is not done without every one of these

1. **THE DESIGN SYSTEM, written through the `design-md` skill**: the top page `DESIGN.md`, and the detail pages in
   `design/` that cover every file of the code — why each file exists and how it connects to everything else. One page
   of conclusions is not the output. The test: a question about the project is answered from the design and its pages,
   without reading the code again.
2. **THE BOARDS carrying what was found**: every state the run established — what works, what is broken, what is
   duplicated, misnamed, missing or in pieces — as rows of the project's boards (the `state-file` skill), each state
   defined with its row where no dev flow defines it yet.
3. **THE DATED RECORD**, `GROUND_TRUTH_<DATETIME>.md` at the project's root: archival, never canon. Beside it, the
   folder `ground-truth-<DATETIME>/` holding every reader's findings file as it was returned.
4. **THE CHECKS PASSING, each run bare and read**: the coverage gate (the `design-md` skill's
   `check_design_covers_code.py`) — every code file named; the read-order check (the `design-toc` skill) — `CURRENT`;
   the reachability check (the `top-level-design` skill) from the new `DESIGN.md` — nothing unreached; the state-file
   gate on each board.
5. **EXACTLY ONE CANONICAL DOCUMENT**: the new `DESIGN.md`. The old one is gone from that name, and the record is
   archive.

## THE STAGES — in order, every one, every time

1. **DEPRECATE.** The broken `DESIGN.md`, where there is one, stops being canonical the moment the process starts.
   Move it aside under a name that says so (`DESIGN.deprecated-<DATETIME>.md`), so nothing reads it as the design
   while the run is going. It is one of the things the run reads, as a claim to check, never as a source.
2. **INVENTORY EVERYTHING, AT THIS DATETIME.** Measure before reading (the rule
   `00-size-the-corpus-before-generating-into-it`): list every file git tracks, with its size, and among them every
   code file — the files the coverage gate will hold the new design to; list what runs — every container, daemon,
   store, port and scheduled job the project owns. Print the numbers and say whether the code fits one window. That
   list is the run's checklist: every file on it ends the run with a line in the design.
3. **ESTABLISH EVERY LINE BY READING OR MEASURING**, regardless of what any document, comment or name seems to say. A
   file is read whole. What a thing does is established by running it or reading its code; whether a thing is stored
   is established by asking the store through its own reader. A claim nobody read or measured does not go in.
   - **The code fits one window** → the session reads all of it itself, writing each file's line as it reads.
   - **It does not fit** → the session cuts the inventory into chunks that each fit one reader, and dispatches one
     reader per chunk with THE READER'S BRIEF below. Every file is in exactly one chunk. The session then reads every
     reader's findings file whole, and opens the cited lines itself for every statement the design's argument rests on:
     a reader locates, the session concludes (the rule `00-explore-reads-everything`).
4. **NO SPIN.** Nothing aspirational is mixed into what was found, and nothing is renamed nicer than it is.
5. **WRITE WHAT WAS FOUND, THEN THE CORRECTED VISION ON TOP OF IT.** What was found goes to the boards as rows
   (output 2). Then the vision: what the project is when it is finished, and the refactor pathways — the steps, in
   order, that carry it there from what was found. The vision is written after the finding, never before it.
6. **OUTPUT THE DESIGN SYSTEM THROUGH THE `design-md` SKILL.** Open that skill and write through it: the READ ORDER;
   one section per feature stating the final state and its steps (the refactor pathways are those steps); then the
   pages. The files pages are ASSEMBLED FROM THE READERS' FILES — each reader's rows of why a file exists and what it
   connects to become the rows of a files page, checked and worded as design — so the code is read once, by the
   readers, and never again to write the pages. Each reader's traces become the end-to-end pages. What a reader
   measured or found broken goes to the boards, never into a page. Then run the checks of output 4, write the dated
   record, and remove the deprecated design from the project's root into the record's folder.

## THE READER'S BRIEF — put it in every reader's dispatch, whole

A reader is dispatched to read, never to change anything. Its dispatch names the model the installation binds for such
agents (the rule `the-subagent-model`), the chunk as an explicit list of files, and the path of the findings file it
writes. It says, in these words:

> READ EVERY FILE ON YOUR LIST WHOLE, with the Read tool — no sampling, no searching in place of reading. Write your
> findings to the file named below, and return only that it is written. The file holds:
>
> 1. **ONE ROW FOR EVERY FILE ON YOUR LIST — no file skipped, no two files merged**, in a table with these columns:
>    the file's path · WHY IT EXISTS, in one line (what it is for; what would be missing without it) · WHAT IT
>    CONNECTS TO (what calls it and what it calls, what it reads and writes, each named with its file and line) · what
>    you MEASURED (did it import, run, pass — the command and its result — or `read only`) · every DEFECT you found,
>    each with its file and line.
> 2. **EVERY ENTRY POINT in your chunk** — a route, a command, a hook, a scheduled job — traced end to end, from the
>    entry to the lowest thing it touches, one hop per line, each hop with its file and line.
> 3. **EVERY CONVENTION the code relies on** that a reader of one file alone would miss, with where it is set.
> 4. **THE LIST OF FILES YOU READ.** It equals your list. A file you could not read is named with the reason.
>
> State only what you read or measured. Where a comment, a name or a document says one thing and the code does
> another, write what the code does and name the disagreement.

When a findings file comes back, count its rows against the chunk's list before using it. A file with no row is a file
unread: dispatch that file again. A row with no file and line in its connections is a claim, not a finding: send it
back.

## THE RECORD — `GROUND_TRUTH_<DATETIME>.md`

It is the record that the process ran, and it stays short: the datetime; the inventory's numbers and the branch taken
(read in one window, or by how many readers over which chunks); where each reader's findings file is; what the old
design claimed that the code contradicts; the checks of output 4 with what each printed; the questions only the owner
can answer, each also a row of the board's OPEN table. Name its folder on the new design's READ ORDER, on the line
`ARCHIVE AND PROGRAM FOLDERS:`. Once the new `DESIGN.md` stands, the record is never consulted as canon; a live ground
truth beside a live `DESIGN.md` means the process did not finish.

## NEVER

- run it on a new project
- write the vision before the finding
- stop at one page of conclusions and the readers' raw files
- brief a reader to "report what it finds": without the row per file, the pages cannot be assembled and the code is
  read a second time
- write a state into the design, or a design statement into the record
- leave two canonical documents

## THE ORDER OF ATTENTION

```rune
[Deprecate] ⇒ [InventoryAtThisDatetime] ⇒ [EstablishByReadingOrMeasuring] ⇒ [RefuseSpin] ⇒ [WriteWhatWasFoundThenTheVisionOnIt] ⇒ [OutputTheDesignSystemThroughDesignMd] ⇒ |ADesignThatAnswersEveryQuestion|
```

## NEXT

- stage 6 → the `design-md` skill: the design system is written through it, and its coverage gate closes the run
- stage 5 → the `state-file` skill: what was found, as rows
- the new `DESIGN.md` stands → the `design-toc` skill (its READ ORDER and table of contents), the `archi-diagram`
  skill (the stack drawn from the new design), the `top-level-design` skill (the reachability check; the project's line
  in the top-level design that holds it)
- a question only the owner can answer was found → the `how-to-settle-a-question-for-the-owner` skill
