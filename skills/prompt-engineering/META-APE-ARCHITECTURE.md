# META-APE / CHAINCOMPILER — THE ARCHITECTURE

A self-hosting prompt/cognition compiler stack: **every prompt is made of blocks**, the chain-compilers are built
ON chaincompiler, and chaincompiler ships as ONE Claude Code PLUGIN whose skills are the compiler functions
themselves. **No heaven anywhere in the ship.** Read §1 before building anything on it.

---

## 1. WHAT NOT TO DO

1. **Never reinvent the blocks.** The blocks are **`pydantic-stack-core`** (`RenderablePiece` / `MetaStack`) — a
   hand-rolled dict-payload "block" system is the wrong foundation.
2. **Never invert CC ↔ the \*CC.** The \*CC are built FROM CC (accc imports CC; corcc imports accc; sccc imports
   corcc + accc + CC). CC never imports the \*CC; CC sits BELOW them.
3. **Never build on dead or downstream sources.** `youknow_kernel` is deprecated — SOMA replaced it. `dogworld` is
   a downstream consumer (a code generator for AGENTS), never the foundation.
4. **Never block on OWL.** OWL is an optional later layer (§5); SOMA does not carry the class-templating the core
   needs.

---

## 2. THE FOUNDATION — `pydantic-stack-core`, and nothing else at the bottom

`RenderablePiece` (a block) + `MetaStack` (a stack of blocks that renders to one output), from PyPI
(`pip install pydantic-stack-core`; dep: `pydantic`). Every prompt in the stack is a `MetaStack` of
`RenderablePiece`s.

---

## 3. THE BUILD CHAIN (bottom → top). "X imports Y" ⇒ X is ABOVE Y, built ON Y.

```
0. FOUNDATION   pydantic-stack-core (RenderablePiece + MetaStack — the blocks). NOTHING else at the bottom.
1. APE          imports FOUNDATION   — the prompt engine: every prompt is a MetaStack of RenderablePieces
2. CC           imports APE          — chaincompiler, the compiler-compiler (`chaincompiler.forge` = the core)
3. ACCC         imports CC
4. CORCC        imports ACCC
5. SCCC         imports CORCC + ACCC + CC
   chainaios    the Bandit AIOS app, its own top package above the *CC — so CC never imports the *CC
```
- **CC does NOT import the \*CC.** The \*CC are built FROM CC. Publish order = dependency order = this chain.
- The layering is enforced by an import-linter contract on the DAG
  `chainaios > sccc > corcc > accc > chaincompiler > prompt_engineering`.

### Invariants (every layer obeys)
- **Every prompt is a `MetaStack` of `RenderablePiece`s.**
- **Every chain type (AC / CoR / SC) is its own system, made of CC.**
- **CC is made of this system; every \*CC is made from CC.**

---

## 4. THE CAPSTONE (the roll-up — the end state, built)

1. **BigGenerator (the prompt generator):** rolls all the per-chain-type generators into ONE generator that takes
   **any template-sequence of chains** and returns **ONE callable that renders**.
2. **PersonaGenerator:** `subclass(BigGenerator)` + a required **system-prompt name** + a **ROLE-intro block
   format** (XML by default, markdown mode) — the ROLE-block format is supplied at this step, never derived.
3. **Extrude:** the big generator makes the versions of everything; stack them, extrude the artifacts.
4. **meta-APE (self-compile):** an APE whose functions are the functions APE was BUILT with, each one a
   coordinate-addressed SKILL. Everything in meta-APE is **made of CC/\*CC objects**, and the **CC/\*CCs make
   everything in meta-APE**.

### Ship
- **The chaincompiler PLUGIN** ships the **meta-APE capability skills** (4 APE + 4 \*CC) + the **APE dep** + **all
  \*CC deps**. Every package → CC. **No heaven shipped.**
- **Downstream:** the prompts this stack makes are **parts of dogworld agents** (dogworld = the agent code
  generator that consumes them).

---

## 5. THE LATER, OPTIONAL LAYERS — not part of the core

- **Class-templating** (`TemplatedClass` + `template_mixins` — every class made by the templating system): comes
  after meta-APE, written against the stack above. Its reference implementation is not carried here.
- **OWL** (each made-thing carrying its own ontology): the canonical `python2owl2` is **SOMA's `vault()`** —
  it introspects a class/Pydantic model, declares it a `system_type` with each arg as a restriction, and POSTs to
  the SOMA daemon (the DB *is* the OWL; `promote_to_owl` projects to `.owl` for Pellet). A SOMA-free version lifts
  `vault.py` and swaps the daemon POST for a local OWL projection with the same `vault(obj, soma_url=…)`
  signature.

---

## 6. MIRROR, NEVER REINVENT

The progenitor template files, `pydantic-stack-core`, the existing \*CC (`chaincompiler/packages`), and — for the
agent-consumer shape only — dogworld's `template_agent.py` (state from a generated class, verbs from
`add_method`).
