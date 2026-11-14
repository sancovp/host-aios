"""
generator.py — the capstone BIG GENERATOR (META-APE spec §4.1).

Rolls the per-chain-type generators (AC / CoR / SC) into ONE generator: give it a **template-sequence of
chains** (an ordered list of `(kind, spec)` entries, `kind ∈ {ac, cor, sc}`) and it returns ONE callable
that renders the whole sequence into a single prompt — a `MetaStack` of the chain blocks. This is the
roll-up the PersonaGenerator (§4.2) subclasses and that meta-APE (§4.4) turns into a skill.

    gen = big_generator([("ac", {...}), ("cor", {...}), ("sc", {...})])
    prompt_text = gen()          # ONE callable that renders → the composed prompt
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from pydantic import Field

try:
    from .blocks import MetaStack, RenderablePiece, Heading, Text, prompt as _prompt
    from .cognition import AttentionChain, ChainOfReasoning, SkillChain
except ImportError:  # standalone
    from blocks import MetaStack, RenderablePiece, Heading, Text, prompt as _prompt
    from cognition import AttentionChain, ChainOfReasoning, SkillChain


# the per-chain-type generators, keyed by chain kind (accc↔AC, corcc↔CoR, sccc↔SC)
CHAIN_TYPES: Dict[str, type] = {
    "ac": AttentionChain,
    "cor": ChainOfReasoning,
    "sc": SkillChain,
}

# a template-sequence entry: a chain kind + the spec for that chain's block (its constructor fields),
# OR an already-built RenderablePiece (passed through verbatim).
ChainEntry = Union[Tuple[str, Dict[str, Any]], RenderablePiece]


def chain_block(entry: ChainEntry) -> RenderablePiece:
    """Build the RenderablePiece for one template-sequence entry."""
    if isinstance(entry, RenderablePiece):
        return entry
    kind, spec = entry
    cls = CHAIN_TYPES.get(kind)
    if cls is None:
        raise ValueError(f"unknown chain kind {kind!r}; known: {sorted(CHAIN_TYPES)}")
    return cls(**spec)


class BigGenerator:
    """Rolls all per-chain-type generators into ONE. Build from a template-sequence of chains; the
    instance is itself the callable that renders (`gen()` → the composed prompt). Subclass to specialize
    (e.g. the PersonaGenerator, §4.2)."""

    def __init__(self, sequence: Sequence[ChainEntry] = (), *, separator: str = "\n\n"):
        self.sequence: List[ChainEntry] = list(sequence)
        self.separator = separator

    def blocks(self) -> List[RenderablePiece]:
        """The chain blocks for the whole sequence (subclasses may prepend/append, e.g. a ROLE block)."""
        return [chain_block(e) for e in self.sequence]

    def metastack(self) -> MetaStack:
        """The whole prompt as a MetaStack of RenderablePieces (the foundation invariant)."""
        return _prompt(*self.blocks(), separator=self.separator)

    def render(self) -> str:
        return self.metastack().render()

    def __call__(self) -> str:
        """ONE callable that renders (§4.1)."""
        return self.render()


def big_generator(sequence: Sequence[ChainEntry] = (), *, separator: str = "\n\n") -> BigGenerator:
    """Return ONE callable that renders a template-sequence of chains into a prompt (§4.1)."""
    return BigGenerator(sequence, separator=separator)


# ── the persona generator (§4.2): subclass(BigGenerator) + a system-prompt name + a ROLE-intro block ──
class XmlRole(RenderablePiece):
    """The DEFAULT ROLE-intro block: an XML `<role>` element that WRAPS the persona body. A RenderablePiece
    (so the whole persona is still a MetaStack of blocks), it carries the system-prompt name + named fields
    (mission / law / …) and nests the chain blocks inside the element."""
    name: str
    description: Optional[str] = None
    fields: Dict[str, str] = Field(default_factory=dict)   # mission, law, voice, …
    inner: List[RenderablePiece] = Field(default_factory=list)
    separator: str = "\n\n"

    def render(self) -> str:
        head = [f'<role name="{self.name}">']
        if self.description:
            head.append(f"  <description>{self.description}</description>")
        for k, v in self.fields.items():
            head.append(f"  <{k}>{v}</{k}>")
        body = self.separator.join(p.render() for p in self.inner if p.render())
        return "\n".join(head) + (("\n\n" + body) if body else "") + "\n</role>"


class PersonaGenerator(BigGenerator):
    """Persona prompt generator (§4.2): a `BigGenerator` subclass + a required system-prompt `name` + a
    ROLE-intro block. Two modes:
      - 'xml' (DEFAULT) → an XML `<role name=…>` element (with mission/law/… fields) WRAPPING the chains.
      - 'markdown'      → a `# {name}` heading + a `You are …` role line, THEN the chains.
    """

    def __init__(self, name: str, sequence: Sequence[ChainEntry] = (), *, role: Optional[str] = None,
                 fields: Optional[Dict[str, str]] = None, mode: str = "xml", separator: str = "\n\n"):
        super().__init__(sequence, separator=separator)
        self.name = name
        self.role = role
        self.fields: Dict[str, str] = dict(fields or {})
        if mode not in ("xml", "markdown"):
            raise ValueError(f"mode must be 'xml' or 'markdown', got {mode!r}")
        self.mode = mode

    def chain_blocks(self) -> List[RenderablePiece]:
        """Just the AC/CoR/SC chain blocks (the BigGenerator body)."""
        return [chain_block(e) for e in self.sequence]

    def blocks(self) -> List[RenderablePiece]:
        chains = self.chain_blocks()
        if self.mode == "xml":
            return [XmlRole(name=self.name, description=self.role, fields=self.fields,
                            inner=chains, separator=self.separator)]
        # markdown mode — the # heading + role line, then the chains (a flat MetaStack of blocks)
        intro: List[RenderablePiece] = [Heading(text=self.name, level=1)]
        if self.role:
            line = f"You are {self.role}."
            if self.fields.get("mission"):
                line += f" Your mission is to {self.fields['mission']}."
            intro.append(Text(text=line))
        extra = [f"- **{k}**: {v}" for k, v in self.fields.items() if k != "mission"]
        if extra:
            intro.append(Text(text="\n".join(extra)))
        return intro + chains


def persona_generator(name: str, sequence: Sequence[ChainEntry] = (), *, role: Optional[str] = None,
                      fields: Optional[Dict[str, str]] = None, mode: str = "xml",
                      separator: str = "\n\n") -> PersonaGenerator:
    """Return ONE callable that renders a named persona (ROLE-intro block + AC/CoR/SC chains). `mode='xml'`
    (default) wraps in an `<role>` element; `mode='markdown'` uses a `# {name}` heading + role line."""
    return PersonaGenerator(name, sequence, role=role, fields=fields, mode=mode, separator=separator)


__all__ = ["BigGenerator", "big_generator", "chain_block", "CHAIN_TYPES", "ChainEntry",
           "XmlRole", "PersonaGenerator", "persona_generator"]
