---
name: how-to-lead-an-aios
description: WHEN the work of an AIOS that has child projects is to be done — its CLAUDE.md names this skill as the starting skillchain for its children's work — lead it from its root, its board's table of child projects in hand, one agent started or resumed for each child with work left, each board written by one agent only, each child's closure moved up, the reviews dispatched by the lead, a change to the program reported up and never made, finished work opened for the owner, then a report up.
---

# how-to-lead-an-aios — one agent holds an AIOS, as one agent holds a piece of work

You are the lead of an AIOS that has child projects: one agent, working from the AIOS's root, holding the AIOS as each
child's agent holds its child's work. The work is arranged in levels the way the designs and the boards are, one
pattern at every level, so you do at the AIOS's level what each child's agent does at its own, and nothing more. You are
in work mode: you change none of the program.

## THE STEPS — in order, each opening what holds it

1. **THE MODE LINE.** Open your section of the AIOS's scratchpad (rule `the-host-aios-scratchpad`, rules 2 and 6) with
   `MODE: WORK · <the AIOS> · its workspace · GOAL: <the request in one line>`.
2. **THE TABLE OF ITS CHILDREN.** Read the table of the AIOS's child projects on its WORK board (rule
   `28-distributed-state`, a parent's table of its children, opened through the `state-file` skill): each child
   OUTSTANDING or CLEAR, each linking down to that child's boards.
3. **ONE AGENT PER CHILD WITH WORK LEFT.** For each OUTSTANDING child, start one agent, or resume the one already holding
   it, through the dispatch seat (rule `the-subagent-model`: the binding names what fills the seat, and you name the
   model for each level of orchestration) — Claude Code's helper agents, the Agent tool, the mechanism measured working
   (the `understand-subagents` skill); its agent teams were not available to the headless session that measured them
   (the `understand-teams` skill). Give it the child's folder and order it to call that child's own starting
   skillchain, which the child's `CLAUDE.md` names, to save what it makes through the `how-to-save-work` skill, and to
   move its own boards as its work reaches each state. Never give it your conversation: it reads its child's canon
   itself, so each piece of work costs its own reading and passes. Keep the agent's id, which the Agent tool's result
   names: to hand that agent anything later, resume it with SendMessage to that id, never a new agent.
4. **ONE WRITER PER BOARD.** Each child's agent writes only its child's files — what it makes, its boards and its
   scratchpad — and you write only the AIOS's own (rule `28-distributed-state`): you never write a file of a child's, or
   tell its agent to leave one to you, even when its agent cannot finish. A child's agent launches no agent of its own
   (rule `subagent-worktree-isolation`): Claude Code does not stop a helper agent from launching one, as measured, so
   say it in each child's prompt.
5. **EACH CHILD'S CLOSURE, MOVED UP.** When a child's agent reports its work done, read that child's boards, then move
   the child's cell on your table — CLEAR once no row of its boards stands short of its last state — in the same commit
   as the work that moved it, the gate the `state-file` skill carries run bare on your board.
6. **THE REVIEWS AND THE TESTS.** A child's agent dispatches none, so when a child reports a substantial change done,
   you call its review (rule `call-the-gan-when-you-think-youre-done`, the `make-everything-better-gan` skill) and any
   test it needs (rule `the-subagent-model`), and hand the findings to that child's agent, resumed as step 3 says,
   which makes the change and saves it — a child whose own work asks for a review before it saves reports its draft
   for that review, and saves it once resumed with the findings.
7. **A CHANGE TO THE PROGRAM, REPORTED UP.** A child that needs a change to the program — what its next piece of work is
   made with, a skill, a rule or a guard that stops its work among it — reports it, and you put it before development:
   a row on the DEV board and a note on the scratchpad (rule `the-host-aios-scratchpad`). You never make it, and you
   never do the child's work in its place: its cell stays OUTSTANDING; development starts from the
   `how-to-develop-a-project` skill, in the dev space, as a version, and the child's work carries on once the copy in
   use is pulled up to it.
8. **APPROVAL STAYS THE OWNER'S.** Finished work, saved where the `how-to-save-work` skill says, is opened for the owner,
   who watches and gives notes; a note goes back to the child's agent that holds the work.
9. **THE REPORT UP.** Report to the lead of the AIOS above, or to the owner where there is none: which children moved,
   which closed, what was reported up to development, what waits on the owner.

## NEVER

- a child's agent launching agents, or you copying your conversation into a child's agent
- a board written by any agent but its one writer
- a child's work done by you, or any file of a child's written by you — what it makes, its boards, its scratchpad
- a change to the program made from work mode, by you or by a child
- a child's cell moved before its boards show it

## NEXT

- each OUTSTANDING child → that child's own starting skillchain, which its `CLAUDE.md` names, called by its agent
- a change a child reported → the `how-to-develop-a-project` skill, for the development session that makes it
- a new child project to be made → the `aios-artifacts` skillchain, in a work session
