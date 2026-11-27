---
name: aios-artifacts
description: WHEN you are about to make a new folder of its own (a project, a tool, a program, any piece of work that will live in a folder of its own), open this skill before that folder's first file and walk its steps, so the folder is made an AIOS in this AIOS's form by you, not later by someone else; also WHEN a folder is found without its design, board or map. It decides whether the project is new or exists, then makes its DESIGN.md, its board and its architecture map through their skills, then wires it into every index above it.
---

# aios-artifacts — compiled skillchain

> Compiled by `skillchain.py`. Orchestrates 6 step(s) composing 4 skill(s).
> **Dependencies (validated present at compile time):** `archi-diagram`, `design-md`, `ground-truth`, `state-file`

**Execute the steps below in order.** Carry each step's result forward; where a step references `{var}`, substitute the captured value from the named earlier step.

## Step 1 — reasoning bridge (CoR / AttentionChain)
Reason explicitly, step by step:

> Decide whether this project is NEW (no folder yet, or a folder with nothing but what you are about to make) or EXISTING (a folder with work in it whose DESIGN.md is wrong, mangled or absent). Make the folder inside this AIOS's workspace, with its CLAUDE.md saying what it is for and its empty .claude/rules, .claude/skills and .claude/agents, before its first file. A NEW project skips the next step, ground-truth, which is never run on a greenfield project, and goes straight to design-md, writing the DESIGN.md from the intent the request states. An EXISTING one runs ground-truth first.

State the conclusion, then carry it forward as the input to the next step.

## Step 2 — invoke skill `ground-truth`
*Run the GROUND_TRUTH process — a project exists and its DESIGN.md is wrong, mangled or absent. Deprecate it, go through everything at this datetime regardless of what it says, establish every line by READING or MEASURING, no spin, then write the corrected vision and the refactor pathways onto what was FOUND. Outputs DESIGN.md; leaves GROUND_TRUTH_<DATETIME>.md as the dated record. THE LAW is 00-samaya section V — never a greenfield, never two canonical docs*

Invoke the **ground-truth** skill (no extra input)

## Step 3 — invoke skill `design-md`
*Author or repair the ONE DESIGN.md a project owes. Prose, one section per FEATURE, the intended final state and the steps by which it evolves — never where anything stands, which is a row of its boards; a state found in it fenced where it stands, every word unchanged, moved into the boards by whoever next works on the project, the fence removed only once that state is reconciled and every intended thing is built as intended — a detail doc rolled IN with a pointer left behind, updated in the same commit as the change it describes. THE LAW is rule 26 — one per PROJECT never per dir, named DESIGN.md and nothing else, and a loading mechanism is never a design doc*

Invoke the **design-md** skill (no extra input)

## Step 4 — invoke skill `state-file`
*Author or repair a _states.md so it is a MAP of where work is. N tables, each the process by which one type of deliverable is produced, its columns that process's general states SPECIALIZED from the construction sequence and stated once in its dev flow, rows are deliverables, every state a row has reached marked and a row never removed for having reached its last state, detail by pointer. THE LAWS are rules 28 and 28b and 29 — a procedure flow gets a 22-seq rule and is never boarded*

Invoke the **state-file** skill (no extra input)

## Step 5 — invoke skill `archi-diagram`
*Author the architecture diagrams a project owes. A mermaid flowchart per altitude, subgraphs marking boundaries, arrows meaning dependency direction, every external dep ending AT ITS SEAM because a dep's internals are its own architecture, plus the three-column general-specific-code bijection. THE LAW is rule 23*

Invoke the **archi-diagram** skill (no extra input)

## Step 6 — reasoning bridge (CoR / AttentionChain)
Reason explicitly, step by step:

> Wire the project into every index above it, the same turn. Its one line in the workspace's CLAUDE.md, saying what it is. Its row in the project registry, which user_info binds. Its line in the top-level design that holds it, written through the top-level-design skill. Its scratchpad rule, its first section opened with your mode line. Then save it all by its own paths. A project that no index above it names has not been made yet.

State the conclusion, then carry it forward as the input to the next step.

## Done
Return the final step's output as the result of this chain.
