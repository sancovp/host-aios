# 00 — THE WORK LOOP (how a conversation is spent, and what the system accumulates)

<docsys kind="shape" role="law"/>

SCOPE:[binds the developer agent's own world — THE WORLD DIR, its repositories and its sessions — never a product's agents (a JobWorld seat or box, OM) or a customer's repositories, which follow their own product's design]

PRECEDENCE:[this is the SHAPE every other process rule fits inside · it composes
[[00-top-level-design-first]] (the read) · [[26-canonical-design]] (DESIGN.md) · [[28-distributed-state]]
(`_states.md`) · [[29-state-indexes-design]] (spine + pointers) · [[22-activity-flow]] (the dev flows) ·
[[23-architecture-layer]] (the architecture map) · the `setup-goal` skill (the goal)]

AUTHORITY:[the GOAL is the most specific current instruction · RULES are the way instructions change ·
the SYSTEM PROMPT changes as the architecture changes · SESSION HOOKS change when they no longer reflect
the way everything else works · where the goal speaks, it wins]

## THE TWO CONVERSATION KINDS — never collapse them

A conversation is ONE of these. Doing both in one window is the waste this rule exists to end. Both are development —
the mode that changes a project; a work session, which uses one, starts from the project's starting skillchain instead
([[00-top-level-design-first]] 0b).

**(A) THE SCOPING CONVERSATION — reads canon, produces a GOAL. Writes docs, never features.**
```
0. IS THE PROJECT CONFIGURABLE YET? Every project ends as exactly one of three things — a PROGRAM (a
   vendored package or a library) · an APPLICATION (deployed in the SaaS network) · a PLUGIN (a repo carrying a
   proper Claude plugin, public or private) — and nothing else is ever being made. Configurable = it hardcodes
   nothing about *USER* or the agent (no person named as the user, no machine, no local setting; authorship
   credit may name the author), and everything particular to one use comes from a configuration filled out to
   specialize it; our own instance is that thing filled out for us — used directly, equipped on the agent, or made
   part of it. So it is always able to be published, and whether it is published is *USER*'s decision. Name which
   one this project ends as, its install shape ([[00-every-dir-has-a-claude-and-projects-nest]] LAW 1), and whether
   it is configurable. Not yet ⇒ making it configurable IS the work, before
   anything else; yes ⇒ the work happens on the configurable thing, and our particulars go only into our
   filled-out configuration.
1. READ THE SCOPE'S CANON ([[00-top-level-design-first]]): the project's CLAUDE.md + DESIGN.md (via its TOC)
   + board · wired into the system ⇒ + THE TOP-LEVEL DESIGN top to bottom (the explained table of contents),
   then only the links the work needs.
2. TALK → contextualize the subsystem THROUGH that canon → drill its BREADCRUMBS to the leaves.
3. AN IDEA LANDS → rewrite, in three places, same turn:
     a. the DESIGN.md that OWNS it          → the design itself, rewritten to state it as part of the final state,
                                               in the step or version that brings it
     b. THE TOP-LEVEL STATES DOC            → the row, marked OUTSTANDING
        (a ROLE — [[00-canonical-doc-paths]]; bound per installation, never a filename here)
     c. that subsystem's OWN `_states.md`   → its rows, where it stands — the one place a state is written
4. WRITE THE GOAL — its READ LIST names the dev flows (`22-seq-*`) the work follows.
```

**(B) THE GOAL'S RUN — reads ONLY what the goal names, and does the work.**
```
0. THE GOAL NAMES WHICH OF THE THREE THE PROJECT ENDS AS, AND WHERE OUR FILLED-OUT CONFIGURATION OF IT LIVES — a
   goal without that line was written against a thing that hardcodes its user, and goes back to (A).
1. READ EXACTLY THE GOAL'S READ LIST — at start and after every compaction. Nothing more, nothing less.
2. DO THE WORK BY READING AND FOLLOWING THE DEV FLOWS it touches.
3. MOVE THE STATES FILE AS YOU GO (same commit as the work).
4. NEW ARCHITECTURE → a NEW DEV FLOW, and every new dev flow goes into the ARCHITECTURE MAP.
```

Then repeat. **Isolating what to do next comes from the STATE docs** — work-state lives there.
**The top-level design receives a thing only when it is CANONICALIZED**, and canonical things flow
top-level design → the DESIGN.md that owns them → that subsystem's per-feature state doc.

## THE READ IS SCOPED BY THE GOAL, AND THE DEV FLOWS CARRY IT

- **A GOAL CARRIES THE NEXT PLANNED RELEASE VERSION, WHOLE.** The design stages the work as planned release versions;
  a goal's table holds every deliverable of the next one not marked HELD, and the version ships once, whole, judged
  complete by the session that builds it. A version that leaves a part out still closes every loop that crossed that
  part, by a bridge that is one of its deliverables ([[a-version-closes-every-loop]]).
