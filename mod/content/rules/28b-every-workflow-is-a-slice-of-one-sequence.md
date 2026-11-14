# 28b — EVERY DEV FLOW IS A SLICE OF ONE SEQUENCE (do not invent phases; specialize)

<docsys kind="dev-flow" role="law+template"/>

> This rule is the generator behind [[28-distributed-state]]'s tables. **THE SEQUENCE ITSELF IS STATED
> INSIDE THIS AIOS** — the thirteen stations, their glyphs, their symbols and their stacked chain
> representations, in the `the-thirteen` skill. This rule is the LAW (every dev flow is a slice of
> it); that skill is the BASE. A rule's number and placement belong to the ruleset's owner.

PRINCIPLE:[a STATE is a position in a process · the only process a task moves through is a DEV
FLOW ⇒ **every table in a state file is a dev flow, and nothing that is not a dev flow can be a
state** · and the dev flows are not independent inventions — each is a SLICE of one construction
sequence, specialized to its domain]

## THE GENERATOR — the 13-step construction sequence (= the yana ladder, 13-for-13)

```
 1  →           representation      give the thing a form you can work
 2  A → B       unopened morphism   ⛔ THE FAILURE: running 1..13 at ONE increment
 3  A→1→2→3→B   open morphism       parts. never a summary
 4  ⊆           monotone refinement Info(Sₙ) ⊆ Info(Sₙ₊₁) — adds, never loses information (text may go)
 5  +1          local witnesses     each part carries its own check
 6  F(x) = x    closure / LFP       the pass stops changing it
 7  ⊢  |  ⊬     admissibility       THE GATE — and what its failure looks like
 8  ⊨           bijective reconstr. it maps back, both directions
 9  X ≅ X       automorphism        same-same-but-different
10  E(you)=you  reify               it becomes a citizen of the domain
11  +1 → 1      MST                 the lift
12  ⌜X⌝         new label           the name IS the diagram
13  ⊢ D∞        repeat              step 13 re-enters as step 1
```

## THE FOUR QUESTIONS — answer these and the phases FALL OUT

| # | question | yields |
|---|---|---|
| Q1 | what IS the thing? | step 1 — the representation phase |
| Q2 | what is a PART of it? | step 3 — what opening produces |
| Q3 | what is its GATE, and what does ⊬ look like? | step 7 — admissibility |
| Q4 | what is it CALLED when it lands? | steps 10/12 — reify · label |

**A domain whose four questions cannot be answered is UNREAD.** It does not need a board; it needs
the read. Writing phases for it produces a fake sequence, which is worse than an empty row.

## WORKED — two flows, one ladder, different nouns

| step | VOLUME PRODUCTION (a book) | CORPUS ROLL-UP (a research archive) |
|---|---|---|
| 1 representation | OUTLINED | SECTIONIZED |
| 3 open morphism | READ (sources opened, never summarized) | ATOMIZED |
| 4 monotone refinement | DRAFTED | GROUPED |
| 6 closure / LFP | — | ORDERED |
| 7 admissibility | AUDITED | — |
| 8 bijective reconstruction | CUT (§H ↔ §M) | — |
| 10/12 reify · label | STAMPED | FACTORED (lands at §N.M) |

A flow SELECTS the steps that apply. It does not run 1–13 in order, and it does not add steps the
sequence does not have.

## THE SPLIT — which artifact a flow becomes

| | LIFECYCLE flow | PROCEDURE flow |
|---|---|---|
| test | a task HOLDS a position between sessions | every stage runs EVERY time |
| example | vol-08 *is* at AUDITED, and still will be tomorrow | RETRIEVE → THE CHANGE → COHERENCE SET → THE PROOF |
| artifact | **a TABLE** in `<dir>/.claude/rules/<name>_states.md`, its states stated once in its dev flow, which the table names | **a RULE** at `<dir>/.claude/rules/22-seq-<feature>.md` |
| shape | rows = DELIVERABLES · columns = their type's general STATES · `●` = each state reached · a row never removed for reaching its last state | the stages, in order, as obligations |

⇒ **a dev flow and a state table are the same object at two grains** — the dev flow (a `22-seq-` rule, or the how-to
skill a procedure becomes) states the flow's states once, the table names them and tracks which deliverable is where
in it. Neither substitutes for the other.

DO:[
- derive a flow by specializing the sequence — Q1–Q4, then name the phases in the domain's nouns
- give a dir one state file per identity — its DEV board, and its WORK board once it has work to track
  ([[28-distributed-state]]) — each with N tables, one per lifecycle flow that starts there
- write a `22-seq-<feature>.md` for each procedure flow, and for each lifecycle flow the dev flow that states its states
  once — a `22-seq-<feature>.md` or a how-to skill — which its table's phases line names
- mark a domain UNREAD when Q1–Q4 cannot be answered, and read it before boarding it
]
NOT:[
- borrow another lane's phases (`BUILT` says nothing true about a book volume; `SECTIONIZED`
  says nothing about a daemon) — a borrowed legend claims the task is in a flow it is not in
- invent a sequence from scratch when the generator already has the step
- put a procedure flow in a table (nothing ever sits in one of its stages)
- track anything that is not a dev flow — it is not a state
]

