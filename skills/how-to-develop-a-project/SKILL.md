---
name: how-to-develop-a-project
description: WHEN a session is asked to fix, add, change or improve a project that exists, or a report from that project's work reaches it — open this skill before anything else and walk its ten steps, the same for every project, from the mode line and the design read to a version a fresh worker has proven, shipped and pulled back. A work session, asked to make or do something with a project, calls that project's own starting skillchain instead.
---

# how-to-develop-a-project — where every development session starts

You are developing a project: changing what its next piece of work is made with — its code, its skills and rules, its
design, its libraries and packages. Every agent carries both modes; a session asked to make or do something with a
project is in work mode and starts from that project's own starting skillchain, which its `CLAUDE.md` names, never
from here. Under a `/goal`, the goal's read list is step 2's read and the goal file is your goal.

## THE STEPS — in order, each opening what holds it

1. **THE STARTING SKILLCHAIN, THEN THE MODE LINE.** Load the project's starting skillchain first: the skill or flow its
   `CLAUDE.md` names on the line holding the words `starting skillchain` — read that `CLAUDE.md`, then open the chain
   with the Skill tool, or read its file whole. A session that has not loaded it does not work in the project, and
   after a compaction, a resume or a clear it is loaded again before anything else (rule `00-top-level-design-first`,
   THE GATE). A project whose `CLAUDE.md` names none owes one: say so, read its `CLAUDE.md`, its `DESIGN.md` and its
   board instead, and name the chain it lacks as work owed (the `how-to-make-the-abstraction` skill). Then open your section of the project's scratchpad (rule `the-host-aios-scratchpad`, rules 2 and 6)
   with `MODE: DEV · <the project> · <its worktree in the dev space, once step 5 makes it> · GOAL: <the goal file, or
   the request in one line>`. The scratchpad loads in every window and after every compaction, so you read it again
   without being asked.
2. **THE DESIGN READ.** Find the top and check the wiring (rule `00-top-level-design-first`), then read the project's
   canon: its `CLAUDE.md`; its `DESIGN.md` through its READ ORDER (the `design-toc` skill); its DEV board (the
   `state-file` skill); its scratchpad; and, for a wired project, its top's top-level design (the `top-level-design`
   skill).
3. **CONFIGURABLE YET?** Name what the project ends as and whether it hardcodes its user, its agent or its machine
   (rule `00-the-work-loop`, step 0). Not yet ⇒ making it configurable is the work, first.
4. **THE DEV FLOW.** Name the dev flow the change follows and open it — the project's `22-seq-<feature>.md`, or its
   how-to-change skill. New architecture gets a new dev flow, placed on the architecture map (rule
   `23-architecture-layer`, the `archi-diagram` skill). A second thing of a kind, or a fix made by hand before, opens
   the `how-to-make-the-abstraction` skill first; a pattern that lacks the abstraction to close it is said first, and
   closed before anything else is inferred about it.
5. **THE DEV SPACE.** Pull the copy in use with nothing lost, then make a worktree of its own (rule
   `top-level-session-worktree`: CODE, and point 12); write its path into your mode line.
6. **THE CHANGE.** Make it there, through the project's own system — its compiler, its library, its generator — never by
   typing what the system computes; the project's `DESIGN.md` rewritten in the same change (rule
   `26-canonical-design`, the `design-md` skill).
7. **A VERSION.** Run every check for the kinds of file the change touches (rule `00-docsys`, THE PATTERNS UP FRONT),
   raise the version in the project's build file and append its `CHANGELOG.md` entry (rule
   `top-level-session-worktree`, point 13).
8. **A FRESH WORKER.** Prove it by a fresh agent in work mode doing the work right with it, from the project's starting
   skillchain. A failure is a defect in the change: fix it at its source and prove it again.
9. **SHIP IT.** By the repository's own git loop — a ready pull request where it has a merge queue, a push where its
   own rules put code on its default branch (rule `top-level-session-worktree`, points 2 to 7) — then pull it back
   into the copy in use, install it, and remove the worktree (point 12). A change to this AIOS itself reaches the
   machine by a release where `user_info` binds THE AIOS RELEASES.
10. **THE BOARD AND THE NOTES.** Move the DEV board in the same commit as the work (rule `28-distributed-state`, the
    `state-file` skill), and roll your scratchpad section up (rule `the-host-aios-scratchpad`, rule 4).

## NEVER

- a change begun before steps 1 and 2, or from a summary of an earlier window
- code changed in the copy in use, or the change handed to a dispatched agent (rule `subagent-worktree-isolation`)
- a change called done before a fresh worker has done the work with it

## NEXT

- the change is shipped → the project's starting skillchain, the one its `CLAUDE.md` names, for the worker who proves it
  (step 8)
- the project has no starting skillchain yet → its first piece of work made by hand, then the
  `how-to-make-the-abstraction` skill
- a new project is to be made → that is this AIOS's own work, started in a work session by the `aios-artifacts`
  skillchain
- the project has child projects → their work starts from the `how-to-lead-an-aios` skill, which its `CLAUDE.md` names
  as the starting skillchain for its children's work
