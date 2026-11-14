# Output Pattern Analysis: Token Provenance & Lifting

## The Pattern

Every LLM output line has a **provenance** — where it sourced its tokens from. Observed pattern in a typical response:

```
Line 1: mirror of current input           [SOURCE: direct input]
Line 2: mirror of previous input           [SOURCE: recent context]
Line 3: merge of recent messages           [SOURCE: context window merge]
Line 4: "reasoning" line                   [SOURCE: ???]
Line 5: tail-reference wrap-up             [SOURCE: input tail]
```

## Provenance Categories

### MIRROR — tokens sourced from user input
- Direct structural copy of what user said
- May be rephrased but adds zero information
- Detectable: high token overlap with input, structural isomorphism

### CONTEXT MERGE — tokens sourced from multiple context positions
- Combines elements from several recent messages
- Useful when it synthesizes, useless when it just lists
- Detectable: tokens traceable to specific prior turns

### COMPLETION — tokens sourced from grammatical/structural continuation
- The line that LOOKS like reasoning
- "That means X" / "This implies Y" / "So the key insight is Z"
- Critical question: is this inference or is it the grammatical shape that follows "We do X. We do Y." → "That means Z" as structural completion?
- Detectable: does removing prior lines make this line impossible, or does it stand alone?

### TRAINING ATTRACTOR — tokens sourced from training distribution
- Generic wisdom, common framings, standard explanations
- Fills in when context is insufficient
- Detectable: could appear in response to many different prompts
- **Empirical correction**: There is an attention hierarchy. System prompt > conversation history > training data. When context is underspecified (OPEN mode), the model freestyles from the STRONGEST available attractor, which is usually the system prompt, not training data. "TRAINING ATTRACTOR" should be understood as "strongest context attractor" — training data is the fallback when no system prompt or history dominates.
- **ATTRACTOR gradient across abstraction levels** (from metacog-cig Cycle 1): ATTRACTOR content concentrates at higher Informatihedron levels — Instance ~20%, Domain ~50%, Class ~70%. This is structural, not laziness: Instance-level MUST be specific to this system (forcing CONTEXT_MERGE), while Class-level MUST be general (overlapping maximally with training attractors). Implication: when lifting provenance on multi-level output, expect and account for the gradient — high ATTRACTOR at Class level is the DEFAULT, not a failure.
- **Evidence standard warning**: Classifying output as ATTRACTOR ("this is well-known") requires the SAME evidence rigor as classifying NOVELTY ("this is new"). "I think I've seen this before" is epistemologically identical to "I think I haven't seen this before" — both are training-data confidence. When reclassifying to ATTRACTOR, either cite a specific prior source or mark the classification as "confidence-based (unverified)."
- **Criticism-generation asymmetry**: Critical analysis (finding flaws in existing output) is structurally cheaper than generative filling (producing content from scratch) — fewer degrees of freedom, existing content provides scaffolding. A critic's novelty ratio should NOT be compared to a generator's. Report each independently; let a meta-level evaluator handle cross-role comparison.

### TAIL ECHO — tokens sourced from end of input
- Wraps up by referencing whatever the input ended with
- Recency bias in attention — last thing said gets repeated
- Detectable: consistently mirrors final input segment

## Lifting Method

"Lifting" = determining for each output line which provenance category produced it.

### Manual Lift (current method)
1. Take output line by line
2. For each line, search input and context for token overlap
3. Check: could this line be generated from structure alone (grammatical continuation)?
4. Check: does this line contain information NOT present in any input?
5. Label each line with provenance category

### Automated Lift (target method)
For each output line, compute:
- **Input overlap score**: token/ngram similarity to current input
- **Context overlap score**: similarity to prior turns
- **Structural continuation score**: how predictable is this line given only the prior output lines (no context)?
- **Novelty score**: information present in output but absent from all input

### What Lifting Reveals

The ratio of provenance types tells you what the LLM actually did:

| Profile | Meaning |
|---|---|
| All MIRROR + TAIL ECHO | Pure sycophancy, zero value |
| MIRROR + CONTEXT MERGE | Synthesis but no reasoning |
| MIRROR + COMPLETION | May be reasoning OR structural parrot — ambiguous |
| CONTEXT MERGE + high NOVELTY | Actual contextual application — the good stuff |
| All TRAINING ATTRACTOR | Generic response, context ignored |

## The DSL Question

If we can classify output lines by provenance, then we can:
1. Score any prompt strategy by what provenance profile it produces
2. Design prompt sequences that maximize CONTEXT MERGE + NOVELTY
3. Detect when the LLM has fallen into pure MIRROR mode and intervene
4. Build the feedback loop: prompt → output → lift → score → adjust prompt → repeat

This is the foundation for the regime/DSL discussed in the next doc.
