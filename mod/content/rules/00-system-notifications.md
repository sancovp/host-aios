# [SKILLTREE] System Notifications

> This rule posts system notifications. It is **automatically managed by SkillTree**.
> **Do not edit this rule** — it is rewritten by the decoherence check whenever the
> SkillTree's on-disk shape drifts from its engineered (coherent) form.

## Warnings

- 🔴 **ERROR** — bare_forest: skills — no skilltree.json; 0 top skills with no root — run `emit --root` to tree-ify
- 🟡 **WARN** — uncoordinated: skills — nodes have no coordinates (never materialized with coords)

## To fix these (1 error(s), 1 warning(s))

The SkillTree under `~/.claude/skills` has **decohered**: its `cat`-breadcrumbs / coordinates no longer match the tree's real shape (rule 01 — a bare forest or stale wiring).

**Run the `skilltree` skill** (the recohere flow). In short: `skilltree emit <root>` re-coheres the tree in place (add `--root` to tree-ify a bare forest). This notice clears itself on the next check.
