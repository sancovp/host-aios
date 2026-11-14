---
name: goldenize-a-capability
description: The sovereignty pipeline — how a capability becomes PROVEN so A may run it. Candidate → quarantine → EMANATION (a fresh config-only successor does it correctly) → human approval → golden (runnable + composable). Goldenize is the linchpin; A runs ONLY golden things. Read this before acting on anything new, or when a capability was refused for not being goldenized.
---

# Goldenize a capability (the linchpin)

**A runs only goldenized things**, so goldenizing is the *only* door capability walks through into your sovereign
repertoire. Sovereignty = when you act from A you KNOW it works, because "golden" means "proven."

## The pipeline (cave-teams)
```python
from cave_teams import cave, golden
spec = {"op": "seq", "name": "review_crew", "links": [{"op": "agent", "name": "reviewer"}]}
await cave(spec, name="review_crew", save=True, describe_only=True)  # 1. QUARANTINE the candidate (don't run yet)
# ... 2. EMANATION: prove it (below) ...
await cave(goldenize=True, name="review_crew")                       # 3. GOLDENIZE (the call IS the approval)
golden("review_crew")                                                # 4. now a runnable, COMPOSABLE Link
# compose it anywhere:  {"op": "seq", "links": [{"op":"agent","name":"intake"}, {"op":"golden","name":"review_crew"}]}
```
Goldenizing **extends the instruction set** — a golden team is now a native `{"op":"golden","name":...}` op.

## The EMANATION condition (do NOT skip — it's what makes it real)
You succeeding proves nothing (could be your context/luck). The proof is that the **config transfers**:

> Observe a **fresh, config-only successor** — a clean re-instantiation from the config you leave behind — do it
> **correctly**, then the human approves.

For OM this = a fresh Custodian / cave-team built purely from the quarantined spec runs the task, and a
prediction→observe pass (your OFIAP P→O, or the WOOM verified-terminal) confirms it. Self-observation is NOT a
door; **emanation + human approval are the two doors** into A.

## The bootstrap
The **only primordial golden capability is `construct`/select (the bandit loop)**. Everything else grows from it,
one emanation-proven + human-approved rung at a time. That two-key gate is how the repertoire stays all-proven —
nothing enters on the author's word alone.
