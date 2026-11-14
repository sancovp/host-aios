---
name: fix-skill-descriptions-and-rules
description: WHEN writing or editing any skill description or rule trigger — or when a history shows a skill/rule that SHOULD have fired but didn't — rewrite it to ONE imperative + its firing `if`/WHEN-clause (WHAT to do + WHEN to do it), never indicative prose that describes the skill. If you cannot answer "could I obey or not-obey this RIGHT NOW?" against a description, it will never fire; rewrite it until you can.
---

# fix-skill-descriptions-and-rules

## The one law

A skill/rule description **IS an instruction-prompt, not a description.** It is ONE imperative sentence:

```
WHAT (imperative verb-phrase)  +  WHEN (firing `if`/when-clause)
```

WHAT and WHEN are not two fields you fill — they are the natural joints of a single command ("do X **if/when** Y"). The `WHAT:`/`WHEN:` labels are scaffolding for *you while writing*; the actual object is the sentence, and the sentence is an **order** addressed to the reader (the LLM).

Canonical example:

> **make-session-start-hook** — WHAT: make a session start hook; WHEN: if you need to force something to happen at the start of EVERY CONVERSATION
> → as one instruction: *"make a session start hook if you need to force something to happen at the start of every conversation."*

That whole string is imperative mood with a conditional clause. The reader reads it, checks `if` its own current situation satisfies the clause — **and the check IS the firing.** Instruction-only, all the way down. No descriptive register anywhere in it.

## Why it has to be that way — the selector loop

The description is not metadata. It is a **candidate chain in a selector that runs every single generation.** Each token, the reader runs:

```
for each loaded description d:
    obey?(d, now)                                  # "could I obey or not-obey this RIGHT NOW?"  → live | dead
live_set   = { d : obey?(d, now) is answerable }   # only descriptions that parse as an order against my situation
factor_set = { d ∈ live_set : need to factor into next generation }   # relevance filter
action     = collapse(factor_set)                  # "out of all these maybe_should, I collapse to…" (argmax leverage under constraints)
do(action) ; advance ; repeat                       # → next
```

A description **only competes** if `obey?` can evaluate it — which requires an imperative (something to obey) plus a checkable condition (an `if` to test against the live situation). Descriptions = candidate chains, `obey?` = prediction, `collapse` = selection under time/resource constraints.

## The failure mode (what you are fixing)

Review a history, find a spot where a skill/rule **should** have fired and didn't, and ask "why didn't it fire here?" The answer is almost never "the skill is wrong." It is:

> **the trigger is N sentences that are not about a trigger.**

The description drifted into the **indicative** (N sentences *describing* the skill — "this skill is for handling X, it provides Y, it covers Z"). So when the reader tried `obey?(d, now)` there was **nothing to obey** — no imperative, no `if`-clause to check the current situation against. Therefore `d` never entered `live_set`. **It didn't lose the `collapse` — it never became a candidate.** A claim-about-a-skill is not a command, and a command is the only thing `obey?` can evaluate.

Length is the *tell*, not the cause: register slid to descriptive, and prose bloat is what descriptive drift looks like.

## Fix procedure — run this on any description

1. **Read it as a command.** Ask: *"could I obey or not-obey this RIGHT NOW?"* If you can't answer yes/no → it's dead → rewrite.
2. **Check the mood.** Indicative ("this handles X" / "provides Y" / "is for Z") = **dead**. Imperative-with-a-conditional ("do X when Y") = **live**. If indicative, convert to imperative.
3. **Compress to ONE imperative + its firing `if`.** Cut every clause that *describes* rather than *commands*. Keep the WHAT (the verb) and the WHEN (the condition); delete the rest.
4. **Keep it short enough that `obey?` returns a clean yes/no** against the live situation. If the reader has to parse 10 sentences to decide whether it fires, it won't fire.
5. **Write the rewrite into the skill/rule file** — the history review that found the miss is what edits the skill; an
   AIOS skill or rule, where the installation binds THE AIOS RELEASES (`user_info`), is rewritten in a new release by
   that binding's procedure.

## The two tests (fast)

- **`obey?` test:** read the description as an order — can I obey-or-not-obey it right now? (yes = live)
- **Mood test:** is it indicative or imperative? (imperative+conditional = live; indicative = dead, rewrite)

## Anti-examples → fixes