TRIGGER:[writing or repairing any `_states.md` · adding a column to any board · a board whose
phases say nothing true about its lane · a project with a `DESIGN.md` and no board · about to
invent a sequence (⇒ specialize instead) · any "what are the stages of X" question]

⚠ **THE FIXPOINT, and it is not decoration:** this rule, the boards, the gate, and the template
were produced by running the sequence on the system's own workflows — represent, open, gate,
reify, name. **The workflow that makes workflows is an instance of itself.** ⊢ D∞.

## THE TYPE LADDER — "dev flow" is the uniform NAME; the TYPE ascends

**In actual ontology the genus is INSTRUCTION.** What varies with altitude is generality and
binding — the word "dev flow" stays constant while the type it names ascends, and the higher type
never refutes the lower (the rule-23 shape, on our own vocabulary):

| altitude | what it actually is | binding | example |
|---|---|---|---|
| generator | **the FORM of instruction-sequences** — instructs nothing directly; it TYPES | none — it is the type | the 13 steps |
| lifecycle flow | instructions whose subject **holds a position** between sessions | a TABLE in `_states.md` | `OUTLINED → … → STAMPED` |
| procedure flow | instructions **run whole, every time** | a `22-seq-<feature>.md` rule | `RETRIEVE → … → PROOF` |
| dev flow proper | literal edit-grain instructions — *"edit this module, add one of Type here"* | the turn's tool calls | an Edit sequence |

⇒ and the neighboring artifact kinds are the SAME genus at other bindings: a **rule** = standing
instruction · a **skill** = callable instruction · a **goal** = scoped instruction-with-terminus ·
a **board** = instructions with position tracked. One genus, projected by binding-time.

## THE DIAGRAM

```
════════════════════════════════════════════════════════════════════════════════════════════
              THE ONE GENERATOR — the construction sequence (⊢ D∞) · §29 · the yana ladder
════════════════════════════════════════════════════════════════════════════════════════════

  1      2       3          4      5       6        7       8      9      10        11     12     13
  →    A → B  A→1→2→3→B    ⊆     +1    F(x)=x    ⊢ | ⊬    ⊨    X ≅ X  E(you)=you  +1→1   ⌜X⌝   ⊢ D∞
  │
  │            ⛔ the ONLY illegal move: run 1..13 at ONE increment (= step 2, the unopened
  │               morphism — it produces commits and exhaust, never the thing)
  ▼
┌───────────────────────────────────────────────────────────────────────────────────────────┐
│ specialize(SEQ, domain) — never invent, ASK Q1..Q4:                                       │
│   Q1 what IS it? ────────────► step 1     Q3 what is its GATE / ⊬? ──► step 7             │
│   Q2 what is a PART of it? ──► step 3     Q4 what is it CALLED? ─────► steps 10/12        │
│   unanswerable ⇒ UNREAD ⇒ read it; NEVER board it                                         │
└────────────────────┬─────────────────────────────────────┬────────────────────────────────┘
                     │ holds a position between sessions   │ every stage runs every time
                     ▼                                     ▼
          ╔════════════════════╗                ╔══════════════════════════╗
          ║  LIFECYCLE FLOW    ║                ║  PROCEDURE FLOW          ║
          ║  = TABLE in the    ║◄─ same object ─║  = 22-seq-<feature>.md   ║
          ║  dir's _states.md  ║   two grains   ║  (obligations, in order) ║
          ╚════════════════════╝                ╚══════════════════════════╝

════════════════════════════════════════════════════════════════════════════════════════════
     WHERE THE TABLES LIVE — one board per identity per DESIGN.md; cd = the next AUTO-INJECTS
════════════════════════════════════════════════════════════════════════════════════════════

 <monorepo>/.claude/rules/states.md          ◄── injects every session
 │  ## THE PROJECTS   IDEA → DESIGN → WIP → MVP → VERSIONED
 │  │                  └─ itself a SLICE: 1 represent · 3 open · 4 refine · 6 closes · 12 ⌜X⌝
 │  ## THE SWEEP      designs ⇄ boards bijection debt, counted
 │  ## THE TEMPLATE   ⛔ do not invent → Q1..Q4 → THIS RULE
 │
 ├─ cd <project>/                            ◄── <project>_states.md injects
 │  │   ## <ITS FLOWS>  each a slice, in ITS nouns (a book: OUTLINED→…→STAMPED ·
 │  │                    an archive: SECTIONIZED→…→FACTORED · + THE STAMPS: RAISED→DECIDED→LANDED)
 │  └─ cd <part>/                            ◄── <part>_states.md injects … (fractal)
 │
 └─ GATE: the state-file skill's check_state_files.py (ships here) · ## owns a table · cell ≤300
      never paragraph · the gate never generates, it only refuses

════════════════════════════════════════════════════════════════════════════════════════════
   THE FIXPOINT: boards REPRESENTED (1) → flows OPENED from the sequence (3) → the checker
   GATED them (7) → the template REIFIED (10) → this rule LABELED it (12) → and the label
   re-enters as step 1 of every future board (13 → 1).   ⊢ D∞
════════════════════════════════════════════════════════════════════════════════════════════
```
