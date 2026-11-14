---
name: make-everything-better-gan
description: "WHAT: get work reviewed by subagent THE RIGHT WAY — ONE comprehensive review, then fix, then show *USER*. WHEN: a substantial change is supposedly done — several subsystems or processes, a shared contract, a multi-stage run. Not for a small feature proven live, and never a second round after the fix pass."
---

# make-everything-better-gan — how to get work reviewed

The reviewer critiques the work, **writes the dev-flow rule for you**, and reports what your
bundle was missing. Call it on every substantial change and the dev-flow rules stay current on
their own — each review re-derives them against reality, so they never rot. A small feature
(one surface, contained) ships on its live proof instead.

**Under a lead** (the `how-to-lead-an-aios` skill) the lead makes this call for a child's change: a child's agent
launches no agent, so it reports its substantial change done, and its lead calls the review and hands the findings back.

**ONE review per change, then the fix, then *USER*.** Make the one review comprehensive — the whole
execution boundary, every store and its readers — fix every finding it returns (a case that fails on
the prior code, or the finding written into the design and boarded), and show *USER* the result.
Never dispatch a second review of the fix pass: a reviewer always finds more, and review → fix →
review is the GAN loop, which spends *USER*'s money on wording and never converges.

## 1 — ASSEMBLE THE BUNDLE YOU HAND IT

Not from memory. A bundle is a TRACE and it has two directions:

```
DOWN  what does this touch?        you did this anyway while working
UP    who reads what it touched?   this is where the silent failures live
```

**DOWN** — every file you actually read or edited, with the line ranges that mattered.

**UP** — name every STORE the work wrote (fs · git objects · DB · socket · spawned process ·
registry), then grep who READS each one. *grep locates readers; it never traces execution.*
A store's readers are the hops with no import edge — the ones nothing reminds you about.

**A measurement per store.** If you cannot say how you would measure that store changing, you
do not have the boundary — you have a guess.

## 2 — THE CALL

Never name the author. Anonymous-and-suspected produces evaluation; a named author produces
deference.

```
Another agent may have done something wrong.

THE CHANGE:  <branch / diff / commit range>
THE BUNDLE it treated as this feature's execution boundary:
  <files + line ranges · the stores written · who reads them>

READ every file at every range listed, fully. Then answer three things:

1. CRITIQUE — is the change correct? Name the failure concretely, not as a risk.

2. AUTHOR (or UPDATE) the dev-flow rule at
   <project>/.claude/rules/22-seq-<feature>.md
     RETRIEVE       files + exact line ranges
     COHERENCE SET  what else must change because this changed
     THE CHANGE     what this feature does
     THE PROOF      the per-store before/after measurement
   If the rule already exists, correct it — do not append.

3. THE DELTA — what did the bundle OMIT that you needed, and what did it
   include that was irrelevant?
   ⭐ If it omitted something, CHECK WHETHER THE CHANGE IS WRONG BECAUSE OF
   THAT OMISSION. A gap in the bundle is the most likely LOCATION of the
   defect — it is the hop the author was not thinking about while working.
```

## 3 — THE DELTA IS THE FINDING

Non-empty delta ⇒ **go re-check the work inside the gap** before believing the change. A green
critique with a non-empty delta is not a pass.

TRIGGER:[a substantial change is supposedly done · about to say it is finished/verified/shipped ·
about to open its PR · about to report it — never for a small feature proven live]
NOT:[assemble the bundle from memory · pass it without asking for the delta back · name the
author in the brace · believe a green result when the delta was non-empty · dispatch a second review
of the same change after its fix pass — fix, then show *USER*]

> Reading an existing `22-seq-<feature>.md` before you work is that RULE doing its job — not
> this skill. This skill is how the rule gets written and kept true.
