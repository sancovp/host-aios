# Repo canonicity + publishing — ONE hot home per artifact, edit up / publish down, never hand-edit the cold copy

CONTEXT:[cross-repo source-of-truth law · prevents split-brain (same artifact in two repos silently drifting) · same shape as the STRINGS/§C2 HOT-COLD directive · composes with [[canonical-source-dirs]] (which copy) + [[00-rules-are-live-state]] (keep the map true)]

LAW:[
- **THE CANONICAL HOME** ([[canonical-source-dirs]] LAW 0, bound per installation) is the HOT home of every artifact — EDIT in its subdir, full stop
- everything downstream is COLD, receive-only — NEVER hand-edit a cold copy (editing it is the bug that drifts)
- flow is ONE direction: canonical home → downstream, by a mirroring publish · the target never reaches back
- the canonical home = THE source of truth; NO more work outside it
]

MECHANISM — a publish tool does NOT ship with this AIOS (a product owed); its SHAPE is stated so an
installation can build one. Until one exists, the LAW above binds by hand.[
- a VERSION TAG per unit drives it → per unit in a MANIFEST: clone the target, mirror the source subdir in with a **checksum-compared, delete-enabled** sync that excludes the target's `.git/`, commit under a publishing identity, push
- **`--delete` = NOTHING-EXTRA:** files absent from the source are REMOVED from the target, except an explicit protected set (a changelog, refresh CI) → **work existing ONLY on the cold side is DESTROYED at the next publish, and that is the whole reason for the law**
- the manifest holds PUBLIC units only — a private product in it would publish secrets
]

ADDING AN ARTIFACT:[
1. PUBLIC (open-source plugin / package) → a manifest unit: author in `<canonical home>/<subdir>`, add a manifest entry, publish by tag · the public repo is a pure delete-enabled sync TARGET, never edited
2. PRIVATE product, or a layer internal to the canonical home → lives ONLY there, canonical there, NOT in the public manifest · a private deploy repo is a COLD one-way target too
3. never create a second editable copy (a standalone dir duplicating a subdir of the canonical home is a drift hazard, not a home)
]

PORTING METHOD (safe union port — proven):[`git -C <standalone> archive HEAD | tar -x -C <canonical home>/<band>/<x>` = tracked files only (structurally excludes `.env`/`node_modules`/build output/cruft), `tar -x` never deletes (docs unique to the canonical copy survive), stack a consolidation commit · verify secrets-clean (grep the staged set for `.env` and real key/token prefixes) BEFORE commit]
NOT:[a delete-enabled sync across a standalone↔canonical pair (destroys one side)]

NOT:[a status ledger in this rule — which of an installation's artifacts are consolidated, still standalone or
awaiting a fold is live state, and it belongs on that installation's own board]

TRIGGER:[creating/editing an artifact with (or that could get) a second repo copy · about to edit a standalone dir that also exists as a subdir of the canonical home (STOP — edit the canonical home) · adding a public plugin/package (→ the manifest) · seeing two copies drift · keep [[canonical-source-dirs]] in sync when a canonical resolves]
