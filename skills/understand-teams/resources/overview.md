# Agent Teams — Overview

**Official docs:** https://code.claude.com/docs/en/agent-teams

---

## What Teams Provide

A team is a group of Claude Code instances that can:
- Message each other directly (SendMessage)
- Share a task list (TaskCreate, TaskUpdate, TaskList)
- Coordinate through shared files
- Run as separate tmux sessions with independent context windows

---

## Coordination Mechanisms

### Direct Messaging
Agents send messages to each other peer-to-peer. Messages are delivered immediately.

```bash
SendMessage(to: "observer", message: "Read cycle-1-executor.md")
```

### Shared Task List
All agents share a task list. Tasks have owners, status, and dependencies.

```javascript
TaskCreate: "Analyze execution output"
  owner: observer
  blockedBy: ["run execution"]  // Can't start until dependency completes
```

### Shared Files
All agents can read/write files in shared directories. Use as:
- Payload exchange (large data in files, pointers in messages)
- State persistence (survives across agent restarts)
- Source of truth (files over memory in context)

---

## Spawning Agents

### With inline prompt
```javascript
Agent: {
  name: "executor",
  prompt: "You are the executor. Your job is to {WORK}.
    Read your skills from: ~/.claude/teams/{team}/state/executor-skills.md
    Write traces to: ~/.claude/teams/{team}/state/cycle-N-executor.md
    Message observer directly when done."
}
```

### With subagent definition
```
Spawn a teammate using the security-reviewer agent type
```
Subagent definition's tools and model are honored. Body is appended to system prompt.

---

## Lead = Coordinator, NOT Relay

The #1 failure mode: lead acts as message relay.

```
WRONG:
  executor → SendMessage(lead) → lead reads → SendMessage(observer)
  // Problem: Lead's context fills. Lead compacts. Chain breaks.

RIGHT:
  executor → SendMessage(observer)       // direct
  observer → SendMessage(meta-observer) // direct
  // Lead: monitors task list, updates pipeline.json, intervenes ONLY on problems
```

---

## Rehydration: Recovering from Context Loss

When any agent loses context:

```
1. Read pipeline.json → know where we are
2. Read your role's skill file
3. Check TaskList → confirm task states match pipeline.json
4. Resume from current phase
```

Files are the rehydration mechanism. Messages are pointers to files.

---

## Task Dependencies Enforce Ordering

```javascript
TaskCreate: "Observe first execution"
  owner: observer
  blockedBy: ["first work cycle"]  // Can't start until executor done

TaskCreate: "Meta-observe first observation"
  owner: meta-observer
  blockedBy: ["first observation"]  // Can't start until observer done
```

Blocked tasks cannot be claimed until dependencies complete.

---

## Compounding Across Runs

Teams are one-shot by default. To compound:
- Accumulate skills in files that persist across team deletions
- On new team: read accumulated files first
- Agents start better than last run

---

## Hooks for Quality Gates

| Event | Exit Code 2 | Purpose |
|-------|-------------|---------|
| TeammateIdle | Blocks idle | Send feedback, keep teammate working |
| TaskCreated | Blocks creation | Validate before task enters system |
| TaskCompleted | Blocks completion | Verify quality before accepting |

---

## Known Limitations

- No session resumption with in-process teammates: /resume doesn't restore them
- Task status can lag: agents may not mark tasks complete
- Shutdown is slow: agents finish current request first
- One team per session: clean up before starting new one
- No nested teams: teammates cannot spawn teams
- Lead is fixed: cannot promote teammate to lead
- Split panes require tmux or iTerm2: not VS Code terminal, Windows Terminal, or Ghostty
