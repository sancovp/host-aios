---
name: design-md
description: WHEN you are about to write, change or repair a project's DESIGN.md or a page under it, or a file is added to, renamed in or removed from its code, open this skill first and write the design through it — one DESIGN.md per project at the head of a design system that covers every file of the code, why it exists and how it connects to everything else, a long explanation a linked page in its `design/` folder, the intended final state and its steps and never where anything stands — then run its coverage gate bare.
---

# design-md — how to write a project's design: one `DESIGN.md` at the head of a design system that covers every file

The law is the rule `26-canonical-design`; this skill is how it is done. Open the `design-toc` skill with it at every
edit of a `DESIGN.md`: that skill keeps the READ ORDER and the table of contents.

## WHAT A DESIGN IS

A project's design is what anyone reads instead of reading the code. It says what the project is when it is finished,
how it works, what its parts are and how they meet, and the steps by which it gets there. It is the thing the code is
checked against, by one question: is this implemented as the design says, or as it implies? So a design is never
rewritten down to describe broken, partial or stubbed code, and it never says where anything stands.

A design is a SYSTEM of documents with one head. `DESIGN.md`, at the project's root, is the head: the top page. Under
it sit detail pages, each linked from the section that owns its topic. Any question about the project is answered from
`DESIGN.md` and the pages it links. A question they cannot answer means a page is missing, and writing that page is
the work: read the code that answers the question once, write the page, link it, then answer from the page. Reading the
code again each time the question comes back is the failure this skill exists to end.

## THE LAWS

1. **ONE PER PROJECT, NAMED `DESIGN.md`.** A project is one entity — its own abstraction, running on its own context.
   It has one `DESIGN.md`, at its root, read inside the folder it designs. A folder inside a project gets a section of
   that design, never a `DESIGN.md` of its own; a project nested inside another keeps its own. A rule or a `CLAUDE.md`
   is a loading mechanism and is never a design document.
2. **IT OPENS WITH ITS READ ORDER.** The first `##` heading is `## READ ORDER`: what this level is, then for which
   work which section, which page, which child design and which procedure to read, then the lines naming the folders
   the checks leave alone (the `design-toc` skill has the form).
3. **THE FINAL STATE AND ITS STEPS, NEVER THE STATE.** Prose, one section per FEATURE. Each section states the intended
   final state of its feature and, where the project reaches it through steps or versions, those steps in order, each one a design of its own: written completely, everything in it solved end to end, through the highest version the vision holds. Whether
   a part is built, how far it has come, what was measured, what is missing — every current state — is a row of the
   project's boards (the `state-file` skill) and is written nowhere in a design.
4. **IT COVERS EVERY FILE OF THE CODE.** Every file that exists in the project's code has its line in the design: WHY
   THE FILE EXISTS — what it is for, which section of the design it carries out, what would be missing without it — and
   HOW IT CONNECTS TO EVERYTHING ELSE — what calls it and what it calls, what it reads and writes, which files and
   functions it hands to and takes from, by name. Every file means every file: the program's modules, its scripts, its
   tests (what each one proves, and of which file), its build and container files, its hooks, the scripts its skills
   carry. A file the final state does not hold is covered too: its line says so, and which step removes it.
5. **AN EXPLANATION TOO LONG FOR ITS SECTION IS A PAGE OF ITS OWN.** It goes in a `design/` folder beside `DESIGN.md`,
   is linked from the section that owns its topic with one line saying what the page answers, and is listed in that
   folder's `CLAUDE.md` with the same line. The section keeps the statement; the page keeps the length.
6. **A FILE ADDED TO THE CODE IS ADDED TO THE DESIGN IN THE SAME CHANGE.** So is a file renamed or removed, and so is
   any change to what a file is for or what it connects to: the design and the code move in one commit, and what
   changed, the reading it replaced and why are appended to the `CHANGELOG.md` beside the design.
