---
name: build-devdir-systems
description: Build a FACTORY — a directory wearing its devdir programs (.onionmorph = its LOOK in the world, .cave/automations = its MACHINES that fire on the daemon's calendar, CLAUDE.md = its WORKER agent) — and run multi-agent work through cave-teams. Use whenever the user wants to make a place in the world, give a dir a look, automate something in a dir, add a worker to a place, wire a factory, or "make stuff in our .devdir format". Triggers: "make a factory", "terraform", "give this dir a look", "add a machine/automation to this place", "add a worker here", "build a devdir system", "wire this dir into the game".
---

# Build devdir systems (the factory skill)

**The law: devdirs are the ONLY substance.** A dir becomes a FACTORY by wearing its programs:

| program | file | what it is |
|---|---|---|
| the LOOK | `<dir>/.onionmorph/world.json` | how the place renders in the world |
| the MACHINES | `<dir>/.cave/automations/<name>.json` | automations that FIRE on the daemon's own calendar |
| the WORKER | `<dir>/CLAUDE.md` | the place's agent — registered on boot, recruitable, chattable |

Everything is a FILE in the dir. The daemon's watcher picks up any write within ~2s:
looks re-render live, machines plug into the calendar live, workers register on the next boot.
You may write the files directly, OR go through the validated server doors (below) — the doors
refuse an invalid program with the schema's own errors and write NOTHING, which is safer.
The user sees the same files through the in-game configurator panels (⚙ on a territory,
THE CAPITAL at the root) — one substrate, two faces.

## The seam — the daemon's doors

```bash
PORT="${ONIONMORPH_PORT:-8126}"; BASE="http://127.0.0.1:$PORT"
```

Paths are WORLD paths: `/` = the onion root, `/forge` = `<onion>/forge`.

## 1. THE LOOK — `.onionmorph/world.json`

```bash
# read a place's current program
curl -s "$BASE/woom/place?path=/forge" | python3 -m json.tool

# write one (TERRAFORMING when the dir had none) — validated, atomic, 422+errors if invalid
curl -s -X POST "$BASE/woom/place" -H 'Content-Type: application/json' -d '{
  "path": "/forge",
  "program": {
    "version": 1,
    "look": {"biome": "stone", "palette": {"primary": "#7a2ff0"}}
  }
}'
```

Schema laws (violations are refused verbatim, nothing written):
- allowed top keys: `version` (must be 1) · `look` (`biome`/`palette`/`knobs`) · `assets` · `halo` · `hints`
- **NEVER `objects`** — substance comes from the devdirs themselves, never a manifest
- `assets` entries are `{id, file, place?}` where `file` is a **relative `.glb` inside the
  `.onionmorph` dir** (Blender-compiled only) and must exist
- unknown keys are errors — the schema is versioned, never key soup

## 2. THE MACHINES — `.cave/automations/<name>.json`

Machines are LIVE: the loader syncs every valid spec onto the daemon's own automation
registry and the heart fires due ones (~60s granularity). Spec shape:

```bash
# mint a machine through the door — validated, 422+errors if invalid
curl -s -X POST "$BASE/woom/automation" -H 'Content-Type: application/json' -d '{
  "path": "/forge",
  "name": "tend-the-forge",
  "spec": {
    "name": "tend-the-forge",
    "schedule": "every:3600",
    "code_pointer": "mypkg.mymodule.my_zero_arg_function"
  }
}'

# see every loaded machine + its live state (dormant · run_count · last_run)
curl -s "$BASE/woom/machines" | python3 -m json.tool
```

Spec laws:
- required: `name` + `schedule` (cron expr like `"0 3 * * *"`, or `"every:N"` seconds)
- exactly ONE of `code_pointer` | `prompt_template` | `chain_spec`
- optional: `delivery` · `enabled` · `expected_deliverables`; unknown keys are errors
- `code_pointer` = `"module.func"`, **zero-arg** (no code_args in v1) — read
  `WOOM_ONION_ROOT` from the env for context; fires in-process, LIVE immediately
- **THE MONEY LAW: `prompt_template`/`chain_spec` machines load DORMANT** (they cost real
  model calls) — they show `"dormant": true` in `/woom/machines` and never fire until the
  operator arms them (`WOOM_ARM_PROMPT_AUTOMATIONS=1`). Never promise a prompt machine
  "will run tonight" — say it is registered dormant and needs arming.
- the canonical smoke target: `onionmorph.woom_automations.write_fire_receipt` writes a
  receipt under `<onion>/.cave/woom/receipts/` — use it to prove a factory's power is on.

## 3. THE WORKER — `CLAUDE.md`

Write a real `CLAUDE.md` in the dir saying what the place IS and what its worker knows/does.
On the next daemon boot the place gets a registered cave ChatAgent named `worker-<dirname>`
(recruitable into the party, chattable from the building panel, a body standing at the place).
The file is re-read every turn — editing it re-teaches the worker live.

## 4. EXECUTION — through cave-teams (never a new runner)

Multi-agent work runs through the TWO existing cave-teams skills — point at them, use them,
never reimplement:
- **construct-and-test-cave-teams-config** — author a team topology in Python, dry-run, run,
  request goldenization
- **search-and-execute-golden-cave-teams-config** — find + run a proven golden team

A machine that should drive agents = a `chain_spec` or `prompt_template` machine (dormant by
the money law) or a `code_pointer` into a function that calls `cave()` — the calendar is the
scheduler either way; never build a second cron.

## 5. THE WORLD-POV LAW

Every act you take through the doors is recorded into the touched onions'
`.claude/rules/woom_state.md` automatically — WORLD POV, never character POV. When YOU write
state lines anywhere, keep that register: "the machine 'x' at /forge was plugged in", never
"I plugged in my machine".

## 6. TEMPLATES — capture a factory's shape, stamp it anywhere (terraforming generalized)

A TEMPLATE is a data file freezing a dir's whole factory shape (look + machines + worker +
starter files) so it can be stamped as a new dir in one act. Templates live in the seat
`<onion>/.cave/woom/templates/<name>.json`:

