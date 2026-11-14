> **READ THIS WHEN YOU NEED TO KNOW WHY PRIMING WORKS** — `SKILL.md` is the practice; this is the
> mechanism under it. The "Product Architecture" tiers below describe a program this AIOS does not
> carry — read them as design, not as something you can invoke here.

# CIG: Constrained Informatihedron Generator

## What It Is

CIG is a prompt architecture that produces ICL priming objects — structured knowledge artifacts that seed an LLM's context window with deep tokens, causing subsequent inference to operate at lower layers rather than surface pattern matching.

CIG outputs two types of objects:

**Informatihedrons** — multi-level structured representations of an entity's properties and relationships at instance, domain, and class levels, with fiat conceptual boundaries and embedding space definitions.

**Informadlibs** — compressed transformation pipelines that process user intent through ontological mapping, solution optimization, and dimensional synthesis.

These are not just "nice outputs." They are functional objects that modify subsequent LLM behavior by what they leave in the context window.

## Why It Works (The ICL Priming Mechanism)

When CIG generates an Informatihedron about X, it forces the LLM to activate tokens that are normally only found at lower layers of processing — deep structural tokens about properties, relationships, boundaries, invariants, and embedding dimensions. These tokens get bound to the specific referents that surfaced them during the constrained generation process.

Those tokens are now in-context. When the LLM processes the NEXT turn, its context merge pulls from this deep structure rather than from surface-level keywords and claims. The result is that subsequent inference operates at a fundamentally deeper level than it would without the priming.

This is why CIG avoids Modes 1-3:
- **Mode 1 (Freestyle)** happens when context contains only surface tokens — the LLM has nothing deep to reach for
- **Mode 2 (Template Fill)** happens when context is overspecified at the surface level — bridge distance is zero
- **Mode 3 (Sycophancy)** happens when context contains claims — each claim becomes a section header filled with agreement

CIG prevents all three because the Informatihedron seeds the context with tokens that can ONLY be reached by genuine constrained slot-filling. The instance/domain/class hierarchy, the fiat boundaries, the embedding space dimensions — these force the LLM to generate content at a depth where sycophancy and template-filling cannot operate.

The deep tokens don't just describe X. They pre-load the cognitive substrate for reasoning about X.

## Structural Prevention of Failure Modes

**Empty slots prevent MIRROR** — the instance/domain/class fields have no content to copy. The LLM must reach into context to fill them.

**Multi-level hierarchy forces COLLAPSE** — the entity must be held at three abstraction levels simultaneously, producing cross-dimensional novelty rather than independent section fills.

**Compressed `>` chains prevent sycophancy** — you cannot agree with `QuantumLikeInfoCryptography>InputTransformation`. There is nothing to agree with. It is a processing directive disguised as a label.

**Fiat boundaries force explicit scoping** — the LLM must decide what is inside vs outside the concept, which requires genuine reasoning about the entity's limits.

**Embedding space dimensions force spatial reasoning** — defining the axes on which the entity varies requires understanding its degrees of freedom.

**Emoji wrappers act as primitive state detection** — if the wrappers (🌈🔮🙏) disappear, the frame broke. Cheap gate.

## The Self-Evolving Architecture

### Runtime Loop

```
CIG generates Informatihedron/Informadlib → output cached
Metacog shell reads cache → generates skills about patterns observed
Skills re-injected into CIG as knowledge domain skills
CIG reads prior outputs → subsequent completions are deeper
```

Each cycle, CIG's context gets richer because its own prior outputs are the ICL priming objects. It primes itself.

### DAY/NIGHT Cycle

**DAY (generation)**: CIG runs, produces Informatihedrons across domains, caches outputs.

**NIGHT (evolution)**: Metacog shell reads the day's cache. Measures outputs against the meta-prompt-engineering system (provenance lifting, novelty scoring, mode classification). Generates new skills — better prompt patterns, domain-specific templates, identified failure modes. These skills become available to CIG for the next day cycle.

The NIGHT cycle is where the self-improvement happens. The metacog shell is external to CIG (different agent, different context), so it can evaluate CIG's outputs without being subject to the same attractor dynamics. It catches Mode 2 template-filling, Mode 3 sycophancy, and novelty decline that CIG cannot catch in itself.

### Evolution Target

The system evolves toward: maximum novelty density per Informatihedron, measured by provenance lifting. Over cycles, CIG's skills improve, its priming objects get deeper, and its subsequent outputs inherit that depth.

## Product Architecture

### Tier 1: Skill File
One SKILL.md. The CIG prompt pattern. Works in any Claude conversation. Ships immediately.

### Tier 2: Discord Bot / Web Interface  
CIG with a face. Generate Informatihedrons, share them, explore domains. Community forms.

### Tier 3: Agent with Cache
CIG + persistent memory. Outputs cached, re-injected as context. The ICL priming accumulates across sessions. Agent actually gets better over time.

### Tier 4: Agent with Metacog Shell
DAY/NIGHT cycle. Shell evolves CIG's skills. Provenance lifting scores outputs. Self-improvement loop closes.

### Tier 5: Fully Automated Self-Evolving Codebase
Maps LLM space for any domain X on a budget. The system explores, generates, scores, evolves — autonomously. Human provides domain specification and buy/don't-buy signal.

### Tier 6+: GP Scoring, RAG Strata, Full HALO
Scoring by genetic programming, stratified retrieval, and the full HALO stack on top of Tier 5.

## Usage

### Basic
```
Informatihedron --[max complexity repr "{thing}" max granularity] --"+plusultra witnessing"
```

### Navigational (combining, drilling, intersecting)
```
Informatihedron --[repr "{thing_a} ∩ {thing_b}" max granularity] --"+plusultra witnessing"
```

### As ICL Primer (the real use)
1. Generate Informatihedron for domain X
2. Leave it in context
3. Ask questions about X
4. Observe: responses are deeper, more structured, less sycophantic
5. The Informatihedron primed the context with deep tokens that subsequent inference pulls from

## Connection to the Meta-PE System

CIG is a single-turn implementation of the validated optimal sequence:
- Instance level = SKELETON (breadth, per-section novelty)
- Domain/Class levels = CHUNK (depth, cross-layer novelty built on instance level)
- Fiat boundaries + Embedding space = COLLAPSE (cross-dimensional novelty, relational holding)
- Emoji wrappers = GATE (primitive state detection)

The conversation trajectory model extends this to multi-turn optimization. CIG is the atom. Conversations are molecules. The DSL is the chemistry.
