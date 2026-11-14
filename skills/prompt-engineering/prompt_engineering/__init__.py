"""
prompt_engineering (APE) — the deterministic prompt engine, on `pydantic-stack-core`.

THE shared foundation of the chaincompiler ecosystem (rule: everyone imports DOWN from here). Rebuilt on
`pydantic-stack-core`: **every prompt is a `MetaStack` of `RenderablePiece`s** (blocks.py). This supersedes
the old dict-payload / exec-code-string mechanism — blocks are now real typed self-rendering models.

  - blocks        : RenderablePiece block library (Text/Heading/Section/Role/BulletList/Fenced/Template/Group)
                    + prompt()/render_prompt() + declarative block_from_dict()/register_block()
  - prompt_engine : render a block spec; load + render stored prompt templates (folders of block specs)
  - cognition     : attention chain / chain-of-reasoning / skill chain as RenderablePiece blocks
  - persona       : make_persona — a full persona prompt from a small spec
  - gate          : optional learned-grammar lint on the `rulecatcher` package (ephemeral convenience)
  - grammar       : the rulecatcher seam (persistent, connection-based learn/gate/render)
  - skillpack     : write_skill — a markdown body → a publishable <name>/SKILL.md (skilltree-aware)
"""

# ── the blocks (the foundation usage layer) ─────────────────────────────────────────────────────────
from .blocks import (
    RenderablePiece, MetaStack, generate_output_from_metastack,
    Text, Heading, Section, Role, BulletList, KeyValue, Fenced, Template, Group,
    REGISTRY, register_block, block_from_dict,
    prompt, render_prompt, render_blocks,
)
# ── the prompt engine (single block + stored templates) ─────────────────────────────────────────────
from .prompt_engine import (
    render, render_file, templates_root,
    list_templates, load_template, render_template, render_template_blocks,
)
# ── cognition chains ────────────────────────────────────────────────────────────────────────────────
from .cognition import (
    chain_notation, parse_chain, validate_chain, cor_skeleton,
    AttentionChain, ChainOfReasoning, SkillChain,
    render_attention_chain, render_cor, render_skillchain,
)
# ── personas ────────────────────────────────────────────────────────────────────────────────────────
from .persona import make_persona, make_persona_file
# ── the capstone generators (§4.1/§4.2): roll the per-chain-type generators into ONE callable ─────────
from .generator import (BigGenerator, big_generator, chain_block, CHAIN_TYPES,
                        XmlRole, PersonaGenerator, persona_generator)
# ── meta-APE (§4.4): each compiler build-function becomes a real SKILL ─────────────────────────────────
from .meta_ape import Capability, APE_CAPABILITIES, emit_meta_ape
# ── the optional grammar gate (ephemeral) + the persistent rulecatcher seam (grammar.py) ─────────────
# NOTE: the persistent gate(connection, chain, *, scope) is intentionally NOT re-exported at top level
# (it would clash with the ephemeral gate(text, exemplars)) — use `prompt_engineering.grammar.gate`.
from .gate import gate
from .grammar import learn, grammar_lines, foreign_tokens
# ── the skill-packager (skilltree-aware) ────────────────────────────────────────────────────────────
from .skillpack import slugify, skill_markdown, write_skill, cohere_skills

__version__ = "0.2.0"

__all__ = [
    # blocks (foundation usage)
    "RenderablePiece", "MetaStack", "generate_output_from_metastack",
    "Text", "Heading", "Section", "Role", "BulletList", "KeyValue", "Fenced", "Template", "Group",
    "REGISTRY", "register_block", "block_from_dict",
    "prompt", "render_prompt", "render_blocks",
    # prompt engine
    "render", "render_file", "templates_root",
    "list_templates", "load_template", "render_template", "render_template_blocks",
    # cognition chains
    "chain_notation", "parse_chain", "validate_chain", "cor_skeleton",
    "AttentionChain", "ChainOfReasoning", "SkillChain",
    "render_attention_chain", "render_cor", "render_skillchain",
    # personas
    "make_persona", "make_persona_file",
    # capstone generators (§4.1/§4.2)
    "BigGenerator", "big_generator", "chain_block", "CHAIN_TYPES",
    "XmlRole", "PersonaGenerator", "persona_generator",
    # meta-APE (§4.4)
    "Capability", "APE_CAPABILITIES", "emit_meta_ape",
    # grammar gate (ephemeral) + the persistent rulecatcher seam (grammar.py)
    "gate", "learn", "grammar_lines", "foreign_tokens",
    # skill packager
    "slugify", "skill_markdown", "write_skill", "cohere_skills",
    "__version__",
]