```json
{
  "template": "code-onion",
  "captured_from": "/forge",
  "description": "what this factory is for",
  "look": { "version": 1, "look": { "biome": "stone", "palette": {"primary": "#1fb6bf"} } },
  "machines": { "<slug>": { "name": "<slug>", "schedule": "…", "code_pointer": "…" } },
  "worker_claude_md": "# The place\n…what the worker knows…",
  "files": { "notes.md": "starter content…" }
}
```

**CAPTURE** (dir → template): read the dir's `.onionmorph/world.json` → `look`; each
`.cave/automations/*.json` → `machines`; `CLAUDE.md` → `worker_claude_md`; any starter files
worth carrying → `files`. Write the template into the seat. Capture only what IS there —
a template is a record of a real shape, never an invention.

**STAMP** (template → a new factory) — all through the existing validated writers, nothing new:
1. `mkdir <onion>/<newdir>` and write `files` + `worker_claude_md` as `CLAUDE.md`.
2. LOOK: `POST /woom/place {"path": "/<newdir>", "program": <look>}` (422 = the template's
   look is invalid — fix the template, never force).
3. MACHINES: `POST /woom/automation {"path": "/<newdir>", "name": <slug>, "spec": <machine>}`
   per machine — valid ones go LIVE on the calendar within seconds (dormant if model-call).
4. VERIFY: the dir renders (avatar + its files as kind objects), `/woom/machines` lists the
   stamped machines, and the worker registers on the next daemon boot (workers are boot-time
   in v1 — say so, never promise a live worker mid-session).

The one worked template: **code-onion** (captured from this onion's `/forge` — a making-place:
teal/stone look, a daily-tend machine, a tend-receipt heartbeat, a making-disciplines worker).

## The checklist for a whole factory

1. `mkdir` the dir (or pick the existing one).
2. WORKER: write its `CLAUDE.md`.
3. LOOK: POST `/woom/place` with the world program (or write `.onionmorph/world.json`).
4. MACHINES: POST `/woom/automation` per machine (or write `.cave/automations/*.json`).
5. VERIFY: `/woom/place?path=…` shows the program with zero errors; `/woom/machines` lists
   the machines (live vs dormant as intended); the world renders the place within seconds.
