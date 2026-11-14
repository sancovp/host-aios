#!/usr/bin/env python3
"""capstone (META-APE spec §4): BigGenerator rolls the per-chain-type generators into ONE callable;
PersonaGenerator wraps a named ROLE-intro block (XML default + markdown mode) around the chains; meta-APE
emits each build-function as a real coordinate-addressed SKILL. Every prompt is a MetaStack of blocks."""
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "prompt_engineering"))
from pydantic_stack_core import MetaStack  # noqa: E402
from prompt_engineering import (  # noqa: E402
    big_generator, persona_generator, emit_meta_ape, APE_CAPABILITIES,
)

SEQ = [
    ("ac",  {"foci": ["Symptom", "Repro", "Hypothesis"], "held": "Localize"}),
    ("cor", {"name": "Debugger", "foci": ["Symptom", "Repro"], "held": "RootCause", "decision": "the minimal fix"}),
    ("sc",  {"steps": [("ac", "debug-focus"), ("cor", "Debugger")], "goal": "ShippedFix"}),
]
FIELDS = {"mission": "find the single root cause and the minimal fix", "law": "reproduce before theorizing"}


def main():
    # §4.1 — BigGenerator: roll AC+CoR+SC into ONE callable that renders a MetaStack
    gen = big_generator(SEQ)
    out = gen()
    assert callable(gen) and isinstance(gen.metastack(), MetaStack)
    for marker in ("ATTENTION CHAIN", "# Persona: Debugger", "SKILL CHAIN", "|ShippedFix|"):
        assert marker in out, marker
    print("  big-gen     §4.1 roll AC+CoR+SC into one callable → MetaStack of chain blocks ✓")

    # §4.2 — PersonaGenerator, XML mode (DEFAULT): <role name=…> wraps the chains, with fields
    px = persona_generator("Ada the Debugger", SEQ, role="a senior debugger", fields=FIELDS)
    xml = px()
    assert xml.startswith('<role name="Ada the Debugger">') and xml.rstrip().endswith("</role>")
    assert "<mission>find the single root cause and the minimal fix</mission>" in xml
    assert "<law>reproduce before theorizing</law>" in xml
    assert "ATTENTION CHAIN" in xml and "SKILL CHAIN" in xml   # chains nested INSIDE the role element
    assert isinstance(px.metastack(), MetaStack)
    print("  persona-xml §4.2 XML ROLE-intro block (default) wraps the chains ✓")

    # §4.2 — PersonaGenerator, markdown mode: # heading + 'You are …' line, then the chains
    pm = persona_generator("Ada the Debugger", SEQ, role="a senior debugger", fields=FIELDS, mode="markdown")
    md = pm()
    assert md.startswith("# Ada the Debugger")
    assert "You are a senior debugger. Your mission is to find the single root cause" in md
    assert "- **law**: reproduce before theorizing" in md and "<role" not in md
    print("  persona-md  §4.2 markdown mode (# heading + role line + chains) ✓")

    # §4.4 — meta-APE: each build function becomes a real coordinate-addressed SKILL
    import skilltree
    with tempfile.TemporaryDirectory() as t:
        rep = emit_meta_ape(t)
        assert len(rep["skills"]) == len(APE_CAPABILITIES) == 4
        assert rep["cohere"] and rep["cohere"].get("ok"), rep["cohere"]
        assert (Path(t) / "skilltree.json").exists(), "cohere must write skilltree.json"
        names = set()

        def walk(n):
            names.add(skilltree.skill_name(n))
            for c in n.children:
                walk(c)
        walk(skilltree.discover(t).root)
        for cap in APE_CAPABILITIES:
            assert any(cap.name in nm for nm in names), f"{cap.name} not placed: {names}"
    print("  meta-APE    §4.4 4 build-functions → coordinate-addressed SKILL.md (skilltree cohered) ✓")

    print("CAPSTONE PASS — big generator · persona generator (XML default + markdown) · meta-APE skills")


if __name__ == "__main__":
    main()
