---
name: state-file
description: Author or repair a _states.md so it is a MAP of where work is. N tables, each the process by which one type of deliverable is produced, its columns that process's general states SPECIALIZED from the construction sequence and stated once in its dev flow, rows are deliverables, every state a row has reached marked and a row never removed for having reached its last state, detail by pointer. THE LAWS are rules 28 and 28b and 29 — a procedure flow gets a 22-seq rule and is never boarded
kind: attention-chain
---

This is an **attention chain** — an INNER template for how to think about something (a scaffold for a section or for your thinking). Not necessarily spoken.

## THE GATE THIS SKILL CARRIES — `check_state_files.py`, beside this file

```
python3 "${CLAUDE_SKILL_DIR}/check_state_files.py" <project>/.claude/rules/<name>_states.md
```

It REFUSES: a file with no table · a `##` heading with no table under it (appended prose) ·
a preamble over 1,500 chars · a cell over 300 (evidence is a POINTER, never a paragraph) ·
more than one board per identity in a dir · a states file in a dir with no `DESIGN.md`.
`--json` emits the findings as a machine-readable backlog.

⛔ **RUN IT BARE AND READ WHAT IT SAYS.** Piping returns the pipe's exit code, not the gate's.
The output names the file, the line, the measure, the limit and the law; the exit code names
none of those. A pass names every file it checked — a pass that does not name the board you meant
did not check it.
**POINT IT AT THE BOARD YOU MEAN** — a relative or an absolute path: every argument is made absolute
first, so the per-dir `DESIGN.md` check reads the board's own dir, whatever the cwd.

⇒ **A rule that binds to a gate must CARRY the gate** — rules 28 and 28b bind to this one, so it
ships here rather than being reached for. ⛔ **NOT rule 29.** 29 governs POINTERS (*every row
carries a path*) and this gate never checks whether a row's pointer RESOLVES; claiming 29 binds
here would advertise a detection that does not exist. Whether it should is an open board question. ([[24-scaffold-to-harness]]: a gate adds
DETECTION, never authority — the rules bind whether or not it runs.)

## THE TWO BOARDS — one per identity (rule 28)

A project's AIOS has two identities, so a project has two boards, both in its `.claude/rules/`: its **DEV board**,
`<project>_dev_states.md` — what the project is building, worked in a dev space — and its **WORK board**,
`<project>_work_states.md` — what it is producing, worked in the copy in use. A project with one board today keeps it
as its DEV board until it has work to track; the WORK board is made the first time it does. A row goes on the board
of the identity whose work it tracks, never on the other.

## Chain (custom syntax)
```rune
[AnswerTheFourQuestions] ⇒ [SpecializeTheSequence] ⇒ [BoardLifecycleOnly] ⇒ [MarkEachReachedState] ⇒ [HangDetailByPointer] ⇒ |PositionMap|
```

## How to use it
# Attention chain — state-file
Attend, in order:
  1. AnswerTheFourQuestions
  2. SpecializeTheSequence
  3. BoardLifecycleOnly
  4. MarkEachReachedState
  5. HangDetailByPointer
Hold: PositionMap  ← converge attention here, then act