- **The goal names the reads** — the most specific, only-the-required version of the context: the design's READ
  ORDER, its table of contents, the boards and the dev flows at start; each row's own sections and files as that row's
  stage is reached. A goal may scope away the top-level design and the top-level states doc.
- **⛔ NOT "the top-level design all the way down + the top-level states doc in full, always."** That is the
  SCOPING conversation's read, and paying it in a goal's run burns the window before the work starts.
- **THE DEV FLOWS ACCUMULATE.** A feature's dev flow (`22-seq-<feature>.md`) states the feature's procedure AND
  names which documents to read, in which order — so a goal points at the feature's dev flow instead of
  re-deriving a read list, and the read cost falls as the system grows.

## THE ARCHITECTURE ACCUMULATES AS FOUR ARTIFACTS

| # | artifact | what it holds | governed by |
|---|---|---|---|
| 1 | **THE TREE** | every DIRECTORY (= every module) with an explanation of what it is FOR; external deps end at their SEAM, never expanded | this file's TREE LAW below |
| 2 | **THE ARCHITECTURE MAP** | the stack / architecture-layer diagrams (mermaid `flowchart`, subgraphs = boundaries, arrows = dependency direction) — and every dev flow, placed on it | [[23-architecture-layer]] |
| 3 | **THE DEV FLOWS** | one per FEATURE (`22-seq-<feature>.md`) — the procedure AND its read order | [[22-activity-flow]] |
| 4 | **THE STATES** | each project's two boards; a parent's table of its children, OUTSTANDING or CLEAR | [[28-distributed-state]] · [[29-state-indexes-design]] |

**THE TREE LAW:** the unit is the **DIRECTORY**, never the file. Every dir gets one line saying what it is
FOR. **A dir with no explanation is UNREAD, and unread means its lane is NOT editable.** Never write an
explanation from a directory's NAME — read the module. **EXTERNAL DEPS ARE NOT OUR ARCHITECTURE**: the map
says WHERE the dep plugs in and stops (a dep's internals are its own architecture; expanding them makes the
system look many times its real size).

TRIGGER:[any conversation start (decide: scoping or a goal's run?) · an idea landing in conversation (⇒ DESIGN.md +
OUTSTANDING row + `_states.md`, same turn) · writing any goal (⇒ it carries the next planned release version whole; its read list names its dev flows) · about to read the top-level design inside a goal's run (⇒ stop; read only what
the goal names) · new architecture (⇒ a new dev flow, placed on the architecture map) · about to edit code
(⇒ the tree must explain every dir involved, and the feature's execution boundary must be read line-by-line
first)]

## NOT

[collapse scoping and a goal's run into one window · pay the full canon read in a goal's run · write a goal
whose read list is "everything" · re-derive a read list a dev flow already carries · build new architecture
without its dev flow · leave a dev flow off the architecture map · put a map or any knowledge outside
`.claude/rules/` · expand an external dep's internals into our architecture · explain a directory from its
name instead of reading it]

## WHERE THE ARTIFACTS LIVE — EACH KIND IS ITS OWN RULE

**Only `.claude/rules/` auto-injects — anything that must be KNOWN goes there, and `.claude/` is not a
backpack** (no other subdir of it carries information). Dev flows are their own rules; the architecture map
and the tree are their own rules. Never one omnibus doc — the kinds separate:

| artifact | rule file |
|---|---|
| the TREE (every dir + what it is FOR) | `<repo>/.claude/rules/20-dir-tree.md` |
| the ARCHITECTURE MAP (the stack, with every dev flow on it) | `<repo>/.claude/rules/21-architecture-diagrams.md` |
| the DEV FLOWS — **ONE RULE PER FEATURE**, each with its read order | `<repo>/.claude/rules/22-seq-<feature>.md` (indexed by `22-seq-diagrams-index.md`) |
| the STATES | each project's two boards, `<project>_dev_states.md` and `<project>_work_states.md` · a parent's table of its child projects, each OUTSTANDING or CLEAR — at a top, THE TOP-LEVEL STATES DOC ([[28-distributed-state]]) |

**THE HISTORY IS NOT A RULE AND IS NEVER INJECTED:** what changed, what it replaced and why is appended to
`<project>/CHANGELOG.md`, at the project root beside `DESIGN.md` — read when the history is the question,
never as boot context, never edited after an entry is written.

Only these three are CANONICAL (who wins on conflict): **THE TOP-LEVEL DESIGN** · each dir's `DESIGN.md` ·
**THE TOP-LEVEL STATES DOC** — the first and third are ROLES bound per installation
([[00-canonical-doc-paths]]). Goals live at `<primary-repo>/.claude/goals/<goal-name>.md`.
