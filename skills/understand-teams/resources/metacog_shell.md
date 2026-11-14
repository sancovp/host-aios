# Metacog Shell Pattern

A team configuration for self-improving observation. Uses direct messaging.

## When to Use

- Observation + evaluation + skill extraction
- Agents need to challenge each other's work
- Quality gates on output
- Multi-pass analysis

## The Configuration

4 agents in a peer-to-peer chain:

```
EXECUTOR ──────────────────────────────────────────────────────┐
  │ Does the work                                              │
  │ Writes trace to file                                       │
  │ Messages OBSERVER directly (not through lead)               │
│                                                             │
OBSERVER ◄──────────────────────────────────────────────────┘
  │ Reads executor's trace from FILE                           │
  │ Extracts domain skills                                     │
  │ Messages META-OBSERVER directly                            │
│                                                             │
META-OBSERVER [STATIC] ◄────────────────────────────────────┘
  │ Reads observer's trace from FILE                           │
  │ Evaluates observation methodology (not domain content)      │
  │ STATIC: fixed point that grounds the recursion             │
│                                                             │
SKILL-EDITOR (runs after all cycles complete)                  │
  │ Reads accumulated skills from files                         │
  │ Persists improvements to actual skill files                │
```

## Write-Then-Send Protocol (CRITICAL)

```
WRONG:
  executor → SendMessage(lead, full_trace)
  lead → SendMessage(observer, full_trace)  # Lead becomes relay

RIGHT:
  executor → Write(cycle-N-executor.md, trace)
           → SendMessage(observer, "Read cycle-N-executor.md")
```

Messages are POINTERS. Files are the source of truth.

## State Directory

```
~/.claude/teams/{team}/state/
├── pipeline.json              # Current cycle state (lead writes)
├── cycle-N-executor.md       # Executor output cache
├── cycle-N-observer.md       # Observer analysis cache
├── cycle-N-meta.md           # Meta-observer assessment cache
├── executor-skills.md         # Accumulated skills (observer → executor)
└── observer-skills.md        # Accumulated meta-skills (meta → observer)
```

## Compounding

```
CYCLE 1: executor → observer → meta-observer
  Skill-editor persists learnings to skill files

CYCLE 2: executor (with improved skills) → observer → meta-observer
  Skill-editor is now better at editing (accumulated rules)
  → compound improvement
```

## Why Static Meta-Observer?

Without a fixed point, the system drifts — Agent 2 "improves" in ways that aren't actually better. The static meta-observer grounds the recursion.

## Spawning

```javascript
Agent: { name: "executor", prompt: "You are the executor..." }
Agent: { name: "observer", prompt: "You are the observer..." }
Agent: { name: "meta-observer", prompt: "You are the meta-observer. You evaluate methodology, not content..." }
Agent: { name: "skill-editor", prompt: "You run after cycles complete. Read accumulated skills, persist improvements." }
```

Each agent messages the next one directly. Lead only coordinates task list.
