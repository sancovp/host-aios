# 00 — THE READ IS SCOPED TO THE WORK (the top found through the master map; its top-level design is a table of contents, read wherever it names the project)

FIRST ACTION — at every conversation start · resume · compaction summary · handed summary, BEFORE touching /
editing / running / committing / answering:[
0. **UNDER A GOAL** → the goal's READ LIST, whole, at start and after every compaction; nothing beyond it.
0b. **NAME THE MODE.** A WORK session — asked to make, produce or do something with a project — writes its mode line,
   reads its WORK board and calls the project's starting skillchain, which its `CLAUDE.md` names, and reads no design
   first; making a new project — anything that will live in a folder of its own, a tool or a program among them — is this AIOS's own work, started by its `aios-artifacts` skillchain before that folder's first file, in WORK mode whatever it is made of. A DEVELOPMENT
   session — asked to fix, add, change or improve a project that exists — opens the `how-to-develop-a-project` skill,
   whose design read is steps 1–4 below.
1. **FIND THE TOP.** THE MASTER MAP ([[00-canonical-doc-paths]]) loads into every session as a user rule: one line and
   a link per top-level design. The top that holds the work is the one whose folder holds the work's folder; where no
   map loads, THE TOP-LEVEL DESIGN binding ([[user_info]]) is the one top. Read that top only — never another top's
   design.
2. **CHECK THE WIRING — MECHANICALLY.** A project is WIRED when its top's top-level design names its dir: `grep` the
   project's path in that document. Named ⇒ wired, whatever its code imports — a part of the architecture talks
   to the rest over HTTP, over a key, over a graph, or over nothing but a shared design, and each of those is
   wiring. Not named ⇒ not wired (a scratch project, a dossier, a fixture).
3. **NOT WIRED** → read the project's own canon and nothing above it: its `CLAUDE.md` · its `DESIGN.md`
   through its READ ORDER and its TOC rule, the sections the work touches · its board · its scratchpad · the files the
   work names. No top-level design and no top-level states doc is opened.
4. **WIRED** → the project's own canon as in 3, PLUS **ITS TOP'S TOP-LEVEL DESIGN, TOP TO BOTTOM**: its opening is
   that top's READ ORDER, and it is the EXPLAINED TABLE OF CONTENTS of a TREE of documents holding everything that top
   does — each section a short bridging statement plus links, so the bridges in sequence are the map of the whole.
   Then follow ONLY the links the work needs; never every link. A document you do follow, read whole
   ([[00-how-to-read]]: contiguous reads; grep locates, never concludes). That top's TOP-LEVEL STATES DOC: only the
   rows the work touches.
]

THE ROLES:[
- **THE MASTER MAP** = the global rule naming every top-level design, one line and a link each; its place is fixed,
  so it needs no binding ([[00-canonical-doc-paths]])
- **THE TOP-LEVEL DESIGN** = the COVER over every `DESIGN.md` beneath one top AIOS, outside its home-unknown band —
  the explained table of contents of that top's architecture ([[00-top-level-design-is-an-lfp-rollup]] SHAPE); the
  map's entry for the top that holds the work
- **THE TOP-LEVEL STATES DOC** = that top's own OUTSTANDING board ([[28-distributed-state]])
- WHERE they are is bound per installation ([[user_info]]) — where no map loads, the TOP-LEVEL DESIGN binding is the
  one top; the binding mechanism is not to be invented
]

CLAUSES:[
1. a compaction summary IS a conversation start — find the top, redo the wiring check and re-read only what the
   pending step needs; the summary carries which project it was
2. an interrupted read RESUMES before anything else — finish the scoped read, then respond or act
3. answering counts as working — a factual assertion requires its scoped canon read this window
4. a SessionStart hook that orders a read orders THIS scoped read
5. memory files, rules and prior sessions' reads do not substitute — the read is per window
6. writing to a top-level design follows [[00-top-level-design-is-an-lfp-rollup]] THE WRITE
]
DO:[say the top, the scope and the wiring verdict in one line before the first read · when no map loads and the
installation has bound no top-level design, wired work reads what the tree actually has, deepest canon first]
NOT:[read a top-level design for a project not wired into it · read another top's design · recurse every link · ask
*USER* whether to read · substitute grep for reading a document you need]

DISCIPLINE:[a development session: find the top → wiring check → scoped canon → act; a work session: its WORK board →
its starting skillchain · ONE thing finished before the next starts · the doc
tree is LIVE STATE — rewrite the scope's `DESIGN.md` + board whenever what they state changes; a top-level design +
its top-level states doc move only when a canonical change reaches them]

TRIGGER:[a conversation start · resume · compaction/summary event (⇒ name the mode; a development session finds the
top, checks the wiring, then reads its scoped canon; a work session calls its starting skillchain) · about to open a top-level design (⇒ is it the top that holds the work, and is the work wired into it? then
which sections?) · acting without the scoped canon read THIS window (⇒ stop and read it) · an interruption during
the read (⇒ finish it first)]
