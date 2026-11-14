# EVERY directory has a CLAUDE.md + .claude — and projects NEST, never sprawl

<docsys kind="scaffold" role="law"/>

SCOPE:[binds the developer agent's own world — THE WORLD DIR, its repositories and its sessions — never a product's agents (a JobWorld seat or box, OM) or a customer's repositories, which follow their own product's design]

## LAW 1 — ONE project dir per project; sub-parts NEST inside it; never siblings in THE WORLD DIR

PRINCIPLE:[a PROJECT is ONE ENTITY — its own abstraction, its own context — and it ENDS AS exactly one of three
things: a PROGRAM (a vendored package or a library) · an APPLICATION (deployed in the SaaS network) · a PLUGIN (a
repo carrying a proper Claude plugin, public or private); nothing else is ever being made · **each declares its
INSTALL SHAPE**, one or more of: skills · an agent file · tool servers and hooks · an AIOS (shipped as its plugin's
install skill, LAW 2) · an agent as its own app · a World · a desktop app with a daemon · a hosted app · a package
· **each is made CONFIGURABLE first** — it hardcodes nothing about the user or the agent, never naming a person as the user and
naming no machine and no local setting, and everything particular to one use comes from a configuration filled out
to specialize it; our own instance is that thing filled out for us — used directly, equipped on the agent, or made
part of it — so it can always be published, and whether it is published is the user's decision · **THE WORLD DIR** ([[canonical-source-dirs]] LAW 1, bound per installation) holds the AIOS's own folder, and
**THE WORKSPACE** inside it ([[user_info]] binds it) holds PROJECTS ONLY, one dir per project — everything the AI does
happens in one of them, under the AIOS's context · it is hierarchical: a project's internal parts (levels, sub-systems)
live INSIDE that project's dir, what using it produces in that project's own `workspace/`, and so on down]

SHAPE (the structure is the law; the names are placeholders):
```
<THE WORKSPACE>/<Project>/     ← THE project. one dir, in the AIOS's workspace.
├── CLAUDE.md                  ← what <Project> IS
├── .claude/{rules,skills,agents}
├── <level-1>/                 ← a part of it (+ its own CLAUDE.md + .claude)
│   ├── CLAUDE.md
│   └── .claude/{rules,skills,agents}
├── <level-2>/
│   ├── CLAUDE.md
│   └── .claude/{rules,skills,agents}
└── <level-3>/
    ├── CLAUDE.md
    └── .claude/{rules,skills,agents}
```

DO:[nest levels / sub-systems / variants inside the project dir · STOP on catching a `mkdir` of a sibling —
nest it in its project · read every path, name and setting in a made thing from configuration, never from the machine
it is written on · keep everything particular to us in our filled-out configuration of it, never in the thing itself]
NOT:[write a person's name as the user ("<name> wants …"), a machine's name or a home-folder path into anything made
— authorship credit (an author field, a byline) is the one place a person's name belongs · shape a made thing to the
machine or the installation that uses it · create a sibling dir in THE WORKSPACE unless it is a NEW, DISTINCT project — **a project is ONE ENTITY: its
own abstraction, running on its own context; a different abstraction is a different project, with or without code
of its own (the deployment that runs several codebases for customers is its own project, never a section of each
codebase's design)** — one project's levels sitting as siblings at THE WORKSPACE's top, each looking like its own
project because it has its own name, is the sprawl this forbids; a distinct entity folded into another's dir
because it has no code of its own is the opposite failure, and this forbids it too]

## LAW 2 — EVERY directory, anywhere, has a CLAUDE.md + a .claude/

REQUIRED in every dir created or touched:
```
<dir>/CLAUDE.md         ← REQUIRED: what this dir is FOR (1+ line, plain, never empty)
<dir>/.claude/rules/    ← REQUIRED (may be EMPTY)
<dir>/.claude/skills/   ← REQUIRED (may be EMPTY)
<dir>/.claude/agents/   ← REQUIRED (may be EMPTY)
```

A project's `CLAUDE.md` also names the starting skillchain its work begins from — the skill a work session calls first
([[00-top-level-design-first]] 0b) — and, for a project with child projects, the `how-to-lead-an-aios` skill as the
starting skillchain of its children's work — or says it has none yet, in which case its first piece of work is made by hand and
then abstracted (the `how-to-make-the-abstraction` skill).

THE TWO EXCEPTIONS:[
- A PLUGIN'S ROOT — a plugin install loads no `CLAUDE.md` at the plugin's root, so the root of a folder that is a
  plugin carries none · when the plugin delivers an AIOS, the AIOS's `CLAUDE.md` is a resource of the plugin's
  INSTALL SKILL, whose script makes a new folder — named by whoever installs it — that holds that `CLAUDE.md` and
  gets the rules and skills the AIOS needs injected into it; the folder it makes carries the full scaffold, and it is
  the installer's own instance, filled out by their configuration
- WHAT A PROGRAM GENERATES — a dir a program writes as its output (a skill dir, whose `SKILL.md` says what it is · a
  tree SkillTree materializes · build output) carries what its generator writes and no scaffold of its own: a
  `CLAUDE.md` at a tree node seats a lord there, and one inside a plugin's skill never loads · the dir that HOLDS the
  output carries the scaffold
]

DO:[create the scaffold every time (even if `.claude/*` are empty; the CLAUDE.md is never empty) · apply to
every dir in THE WORLD DIR and every dir made anywhere · fix a dir missing its CLAUDE.md / .claude the instant
it is noticed, before anything else]
NOT:[make a directory without a CLAUDE.md explaining it — a plugin's root and a program's generated output excepted
· put a `CLAUDE.md` at a plugin's root (it ships inside the install skill instead) · hand-write a scaffold into a
generated dir (the next generation deletes it, or it seats a lord nobody warranted)]
COMPOSES:[[[20-progressive-disclosure]] (the 3 tiers) · [[28-distributed-state]] (state lives where the work
is) — this rule makes the SCAFFOLD mandatory in EVERY dir]

TRIGGER:[any `mkdir` · any new directory · any dir noticed without a CLAUDE.md + .claude/ (⇒ create them that
instant) · any urge to make a sibling at the top of THE WORKSPACE (⇒ STOP, nest it in its project)]
