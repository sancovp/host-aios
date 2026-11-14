---
name: how-to-make-the-abstraction
description: WHEN a second thing of a kind is about to be made, or a fix is about to be made by hand again — before it starts, abstract the kind into the project's own system (its compiler, its library, its generator), rebuild the first piece through it as the proof, and make the second piece through it; then lift it to a command once it is mechanical and needed across sessions, and trust it once it has an acceptance test and a test that must fail. Each fix lands in the abstraction once, so each piece costs less than the last. And when a pattern lacks the abstraction that would close it, say so first and close it before inferring anything else about it.
---

# how-to-make-the-abstraction — a kind made once by hand, then every piece made through it

You are about to make a second thing of a kind — a second asset, a second page, a second script doing what a first one
did, a second table of the same shape — or to make a fix by hand that has been made before. This skill says what to do
before you start it. A piece made by hand twice is a failure whose class is the missing abstraction, and the
abstraction is its guard.

## 0 — NAME THE MISSING ABSTRACTION FIRST

When a pattern lacks the abstraction that would close it, say that first and plainly — what is missing, and what it
would close — before anything else is inferred about the pattern. Close it; then read what is left again, since closing
it may settle it. A question asked, or a conclusion drawn, about a pattern whose abstraction is missing is secondary
until the abstraction exists.

## 1 — THE LADDER: each rung is a life stage of one kind

1. **FREEFORM** — the first piece of a kind is made by hand, freely, to learn what the kind is. Once.
2. **THE ABSTRACTION** — before the second piece begins, the kind goes into the project's own system — its compiler, its
   library, its generator — as a named part with its parameters. The first piece is rebuilt through it, and the rebuild
   matching the first is the proof the abstraction holds. The second piece is made through it.
3. **A COMMAND** — once the abstraction is mechanical (no taste in it), shaped by a few parameters, and needed across
   sessions or by a loop or a gate, it becomes a command an agent calls instead of code it writes again: one call, named
   where the next session finds it — the project's tool list, its skill.
4. **TRUSTED** — once it has an acceptance test and a test that must fail (a case it refuses), other pipelines may
   depend on it.

## 2 — CHANGE THE WORK AT THE HIGHEST LEVEL

- Change a piece by editing the highest-level code about its world — the description the compiler compiles, the
  parameters the library takes — never by typing low-level values into its output by hand.
- What attaches to a thing attaches to a named part of it, and its position is computed from that part — never a
  coordinate, an offset or an index typed in.
- A fix lands in the abstraction, once, so every piece made through it carries it, and it is never made by hand again.

## 3 — THE COST FALLS, AND A COST THAT DOES NOT NAMES WHAT IS MISSING

- A piece's cost is its tokens, read from its session's transcript; each kind keeps a target cost, written where the
  project's design states the kind.
- Each piece of a kind costs less than the last, because every fix is already in the abstraction.
- A piece that costs more than its kind's target names a missing abstraction: name it, build it into the system, and
  only then start the next piece.

## 4 — THE PROJECT'S OWN CHECK

The project's compiler, library or generator refuses what its abstraction covers when it is typed by hand — a value it
computes, written in literally. That refusal is the project's check that the abstraction is used; build it with the
abstraction, and write into the project's `DESIGN.md`, in the section that states the kind, what the abstraction covers
and what its check refuses.

## 5 — THE LAWS OF PROMOTION

- Never promote taste: an abstraction holds deterministic mechanics, and judgment — does it look right, does it read
  well — stays with whoever judges. A threshold someone might tune is a parameter, never a constant.
- One implementation, two surfaces: a command wraps the library's function and never forks it.
- Every command ships with its blind spot: what a pass does not certify.
- Record the promotion where the project's knowledge lives — the design section that states the kind, and the skill
  that says how to use it — the same turn.

## 6 — NEVER

- a second piece of a kind made by hand
- the same fix made by hand twice
- a command made before its abstraction is needed across sessions, because it might be useful
- an abstraction whose parameters encode taste
- a low-level value typed into an output the abstraction computes
- an inference made about a pattern, or a question asked about it, before its missing abstraction is named

## NEXT

- the abstraction is made and the first piece rebuilt through it → make the second piece through it, and read its cost
  from its transcript
- a project carries its own instance of this skill (its compiler's promotion skill) → open that one for the project's
  own surfaces; it names this skill as its class and keeps only what is its own
- using the abstraction is a procedure that runs whole every time → write its dev flow, `22-seq-<kind>.md`, placed on
  the project's architecture map
