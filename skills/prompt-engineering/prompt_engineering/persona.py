"""
persona.py — a full persona prompt from a small spec, composed as a MetaStack of blocks.

Compose block types (role, persona, rules, output) PLUS a cognition-chain block (a chain-of-reasoning,
which itself NESTS an attention chain) into ONE persona prompt — deterministically (same spec → same
prompt). This is the worked example of 'a prompt is a MetaStack of RenderablePieces'; the capstone
persona-GENERATOR (META-APE spec §4) is the parameterized, rolled-up version of this.

    make_persona(spec) -> prompt        # spec = {name, role, voice?, mission?, reasoning?, rules?, output?}
    make_persona_file(path) -> prompt   # spec from JSON

`reasoning` = {foci:[...], held:"...", decision:"...", cues?:...} → a CoR block (the complex part).
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Union

try:
    from .blocks import RenderablePiece, Role, BulletList, Text, Section, render_prompt
    from .cognition import ChainOfReasoning
except ImportError:  # standalone
    from blocks import RenderablePiece, Role, BulletList, Text, Section, render_prompt
    from cognition import ChainOfReasoning


def make_persona(spec: Dict[str, Any]) -> str:
    """Compose a persona prompt from a small spec — block types + a cognition DSL block."""
    pieces: List[RenderablePiece] = []
    # role block — the system line (+ optional mission)
    pieces.append(Role(role=spec["role"], mission=spec.get("mission")))
    # persona block — name + voice
    voice = spec.get("voice", "")
    persona_body = f"You are {spec['name']}." + (f" Voice: {voice}." if voice else "")
    pieces.append(Section(heading="Persona", body=persona_body))
    # reasoning block — a chain-of-reasoning (nests an attention chain): the COMPLEX block
    r = spec.get("reasoning")
    if r:
        pieces.append(ChainOfReasoning(name=spec["name"], foci=r["foci"], held=r["held"],
                                       decision=r["decision"], cues=r.get("cues")))
    # rules block
    if spec.get("rules"):
        pieces.append(BulletList(title="Rules", items=spec["rules"]))
    # output-format block
    if spec.get("output"):
        pieces.append(Section(heading="Output format", body=spec["output"]))
    return render_prompt(*pieces)


def make_persona_file(path: Union[str, Path]) -> str:
    return make_persona(json.loads(Path(path).read_text()))


__all__ = ["make_persona", "make_persona_file"]
