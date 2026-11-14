"""
cognition.py — the cognition-chain primitives (AC / CoR / SC) as RenderablePiece blocks.

The three chain types are PROMPT BLOCKS on the foundation (META-APE spec invariant: *every chain type
is its own system, every prompt is a MetaStack of RenderablePieces*). A chain renders by composing smaller
blocks into a MetaStack; a CoR NESTS an AC (the inner chain is a field/piece of the outer) = block-nesting.

  attention chain   [A] ⇒ [B] ⇒ |Held|              inner "how to think" scaffold (not necessarily spoken)
  chain of reasoning  a CoR nests an AC + a spoken paragraph that ends in a DECISION
  skill chain       [ac:x] ⇒ [cor:y] ⇒ [skill:z] ⇒ |Goal|   resolved steps, rolled up

The validator is DERIVED FROM THE SHAPE (validate_chain): author the shape (+ optional vocabulary) once,
and it checks conformance deterministically — no induction, no DB. (The learned-grammar gate is the
optional `gate`/`grammar` layer on rulecatcher.)
"""

import re
from typing import List, Optional, Tuple, Union

from pydantic import Field

try:
    from .blocks import (RenderablePiece, Text, Heading, Fenced, Group,
                         register_block, generate_output_from_metastack, MetaStack)
except ImportError:  # standalone
    from blocks import (RenderablePiece, Text, Heading, Fenced, Group,
                        register_block, generate_output_from_metastack, MetaStack)

ARROW = "⇒"
_FOCUS = re.compile(r"\[([^\]]+)\]")
_HELD = re.compile(r"\|([^|]+)\|")


# ── notation + validator (pure functions; the shape IS the grammar) ─────────────────────────────────
def chain_notation(foci: List[str], held: Optional[str] = None) -> str:
    s = f" {ARROW} ".join(f"[{f}]" for f in foci)
    if held:
        s += f" {ARROW} |{held}|"
    return s


def parse_chain(text: str) -> Tuple[List[str], Optional[str]]:
    foci = [m.group(1).strip() for m in _FOCUS.finditer(text)]
    held = _HELD.search(text)
    return foci, (held.group(1).strip() if held else None)


def validate_chain(text: str, *, vocab: Optional[List[str]] = None,
                   require_held: bool = True, min_foci: int = 1) -> Tuple[bool, List[str]]:
    """The broken-detector. The chain's shape (+ optional authored vocabulary) IS the grammar; this checks
    conformance deterministically. Returns (ok, errors)."""
    errors: List[str] = []
    foci, held = parse_chain(text)
    if len(foci) < min_foci:
        errors.append(f"need >= {min_foci} focus block(s) [X]; found {len(foci)}")
    if require_held and not held:
        errors.append("missing terminal |Held| focus")
    if vocab is not None:
        allowed = set(vocab)
        for f in foci:
            if f not in allowed:
                errors.append(f"focus '{f}' not in authored vocabulary {sorted(allowed)}")
        if held and held not in allowed:
            errors.append(f"held '{held}' not in authored vocabulary {sorted(allowed)}")
    expected_arrows = max(0, len(foci) - 1) + (1 if held else 0)
    if (foci or held) and text.count(ARROW) != expected_arrows:
        errors.append(f"arrow count {text.count(ARROW)} != expected {expected_arrows} (malformed chain)")
    return (not errors), errors


def cor_skeleton(moves: List[str], cues: Optional[dict] = None) -> str:
    """The CoR fill-in paragraph skeleton: `[move: …cue…] → …` (one clause per move). `cues` maps a move
    name to its cue phrase (defaults to the move name)."""
    cue_for = cues or {}
    return " → ".join(f"[{m}: …{cue_for.get(m, m)}…]" for m in moves)


