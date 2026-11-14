---
name: adding-a-skill
description: When you make/add ANY skill (an AC, a CoR, a chain, a domain), do NOT just write the file — place it in the skilltree (coordinate-addressed), and because every directory is automatically an AIOS, give a new domain/role its own AIOS. Version it so the tree self-expands and search forwards to the newest. Use this whenever you create or improve a skill.
---

# Adding a skill — the base-agent obligation (always do this)

A skill is never just a file you drop. Whenever you make or improve one, you **place it and expand**.
The Python tools guarantee the shapes; you provide the info so the system can grow itself.

1. **Gate the form.** The skill must be well-formed (rulecatcher / the relevant `*CC` does this). Never
   judge content; always gate form.
2. **Place it in the tree, coordinate-addressed.** Don't leave it flat. Use the skilltree:
   `chaincompiler gba construct <agent-dir> <name> "[Focus] ⇒ [Focus] ⇒ |Converge|"` — it mints, gates,
   places it in the tree with a coord (`0.1`, `0.2.1`, …), and re-indexes so search can find it.
3. **Every dir is automatically an AIOS.** If the new thing is a **domain / role / agent** (not a leaf
   AC/CoR), give it its own AIOS — you are *required* to provide the info that lets the system build one:
   `chaincompiler gba new <domain> <agent-dir>/<thing> -a "<attention-chain>"`. Now it's a sub-agent you
   `cd` into. (A COG seat, a sub-domain, a worker — all get their own AIOS dir.)
4. **Version it for self-expansion.** When you *improve* an existing skill, write the new one with a higher
   `version:` (keep the old as history — the warrant). **Search forwards to the newest version**
   (`gba search … --newest`), so the tree improves over time without losing provenance.
5. **Coordinates make it globally legible.** Names + coords resolve everywhere, so a chain (a flow through
   dirs) is readable by the whole system. That legibility is the point.

The base agent does this **every time** — place + (if a domain) AIOS + version. That is how the tree
self-expands and the system stays navigable instead of becoming a flat pile.
