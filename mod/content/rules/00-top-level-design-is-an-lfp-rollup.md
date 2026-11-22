# 00 — THE TOP-LEVEL DESIGN IS AN LFP ROLL-UP

<docsys kind="canon" role="law"/>

TARGET:[EACH TOP-LEVEL DESIGN — the document that is the cover over every `DESIGN.md` outside the home-unknown band beneath
one top AIOS ([[00-top-level-design-first]]); THE MASTER MAP names each one ([[00-canonical-doc-paths]]), and where no
map loads the installation's TOP-LEVEL DESIGN binding ([[user_info]]) names the one top · an installation with neither
owes one — say so; this rule does not fire until one is named, and the absence is never a licence to invent a target]

SHAPE:[
- AN EXPLAINED TABLE OF CONTENTS of the tree of documents holding everything the system does: every
  section is a short BRIDGING statement + the LINKS to where its detail lives, and the bridges, read in
  sequence top to bottom, explain the ENTIRE architecture · every project and how they interrelate · the
  vision · where each thing's state lives, never the state itself — ONE CONTINUOUS DOCUMENT, the architecture as ruled now · a bridge that grows
  into the detail it points at is the violation; that detail moves to its own document and the bridge stays
- LFP ROLL-UP: OVERVIEW → PARTS → ATTRIBUTES → COMPOSE · every part defined (what · when · how · utility),
  rolled up to the least fixed point, then composed granularly · a flat list is the failure
- IT CLOSES: the last line is exactly `AND THAT'S THE ARCHITECTURE.`
- each section = the architecture description + LINKS to the documents holding the detail · a section that
  inlines its own source document is a violation ([[29-state-indexes-design]])
- the opening section is the top's READ ORDER, and states, in full: WHAT the document is · HOW to read it (only when the work is wired
  into the system; then top to bottom, and only the links the work needs — [[00-top-level-design-first]] ·
  [[00-how-to-read]]) · HOW to change it (THE WRITE, below) · WHERE live work-state lives (the top-level
  states doc and each dir's `_states.md`) · WHERE every detail lives (the link table) · if an agent could
  still ask a question about the document itself, the opening is incomplete — fix the opening
- section numbers are STABLE, UNIQUE and ASCENDING · new material goes INTO the section that owns it · a new
  section only for a genuinely new architectural PART
]

THE WRITE — the only legal change, whatever the change is (a decision, a correction, *USER* saying something
must change):[
1. READ THE WHOLE DOCUMENT
2. find EVERY place the change touches — every claim it changes, contradicts or completes
3. REWRITE each of those places so the document states the current architecture and nothing else — the
   reader never works out what is current
4. re-read the affected sections — the roll-up still closes
5. commit — git holds the versions; the document carries none of its own history
6. append the change — what changed, the reading it replaced, why — to the `CHANGELOG.md` beside the document
]
DO:[move detail that would bloat a section into its own document, and leave the one-line architecture
statement plus a link]
NOT:[append a section · add a dated entry, an ADDENDUM, an "additive only", an "UPDATED" block or a changelog
inside the document · keep a superseded reading, a "was"/"kept" clause, a date or a quote of *USER* in the text · stack a
correction after the text it corrects · state history, incidents or how the document got here]

GATE:[THE TOP-LEVEL-DESIGN GATE ships with this AIOS — the `top-level-design` skill:
`check_top_level_design.py` finds each top through THE MASTER MAP — where no map loads, through THE TOP-LEVEL DESIGN
binding — and refuses a section number repeated or out of order · a missing closing line · an opening that does not
state what the document is, how to read it, how to change it and where progress lives · a date · a quote or the user's
name · a replaced or superseded reading · history · a patch block · a moved stub · a state-of-construction word · a
section grown past a bridge · `--map <the map>` checks the map itself, refusing a line with no link, a link that
resolves to nothing, a line over 200 characters, two lines naming one top and any text that is not a line · run it
bare after any edit and before any commit touching a top-level design or the map, and read what it says · `hook.py`
beside it runs the same check on every Edit/Write to any top the map names (else the bound one), installed in the
project settings of the repository that holds the document, and refuses an edit that adds a finding · red = fix the
edit, never the checker ([[24-scaffold-to-harness]]: the law binds whether or not it runs)]

TRIGGER:[about to write to a top-level design or THE MASTER MAP · about to record a decision, ruling or build anywhere ·
"addendum" / "additive only" / "append" / "superseded" / a date near this document · a section-number
collision · the document not ending with `AND THAT'S THE ARCHITECTURE.` · an agent about to ask what to do
with the top-level design (⇒ fix the opening)]