# ── the chain blocks (RenderablePiece subclasses) ──────────────────────────────────────────────────
@register_block
class AttentionChain(RenderablePiece):
    """An attention chain: the inner 'how to think' scaffold. Renders head + chain + how-to as a stack."""
    foci: List[str] = Field(default_factory=list)
    held: Optional[str] = None

    def notation(self) -> str:
        return chain_notation(self.foci, self.held)

    def render(self) -> str:
        head = ("This is an ATTENTION CHAIN — an inner template for how to think (a scaffold for a "
                "section or your reasoning). Not necessarily spoken.")
        chain_md = "## Chain\n" + Fenced(content=self.notation(), lang="rune").render()
        how = ("Attend, in order, to: " + ", ".join(self.foci)
               + (f"  —  then hold |{self.held}|." if self.held else "."))
        return generate_output_from_metastack(
            MetaStack(pieces=[Text(text=head), Text(text=chain_md), Text(text=how)], separator="\n\n"))


@register_block
class ChainOfReasoning(RenderablePiece):
    """A chain-of-reasoning persona. NESTS an AttentionChain (the inner scaffold) + a spoken paragraph
    that ends in a DECISION. If `cues` is given (a {move: cue} dict or a list aligned to foci+[held]),
    it also renders the fill-in SKELETON + a must-surface-each-cue directive."""
    name: str
    foci: List[str] = Field(default_factory=list)
    held: str
    decision: str
    cues: Optional[Union[dict, list]] = None

    def inner_chain(self) -> AttentionChain:
        return AttentionChain(foci=self.foci, held=self.held)

    def render(self) -> str:
        moves = list(self.foci) + [self.held]
        pieces: List[RenderablePiece] = [
            Heading(text=f"Persona: {self.name}", level=1),
            Text(text=("## Chain of reasoning (SAY this — a paragraph that ends in a decision)\n"
                       + Fenced(content=chain_notation(self.foci, self.held), lang="rune").render()
                       + "\nWork the moves in order; converge on: " + self.decision + ".")),
        ]
        if self.cues:
            cue_for = self.cues if isinstance(self.cues, dict) else dict(zip(moves, self.cues))
            pieces.append(Text(text="## Say it like this (fill in each cue)\n" + cor_skeleton(moves, cue_for)))
            pieces.append(Text(text=(f"Say ONE paragraph that, in order, works {len(self.foci)} moves "
                                     f"({', '.join(self.foci)}) and converges on {self.held}; "
                                     f"surface each move's cue.")))
        pieces.append(Text(text="## Inner attention chain (use silently to generate the above)\n"
                                + self.inner_chain().render()))
        return generate_output_from_metastack(MetaStack(pieces=pieces, separator="\n\n"))


@register_block
class SkillChain(RenderablePiece):
    """A skill chain: ordered [kind:ref] steps (ac|cor|skill) converging on a goal."""
    steps: List[Tuple[str, str]] = Field(default_factory=list)
    goal: str

    def render(self) -> str:
        steps_md = "\n".join(f"{i}. [{kind}:{ref}]" for i, (kind, ref) in enumerate(self.steps, 1))
        pieces = [
            Text(text="This is a SKILL CHAIN — resolve each step in order, then converge on the goal."),
            Text(text="## Steps\n" + steps_md),
            Text(text="## Goal\n|" + self.goal + "|"),
        ]
        return generate_output_from_metastack(MetaStack(pieces=pieces, separator="\n\n"))


# ── public render helpers (names preserved) ────────────────────────────────────────────────────────
def render_attention_chain(foci: List[str], held: Optional[str] = None) -> str:
    return AttentionChain(foci=foci, held=held).render()


def render_cor(name: str, foci: List[str], held: str, decision: str, cues=None) -> str:
    return ChainOfReasoning(name=name, foci=foci, held=held, decision=decision, cues=cues).render()


def render_skillchain(steps: List[Tuple[str, str]], goal: str) -> str:
    return SkillChain(steps=steps, goal=goal).render()


__all__ = ["chain_notation", "parse_chain", "validate_chain", "cor_skeleton",
           "AttentionChain", "ChainOfReasoning", "SkillChain",
           "render_attention_chain", "render_cor", "render_skillchain", "ARROW"]
