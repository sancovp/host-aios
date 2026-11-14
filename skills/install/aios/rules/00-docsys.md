# 00 — THE DOC SYSTEM (the index of the rules that ARE the system, and where the templates live)

<docsys kind="index" role="index"/>

PRINCIPLE:[the design / states / dev-flow / architecture rules are ONE SYSTEM · every member carries one
greppable tag on its second line: `<docsys kind="…" role="…"/>` · a rule's number and placement belong to the
ruleset's owner, never to its author — except a DEV FLOW's, which the system's own law decides (`28b`: the
`.claude/rules/` of the dir whose procedure it is, named after its feature, drawn on its map), so the agent places it]

## THE TAG

```
<docsys kind="KIND" role="ROLE"/>
  KIND: shape · design · tree · arch-map · dev-flow · states · pointers · scaffold · canon · method · gate · index
  ROLE: law (what must be) · template (copy this) · instance (a real one) · index (lists them)
```

**Membership = the grep:** `grep -rl '<docsys' <the AIOS's rules> <repo>/.claude/rules` — the AIOS's rules being the
release in use's `rules/` where [[user_info]] binds THE AIOS RELEASES, else `~/.claude/rules` — that IS the system,
always current, no list to go stale. A doc-system rule without the tag is a bug; tag it on sight, an AIOS rule in a
new release
([[00-rules-are-live-state]]).

## THE SYSTEM — artifact kind → its LAW → its TEMPLATE → its instances

| artifact | the LAW (global) | THE TEMPLATE | per-project instance |
|---|---|---|---|
| THE SHAPE (how work is spent) | `00-the-work-loop` | — (it is the shape) | — |
| DESIGN.md | `26-canonical-design` | its READ ORDER first, then prose, one section per FEATURE, current truth only; ASPIRATIONAL: marks unbuilt | `<project>/DESIGN.md` |
| THE TREE | `00-the-work-loop` § TREE LAW | root `20-dir-tree.md` IS the worked template | `<repo>/.claude/rules/20-dir-tree.md` |
| THE ARCHITECTURE MAP (the stack diagram) | `23-architecture-layer` | rule 23's worked stack (flowchart TB · subgraph = layer/boundary · arrow = dependency · deps end at their seam · drawn from DESIGN.md, before any code · every dev flow placed on it) | `<project>/.claude/rules/21-architecture-diagrams.md` |
| DEV FLOWS | `22-activity-flow` + `28b` (THE GENERATOR — never invent, specialize) | 28b's worked table + diagram | lifecycle → a states TABLE · procedure → `22-seq-<feature>.md` |
| STATES | `28-distributed-state` + `28b` | the monorepo `states.md` § THE TEMPLATE | `<project>/.claude/rules/<name>_states.md` |
| POINTERS | `29-state-indexes-design` | every row carries a path | — |
| INDEXES | this file | — | `29b-state-index` (states) · THE MASTER MAP (tops) · each top-level design (designs) · each `DESIGN.md`'s READ ORDER (its children) |
| SCAFFOLD | `00-every-dir-has-a-claude-and-projects-nest` · `20-progressive-disclosure` · `every-level-describes-and-breadcrumbs-below` | the CLAUDE.md + `.claude/{rules,skills,agents}` shape | every dir |
| CANON | `00-canonical-doc-paths` · `00-top-level-design-is-an-lfp-rollup` | — | THE MASTER MAP, and each top's two anchors: its TOP-LEVEL DESIGN · its TOP-LEVEL STATES DOC |
| METHOD | `00-size-the-corpus…` (the algebra) | project-scoped — a project writes its own worked instance | — |
| GATES | `24-scaffold-to-harness` | — | the `state-file` skill's `check_state_files.py` · the `top-level-design` skill's `check_top_level_design.py` + its `hook.py` and its `check_reachable.py` · the `design-toc` skill's `design_toc.py --check` (all ship with this AIOS) |

## THE PATTERNS UP FRONT — each kind of file, the check it passes before a version leaves the machine

| kind of file a version changes | its check |
|---|---|
| a board (`*_states.md`) | the state-file gate, `check_state_files.py <the board's path>` |
| a `DESIGN.md` | the read-order check: its READ ORDER and its TOC rule current, then `design_toc.py <project> --check` (the `design-toc` skill) → CURRENT — the read order of every `DESIGN.md` checked, and its table of contents where the project keeps one |
| every document a design reaches | the reachability check, `check_reachable.py` (the `top-level-design` skill), run from each top-level design and each `DESIGN.md` the version changes → nothing unreached |
| a top-level design | the top-level-design gate, `check_top_level_design.py` — every top THE MASTER MAP names, else the bound one |
| THE MASTER MAP | the map check, `check_top_level_design.py --map <the map>` |
| a skill tree | `skilltree validate` |
| an AI file of this AIOS — a rule, a skill, an agent definition, the boot config, a hook | the AIOS's own-file checks: no person named but in [[user_info]], no home-folder path, no out-of-bounds folder — the release's audit where [[user_info]] binds THE AIOS RELEASES |
| every file | the secret scan ([[canonical-source-dirs]] LAW 2) |
| a program | its own tests |
| a published unit | its version raised in its build file |

Each check is a script of the skill that carries it: open that skill with the Skill tool, by its name, and run the
script from the folder Claude Code names as the skill's base directory when it loads — never search the disk for it;
where the package's skill guard is installed, a write of a `DESIGN.md`, a board, an architecture map or a top-level
design is refused until its skill is opened. A work file — a document, a note, a record, a project's `workspace/` output (`how-to-save-work`) — carries no check. Before a version leaves the
machine the agent runs every check for the kinds of file it changes ([[top-level-session-worktree]] point 13), so each
repository's reviewer receives it already following its patterns.

## THE PORT (derivable from kind/role)

Porting the workspace method into a fresh Claude Code: **KERNEL = every tagged rule except `kind="canon"` and
`role="instance"` — copy as is.** `kind="canon"` = binding templates — copy the SHAPE, re-point the paths at the
new workspace's own canon docs. `role="instance"` = this workspace's artifacts — never ported, rebuilt in
place.

## THE CONVERSION DEBT (what a fresh installation owes — tracked on ITS top-level states doc)

COUNT the projects, then count how many carry each artifact of the table above; the difference IS the debt,
and it goes on that installation's own top-level board as rows. Everything already KNOWN about a project
converts into its dev flows + architecture map; a project where the four questions (28b) cannot be answered is
UNREAD and gets read, not boarded.

TRIGGER:[writing any rule that governs designs / states / flows / diagrams (⇒ tag it) · finding an untagged
member (⇒ tag it, same turn — an AIOS rule in a new release) · needing "which rules are the doc system?" (⇒ the grep) · needing a template (⇒
the TEMPLATE column) · creating a project (⇒ it owes every artifact in the table — make them through the
`aios-artifacts` skillchain, in its order)]
