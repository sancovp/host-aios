---
name: prompt-engineering
description: The Prompt Engineering System (APE) — a deterministic prompt builder on pydantic-stack-core. A prompt is a MetaStack of RenderablePiece "blocks" (typed, self-rendering pydantic models); the same blocks render the SAME prompt every time. Compose blocks into stored "prompt templates". Use it to make system prompts, personas, rule blocks, few-shot blocks, cognition chains, or any prompt. No model call, no randomness.
when_to_use: Building or reusing prompts/personas/templates programmatically; you want the same spec to render the same prompt every time; making a new prompt template (folder of block specs).
---

# Prompt Engineering System (APE)

A skill (this `SKILL.md` + the code beside it) that turns **data → a prompt**, deterministically, on the
**`pydantic-stack-core`** foundation. The model decides *what* blocks to write; this engine guarantees
*how* they render — same inputs, same output, every time. That reliability is the point: an agent reads
this skill and uses it to make prompts/personas the same way each time.

**The foundation rule:** *every prompt is a `MetaStack` of `RenderablePiece`s.* A block is a real, typed,
self-rendering pydantic model (`RenderablePiece` subclass) — not an exec'd code string. (This supersedes
the old `{values, methods:[code-string]}` mechanism; see `META-APE-ARCHITECTURE.md` §1.)

## Vocabulary

- **block** — a `RenderablePiece`: typed fields + a pure `render()` → a chunk of prompt. Concrete blocks
  ship in `blocks.py` (`Text`, `Heading`, `Section`, `Role`, `BulletList`, `KeyValue`, `Fenced`,
  `Template`, `Group`). Declarative form: `{"type": <BlockName>, **fields}`.
- **prompt** — a `MetaStack` of blocks, built with `prompt(...)` / `render_prompt(...)`.
- **prompt template** — a stored, ordered set of block files (a folder under `templates/`) → one prompt.

There is **no baked-in structure and no "levels."** You bring your own via blocks and templates.

## Use it (the package `prompt_engineering`)

```python
# pip install -e .   (deps: pydantic-stack-core, rulecatcher, agent-skilltree)
from prompt_engineering import Role, BulletList, render_prompt, render, render_template, list_templates

# 1) compose blocks (RenderablePieces) into one prompt — a MetaStack
render_prompt(
    Role(role="a senior Python code reviewer", mission="find correctness bugs"),
    BulletList(title="Rules", items=["Cite file:line.", "Never invent an API."]),
)  # → "You are a senior Python code reviewer. Your mission is to find correctness bugs.\n\n## Rules\n- ..."

# 2) render a single block from a declarative spec (data → prompt, no exec)
render({"type": "Template",
        "template": "# {role}\n\nYou are the {role} of {domain}.",
        "values": {"role": "Worldsmith", "domain": "otters"}})   # same spec → same prompt, always

# 3) render a stored prompt template (its blocks composed in order)
list_templates()               # ['five_level', 'persona', 'simple_agent']
render_template("five_level")  # → one prompt with WORLD/EGREGORE/DEITY/PROGENITOR/AGENT sections
```

Define your own block by subclassing `RenderablePiece` and (optionally) registering it for declarative use:

```python
from prompt_engineering import RenderablePiece, register_block

@register_block
class Callout(RenderablePiece):
    emoji: str
    text: str
    def render(self) -> str:
        return f"> {self.emoji} {self.text}"
# now usable directly or as {"type": "Callout", "emoji": "⚠️", "text": "..."}
```

## Add a prompt template — DROP A FOLDER, in the project's own templates folder

```
<the project's templates folder>/
  {template_name}/
    template.json   # {name, description, blocks: ["block1.json", "block2.json", ...]}
    {block}.json    # a declarative block spec: {"type": <BlockName>, **fields}
```

Create the folder in the templates folder of the project you are working on, write `template.json`, drop in the block
specs, and pass that folder as `base`: `list_templates(base=...)` / `render_template(name, base=...)` pick it up by
convention. Nothing in the engine changes. The `templates/` beside the engine holds the templates the skill ships, read
only — never add to it: where it is loaded from a release, it cannot be written.

