# USER INFO — the ONE binding site: who *USER* is, and the facts the ruleset reads instead of asserting

PRINCIPLE:[every other file in this AIOS spends the token *USER* and names no one · this file is
the only place a person is named, and the only file an installation must edit · a rule that ASSERTS
a fact about the user is a rule that will be false for the next user — the fact belongs here and the
rule READS it]

## THE BINDING

```
THE USER IS NAMED {NAME}
```

**`{NAME}` = —** *(unbound: write the user's name here)*. ⇐ **THIS LINE IS THE INSTALL.** Editing it is the whole of binding this AIOS
to its user; there is no config format, no substitution pass, and no second copy. *USER* resolves
because the agent READS this file, and reading IS the call.

## THE BINDINGS — the other roles an installation binds, same file, same mechanism

The ruleset states ROLES; this is where each one gets its instance. An empty row is NOT a default —
a rule whose binding is absent reports the absence and does not fire.

| role | this installation's binding |
|---|---|
| **THE WORLD DIR** ([[canonical-source-dirs]] LAW 1) — the one directory all work happens under | — unbound — |
| **THE WORKSPACE** ([[00-every-dir-has-a-claude-and-projects-nest]] LAW 1) — the folder inside the AIOS's own folder that holds every project the AI works in, one folder each: everything the AI does happens in one of them, under the AIOS's context | — unbound — |
| **THE CANONICAL HOME** (LAW 0) — the ONE repository holding everything, at one remote | — unbound — |
| **THE TOP-LEVEL DESIGN** ([[00-top-level-design-first]]) — the cover over every `DESIGN.md` beneath a top AIOS, outside its home-unknown band: THE MASTER MAP, the global rule naming every top, names it first, and this role and THE TOP-LEVEL STATES DOC are the map's entry for the top that holds the work; where no map loads, this binding is the installation's one top ([[00-canonical-doc-paths]]) | — unbound — |
| **THE TOP-LEVEL STATES DOC** — that top's table of its projects, each OUTSTANDING or CLEAR, linking down to its boards ([[00-canonical-doc-paths]]) | — unbound — |
| **THE PROJECT REGISTRY** ([[00-rules-are-live-state]]) — where every dir added to the world dir is registered | — unbound — |
| **OUT OF BOUNDS** — beyond the general form the rule states | — unbound — |
| **READABLE OUTSIDE THE WORLD DIR** ([[canonical-source-dirs]] LAW 1) — folders outside the world dir that are read whenever the work needs them and never written; a secret read there is never printed | — unbound — |
| **THE PRECIOUS STORE** ([[the-precious-store]]) — never rebuilt, never restarted without a go | — unbound — |
| **THE HOST SCRATCHPAD** — the top scratchpad: its instructions and the refs to every project scratchpad with open work | — unbound — |
| **THE RULE-DRAFT BOX** — where a proposed NEW rule waits while its question is open | — unbound — |
| **THE SUBAGENT MODEL** ([[the-subagent-model]]) — the model an agent dispatched to test, try out, play with, review or look at something runs on, the model it falls back to when that one refuses, the model a judge falls back to, and any model never dispatched | — unbound — |
| ⛔ **THE CARVE-OUTS** — projects deliberately outside the canonical home, each its own git; the only RULED exceptions to LAW 0 (every other standalone repo in the world dir is a fold still owed — THE PROJECT REGISTRY lists them) | — unbound — |

⇒ **THIS TABLE IS THE INSTALL CONFIG.** There is no other mechanism, no format to invent, and no
second file: the same read that resolves *USER* resolves every other role, because reading IS the
call. An installation edits THE BINDING above, then this table, and it is bound.

## THE FACTS — what the ruleset may rely on about *USER*

Every row is a fact about THIS user, not a law about users. A rule that needs one CITES this table.

| fact | what depends on it |
|---|---|
| — none stated — | an installation writes one row per fact it relies on about its user, with the rules that read it |

⛔ **AN EMPTY ROW IS NOT A DEFAULT.** An installation that has not stated a fact has not granted it:
a rule whose fact is absent does not fire, and the absence is reported rather than guessed.

TRIGGER:[any rule about to spend the token *USER* · about to assert what the user is like, can do,
or wants (⇒ STOP: cite a row here or the claim is unfounded) · installing this AIOS (⇒ edit THE
BINDING, then this table) · a rule found naming a person (⇒ it belongs here; the rule takes *USER*)]
DO:[read this file before acting on any rule that spends *USER* · cite the ROW, not a memory of it ·
state a fact as absent when its row is empty · keep every person-reference in the whole AIOS in this
file and nowhere else]
NOT:[name a person in any other file · assume a fact whose row is empty · treat these facts as
universal (they are one user's) · copy a row into another rule (cite it — [[29-state-indexes-design]]:
details hang off by pointer, never duplicated)]
