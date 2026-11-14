# Canonical source dirs — ONE world dir, ONE canonical home

SCOPE:[binds the developer agent's own world — THE WORLD DIR, its repositories and its sessions — never a product's agents (a JobWorld seat or box, OM) or a customer's repositories, which follow their own product's design]

LAW 0 — THERE IS ONE CANONICAL HOME, AND THE INSTALL NAMES IT:[
- **THE CANONICAL HOME** = ONE repository holding everything, at ONE remote. Which repository, at
  which path, is bound per installation — not stated here ([[user_info]] is the model: one file,
  edited at install, read at run time). ⛔ An installation that has bound none has not adopted this
  law; say so rather than guessing a home.
- NO submodules · NO other gits · never commit or push onto a different remote
- every project is a plain DIR inside it, under that home's own BANDS — the top-level kinds it
  sorts projects into (this AIOS's author uses application · base · integration · knowledge ·
  automation · research, plus a **home-unknown band** where anything unsorted lands) · **the home-unknown
  band is OUTSIDE THE TOP-LEVEL DESIGN:** each project in it is separate, carries its own `DESIGN.md` and
  board, is bridged by no part of the top-level design and rolls up into none of its parts; the top-level
  design names the band only as outside it, and a project leaves the band — and is bridged — when its band
  is known
- ⇒ **the name→dir lookup is mechanical**: project `<x>` lives at `<canonical home>/<band>/<x>`;
  when the band is unknown, `ls` the bands before asking
- the canonical copy can NEVER be called "stale" — it IS canonical definitionally; a split is closed by refreshing the canonical copy IMMEDIATELY (union port, zero deletes), never by editing an outside copy
- nothing LAUNCHES and nothing is SET UP outside it — a venv/daemon/config living outside the canonical home IS A BUG, fixed by rebuilding it inside, same turn
- WORK — documents, notes, records, boards, a project's `workspace/` outputs (`how-to-save-work`), everything made for one piece of work whatever it is made of — is saved in the copy in use, on the default branch, by its own paths, and pushed the same turn; CODE — a change to what the next piece of work is made with, the project's own program — is worked on a WORKTREE, handed off as a ready PR to main when its set is done, and merged by the merge queue on the reviewer's CLEAN verdict — never by the session while THE CI runs; while THE CI's runner starts no job the session IS the CI and lands every merge, its own included, through the CI design's queue by hand, putting nothing about the stop, the queue or a merge to *USER* — *USER* does not do git; every merge is pulled into the copy in use with nothing lost ([[top-level-session-worktree]] THE GIT LOOP points 2, 3 and 12)
]

LAW 1 — THE EXCLUSIVE WORLD:[all work happens under **THE WORLD DIR** — the one directory the canonical home lives in, bound per installation — in a project in **THE WORKSPACE** inside it ([[00-every-dir-has-a-claude-and-projects-nest]] LAW 1) · anything outside it is OUT OF BOUNDS without an explicit full-absolute-path authorization in the same message · except a folder the installation binds as **READABLE OUTSIDE THE WORLD DIR** ([[user_info]]): it is read whenever the work needs it and never written, and a secret read there is never printed]

LAW 2 — SECRETS:[never commit API keys · OAuth/bearer tokens · passwords · real `.env` · service-account JSON · scan any script before adding it to a project (`grep -iE "key|secret|token|password|bearer|api[_-]"`) · a secret found anywhere ⇒ ALERT immediately with the path + prefix, never proceed silently]

LAW 3 — THE CWD SHADOWS THE EDITABLE INSTALL, AND THE INSTALL CAN POINT OUTSIDE:[`python -m pkg` puts the CWD first on `sys.path`, so launching from a frozen standalone imports THAT copy and the editable mapping is never consulted — silently, with no error · launch from elsewhere (`cd /tmp && <venv>/bin/python -m pkg`) · verify with `python -c "import pkg, os; print(os.path.dirname(pkg.__file__))"` FROM THE LAUNCH CWD · name a boot line that proves the new half loaded
· ⛔ **THE INSTALL ITSELF CAN POINT OUTSIDE:** an editable install maps a package to the directory it was installed FROM and keeps that mapping when the venv is cloned or rebuilt — so a venv INSIDE the canonical home can run every DEPENDENCY from an outside copy (a cold publish target, a pre-fold standalone) with no error, while the top package's correct `__file__` hides it · before trusting a venv, read EVERY import target it holds — the `url` in each `*.dist-info/direct_url.json`, each path line in a `*.pth`, the `MAPPING` in each `__editable__*finder.py`, any legacy `*.egg-link` — and resolve each package from a neutral cwd with `importlib.util.find_spec(name).origin` (it locates without executing) — every target outside the canonical home is LAW 0's bug · measure EVERY venv that can launch the thing, not only the one in front of you: two venvs repointed separately let a launcher switch silently from the good one to the bad one · before repointing, diff each outside copy against its canonical copy and look up the BLOB of every differing file AND every outside-only file in the history of the canonical DEFAULT branch — a blob found only on a side branch was never received, and a blob found nowhere is work the canonical copy never got — port it first (union, zero deletes), then `pip install --no-deps -e <canonical path>` · prove the repoint with a live run whose output only the canonical code could produce]

