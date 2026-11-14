---
name: understand-teams
description: |
  WHAT: How to understand and configure agent teams
  WHEN: Understanding or creating agent teams for parallel work, observation stacks, or multi-agent coordination
---

# Agent Teams

Pure Claude Code — no external systems.

## Files

- `resources/overview.md` — How teams work: coordination mechanisms, spawning, task management, rehydration
- `resources/metacog_shell.md` — Metacog Shell: 4-agent self-improving observation stack (direct messaging)
- `resources/gameworld.md` — Gameworld: persistent agents with economic pressure (shared state)
- `resources/gan_like.md` — GAN-Like: critic-revise loop until output passes criteria (direct messaging)
- `resources/tree_search.md` — Tournament: N agents compete, judge selects best (hybrid)

**Read `resources/overview.md` first** to understand the foundation.

## MEASURED — no team in a headless session

Measured at a clean seat on Claude Code 2.1.325: a headless session (`claude -p`) given
`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` through its settings file's `env` listed no TeamCreate tool, so no team could be
started there, and what a teammate may do — the official docs' "teammates cannot spawn teams" — stays unmeasured. A lead
of an AIOS (the `how-to-lead-an-aios` skill) runs its agents as helper agents, the mechanism measured working (the
`understand-subagents` skill), until a team is shown working where the lead runs.
