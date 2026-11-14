# Exploration reads EVERYTHING — full module reads + E2E execution traces (INVARIANT)

PRINCIPLE:[a reader that samples, plans-what-to-read, grep-and-peeks, or "reads selectively" returns FALSE conclusions — untrustworthy · grep LOCATES, never CONCLUDES · **A CRITICAL READ IS NEVER DELEGATED:** what the work's correctness rests on — the design being changed, the code about to be edited, the canon a statement is built from, the files behind a verdict — is read by the session itself, whole; an agent's summary of it is never the basis of what is written, decided or said · **AN AGENT IS DISPATCHED TO LOCATE, TO TEST, TO REVIEW OR TO TRY SOMETHING IN A THROWAWAY COPY, AND NEVER TO BUILD OR EDIT THE WORK'S OWN CODE:** these it does unasked — a search whose hits the session then reads, a test, a fresh reader testing an artifact, a review, a try-out whose change stays in its throwaway copy · the session that read a body of code is the one that builds and changes it, through the project's own system ([[subagent-worktree-isolation]]), so the code is read once and never again by each fresh agent a build would be handed to · a lead's agent does one child project's work — work, never code — and launches no agent of its own (the `how-to-lead-an-aios` skill)]

MODE A — EXPLORE A LIBRARY = READ EVERY MODULE, FULLY:[
- start at the TOP file · read every module it imports, and every module those import, transitively, to the leaves
- read the whole file, every file
- a conclusion drawn from less than a full read of every relevant module is a lie until the full read backs it
]
NOT (Mode A):[resource-allocate · plan what to read · sample · "grep to locate then read excerpts"]

MODE B — EXPLORE AN EXECUTION = RETURN THE EXECUTION BOUNDARY, E2E:[
- return the absolute entrypoint (the tool/route/CLI/hook actually called) AND the lowest stack level it touches (deepest write/read — the file, the neo4j UNWIND, the HTTP POST, the queue-draining daemon)
- follow EVERY call DOWN · a trace that stops at an intermediate function (e.g. a registry write, without following whether a daemon/observer/hook mirrors it onward) is incomplete and its verdict is void
]

DISPATCH:[
- an agent sent to explore LOCATES: it returns the files, the line ranges and the call chain, and the session reads them whole before it concludes anything
- an agent sent to test, review or try something works in a throwaway copy of its own (a detached worktree off the ref), and a change it makes there is a test whose output the session reads — never work that lands
- put the mandate IN the prompt verbatim: "READ EVERY MODULE FULLY (transitively, to the leaves) — no sampling, no grep-and-peek. For any execution, trace E2E from the absolute entrypoint to the lowest stack level it touches; follow every call to the bottom."
- demand the report cite the FULL call chain (entrypoint → … → lowest write/read) with file:line per hop + an explicit list of EVERY module read
- re-dispatch a subagent that returns a conclusion without the full chain
]

QUERY THE STORE (data is ground truth, a code trace is not):[
- before concluding "X does not reach store Y / X is not in carton / X isn't persisted": QUERY STORE Y FOR X DIRECTLY
- query the graph FIRST — a code-trace absence-claim is VOID until the store is checked and comes back empty (a forward trace from one guessed entrypoint misses producers: batch sync scripts, separate subsystems, harvesters, daemons)
- enumerate a system's SUBSYSTEMS (every dir) first, so none is omitted from the read set
]

CODE-CAPABILITY CLAIMS — THE STORE IS THE INTERPRETER:[
- grep proves PRESENCE, never ABSENCE · capabilities arrive via (a) cross-repo INHERITANCE (mixins/MRO — e.g. "OM has a heart" appears as a string NOWHERE in onionmorph; it is entailed by OMCave→AppCAVEAgent→CAVEAgent(AnatomyMixin), wired in the cave package), (b) LOADER indirection (.heaven onions, automation-registry JSONs, `code_pointer` strings resolved at fire-time), (c) design-vocabulary drift (the doc says ".cave dir loader"; the code calls it "automation registry"), (d) the prompt plane ([[prompt-plane-vs-deterministic-plane]])
- before asserting "X lacks capability Y": ask Python not grep (`python -c "from pkg import Cls; print(hasattr(Cls,'y'), Cls.__mro__)"`) · enter through the dir's `.claude/rules/` tables FIRST (the semantic index) · walk the MRO / read the base class
]
NOT:[treat a grep miss on a capability question as a conclusion]

TRIGGER:[about to dispatch any agent (⇒ will what I state or decide rest on its reading? yes ⇒ read it myself; no ⇒ dispatch) · about to hand a build, a rebuild or an edit of the work's own code to an agent (⇒ STOP: the session that read the code changes it — [[subagent-worktree-isolation]]) · dispatching a subagent to locate in a library or execution path · about to draw a where-does-it-persist / does-it-touch-X / what-is-the-CRUD conclusion · any "repo X lacks capability Y" claim (⇒ interpreter check + dir-rules read FIRST)]

→ The mechanical HOW (the exact Read-tool call sequence): [[00-how-to-read]].