7. **NOTHING ELSE IS KEPT BESIDE IT.** A written file that says what the project is, does or is meant to be, and is
   no page of the design, is absorbed: every statement of it is placed in the page that owns its topic, what a
   statement replaced is appended to `CHANGELOG.md`, and the file is deleted. It is never kept as archive, record,
   pointer or reference.
8. **THE CODE IS THE REALITY; THE DOCUMENTS HOLD THE VISION.** What the project is meant to be is gathered from every
   document that ever spoke about it, resolved in date order, and factored into the designs about the code. What the
   code does is gathered from the code. A design is never written from the code alone, and where the two differ the
   difference is a row of the board.

## HOW TO WRITE ONE — in order

1. **Find the project that owns the thing.** Name what the project ends as — a program, an application or a plugin —
   and its install shape; the design says both.
2. **List the code.** Run this skill's gate (below) on the project before writing: what it lists is every code file
   the design does not yet name, which is the list to cover. For a new project the list is empty and grows with the code.
3. **Write the READ ORDER**, then one section per feature: the final state, then its steps.
4. **Cover the files.** Group them by the feature or the folder they belong to. Where a group is a handful of files,
   give each its line inside the section. Where it is long, write a files page in `design/` — one table per group,
   three columns: the file, why it exists, what it connects to — and link it from the section. Write each file by a
   name no other file shares: its folder with its name wherever two files have the same name.
5. **Write a page for every explanation that outgrew its section**: one thing traced end to end with each hand-off
   named, the conventions in the order they run, a protocol, a format. Each page opens by naming the sections it
   details, and says nothing a section already says in full.
6. **List the pages** in the `CLAUDE.md` of the `design/` folder, one line each, the same line the section uses for its link.
7. **Move every state out.** Anything you were about to write about where things stand goes to the board as a row.
8. **Run the checks, bare, and read what each says**: this skill's coverage gate; the read-order check (the
   `design-toc` skill); the reachability check (the `top-level-design` skill), from this `DESIGN.md`.
9. **Read it as a stranger.** Take three questions someone new to the project would ask and answer each from the
   design alone. A question that sends you to the code names the page to write next.

## THE PAGES — the `design/` folder

```
<project>/DESIGN.md              the top page: READ ORDER, one section per feature, each linking its pages
<project>/design/CLAUDE.md       what the folder is, and one line per page
<project>/design/<topic>.md      a detail page: opens by naming the sections of DESIGN.md it details
```

A page is a design document like the top page: the final state only, no current state, rewritten whole when its
ruling changes. Its first lines carry the banner `REFERENCE DETAIL — READ when its topic is the active task; NOT
deprecated, NOT skippable`. A page may link further pages; every page is reached from `DESIGN.md`.

## THE GATE THIS SKILL CARRIES — `check_design_covers_code.py`, beside this file

```
python3 "${CLAUDE_SKILL_DIR}/check_design_covers_code.py" <project folder, or its DESIGN.md>
```

It lists every code file under the project that neither `DESIGN.md` nor a page it reaches names, exit 1 when any; a
pass names the design it checked and how many code files and pages it read. A code file is one git tracks or would
track with a source extension, a build file such as a `Dockerfile`, or a script with no extension and a `#!` first
line (`--ext .xyz` adds an extension). A file is named when a page writes its path from the project folder, or an end
of that path no other code file shares; a file written only by a name other files share is listed apart, to be written
with its folder. A board, a scratchpad, a changelog, a dated ground-truth record and a `CLAUDE.md` are never counted
as a page: none of them is the design.

It leaves unchecked, and counts in its output: build output; the project's own `workspace/`, which holds what using
the project made and never its program; the folder of a child project, which its own design covers; and the folders
the READ ORDER names on the line `COPIES, GENERATED OUTPUT AND RUN EVIDENCE:`. Name a folder on that line only when
its code is a copy of code that lives elsewhere, the output of a generator, or the evidence of a run, and say in the
design which it is and what makes it. The code a design is the design of is never named there. The line `ARCHIVE AND
PROGRAM FOLDERS:` is about documents and exempts no code.

