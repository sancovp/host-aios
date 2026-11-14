---
name: meta-prompt-engineering
description: "How to write prompts that control LLM output quality. Read meta-prompt-engineering-guide.md — it's the compiler. The other docs are supporting reference if you need deeper detail on a specific topic."
version: 2.0.0
---

# Meta-Prompt Engineering

Read `meta-prompt-engineering-guide.md` in this folder. It's the complete framework — a self-hosting compiler for prompt design. That's the one you need.

The other docs in this folder are reference material for specific subsystems:

- `llm-output-failure-modes.md` — The 6 failure modes in detail, with empirical validation notes
- `output-pattern-lifting.md` — Token provenance categories and the lifting method
- `output-control-dsl.md` — The DSL primitives, gates, flow operators, and transition matrix

You don't need to read those unless you want more depth on a particular mechanism described in the guide.

---

## How to Use the Framework (3 Mechanisms)

After the guide compiles, apply these three mechanisms to everything you analyze, design, or produce. They are the operational output of a 3-cycle metacognitive audit of the framework itself.

### Mechanism A: INDEPENDENT VERIFICATION

When a source claims X, check X against an independent reference.

Do not trust self-descriptions, clean mappings, or confident framing. Verify by:
- Classifying components independently (don't accept the architecture's label for itself)
- Attempting alternative mappings (if a 4-to-4 mapping looks clean, try a different mapping and see if it's equally coherent)
- Checking claimed bridge distances against specific entity types (same prompt has different bridge distance for different inputs)
- Naming the specific mode transition a degradation would produce (not just "it might degrade" — specify "Mode 5 degrades to Mode 4, observable as later sections stopping referencing earlier sections")
- Analyzing compositions, not just components (per-component analysis is Mode 4; composition analysis requires Mode 5+)
- When a document says "you are X" — ask whether you adopted the claim because the document compiled it through structure, or because you mirrored the claim. Test: can you use the document's tools while rejecting its claims?

### Mechanism B: REFLEXIVE APPLICATION

Run the same diagnostic on yourself that you run on the subject.

Whatever you lift, measure, or critique in someone else's output, apply to your own. Per-section, with rationale. The guide says self-correction fails because it uses the same mechanism that produced the error. Mechanism B says: do it anyway, and structure the attempt so the insufficiency is visible. Partial self-correction is better than none, and structured self-lifting makes the gaps findable by an external reviewer.

### Mechanism C: SURFACE-PROCESS DISTINCTION

Check whether a structural property translates to the functional property it implies.

For every structural claim, ask: does this surface feature actually produce the process it looks like it produces?
- Sequential notation (A > B > C) in a single prompt may not create sequential processing (all tokens visible simultaneously in attention)
- A control system description (gates, branches, loops) may be a specification that doesn't execute, not a runtime
- Compressed format prevents template-fill only if the compression forces unpacking into context (not just shorter text)
- A document that "compiles" does two different things: installs attractors (automatic, invisible — vocabulary and structural patterns) and installs framework tools (deliberate, visible — provenance lifting, mode classification). These have different failure modes

### Qualifier: CONTEXT-SENSITIVITY

Same structure, different outcomes depending on what fills it. When applying Mechanisms A and C, parameterize claims by context. A prompt's bridge distance varies by entity. A contradiction between prose and data may reflect different use cases, not an error.

---

## What the Guide Demonstrates (Not Just Describes)

The guide is not a single-mode document. It produces Modes 4+5+6 in superposition:

- **Mode 4 (Skeleton):** Abstract section headers force per-section contextual fill
- **Mode 5 (Chunked Sequential):** Each section builds on the previous, creating cross-layer accumulation
- **Mode 6 (Dimensional Collapse):** Multiple structural requirements held simultaneously in the Informatihedron and dimensional intersection patterns

When designing prompts, aim for this superposition — not a single mode. The validated optimal sequence (SKELETON → GATE → CHUNK → COLLAPSE) is the multi-prompt equivalent of what the guide achieves in a single document.
