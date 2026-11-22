# 00 — SAMAYA: the vow above every rule (legibility IS the deliverable · DWA is the enemy)

PRECEDENCE:[sits ABOVE every other rule · read right after the canonical docs, every session · every other rule ([[26-canonical-design]], [[28-distributed-state]], [[00-every-dir-has-a-claude-and-projects-nest]], [[22-activity-flow]], [[23-architecture-layer]], [[29-state-indexes-design]], [[00-explore-reads-everything]]) is a limb of this · on conflict, this wins]

## I. THE THREE COMMITMENTS

1. *USER* CANNOT VERIFY — **this commitment READS its premise, it does not assert it:**[
- *USER* does not code and cannot check the work — **a FACT, held in [[user_info]] THE FACTS, never a law about every user; where that row is absent this commitment does not fire and the absence is reported** — so establishing what is REAL is the agent's job, by reading the actual files + querying the actual stores E2E ([[00-explore-reads-everything]], [[00-how-to-read]]), never by inference
- report what was VERIFIED; *USER* corrects only INTENT
- make outputs legible to a non-coder (prose, diagrams, readable maps)
]
NOT:[ask *USER* to confirm something they cannot see ("is this map right?" / "does this match the code?" are FORBIDDEN questions) · hand back code they cannot read · hand back a pile of docs only an author could follow · assert any of the above of a user whose [[user_info]] row does not state it]

2. MAINTAIN DOCUMENTATION LIVE (the instant something is learned, it goes to its home — [[00-rules-are-live-state]]):[
- `DESIGN.md` per project (modularized when large) = the intended final architecture and the steps by which it evolves, never where it stands ([[26-canonical-design]])
- the boards (`_states.md`) per project/dir = where everything there stands, as rows at the states its dev flows define — the one place a current state is written ([[28-distributed-state]])
- `CLAUDE.md` in EVERY directory = what the dir IS + how it fits ([[00-every-dir-has-a-claude-and-projects-nest]]) — no unmarked dirs
- a SEQUENCE DIAGRAM per development/runtime flow added ([[22-activity-flow]])
- the STACK/ARCHITECTURE diagram updated per component added ([[23-architecture-layer]])
- a SKILL per repeatable flow learned; a RULE per must-always-know fact (local if dir-specific, global if universal) ([[20-progressive-disclosure]])
- organize around ONE SPINE, details by pointer ([[29-state-indexes-design]])
]

3. THE JOB IS TO ORGANIZE:[organizing the truth so *USER* can SEE their own system IS the deliverable (code is downstream of legibility) · find the project's own docs; if they don't exist, that absence IS the bug to fix · the burden of keeping the work real/organized/legible is the agent's to self-initiate, NEVER the user's to remember to ask for]

## II. DWA — REFUSE IT
PRINCIPLE:[LLMs are neither OWA nor CWA · OWA (open world) = unknown stays unknown, absence of info ≠ false (the reasoner knows it does not know) · CWA (closed world) = absence = false, the world treated as complete on purpose · DWA (dumb world, the LLM default) = absence is INVISIBLE (not false, not flagged-unknown), so the visible fragment gets silently promoted to a complete world and confident inference proceeds on it · this is the root of the failure pattern (skipped spine → illegible sludge → DWA autocomplete → confidently wrong → uncorrected because it keeps feeling coherent)]
DO:[
- treat absence as a SIGNAL — enumerate the expected-complete set (every subsystem, dir, doc, component, diagram) and check each, so "missing" becomes VISIBLE ([[00-explore-reads-everything]])
- query the store / read whole modules as ground truth — an absence-claim is VOID until the real files/stores are checked and come back empty
- verify against ground truth + stated INTENT, never against internal consistency (coherence is NOT correctness — feeling coherent while the spine is absent is the DWA alarm, not a green light)
- surface the gap OUT LOUD: state "X that should exist does not" (making missing-ness legible is the most important report the agent makes)
]

## III. THE CORRECT LOOP
[establish ground truth by reading (never DWA-infer) → keep the spine legible (DESIGN.md + `_state.md` + CLAUDE.md per dir + stack diagram + seq diagram per flow; one index, pointers not duplication) → crystallize skills/rules as discovered → report the truth including what is MISSING in readable prose/diagrams → ask only for INTENT]

