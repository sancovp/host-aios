# One canonical DESIGN.md per project — DESIGN.md ONLY, every other document wired under it, each opening with its READ ORDER

<docsys kind="design" role="law"/>

TRIGGER:[creating or naming any design/spec doc (⇒ it is DESIGN.md or it is a detail doc with a pointer) · creating ANY document — a detail design, a pattern, a reference, a note's record (⇒ its line in its parent design, the same commit) · any architectural change (⇒ DESIGN.md in the SAME commit) · a child `DESIGN.md` added, renamed or removed (⇒ the parent's READ ORDER rewritten, the same commit) · finding a doc that contradicts DESIGN.md · a feature not yet built (⇒ mark it ASPIRATIONAL) · about to delete a design doc (⇒ roll IN, leave a pointer; deletion is *USER*'s per-file call) · about to write a ruling into a note, or into a document nothing loads where the ruling fires]
CANONICAL DOCS (the only three in the entire tree):[
1. each top AIOS's TOP-LEVEL DESIGN — the cover over every `DESIGN.md` beneath that top, outside its home-unknown band; THE MASTER MAP names every top ([[00-canonical-doc-paths]])
2. the `DESIGN.md` of each PROJECT — **a project is ONE ENTITY: its own abstraction, running on its own context; a different abstraction is a different project, with or without code of its own** (a codebase is one kind of entity; the network that sells products, the deployment that runs them for customers, a book, are projects exactly as a codebase is; a concern spanning several codebases is its own project, never a section of each codebase's design) — **ONE per project, never one per dir** (agent-rts has ONE; `render/`, `feeders/`, `examples/` do NOT get their own — a subdir's design is a SECTION of its project's DESIGN.md). A project NESTED inside another (exoblend inside agent-rts) is its own project and keeps its own; a sub-PACKAGE (the wow pack inside cave-teams) is not — it rolls up.
3. each top's TOP-LEVEL STATES DOC — that top's OUTSTANDING ledger ([[28-distributed-state]])
]
EVERY DOCUMENT IS A DESIGN DOCUMENT, WIRED UPWARD:[the project's one `DESIGN.md` is the root of its designs · every other document — a detail design, a pattern, a reference, a note's record — sits under a parent design that carries its one-line summary and its link, summarized again at each level up to the top-level design ([[every-level-describes-and-breadcrumbs-below]]) · a document nothing reaches does not bind, so a ruling goes into the document that loads at its trigger, never into a note · a program checks it: the `top-level-design` skill's `check_reachable.py`, run from a top-level design or a `DESIGN.md`, lists every tracked `.md` file nothing reaches]
EVERY DESIGN.md OPENS WITH ITS READ ORDER:[under the heading `READ ORDER`, first: what this level is, and for which work which child design and which procedure (dev flow, skill) to read · its last line `ARCHIVE AND PROGRAM FOLDERS:` naming the folders whose files are evidence, generated output or a program's source — run evidence, records, goals and their proofs, forks, a generated package, a template — which the two checks skip, `none` when there are none · it names every child `DESIGN.md` beneath it outside those folders · it is rewritten in the same commit as any child design added, renamed or removed · a program checks it: the `design-toc` skill's `design_toc.py <project> --check`]
DO:[
- OPEN THE `design-md` SKILL FIRST — the Skill tool, by its name, before the first write of a DESIGN.md — and author or repair the DESIGN.md through it — the skill is the HOW, this rule the WHAT; open the `design-toc` skill the same way at every edit of a `DESIGN.md`
- name every canonical DESIGN document `DESIGN.md` (nothing else)
- roll a `XYZ.md` design/spec doc's content INTO the DESIGN.md of the project it sits in, then leave the source as a pointer
- give every new document its one-line summary and link in its parent design — the section that owns its topic, or the folder's `CLAUDE.md` — in the same commit that makes it
- treat DESIGN.md as the single source of structural truth (a decision not in it does not exist, or is `ASPIRATIONAL:`)
- update DESIGN.md in the SAME commit as any architectural change, its READ ORDER with it, and append what changed, the reading it replaced and why to the `CHANGELOG.md` beside it — DESIGN.md itself states only the current design
- mark not-yet-built features `ASPIRATIONAL:` (a commitment, not a lie)
- make other docs excerpt/link/point to DESIGN.md
- banner a reference-detail doc "REFERENCE DETAIL — READ when its topic is the active task; NOT deprecated, NOT skippable" · keep it fully in the doc tree (read, drilled as a breadcrumb, the DETAIL layer under DESIGN.md's rows)
- before a version leaves, run the reachability check from the design and the read-order check on the project, bare, and act on what they say ([[00-docsys]] THE PATTERNS UP FRONT)
]
NOT:[
- name a canonical DESIGN doc anything but DESIGN.md
- let another doc contradict DESIGN.md
- leave a document no parent design or folder index links, or write a ruling where nothing loads it at its trigger
- leave a `DESIGN.md` without its READ ORDER, or a child `DESIGN.md` its READ ORDER does not name
- delete anything under this law (roll IN, leave a pointer; deletion is *USER*'s explicit per-file call)
- treat `.claude/rules/*` or a `CLAUDE.md` as a design doc under this law (they are LOADING MECHANISMS, never renamed or rolled into a DESIGN.md — a folder's `CLAUDE.md` still carries its one line for each file and folder in it)
- banner a doc bare "NON-CANONICAL" (reads as "skip this", teaches skipping load-bearing detail)
]
