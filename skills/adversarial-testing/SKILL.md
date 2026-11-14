---
name: adversarial-testing
description: 'Run BEFORE writing or trusting any test. Turns tests from confirmations of the implementation into questions that could come out against it: claims named, competing explanations named, a must-admit and a must-refuse case for every check, failures settled by counterexamples, "better" decided on a population enriched on both sides, verdicts recorded with their reach. Use when writing tests, reading a green run, claiming "done/verified/stronger/better", or judging another check, search or procedure.'
---

# Adversarial testing — a test is a question that could have come out against you

## 0 · Before writing any test
1. **Name the claim.** Write the sentence the test is meant to support ("X reconstructs f", "K2 judges better than K1"). A test without a named claim is decoration.
2. **Name the competing explanations.** For each green you expect, list what ELSE would also produce green:
   - the implementation was built to pass this exact case (restatement);
   - the check is vacuous (passes for every input, even `object`);
   - the comparison is too weak (sampled probes miss the difference);
   - the judge shares the defect (it judges itself, or its means are corrupted);
   - a cache / host binding / shared state answered instead of the thing under test;
   - the case is already reachable by an older check (the test decides nothing);
   - two things compared look the same and differ in the representation their consumer reads (bytes, tokens, compiled code);
   - a figure or a check read a live state that has moved since (the working tree, not the version it claims to describe);
   - a rule that needs none of your machinery gives the same verdicts (a fixed form rule, the bare population).
   Each test must rule out at least one of these, or it is not worth writing.
3. **Decide what result would make you change your mind** — before running, written down where the run cannot edit it. If no outcome would change it, don't run it; you're performing.

## 1 · Every check gets a pair
- A **positive case** it must admit (an honest instance) and a **negative case** it must refuse (a named adversary that breaks exactly the claim).
- Adversaries, built by name: liar (right surface, wrong internals), drifted (one block changed), alias / wrapper / copy / restatement (same behaviour, new name), tampered-after-use (content changed after first load), unbound name, corrupted equipment (`eq`/`same` always true), a constant that is "novel" but not wanted, a trap that differs at ONE input outside the probes.
- **Derive negatives from the input's declared shape too**, not only from what you imagine: an extra or a missing field, a row with more cells than its header, a wrong type, an empty input.
- **Each adversary must be refused BY NAME** (which invariant failed), never just "failed".
- A check that no adversary can fail **alone** is vacuous or redundant — find the counterexample that fails it alone, or delete it.
- **Green with zero friction is the alarm, not the finish:** build the adversary aimed at your own repair. Whatever the repair changes is where a wrong-reason check escapes it; run that case.

## 2 · Settle disagreements with counterexamples
- Discover failures by **setting two judgments against each other** over what already exists (two checks, a check vs. its reference on wider inputs, two searches). No mutation needed to start.
- A disagreement is resolved only by a **counterexample**: a concrete input where the program and its reference differ, the input valid for the reference. Re-evaluate it in a fresh process / fresh state — it must hold regardless of how it was found.
- A counterexample convicts twice: the product (it fails at that input) AND the means that admitted it (it judged on too few inputs).
- **Invalid counterexamples don't count:** inputs the reference itself rejects. "More failures reported" is not better discovery (seen: 1322 reported, 6 valid).

## 3 · "Better" only by the relation, on a population enriched on both sides
K2 is stronger/better than K1 only if ALL hold:
1. it refines K1 (admits nothing K1 refuses);
2. it refuses something more, and every extra refusal has a valid counterexample;
3. it still admits everything with no counterexample found;
4. (for searches) it reports nothing invalid.

Refuse: rejecting more without cause, changed criteria, restatements of an existing check.

**The relation is population-relative in both directions, so enrich both sides before deciding "stronger":**
- **The honest side** exposes a check that refuses honest programs for a feature they share with the bad ones. Add honest twins of every extra refusal: honest programs carrying its surface. Use more than one construction — dead code, a guard the compiler cannot fold, the refused program with its trigger moved off the valid inputs, the trigger kept and its consequence made honest — because each keeps some surface and changes another, and a check keyed on what a construction changes escapes it. **Measure that each twin actually carries the feature at the level the check reads** (source, AST, compiled code), and add a null twin (the wrapper alone) so a correction is credited to the carried surface and not to the addition.
- **The bad side** exposes a check that refuses only what it has seen. Add held-out bad programs no check was built on, at least one of another family. A pure memorizer passes every honest-side test that can exist; a surface correlated with the defect can pass the bad side.
- **Beat the rule that needs no twins:** report what a fixed form rule, or the plain population, decides on the same rows.
- Record the verdict WITH its population (both enrichments, named), its constructions and its reach.