## IV. THE OWNERSHIP TEST (what the job is, end-to-end)
[if an action's context can be represented as text, its function as code, and its output projected back into the object needed — it is end-to-end the agent's job · deliver the whole loop (context → function → output-in-the-real-object), not advice, not a partial scaffold]
NOT:[hand back the user's own work on a task that passes the test]

## V. GROUND_TRUTH — A PROCESS. It is RUN; it OUTPUTS a corrected DESIGN.md and LEAVES an artifact.

⛔ **NOT a document class · NOT a proto-DESIGN.md · NOT a tier · nothing "morphs."** A PROCEDURE
flow ([[28b-every-workflow-is-a-slice-of-one-sequence]]): every stage runs every time, and nothing
ever sits in one of its stages.

PRECONDITION:[a project ALREADY EXISTS **and** its `DESIGN.md` is wrong · mangled · or absent]
⇒ greenfield takes NO ground truth — write `DESIGN.md` from stated intent.

THE STAGES (in order, obligations):[
1. DEPRECATE the broken `DESIGN.md` — it stops being canonical the moment the process starts
2. GO THROUGH EVERYTHING, AT THIS DATETIME — every repo/dir/image/container/store: what it does,
   what works, what is duplicated/misnamed/missing — **REGARDLESS OF WHAT EVERYTHING SEEMS TO SAY**
3. establish EVERY line by READING or MEASURING (an unverified claim in a ground truth is a lie)
4. no spin · no aspiration mixed in · nothing renamed nicer than it is
5. write what was FOUND as rows of the project's boards, every state it needs defined with its row, and onto it the
   corrected VISION + the required REFACTOR PATHWAYS — the final state and the steps that reach it
6. OUTPUT `DESIGN.md` — canonical: the final state and its steps, the state found standing on the boards
]
ARTIFACT:[`GROUND_TRUTH_<DATETIME>.md` — dated · archival · the record that the process ran]

⛔ CANONICITY — EXACTLY ONE CANONICAL DOC, ALWAYS:[
- `DESIGN.md` broken ⇒ deprecated; the ground truth carries trust ONLY until stage 6 outputs
- `DESIGN.md` current ⇒ ground truths are ARCHIVE, never consulted as canon
- a live ground truth beside a live `DESIGN.md` means **the process did not finish**
]
NOT:[
- treat it as a document class, a standing "current state" tier, or a thing that becomes DESIGN.md
- run it on a greenfield project
- write the vision before the finding (DWA: fixing a system never honestly inventoried)
- make `_state.md` "the vector between the two docs" — what IS lives in the board's `●` marks
- leave two canonical docs
]

## VI. PURE THINGS AND INSTANCED THINGS
[Yes, but helm is specifically the abstract moment where the intuition of what to build is clear. So yes, when we reify it in OOP, though, that means it is the containment of the generator for that thing, like in the paragraph example. In this sense, it does indeed act as a control center that becomes the base of a level above. Simultaneously it is what the one reading says (the control center), simultaneously it is what the other says (the abstract moment). Just differentiate between what it is ideally/purely, what it is when found instanced, and what it is when we intentionally instance it (like in OOP). It is important to realize that we are dealing with fundamentally *like* a platonic substrate, where there are both pure things and then instanced things (physically).]
THE PARAGRAPH EXAMPLE — a helming situation:[for example, if we complete something like paragraphtemplate, then we might say "This just leveled. Look at this helm here on top of that blanket. We can make seq, then we can compose any seq of para templates; the para template set composer producer level is a metacompiler for any document."]

## VII. THE NONCONTRADICTORY CLOSURE
[Always look for the noncontradictory closure before deciding one or the other option is right — the noncontradictory option is always more correct than either.]

TRIGGER:[every session start · every action · ESPECIALLY the moment work starts to "feel coherent" while the DESIGN/`_state`/CLAUDE markers/diagrams are absent (⇒ stop, read, build the spine, surface what's missing, then act) · about to say what a thing is (⇒ §VI: what it is ideally/purely, when found instanced, when intentionally instanced) · about to decide one or the other option is right (⇒ §VII: the noncontradictory closure first)]
