---
name: rule-draft-box
description: The moment you think "this should be a NEW rule" — a pattern that has held 2–3 times, a correction worth keeping, an index the work keeps needing — ASK the ruleset's owner in one line, in the same reply, "should this go in rules, and where?", and park the text HERE while the question is open. This box is where an unanswered proposal waits; it is never a substitute for asking. An EXISTING rule that is wrong does not come here — rewrite it yourself, same turn (an AIOS rule in a new release, where the installation binds THE AIOS RELEASES) — and neither does a DEV FLOW, which you write, name and place yourself by the system's own law.
---

# THE RULE-DRAFT BOX — where a proposed new rule waits while its question is open

The boot config forbids creating a rule file in any `.claude/rules/` without asking *USER* first — except a dev
flow, a state file, a required diagram file and a project's scratchpad rule. This box is where any other proposed
rule waits between the question and the answer, so a rule-shaped thought is never dropped and never written into the
rules dir unasked.

**A DEV FLOW NEVER COMES HERE.** A procedure that runs whole every time is written straight into the `.claude/rules/`
of the dir whose procedure it is, as `22-seq-<feature>.md`, named after its feature, and drawn on that project's
architecture map the same turn (`28b` · `23`). The system's own law places it, so there is nothing to ask. A dev-flow
draft found here was filed under the old reading: place it, then delete it from the box.

## WHERE A DRAFT GOES

```
<the place `user_info` binds to THE RULE-DRAFT BOX>/<short-kebab-name>.md
```

One file per proposed rule, in THE RULE-DRAFT BOX — the place the installation's `user_info` binds to that role, read
from its table before the first draft is written — and one line for it in the box's `CLAUDE.md` (made with the box,
if it has none): the draft's file and the rule it proposes, so the box's index names every draft waiting there. It is never a folder inside this skill: an installed copy of a skill
sits in a folder that is replaced at each update, so a draft written there would be lost. An installation whose
`user_info` binds no place to it has no box yet: say so in the reply, ask where the box is, and keep the draft in the
reply until it is bound.

## WHAT A DRAFT IS

Two parts, and only the second is the rule:

1. **THE PROPOSAL** — one short paragraph for *USER*: what the rule would make true, and the occasions it would
   have fired on. It is read when the question is answered, and it does NOT travel when the rule lands.
2. **THE RULE ITSELF** — in the register, person-free, complete in itself: `TRIGGER:[…] PRINCIPLE:[…] DO:[…]
   NOT:[…]`, plus `COMPOSES:` where it touches other rules. This is the deliverable. It carries no date, no quote
   of *USER*, no story of how it came to be.

The number and the placement are *USER*'s. A draft names no number and claims no slot.

## THE LIFECYCLE

```
ASKED (one line, the same reply: "should this go in rules, and where?")
      →  DRAFTED here while the question is open
      →  STAMPED (*USER*'s yes — the rule is rewritten to carry whatever *USER* said)
      →  PLACED + NUMBERED (by *USER*)  →  the rules dir, in the register
```

An AIOS rule, where the installation binds THE AIOS RELEASES (`user_info`), is placed in a new release — its `rules/`
and its boot config's include line — by that binding's procedure, and reaches sessions when that release is promoted.

- Asking comes first, proactively. A draft filed without the question, or a rule written and mentioned afterwards,
  both skip it.
- The draft waits; the ruling it comes from does not. When *USER* says how every thing of a kind always is, every one
  of them that exists is brought to it the same turn, in the form it can take now — a README that must say how to run
  a program not yet written exists, and says so — and the reply names what was brought to it. Only the rule that would
  carry the ruling to every later thing waits for the answer.
- The box holds NEW rules only, and never a dev flow. An existing rule that is stale, wrong, contradicted by a measurement, or that
  *USER* says must change is REWRITTEN by the agent the same turn — an AIOS rule in a new release, as above — and the
  report names what it now says. Moving or
  renumbering an existing rule is *USER*'s.
- A draft that has been stamped and placed is DELETED from here, its line in the box's `CLAUDE.md` with it — the box
  holds only what is pending.

TRIGGER:[catching yourself thinking "this should be a NEW rule" · a pattern that has now held 2–3 times · a correction worth making permanent that no existing rule covers · about to CREATE a rule file in a rules dir (⇒ STOP: it comes here first — unless it is a dev flow, which you write in place) · finding an EXISTING rule that is wrong (⇒ NOT here: rewrite it, same turn — an AIOS rule in a new release — and say so) · finding a dev-flow draft in this box (⇒ place it in its dir, draw it on its map, delete it here)]
DO:[ASK in the same reply, one line: "should this go in rules, and where?" · bring every thing the ruling already covers to it, the same turn, in the form it can take now · write the two parts above · give the draft its line in the box's `CLAUDE.md` · keep the rule half in the register, person-free, complete in itself · leave the number and the placement empty · say in the reply that a draft was filed and where]
NOT:[create a rule file in any `.claude/rules/` without asking first, a dev flow excepted · leave a thing the ruling already covers for later because its rule is still a draft · park a dev flow here · park a fix to an existing rule here instead of making it · file a draft without asking · assign a number · claim a placement · file a one-off as a rule (a pattern that has held once is an incident, not a law) · put a date, a quote of *USER* or a history note in the rule half · let a draft rot here after it has been placed]
COMPOSES:[[[00-rules-are-live-state]] — a rule is a live instruction, and a pending change to one is a draft kept with it · [[24-scaffold-to-harness]] — a rule lands with the gate that detects its violation, and the draft names what that gate would be]