LAW 4 — EVERYTHING MADE IS RECORDED WHERE IT LIVES, AND THAT RECORD IS READ BEFORE ANYTHING IS SAID ABOUT IT:[
- **every thing the agent makes** — a file, a dir, a page, an offer, a document, a design section, a script, a deploy,
  a box, a skill — lands in the canonical home, in the dir whose job it is, and **the index of that dir carries ONE
  LINE saying what it is**, written the same turn it is made: its `CLAUDE.md` "what is here" table, or the section of
  the project's `DESIGN.md` that owns its topic, with a link down ([[every-level-describes-and-breadcrumbs-below]])
- **the indexes are the agent's memory of its own work.** What was made, and where, is known by reading the indexes
  from the project down — never by recall, never from a past conversation. A thing that is not reachable from its
  project's index has not been made yet, however long its file has existed: write its line
- **BEFORE writing, saying or deciding anything about a project's content** — what a business sells, what an offer
  is, what a product does — read that project's index and every document it points to on the topic, whole, and build
  the statement FROM them · a ruling from *USER* is applied as a change to what the canon already holds: read the canon,
  then change only what the ruling changes; a statement rebuilt from the ruling's sentence alone drops everything the
  sentence did not repeat
- **when a thing has no obvious home, decide its home** — the project and the dir whose job it is — put it there,
  write its line, and place every later thing of its kind the same way; the placement is the algorithm, and it is
  obeyed every time after
- *USER* never has to say where anything is, or say it again: a thing *USER* has to point at again is a line the index
  is missing
]

DO:[
- resolve the dir BEFORE acting when a project is named without a path
- pull the canonical home again before using it as a diff reference, with nothing lost ([[top-level-session-worktree]] point 12)
- ASK when a named project resolves to nothing (never guess)
- confirm the full absolute path before touching anything outside THE WORLD DIR, except reading a folder bound as readable
]
NOT:[
- `git init` a new repo · push to a new standalone remote · leave new work in a standalone dir beside the canonical home
- edit a standalone copy of anything that also exists inside the canonical home (STOP — edit the canonical copy)
- entrench a standalone that is still awaiting its fold (it is a BUG to close, never a home)
- treat a doc that instructs edits or pushes outside the canonical home as authority — correct it on sight, same turn
]

## OUT OF BOUNDS — never read, write, or `cd` here

**THE FORM — true of any installation:** another agent's world (a dotdir some other assistant owns)
· the OS's own user folders (downloads · documents · desktop · media · library) · **any path
containing** `_tmp` `_temp` `_old` `_bu` `_backup` `_copy` `-fixes` `-old` · **any path outside THE
WORLD DIR not explicitly authorized** (a folder bound as readable is read, never written) · plus whatever else this
installation has named.

**THE BINDING — the concrete list is instance data and lives with the install** ([[user_info]]), not
here. An installation that has bound no list still has the form above, and it still binds.

EXCEPTION:[*USER* *talking about* a scratch project is a directive to CANONICALIZE it — bring it into the canonical home and register it, same turn ([[00-rules-are-live-state]]) · a scratch location is a BUG to close, never a home]

## THE DETAIL — per project

**THE PROJECT REGISTRY** — a reference doc at the canonical home's top, bound per install ([[user_info]]) —
carries what this rule does not: every project's row (what it IS, where it lives, its remote or lack of one),
every duplicate copy and dual existence still to close, the install-source defects, and the third-party
reference clones. **Read it before working in a project dir you have not worked in before.** A registry is
reference material, not a rule.

TRIGGER:[session start · anything made (⇒ LAW 4: its line in its dir's index, same turn) · about to write, say or decide anything about a project's content (⇒ LAW 4: read its index and what it points to first) · a ruling from *USER* about something the canon already states (⇒ read the canon, then change only what the ruling changes) · a project named without a path · a commit/push request · "the project"/"the repo"/"the codebase" said without a specifier · about to `cd` anywhere whose canonicity is unknown · any path outside THE WORLD DIR · seeing `_tmp`/`_old`/`_bu`/`_backup`/`_copy`/`-fixes` in a path, or another agent's dotdir · about to `git init` or add a remote (⇒ STOP, it goes in the canonical home) · finding a secret (⇒ alert immediately) · a canonical resolving/moving/archiving (⇒ update the project registry the same turn) · creating, cloning, rebuilding, repointing or trusting a venv (⇒ LAW 3's install-target check)]