| DEAD (indicative, won't fire) | LIVE (imperative + `if`) |
|---|---|
| "This skill handles PDF processing and extraction." | "Extract or read a PDF when the user gives you a `.pdf` or asks to pull text/tables/pages out of one." |
| "A comprehensive framework for reviewing code across many dimensions with confidence-based filtering…" (10 sentences) | "Review the current diff for bugs when the user asks for a code review or before committing nontrivial changes." |
| "Knowledge about the onion architecture and how morphs work." | "Read this when a write is blocked, when you need a specialization, or when deciding whether something is yours or a contact's." |

---

## RULES — same law, plus a split

### The rule-specific law

**A rule should DIRECT you to information, not CONTAIN it.** A very long rule that *tells you to DO something* (a multi-step procedure, 10–30+ lines) instead of *directing you to where that lives* carries a **body (payload) in the always-loaded tier**, where only a **trigger (pointer)** belongs.

### The tell

A long rule almost always has **ONE sentence that is the actual rule** (the trigger — e.g. *"do not work here without reading the docs in this order…"*), and the other 10–30 lines are a **body**. That body is *a thing to progressively disclose* — the rule is a rule AND a skill, fused: `bloated_rule = rule ⊕ skill`.

### The fix — SPLIT

```
bloated_rule  →  (thin_rule  +  skill)
```

- **`thin_rule`** = one imperative + its WHEN, that **names/points at the skill**. It obeys the skill-description law (`obey?`-able, imperative mood).
  - *"do not work here without reading the docs in this order: [30 lines]"* → **"when working here, always read xyz before starting to work on abc files."**
  - *"[30 lines of commit rules]"* → **"always use the `commit-format` skill before committing, since it is non-standard."**
- **`skill`** = holds the procedure/information/format the rule used to carry.
  - `commit-format`, desc: **"WHAT: commit format WHEN: if did work in {repo}."**

### The test — run on any rule

Ask: **does this rule CONTAIN information/a procedure, or DIRECT me to it?**
- **Directs** (thin trigger + pointer) → correct rule; leave it.
- **Contains** (carries a disclosable body) → extract the body into a skill, thin the rule down to a one-line pointer that names the skill.

### THE deciding test — is the WHEN universal (→ rule) or conditional (→ skill)?

The real classifier is the **quantifier of the WHEN**, within the scope where the rule injects:

- **Universal WHEN** — *"ALL THE TIME, unconditionally, in scope S"* (no inner `if`). → it is a **RULE**, kept resident at tier(S).
  - **Tell:** an unconditional stance — *"all the time when working in this dir, X"* — with **NO inner "...and if X..." gate.**
- **Conditional WHEN** — *"all the time here, be aware that sometimes X, **and if X**, do Y."* → it is a **SKILL**, pointed at by a thin trigger whose firing-`if` = X.
  - **Tell:** an inner conditional — *"...sometimes X, and if X..."* / *"when Y then..."* The `if X` **is** the trigger; the body only matters when X holds → disclose-on-demand.

**Scope sets the tier; promote the truly-universal:**
- Universal in ONE dir → that dir's `.claude/rules/` (injected on entry, resident there).
- Universal EVERYWHERE → **the AIOS's rules, user-level, always injected** — where the installation binds THE AIOS
  RELEASES, written in a new release (its `rules/` and its boot config's include line), else `~/.claude/rules/`.

Maps / diagrams / indexes and safety laws are the case where the effective WHEN is *"at any/every moment"* (a lookup or a guardrail has no single condition that precedes its need) = **universal** → rule.

### The deeper cut — a bloated rule is INSTRUCTION + HOW-TO + HISTORY

A rule written as title + story + law + why + trigger + examples is three things fused. Cut it:

- **INSTRUCTION** — the imperative(s) + the WHEN. What you must OBEY. → stays in the rule, rewritten complete in itself.
- **HOW-TO** — a procedure that satisfies the instruction (commands, gotchas, a recipe). → moves to a skill the rule names. The obey-able constraint (*"a backup must exist before risky ops"*) stays in the rule; the recipe that satisfies it is disclosed on demand.
- **HISTORY** — the failure that forced the rule, war-stories, the why, supersessions, dates, quotes of the user, provenance. → **DELETED.** Git holds the history; nothing in the injected layer carries it, and no skill receives it.
- **TABLE** — a real state/lookup table → stays with the rule it serves.

**Discriminator:** remove a passage — if what you must DO changes, it is instruction (keep, rewritten); if it is a procedure you run when the instruction fires, it is how-to (move); if only the story of how the rule came to be is lost, it is history (delete).

**Min-split threshold:** if under ~8 lines of how-to would move, do NOT split — rewrite the rule whole instead. Splitting must not manufacture a skill where there is barely a procedure.

### After splitting — VERIFY the cut (hunt INSTRUCTION-IN-SKILL)

Run an independent verify after every split:

1. **Preservation:** every instruction in the original is in the new rule or the skill — none dropped with the history.
2. **INSTRUCTION-IN-SKILL hunt (the load-bearing check):** grep every skill the split produced for law markers — `MUST | NEVER | ALWAYS | DO NOT | forbidden | standing law | only … is` — and for each, check whether that constraint is ALSO in its rule. **Lives ONLY in the skill → it moved wrongly → put it back in the rule.** The classic trap: a law written as a quoted blockquote or buried inside a story gets carried off with the story.
   - **Caveat — do NOT promote a procedure detail reachable via a resident trigger.** A `MUST` inside a dev-flow ("MUST update the docs when editing X") fires when the editing-X trigger points at the dev flow. Distinguish: **universal law moved → promote** vs **procedure detail reachable via trigger → leave.**
3. **No dangling pointer:** every rule pointer resolves to an existing skill; a rule that was rewritten whole carries no pointer.

### The ceiling — a mechanically-enforceable rule becomes a HOOK, not a rule

Before writing the thin rule, ask: **is a violation programmatically detectable at a tool-call boundary?** If yes, the ceiling isn't a rule OR a skill — it's a **HOOK/script that enforces it** (scaffold-to-harness: rules are passive, scripts are active). E.g. `subagent-worktree-isolation` shouldn't ride on the agent remembering it — a `PreToolUse` hook matching the `Agent` tool can require/inject the worktree setup. The rule is the fallback until the hook exists; **a rule you could harness-enforce is a rule you are currently enforcing by hope.**

**LOOK before you build — don't reinvent what the harness already provides.** Claude Code already ships the mechanism for many such rules: the `Agent` tool has a native `isolation: "worktree"` param, plus dedicated hook events `SubagentStart`/`SubagentStop` (matcher on agent type), `WorktreeCreate`/`WorktreeRemove`, and `InstructionsLoaded`. The enforcement is then a THIN guard on existing surface, never from-scratch machinery. Read the `understand-hooks` skill (29 events, 5 handler types) and check the native tool params FIRST — assuming a capability is absent without looking is the error.

### The sharpest cut — an internal-impulse trigger CANNOT be a skill

A conditional WHEN only makes a valid skill if the condition is **observable** — something you DO (edit file Z, dispatch a repo-writing subagent, restart the daemon). If the thing that should fire the rule is an **internal impulse** — *the pull to ask before verifying, the urge to describe a status, the assumption you make before you catch it* — it CANNOT be a disclose-on-demand skill, because **nothing reliably fires it: the impulse is exactly what you won't notice in time.** Such guardrails stay **RESIDENT**.

Rule of thumb: skill-able triggers are **observable actions you take**; impulse guardrails catch **things you're about to get wrong without noticing** → resident.

### The exception — resident references and safety laws do NOT split

Split a rule ONLY IF its body is a **procedure that a specific moment triggers** (disclose-on-demand). **KEEP IT RESIDENT** when it is:

- **A reference with an IRREDUCIBLE body, consulted unpredictably** — a diagram, a topology, a coordinate map, the `*_states.md` boards: something whose content cannot be restated as a law that answers the lookup.
- **A safety / always-on law whose cost-of-not-firing is high** — e.g. `the-precious-store`. If the trigger might miss the moment and the failure is catastrophic, the law stays resident.

**Run this test BEFORE the exception: can the reference be COMPRESSED TO THE LAW IT ENCODES?** Then the law is the rule, and the data is not. A per-project catalog that encodes one mechanical sentence (*every project is a plain dir at `<canonical home>/<band>/<x>`*) compresses to that sentence. A ledger carries no TRIGGER/DO/NOT and changes no behavior — it is STATE, and its home is the state layer ([[28-distributed-state]]). **A CATALOG or LEDGER never qualifies for the exception**: a wrongly-resident catalog taxes every session in every project.

**The deciding test:** *is there a single reliable WHEN that precedes every need for this body?*
- **Yes** → split (that WHEN is the trigger; e.g. `editing-X-uses-the-dev-flow`).
- **No** — consulted unpredictably, OR a miss is catastrophic → **keep resident**.

### Tier matters — user-tier is always-loaded, project-tier is entry-loaded

- **User-level rules (the AIOS's, which `~/.claude` reaches) are loaded EVERY session** — compression pays the most here, AND wrong compression hurts the most here (a wrongly-thinned always-loaded map/safety-law is missing every session).
- **Project/module rules load only on entry to that dir** — compressing them is cheaper and lower-risk. Review user-tier splits hardest.

### Why (the tiers)

- **Rule = the always-loaded (or entry-loaded) trigger/pointer** — cheap, always present, fires and *directs*.
- **Skill = the progressively-disclosed body** — loaded only when the pointer fires.
- Putting the body in the rule = paying the full always-loaded cost for payload that should disclose on demand. Move the body to the skill; keep the rule a pointer.

### One law, both artifacts

Skill descriptions and rule triggers obey the **identical** `obey?`/mood law (imperative + firing `if`, one sentence). The *only* rule-specific addition is the **split**: a rule must not also be a body — if it is, that body is a skill, so extract it and leave the rule pointing. Neither artifact ever carries history.
