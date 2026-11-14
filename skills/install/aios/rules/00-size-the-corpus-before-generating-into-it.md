# 00 — SIZE THE CORPUS BEFORE GENERATING INTO IT (the algebra; FIRST ACTION, before any read)

<docsys kind="method" role="law"/>

PRINCIPLE:[an agent's knowledge at generation time IS its context window, exactly · so the first
question on any corpus is never "where do I start reading" but **"does this fit"** · the answer
picks the ARCHITECTURE, and an architecture chosen wrong is not recoverable by effort, diligence,
or more turns — it produces motion without ground, indefinitely]

## THE ALGEBRA — run it BEFORE the first Read, before any goal, plan, or edit

```
1. MEASURE      every file that constitutes the corpus (`wc -l`, `wc -c`; bytes/4 ≈ tokens)
2. SUBTRACT     the EXHAUST — derived artifacts are NOT the corpus
3. COMPARE      against the window (the running model's context size)
4. BRANCH       fits ⇒ READ ALL OF IT   ·   exceeds ⇒ BUILD THE ORCHESTRATION
5. PRINT        the numbers and the branch chosen, so the choice is checkable
```

**FITS ⇒ READ EVERY SINGLE LINE BEFORE GENERATING ONE WORD INTO IT.** Not sampled, not
read-as-you-go, not "the files a goal happens to name." All of it, first. A book, a package, a
design corpus — 800 pages of ordinary prose fits; most projects fit; assume it fits until the
measurement says otherwise.

**EXCEEDS ⇒ THE DELIVERABLE IS THE ORCHESTRATION, NOT THE READING.** Subagents specialized per
chunk that KNOW their chunk · an orchestrator over them · and the skills/rules that force routing
through it. Build that first and work through it after. Never improvise across an oversized corpus
one window at a time.

## THE EXHAUST CLAUSE — measure the CORPUS, never the residue

Derived artifacts — extraction files, read-ladders, intermediate banks, generated indexes,
per-increment write-ups — are **not** the corpus. Count them separately and say so.

⚠ **A broken process generates exhaust, and the exhaust then makes the corpus look too large to
read, which appears to justify more process.** That loop is self-feeding and it is invisible
unless the measurement separates the two. When exhaust exceeds the corpus, the exhaust is the
finding.

## WHAT COUNTS AS "GENERATING INTO IT"

Writing a goal about it · planning it · editing any file in it · asserting anything about what it
contains or how it is organized. All of these are generation. All of them require the read.

DO:[
- run the algebra as the FIRST action of any corpus task, and print it
- state the branch out loud before acting on it
- re-run it whenever the corpus changes size or the scope changes
- when a rehydration set names fewer files than the corpus, treat that as a defect in the set,
  not as permission to read less
]
NOT:[
- start reading from the top and stop when interrupted
- treat missing knowledge as something to fill in while working
- accept a scoped read-set as a substitute for the measurement
- count a process's own output as the thing that process must read
- declare a corpus oversized without printing the arithmetic
]

TRIGGER:[any task touching a project, codebase, book, archive, or conversation set · before any
goal is written or executed · any moment of not knowing what a corpus contains (⇒ measure, then
branch) · any claim that something is too big to read (⇒ show the numbers, minus exhaust)]
