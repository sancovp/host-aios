"""
meta_ape.py — meta-APE (META-APE spec §4.4): each build-function of the compiler becomes a real SKILL.

The self-compilation move: the functions APE is built with (compose a prompt, make a persona, roll up the
big/persona generator) are emitted as coordinate-addressed `SKILL.md` packages — the skills the
chaincompiler PLUGIN ships (§6). Each skill is written with APE's OWN `write_skill` (skillpack) and is made
of the same blocks/generators it describes, so meta-APE is APE re-expressed through itself.

  emit_meta_ape(out_dir)                          → write the APE build-function skills (coordinate-addressed)
  emit_meta_ape(out_dir, caps=APE_CAPABILITIES + EXTRA)  → extend the catalog (e.g. with the *CC capabilities)

The catalog is data: a `Capability` is (skill name, description, SKILL.md body). The chaincompiler plugin
appends the *CC forge/package capabilities to APE_CAPABILITIES (they live above APE), then emits the lot.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

try:
    from .skillpack import write_skill, cohere_skills
except ImportError:  # standalone
    from skillpack import write_skill, cohere_skills


@dataclass
class Capability:
    """One compiler build-function, ready to become a SKILL.md (name + description + body)."""
    name: str
    description: str
    body: str


# ── the APE build-function catalog (each becomes a real skill) ──────────────────────────────────────
APE_CAPABILITIES: List[Capability] = [
    Capability(
        "make-prompt",
        "Compose a prompt as a MetaStack of RenderablePiece blocks (deterministic data → prompt).",
        "Build a prompt from blocks — the foundation move (every prompt IS a MetaStack of RenderablePieces).\n\n"
        "```python\n"
        "from prompt_engineering import Role, BulletList, render_prompt\n"
        "render_prompt(\n"
        "    Role(role='a senior code reviewer', mission='find correctness bugs'),\n"
        "    BulletList(title='Rules', items=['Cite file:line.', 'Never invent an API.']),\n"
        ")\n"
        "```\n\n"
        "Blocks: Text, Heading, Section, Role, BulletList, KeyValue, Fenced, Template, Group. Declarative "
        "form: `{\"type\": \"Role\", \"role\": \"...\"}` via `block_from_dict`. Same blocks → same prompt.",
    ),
    Capability(
        "make-persona",
        "Generate a full persona prompt from a small spec (block types + a chain-of-reasoning DSL block).",
        "One call → a complete persona prompt, deterministically.\n\n"
        "```python\n"
        "from prompt_engineering import make_persona\n"
        "make_persona({\n"
        "    'name': 'Ada', 'role': 'a senior debugger',\n"
        "    'reasoning': {'foci': ['Symptom','Repro','Bisect'], 'held': 'RootCause', 'decision': 'the minimal fix'},\n"
        "    'rules': ['Reproduce before theorizing.'], 'output': 'A markdown report.',\n"
        "})\n"
        "```\n\n"
        "`reasoning` becomes a ChainOfReasoning block that NESTS an attention chain.",
    ),
    Capability(
        "big-generator",
        "Roll the per-chain-type generators (AC/CoR/SC) into ONE callable that renders a chain sequence.",
        "Give a template-sequence of chains (`(kind, spec)`, kind ∈ {ac, cor, sc}); get ONE callable that "
        "renders them into one prompt (a MetaStack of the chain blocks).\n\n"
        "```python\n"
        "from prompt_engineering import big_generator\n"
        "gen = big_generator([\n"
        "    ('ac',  {'foci': ['Symptom','Repro'], 'held': 'Localize'}),\n"
        "    ('cor', {'name': 'Debugger', 'foci': ['Symptom','Repro'], 'held': 'RootCause', 'decision': 'the fix'}),\n"
        "])\n"
        "gen()   # → the composed prompt\n"
        "```",
    ),
    Capability(
        "persona-generator",
        "A named persona from a ROLE-intro block + a chain sequence; XML by default, or markdown mode.",
        "Subclass of the big generator: a system-prompt name + a ROLE-intro block wrapping the chains.\n\n"
        "```python\n"
        "from prompt_engineering import persona_generator\n"
        "gen = persona_generator('Ada the Debugger',\n"
        "    [('ac', {'foci': ['Symptom','Repro'], 'held': 'Localize'})],\n"
        "    role='a senior debugger',\n"
        "    fields={'mission': 'find the root cause', 'law': 'reproduce before theorizing'},\n"
        "    mode='xml')        # default: <role name=…><mission>…</mission> … </role>\n"
        "gen()\n"
        "```\n\n"
        "`mode='markdown'` → a `# {name}` heading + a `You are …` role line, then the chains.",
    ),
]


def emit_meta_ape(out_dir: str | Path, caps: Optional[List[Capability]] = None, *,
                  coordinate: bool = True) -> dict:
    """Emit one SKILL.md per build-function (meta-APE). With `coordinate=True` the skills are placed as
    coordinate-addressed skilltree nodes and cohered once. Returns {skills:[paths], cohere: report|None}.

    Pass `caps` to extend the catalog (e.g. `APE_CAPABILITIES + CC_CAPABILITIES` from the chaincompiler
    plugin, so the meta-APE skill set spans APE + the *CC).
    """
    catalog = APE_CAPABILITIES if caps is None else caps
    paths = [write_skill(c.name, c.description, c.body, out_dir=out_dir, coordinate=coordinate)
             for c in catalog]
    report = cohere_skills(out_dir) if coordinate else None
    return {"skills": [str(p) for p in paths], "cohere": report}


__all__ = ["Capability", "APE_CAPABILITIES", "emit_meta_ape"]
