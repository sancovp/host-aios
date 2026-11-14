"""
blocks.py — the APE block library: RenderablePiece subclasses on `pydantic-stack-core`.

THE FOUNDATION RULE (META-APE spec §2/§3): **every prompt is a `MetaStack` of `RenderablePiece`s.**
This module supersedes the old dict-payload / `exec()`-code-string mechanism (`template_mixins`): a block
is now a real, typed, self-rendering pydantic model (`RenderablePiece`), and a prompt is a `MetaStack`
(or a nestable `Group`) of them. Same data in → same string out, with no `exec`, no shared mutable state.

  - concrete blocks : Text, Heading, Section, Role, BulletList, Fenced, KeyValue, Template (data-driven)
  - composition     : Group (a nestable RenderablePiece bundle) + prompt()/render_prompt()/render_blocks()
  - declarative I/O : REGISTRY + block_from_dict({"type": ..., ...}) → instantiate a block from data/JSON

Everything downstream (cognition chains, personas, CC, the *CC) builds on these.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Type, Union

from pydantic import Field
from pydantic_stack_core import RenderablePiece, MetaStack, generate_output_from_metastack


# ── concrete blocks (each a RenderablePiece: typed fields + a pure render()) ────────────────────────
class Text(RenderablePiece):
    """Raw text, rendered verbatim."""
    text: str

    def render(self) -> str:
        return self.text


class Heading(RenderablePiece):
    """A markdown heading (`#` × level + text)."""
    text: str
    level: int = Field(default=2, ge=1, le=6)

    def render(self) -> str:
        return f"{'#' * self.level} {self.text}"


class Section(RenderablePiece):
    """A heading + a body paragraph."""
    heading: str
    body: str
    level: int = Field(default=2, ge=1, le=6)

    def render(self) -> str:
        return f"{'#' * self.level} {self.heading}\n{self.body}"


class Role(RenderablePiece):
    """A system/role line — `You are {role}.` (+ an optional mission clause)."""
    role: str
    mission: Optional[str] = None

    def render(self) -> str:
        s = f"You are {self.role}."
        if self.mission:
            s += f" Your mission is to {self.mission}."
        return s


class BulletList(RenderablePiece):
    """A bullet list, optionally under a `## title` heading."""
    items: List[str] = Field(default_factory=list)
    title: Optional[str] = None
    bullet: str = "-"

    def render(self) -> str:
        body = "\n".join(f"{self.bullet} {it}" for it in self.items)
        return f"## {self.title}\n{body}" if self.title else body


class KeyValue(RenderablePiece):
    """A `**key**: value` list, optionally under a `## title` heading."""
    pairs: Dict[str, str] = Field(default_factory=dict)
    title: Optional[str] = None

    def render(self) -> str:
        body = "\n".join(f"**{k}**: {v}" for k, v in self.pairs.items())
        return f"## {self.title}\n{body}" if self.title else body


class Fenced(RenderablePiece):
    """A fenced code block (```lang … ```)."""
    content: str
    lang: str = ""

    def render(self) -> str:
        return f"```{self.lang}\n{self.content}\n```"


class Template(RenderablePiece):
    """Generic data-driven block: a `str.format` template + `values` → a deterministic string.

    The SAFE replacement for the old `{values, methods:[code-string]}` block: same inputs → same output,
    pure composition, NO `exec`. Use this when a bespoke RenderablePiece subclass would be overkill.
    """
    template: str
    values: Dict[str, Any] = Field(default_factory=dict)

    def render(self) -> str:
        return self.template.format(**self.values)


class Group(RenderablePiece):
    """A nestable bundle of pieces. It IS a RenderablePiece, so (unlike a bare `MetaStack`) it can sit
    INSIDE another MetaStack/Group — this is how composite prompts (a CoR that nests an AC) compose."""
    pieces: List[RenderablePiece] = Field(default_factory=list)
    separator: str = "\n\n"

    def render(self) -> str:
        return self.separator.join(p.render() for p in self.pieces if p.render())

    def add_piece(self, piece: RenderablePiece) -> "Group":
        self.pieces.append(piece)
        return self


# ── declarative block I/O (data/JSON → a block) ────────────────────────────────────────────────────
# The replacement for the old JSON `{values, methods:[code-string]}` files: a block is now named by its
# `type` and carries its fields directly — `{"type": "Role", "role": "...", "mission": "..."}`.
REGISTRY: Dict[str, Type[RenderablePiece]] = {
    "Text": Text, "Heading": Heading, "Section": Section, "Role": Role,
    "BulletList": BulletList, "KeyValue": KeyValue, "Fenced": Fenced,
    "Template": Template, "Group": Group,
}


def register_block(cls: Type[RenderablePiece]) -> Type[RenderablePiece]:
    """Register a RenderablePiece subclass so block_from_dict can build it by name (also usable as a
    class decorator). Downstream layers (cognition, the *CC) register their own block types here."""
    REGISTRY[cls.__name__] = cls
    return cls


def block_from_dict(spec: Dict[str, Any]) -> RenderablePiece:
    """Instantiate a block from a declarative spec: `{"type": <RegistryName>, **fields}`.

    `Group` specs may carry nested `pieces` as either RenderablePiece instances or sub-specs.
    """
    data = dict(spec)
    type_name = data.pop("type", None)
    if type_name is None:
        raise ValueError("block spec must contain a 'type' key")
    cls = REGISTRY.get(type_name)
    if cls is None:
        raise ValueError(f"unknown block type {type_name!r}; known: {sorted(REGISTRY)}")
    if "pieces" in data:  # recurse into nested specs (Group and friends)
        data["pieces"] = [p if isinstance(p, RenderablePiece) else block_from_dict(p)
                          for p in data["pieces"]]
    return cls(**data)


# ── composition: pieces → a prompt (a MetaStack) ───────────────────────────────────────────────────
PieceLike = Union[RenderablePiece, Dict[str, Any]]


def _coerce(piece: PieceLike) -> RenderablePiece:
    return piece if isinstance(piece, RenderablePiece) else block_from_dict(piece)


def prompt(*pieces: Union[PieceLike, List[PieceLike]], separator: str = "\n\n") -> MetaStack:
    """Compose blocks (instances and/or declarative dicts; lists are flattened) into a `MetaStack` —
    the canonical 'a prompt is a MetaStack of RenderablePieces' constructor."""
    flat: List[RenderablePiece] = []
    for p in pieces:
        items = p if isinstance(p, (list, tuple)) else [p]
        flat.extend(_coerce(x) for x in items)
    return MetaStack(pieces=flat, separator=separator)


def render_prompt(*pieces: Union[PieceLike, List[PieceLike]], separator: str = "\n\n") -> str:
    """Compose + render a prompt in one call → the final string."""
    return generate_output_from_metastack(prompt(*pieces, separator=separator))


# back-compat / explicit alias used by the templates-folder loader
render_blocks = render_prompt


__all__ = [
    # foundation re-exports (so downstream imports the blocks from APE, the base)
    "RenderablePiece", "MetaStack", "generate_output_from_metastack",
    # concrete blocks
    "Text", "Heading", "Section", "Role", "BulletList", "KeyValue", "Fenced", "Template", "Group",
    # declarative I/O
    "REGISTRY", "register_block", "block_from_dict",
    # composition
    "prompt", "render_prompt", "render_blocks",
]