## Resource files (referenced by relative path)

- `prompt_engineering/blocks.py` — the **block library** (RenderablePiece subclasses on pydantic-stack-core)
  + `prompt()` / `render_prompt()` + declarative `block_from_dict()` / `register_block()` / `REGISTRY`
- `prompt_engineering/prompt_engine.py` — `render`, `render_file`, `list_templates`, `load_template`,
  `render_template`, `render_template_blocks` (single block + stored templates)
- `examples/` — single-block specs for different **block types** (system/role, persona, rules, few-shot,
  constraints, output-format) and full personas — read these to learn the declarative block format
- `templates/five_level/`, `templates/simple_agent/`, `templates/persona/` — worked prompt templates
- `prompt_engineering/cognition.py` — the cognition-chain blocks (`AttentionChain` / `ChainOfReasoning` /
  `SkillChain`, all RenderablePieces; a CoR *nests* an AC) + `validate_chain` (a no-dep broken-detector)
- `prompt_engineering/gate.py` — the REAL gate: `gate(text, exemplars)` LEARNS the grammar from exemplar
  chains → violations + fixes + the `orthogonal`/`syntax_break` (steerable/fatal) verdict
- `prompt_engineering/grammar.py` — the persistent rulecatcher seam (learn/gate/render on a `Connection`)
- `prompt_engineering/skillpack.py` — `write_skill` / `cohere_skills`: a markdown body → a publishable
  `<name>/SKILL.md` (skilltree-aware)
- **`pydantic-stack-core`** — THE foundation (RenderablePiece + MetaStack); **`rulecatcher`** — the grammar
  engine the gate runs on; **`agent-skilltree`** — coordinate-addressed skill placement
- `prompt_engineering/persona.py` — `make_persona(spec)` / `make_persona_file(path)`: a full persona prompt
  (block types + a cognition DSL block) from a small spec
- `scripts/` — `make_prompt.py`, `make_persona.py`, `new_template_skill.py` (scaffold a skill for a template)
- `test_*.py` — run to verify (all NO-API): prompt engine · cognition · persona · gate · skillpack

## Cognition chains & personas

`cognition.py` gives the three chain primitives as RenderablePiece blocks: an **attention chain**, a
**chain-of-reasoning** (which *nests* an AC = block-nesting), and a **skill chain**. **Rendering never
touches a grammar engine or a DB.** The **gate is a separate, optional layer** (`gate.py`, on
`rulecatcher`): `gate(text, exemplars)` LEARNS the grammar from exemplar chains (`next_kind` = shape,
`next_token` = vocabulary), then lints a candidate → violations + fixes + the `orthogonal` (in the
language, wrong slot → **steerable**) vs `syntax_break` (foreign → **fatal**) verdict.

```python
from prompt_engineering import render_cor, gate, make_persona

render_cor("Debugger", ["Symptom", "Repro", "Hypothesis"], "Localize", "the root cause")  # a CoR persona
gate("[Goal] ⇒ [Repro] ⇒ |Localize|",                                                     # learn, then lint:
     exemplars=["[Symptom] ⇒ [Repro] ⇒ |Localize|", "[Symptom] ⇒ [Bisect] ⇒ |RootCause|"])
# → {ok: False, verdict: 'orthogonal', violations: [{found:'Goal', candidates:['Symptom'], ...}]}

make_persona({                                   # a whole persona with a complex reasoning DSL, in one call
  "name": "Ada", "role": "a senior debugger",
  "reasoning": {"foci": ["Symptom", "Repro", "Bisect"], "held": "RootCause", "decision": "the minimal fix"},
  "rules": ["Reproduce before theorizing."], "output": "A markdown report.",
})
```

## Why deterministic matters

Each block's `render()` is a pure function of its typed fields; a `MetaStack` joins the rendered pieces in
order with a separator — pure composition, no model call. That's what lets an agent rely on it to produce
prompts consistently across runs. This is the base layer of the chaincompiler ecosystem (CC → ACCC →
CORCC → SCCC all import DOWN to here; see `META-APE-ARCHITECTURE.md`).
