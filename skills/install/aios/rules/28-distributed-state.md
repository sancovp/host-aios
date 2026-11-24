# Distributed dir-state — a `_states` rule is N TABLES, one per workflow

<docsys kind="states" role="law"/>

SHAPE:[
- `DESIGN.md` = PROSE, section by section, where a SECTION IS A FEATURE, stating the intended final state and the steps
  by which it evolves, never where anything stands
- **EVERY CURRENT STATE IS A ROW OF A BOARD, AND LIVES NOWHERE ELSE** — whether a part is built, how far it has come,
  what was measured, what is missing, what stands in pieces: a row at the states its dev flow defines, never a sentence
  in a design, a `CLAUDE.md`, a rule, a skill, a note or a scratchpad, and never in code — a comment, a docstring or a
  message string · a position no dev flow defines is defined in the
  same change: its dev flow states the state, its table gets the column, and the row is written with them
- a feature may have its own `DESIGN.md` in its own dir
- EVERY dir with a `DESIGN.md` has a `_states` rule — ONE PER IDENTITY: a project's AIOS has two, WORK (using the
  thing, in the copy in use) and DEV (building its next version, in a dev space — [[top-level-session-worktree]]),
  so it has two boards, both in its `.claude/rules/`: its DEV board, `<project>_dev_states.md`, what the project is
  building, and its WORK board, `<project>_work_states.md`, what it is producing · a project with one board today
  keeps it as its DEV board until it has work to track
- **A PARENT ROLLS ITS CHILDREN UP** — a dir whose design has child projects keeps on its board one table, `## THE
  PROJECTS`: one row per child project, linking down to that child's boards, its phases OUTSTANDING (a row of the
  child's boards stands short of its last phase) and CLEAR (none does), and nothing more — everything else is found
  below, by progressive disclosure · at a top, that table is THE TOP-LEVEL STATES DOC: redundant by construction, kept
  for closure ([[00-canonical-doc-paths]]) · above the tops, at the global home, the state is only the pointer down
- **a `_states` rule = N TABLES, ONE PER WORKFLOW TYPE** — a table IS the process by which one type of deliverable is
  produced in one type of situation: its COLUMNS are that process's general states, stated once in that type's dev
  flow and named, with that dev flow, by the table's phases line; its ROWS are the deliverables of that type, each a
  process — the set of its states, every state it has reached marked `●` · derive the states from the sequence the
  work actually traverses ([[28b-every-workflow-is-a-slice-of-one-sequence]]) · never borrow another lane's states
  (`BUILT` says nothing true about a book volume; `SECTIONIZED` says nothing about a daemon)
- the architecture map → `21-architecture-diagrams.md` · dev flows → `22-seq-<feature>.md`
- every `DESIGN.md` outside the home-unknown band ([[canonical-source-dirs]] LAW 0) is described in the top-level design and cohered into the global architecture
]

TRIGGER:[any dir where something is created / changed / built · dispatched agents included · writing or editing a
comment, a docstring or a message string in code · reading a comment that states a status · about to cite a code
comment as evidence]
DO:[OPEN THE `state-file` SKILL FIRST — the Skill tool, by its name, before the board's first write — and author the file
through it, then run its gate, the script in the folder Claude Code names as the skill's base directory when it loads · ONE BOARD PER IDENTITY IN
EACH DIR THAT HAS A `DESIGN.md` — its DEV board, and its WORK board once it has work to track — each N TABLES and
nothing else · THE COLUMNS ARE THE STATES, one column per state, named once in the table's phases line with the dev
flow that states them — never one "phase"/"status" column holding a word · A ROW IS ONE DELIVERABLE, the set of its
states, every state it has reached marked `●` in its cell, never a note below it · A ROW IS NEVER REMOVED for having
reached its last state: reaching the end says nothing about whether its states stay available · THE PROJECT'S OPEN LIST IS A
TABLE HERE: `## OPEN`, one row per question for *USER*, phases RAISED → PUT → RULED → CLEARED · the states file shows
DELIVERABLES AND THE STATES THEY HAVE REACHED IN THEIR DEV FLOWS, and nothing else ever shows there · a task's detail hangs off BY
POINTER into the project's real doc tree · keep the state of dir X IN dir X · EACH BOARD HAS ONE WRITER, the agent that holds its project's work: under a lead (the `how-to-lead-an-aios` skill), the lead writes only the parent's board and each child's agent only its own child's · a `## ` heading in a states file
introduces a WORKFLOW TABLE, never prose · move the states file as the work goes, in the same commit as the
work · IN CODE, A COMMENT SAYS ONLY WHAT THE CODE BESIDE IT DOES AND WHY IT IS SHAPED SO, a docstring and a message
string the same · remove a status statement found in code the turn it is found, and put its claim to a run before it is
repeated · establish what a system does by running it or reading its code, never by its comments]
NOT:[a file per CONCERN (a dir gets one board per identity, never more) · a work board's row in the dev board, or
the reverse · a `_states.md` in a dir with no `DESIGN.md` (write the DESIGN.md or
it has no state to keep) · a NOTES / INVENTORY / COVERAGE / DESIGN doc wearing the `_states` name · prose
sections (narrative · rulings · evidence write-ups) · ESSAY CELLS · a NOTE in any cell — a review status, a
date, a progress count, a commit, a ruling attached to another row's task, a pointer to a goal (notes go to the
project's own scratchpad, a committed rule, its ref in [[the-host-aios-scratchpad]]) · ARCHITECTURE (it goes in architecture documents) · one
central `everything_states.md` · a child's rows copied up into its parent (the parent says only whether the child has
work, linking down) · a comment, a docstring or a message string in code saying whether something else is built, works,
is reached, is pending, is disabled or was changed · a date, an incident or a ruling in code · a code comment cited as
evidence of what a system does or of where anything stands]
GATE:[the `state-file` skill's `check_state_files.py`, `python3 <its folder>/check_state_files.py <project>/.claude/rules/<name>_states.md` — ships
with this AIOS, beside the skill that authors what it checks; a relative or absolute board path both work ·
fails prose sections and essay cells · run it BARE and read its OUTPUT, never only its exit code · with NO
argument it refuses (`NOTHING WAS CHECKED — 0 files`, exit 1), which is not a pass]