⛔ **RUN IT BARE AND READ WHAT IT SAYS.** It tells that a file is named. It cannot tell whether the line beside the
name says why the file exists and what it connects to: that is judged by reading the page. A design that passes the
gate with a list of bare names has not covered anything.

## THE GROUP PAGES — every line of the code, and the vision factored onto it

Where the ground-truth process writes the design (the `ground-truth` skill), the code is cut into groups of modules
that make sense to group, and each group has ONE page in `design/`. A group page holds three things, in this order:

1. **THE DESIGN of the group** — the whole vision for it, gathered from every document that ever spoke about it and
   resolved: what the group is when it is finished, and every stage on the way there, each stage a design of its own,
   written completely and solved end to end.
2. **THE CODE, line by line** — the reality. Per file, a heading `## <the file's path in backticks> — N lines`, a
   paragraph of why the file exists and what it connects to, then a table whose first column is a line range `a-b`:
   what the range is, what it does, what calls it, what it calls. The ranges of a file run from 1 to N with no gap.
3. Nothing about where anything stands: for every part of the design, whether the code does it, differs from it or
   lacks it is a row of the project's board.

The code is the reality and never the truth of what is meant: a group's design is never written from its code alone.

## THE WHOLENESS GATE — `check_design_is_whole.py`, beside this file

```
python3 "${CLAUDE_SKILL_DIR}/check_design_is_whole.py" <project folder, or its DESIGN.md>
```

It fails while the design is not the whole of the project's writing and code. It lists every code file whose lines
no page accounts for from 1 to its last line with no gap, and every written file that is not the design, the code or
the AIOS's own files. A written file is allowed only as: `DESIGN.md` and the pages of `design/`; a `CLAUDE.md`;
anything under a `.claude/` folder; the root `CHANGELOG.md`; a `README` beside a build file; a licence or a
requirements file; a file under a `workspace/` folder the READ ORDER names on a line `OUTPUTS OF USE:`; and the files
of a child project. A code file the owner ruled is not to be read is named on a READ ORDER line `NOT READ BY RULING:`.
Run it bare and read what it prints. It cannot tell whether a row says what its lines do: that is judged by a reader
who built nothing.

## WHEN A DESIGN IS FOUND HOLDING STATE

State is found by reading the design, never by a program. Each passage of it — the whole paragraph, list item, table or
section that holds it, never part of a sentence — is fenced where it stands, every word unchanged, between the line
`> **WARNING: STATE MENTIONED IN DESIGN.MD -- NOT ALLOWED IN DESIGN. THIS MUST MOVE TO STATE FILE WHEN WORKED ON. DO NOT
REMOVE THIS FENCE UNTIL THE STATE IS RECONCILED AND EVERY INTENDED THING IS BUILT AS INTENDED. DO NOT SKIP THIS.**`
before it and the line `> **END OF STATE FENCE**` after it, each written as one line. Whoever next works on the project
moves each fenced passage into its boards as rows; the fence is removed only once that state is reconciled and every
intended thing is built as intended.

## THE ORDER OF ATTENTION

```rune
[LocateTheOwningProject] ⇒ [OneSectionPerFeature] ⇒ [StateTheFinalStateAndItsSteps] ⇒ [CoverEveryFileOfTheCode] ⇒ [GiveEachLongExplanationItsPage] ⇒ [MoveEveryStateToTheBoards] ⇒ [RollDetailInAndLeaveAPointer] ⇒ |OneDesignSystemThatAnswersEveryQuestion|
```

## NEXT

- the `DESIGN.md` changed → the `design-toc` skill: its READ ORDER and its table of contents, in the same commit
- a state turned up while writing → the `state-file` skill: a row of the board
- a layer, a component or a dependency was added, removed or moved → the `archi-diagram` skill: the stack redrawn
- the project exists and its design is wrong, mangled or absent → the `ground-truth` skill first; it outputs the
  design system through this skill
- a page was added → the `top-level-design` skill's reachability check, from this `DESIGN.md`
