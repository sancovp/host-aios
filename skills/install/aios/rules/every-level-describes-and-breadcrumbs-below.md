# EVERY HIGHER LEVEL DESCRIBES THE LEVELS BELOW IT — AND BREADCRUMBS TO THEM, FROM THE MASTER MAP DOWN TO EVERY DOCUMENT

<docsys kind="scaffold" role="law"/>

LAW:[every higher level gives the description of the levels below it, and breadcrumbs to them · every document is reached from the top, and a program checks it]

PRINCIPLE:[a doc tree is only navigable TOP-DOWN · at every level the reader must learn (a) WHAT is below and
(b) HOW TO GET THERE · a child that announces itself only INSIDE itself is UNREACHABLE, because the only reader
who sees the announcement is one who already found it · a file that still exists but that nothing points at,
from where its reader lands, is lost · a ruling binds only where it fires: written into a document that does not
load at the moment it matters, it does not bind]

THE CHAIN (each level owes a description + a link to the next):[
- THE MASTER MAP ([[00-canonical-doc-paths]]) → every top-level design, one line and a link each
- a top-level design → every `DESIGN.md` beneath its top outside the home-unknown band, and the band itself named as outside it
- a `DESIGN.md` → every child dir's `DESIGN.md` (its READ ORDER names each — [[26-canonical-design]]) AND every document under it — a detail design, a pattern, a reference, a note's record — each by its one-line summary and link, AND every file of its code, each by its line of why it exists and what it connects to, in the section that owns its topic or in a page of `design/` that section links
- **EVERY SECTION → the detail docs for ITS OWN TOPIC**
- a folder's `CLAUDE.md` → every file and folder in it that a reader may need, one line each
- the states index (`29b-state-index`) → every `_states.md`
- every `_states.md` row → the thing it tracks ([[29-state-indexes-design]])
]

THE CHECK:[the `top-level-design` skill's `check_reachable.py`, run from a top-level design or a `DESIGN.md`: it follows every link and every named path to a file or a folder, counts a reached folder's `CLAUDE.md`, `.claude/rules/` and `.claude/skills/` as reached (Claude Code loads or lists them with it), skips the folders the design's READ ORDER names on its `ARCHIVE AND PROGRAM FOLDERS:` line, and lists every tracked `.md` file nothing reaches, exit 1 when any · run it bare before a version leaves ([[00-docsys]] THE PATTERNS UP FRONT), and give each document it lists its line in the parent that owns its topic — or name the folder it sits in on that line, when it is evidence, generated output or a program's source]

DO:[
- when you write or find a detail doc, add its DESCRIPTION + LINK to the section that OWNS its topic, not only to
  a registry — the pointer belongs WHERE THE READER LANDS
- describe it in one line of what it ANSWERS, so a reader can tell from the parent whether to open it (a bare
  filename is a link, not a description)
- when you CREATE any doc or state file, add the parent's row the SAME TURN ([[00-rules-are-live-state]])
- when you read down a level and the parent did not describe it, FIX THE PARENT before continuing
- write a ruling into the document that loads where it fires — a rule for what must always load, the skill opened at
  its trigger, the design read for its work — never into a note
]
NOT:[
- rely on a single registry section to make N detail docs reachable from N other sections
- write at one level without maintaining the pointer chain above it — that DESTROYS THE CONNECTION even though
  every file still exists
- re-derive from source what a detail doc states — that is the symptom of a broken chain above you
- leave a document the reachability check lists
]

TRIGGER:[writing or finding any doc · creating a `_states.md` / `DESIGN.md` · about to read a child doc (⇒ did
the parent describe it? if not, fix the parent) · catching yourself deriving from code something a doc probably
states (⇒ the chain is broken above you — repair it, then read) · about to write a ruling (⇒ into the document that
loads where it fires) · a version about to leave (⇒ run the reachability check)]
