#!/usr/bin/env python3
"""example persona prompt-engineering systems — generate different personas from small specs, each with a
complex cognition-chain DSL block. NO API; deterministic."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "prompt_engineering"))
from persona import make_persona, make_persona_file  # noqa: E402


def main():
    # generate three DIFFERENT personas from specs, easily
    debugger = make_persona_file(HERE / "examples" / "persona_debugger.json")
    assert "# Persona: Ada the Debugger" in debugger
    assert "[Symptom] ⇒ [Repro] ⇒ [Hypothesis] ⇒ [Bisect] ⇒ |RootCause|" in debugger  # the CoR DSL block
    assert "## Inner attention chain" in debugger        # the CoR nests an attention chain
    assert "## Rules" in debugger and "## Output format" in debugger
    print("  debugger    persona w/ a CoR reasoning DSL generated from a spec ✓")

    socratic = make_persona_file(HERE / "examples" / "persona_socratic.json")
    assert "Sage the Socratic Tutor" in socratic and "[Probe] ⇒ [Surface-assumption]" in socratic
    print("  socratic    a different persona, different DSL, one call ✓")

    reviewer = make_persona_file(HERE / "examples" / "persona_code_reviewer.json")
    assert "Lint the Code Reviewer" in reviewer and "|Verdict|" in reviewer
    print("  reviewer    a third persona w/ its own reasoning chain ✓")

    # deterministic + easy: same spec → same persona; an inline spec works too
    spec = {"name": "Quill", "role": "a tech writer", "voice": "crisp",
            "reasoning": {"foci": ["Audience", "Claim", "Evidence"], "held": "Draft", "decision": "the clearest sentence"},
            "rules": ["Active voice."], "output": "One paragraph."}
    assert make_persona(spec) == make_persona(spec)
    assert "Quill" in make_persona(spec) and "[Audience] ⇒ [Claim] ⇒ [Evidence] ⇒ |Draft|" in make_persona(spec)
    print("  inline      make_persona(spec) is deterministic + one-call ✓")

    print("PERSONA-SYSTEMS PASS — generate different personas (with complex DSL blocks) from small specs")


if __name__ == "__main__":
    main()