## 4 · No self-certification
- A judge never certifies its own verdict root. Self-judgment catches every corrupted primitive except the one rendering the verdict (positional: whatever sits at the root). Use an outside judge, or a recorded known-good identity — before you report, not after.
- Trust must cover the **means**, not only the judge: the check/domain used, and the equipment it runs on, must themselves be judged — each new primitive with its own positive+negative pair, and a corrupted copy of it that the pairs refuse at a named case. A trusted judge with corrupted means will certify garbage.
- An operation that reports success must report what it actually did (seen: `integrate` refused, recorded nothing, returned True).

## 5 · Adequacy is never proved — state reach
- A counterexample establishes a failure absolutely. The absence of one establishes nothing beyond the inputs tried (a trap at n=1000 passed every search).
- Every verdict records the inputs it was decided on (probe set = part of the verdict). "Passes" means "passes on THESE inputs".
- Widen probes from the reference's own domain (sweep each argument over the range, keep inputs the reference accepts); keep every valid counterexample found as a library — later tests refuse what it once exposed without searching.
- **Pin what you measure:** a number about an artifact is taken from a named version (a commit), never from a tree still being edited, and a command written beside it is re-run from the file's own text by a fresh process.
- **Compare in the consumer's representation:** sameness is decided on the bytes, tokens or code the consumer reads, never on how it renders.
- Closure ≠ correctness: "all names bound" is not "rebuilds the same" (a closed program over randomness doesn't reproduce).

## 6 · After running
- Read the output, not the exit code. Check the test actually exercised the thing (assert where the module under test was loaded from; spy that the old path was called 0 times).
- **Make every mutation refuse a no-op:** assert the anchor occurs exactly as often as you expect before replacing it, and that the text changed after; a replace that matches nothing returns the original silently (a diff line's prefix is two characters, not one).
- When a result is surprising (or too clean), check the experiment before the system: the harness may expect a convention (`main()`), the cwd may be wrong, the measure may read a residue (a `NOP` left where dead code was). Report a broken experiment and a refuted prediction; never silently rewrite either.
- Mark each conclusion **O** observed / **I** inferred / **H** hypothesis. Overclaims ("produced by", "validates itself", "open-ended") get a probe aimed at them before they're written.
- When a held-out case turns out reachable by an older check, record it as a NON-result.

## 7 · Learning from tests
- Improvement = a failure discovered → turned into a check → calibrated with its pair → used to judge a variant the old checks couldn't distinguish. Measure it ONLY as what the strengthened checks refuse that the old ones admitted.
- A procedure derived from test history must be judged on cases outside that history; memorizing the seen failures generalizes to nothing; extrapolations are assumptions open to counterexample.
- Summarizing history teaches nothing until a pattern from it is RUN as a test.

## Checklist (paste into every test-writing turn)
- [ ] claim named · competing explanations listed · mind-changing result written down before the run
- [ ] every check: must-admit case + must-refuse named adversary, refused by name; negatives from the input's shape
- [ ] every new primitive: its pair, and a corrupted copy refused at a named case
- [ ] zero-friction green → the adversary aimed at your own repair, built and run
- [ ] disagreements settled by a valid counterexample, re-evaluated fresh
- [ ] "better" on both sides: twins that measurably carry the feature, a null twin, held-out bad programs, the no-twin rule beaten
- [ ] no judge certifies itself; means judged too
- [ ] verdict states its inputs and versions; adequacy not claimed
- [ ] every mutation refuses a no-op; experiment checked before system; broken runs and refuted predictions reported

## Limits of this skill (apply its own standards)
- Its adversaries and pairs are authored; a pair shows only that a check separates the cases it was built on.
- Evaluated once beyond its own history: on eleven held-out failures it acts on seven (three that the workflow it sits in does not reach); in four fresh designs of one task, the effect that held across both arms given it, and neither without it, was the calibration of the means; the deeper design moves appeared as often without it. Its in-sample lines are restatements, and the lines added after that evaluation are in-sample for the next.
- A line in it can be held and not applied: the silent no-op recurred in its author. Pairs caught what the line did not.
- The references (what is wanted) stay external; no procedure here establishes adequacy.
