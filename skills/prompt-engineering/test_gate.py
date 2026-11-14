#!/usr/bin/env python3
"""the REAL gate, on vendored rulecatcher — learn the grammar from exemplars (no hand-written errors),
lint a candidate → violations + fixes + the steerable/fatal verdict. NO API."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "prompt_engineering"))
from gate import gate  # noqa: E402

# exemplar debug attention-chains — the grammar is LEARNED from these (not hand-written)
EXEMPLARS = [
    "[Symptom] ⇒ [Repro] ⇒ |Localize|",
    "[Symptom] ⇒ [Hypothesis] ⇒ |Localize|",
    "[Symptom] ⇒ [Bisect] ⇒ |RootCause|",
]


def main():
    # it actually used the vendored engine (not the shallow fallback) and learned rules
    clean = gate("[Symptom] ⇒ [Repro] ⇒ |Localize|", EXEMPLARS)
    assert clean["engine"] == "rulecatcher", clean
    assert clean["rules"] > 0, "should have LEARNED a grammar from the exemplars"
    assert clean["ok"] and clean["verdict"] == "clean", clean
    print(f"  learn+gate  grammar learned from exemplars ({clean['rules']} rules); valid chain → clean ✓")

    # an off-vocabulary opener: [Goal] is a valid identifier (right KIND) but the wrong TOKEN at that slot
    # → ORTHOGONAL = steerable (the gate genus the hand-rolled validator can't produce)
    off = gate("[Goal] ⇒ [Repro] ⇒ |Localize|", EXEMPLARS)
    assert off["engine"] == "rulecatcher" and not off["ok"], off
    assert off["verdict"] in ("orthogonal", "syntax_break"), off
    assert off["violations"], off
    v = off["violations"][0]
    print(f"  verdict     off-vocab opener → {off['verdict']} (found '{v['found']}', candidates {v['candidates']}) ✓")

    # the fix is supplied by the engine (candidate tokens / action) — not hand-written
    assert any(vi["candidates"] or vi["action"] for vi in off["violations"]), off
    print("  fixes       engine supplies candidate tokens / suggested action ✓")

    print("GATE PASS — rulecatcher vendored: learn-from-exemplars + violations + fixes + steerable/fatal verdict")


if __name__ == "__main__":
    main()
