#!/usr/bin/env python3
"""cognition-chain stack (ACCC/CORCC/SCCC) rebuilt on the prompt engine. NO API, no DB, no induction.
Proves: AC/CoR/SC render on the primitive; CoR NESTS the AC (block-nesting); the validator is derived
from the template (catches broken/off-vocab chains deterministically)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "prompt_engineering"))
from cognition import (  # noqa: E402
    chain_notation, parse_chain, validate_chain, cor_skeleton,
    render_attention_chain, render_cor, render_skillchain,
)


def main():
    # AC — an attention chain renders as a prompt block (was ACCC, minus the induction tower)
    ac = render_attention_chain(["Symptom", "Repro", "Hypothesis"], "Localize")
    assert "ATTENTION CHAIN" in ac and "[Symptom] ⇒ [Repro] ⇒ [Hypothesis] ⇒ |Localize|" in ac
    print("  AC        attention chain renders on the primitive ✓")

    # CoR — a persona that NESTS the AC (CORCC-embeds-ACCC = block-nesting, not grammar-embedding)
    cor = render_cor("Debugger", ["Symptom", "Repro", "Hypothesis"], "Localize", "the single root cause")
    assert "# Persona: Debugger" in cor
    assert "## Chain of reasoning" in cor and "the single root cause" in cor
    assert "## Inner attention chain" in cor and "[Symptom] ⇒ [Repro]" in cor  # the AC is nested inside
    print("  CoR       chain-of-reasoning persona NESTS the attention chain ✓")

    # §5 cue-aware CoR — cor_skeleton renders the fill-in skeleton; render_cor(cues=...) embeds it + a
    # must-say directive (the CORCC feature, now a base primitive; corcc renders THROUGH cor_skeleton).
    skel = cor_skeleton(["Symptom", "Repro", "RootCause"], {"Symptom": "what broke", "RootCause": "the cause"})
    assert skel == "[Symptom: …what broke…] → [Repro: …Repro…] → [RootCause: …the cause…]"
    cued = render_cor("Debugger", ["Symptom", "Repro"], "RootCause", "the fix",
                      cues={"Symptom": "what broke", "Repro": "how to trigger", "RootCause": "the cause"})
    assert "## Say it like this" in cued and "[Symptom: …what broke…]" in cued and "surface each move's cue" in cued
    assert "Say it like this" not in render_cor("Debugger", ["Symptom", "Repro"], "RootCause", "the fix")
    print("  cues      cue-aware CoR skeleton + directive (§5; corcc renders through cor_skeleton) ✓")

    # SC — a skill chain composes resolved steps toward a goal (was SCCC)
    sc = render_skillchain([("ac", "debug-focus"), ("cor", "Debugger"), ("skill", "write-patch")], "ShippedFix")
    assert "[ac:debug-focus]" in sc and "[cor:Debugger]" in sc and "|ShippedFix|" in sc
    print("  SC        skill chain composes ac/cor/skill steps → goal ✓")

    # THE VALIDATOR — derived from the template (no DB, no learned grammar). The rule-learner's intent.
    ok, errs = validate_chain("[Symptom] ⇒ [Repro] ⇒ |Localize|", vocab=["Symptom", "Repro", "Localize"])
    assert ok and not errs
    # broken: missing held terminal
    ok, errs = validate_chain("[Symptom] ⇒ [Repro]")
    assert not ok and any("terminal" in e for e in errs)
    # broken: off-vocabulary focus (authored vocab, not learned) → caught (the "orthogonal" verdict, clean)
    ok, errs = validate_chain("[Goal] ⇒ [Repro] ⇒ |Localize|", vocab=["Symptom", "Repro", "Localize"])
    assert not ok and any("not in authored vocabulary" in e for e in errs)
    print("  validate  template-derived broken-detector (missing held / off-vocab) ✓")

    # notation round-trips
    foci, held = parse_chain(chain_notation(["A", "B"], "C"))
    assert foci == ["A", "B"] and held == "C"
    print("  notation  chain_notation / parse_chain round-trip ✓")

    print("COGNITION-STACK PASS — AC/CoR/SC on the primitive · CoR nests AC · validator from the template")


if __name__ == "__main__":
    main()
