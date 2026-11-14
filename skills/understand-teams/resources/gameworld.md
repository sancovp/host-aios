# Gameworld Pattern

A team configuration for persistent agents with economic pressure. Uses shared state via files. No direct messaging between agents.

## When to Use

- Persistent agents with progression and leveling
- Trade/economy simulation
- Agents that accumulate state across sessions
- Market/auction scenarios

## The Configuration

Each agent is a separate Claude Code instance. They NEVER message each other.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Claude Code  │     │ Claude Code  │     │ Claude Code  │
│  Instance 1  │     │  Instance 2  │     │  Instance 3  │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                      │                      │
       │ action.json         │ action.json         │ action.json
       │    (poll)          │    (poll)          │    (poll)
       ▼                     ▼                     ▼
┌─────────────────────────────────────────────────────────────┐
│                      game.json                               │
│  (shared world state: gold, trade board, quest log, etc)  │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │    execute.sh (bash)      │
              │    ALL game logic here   │
              └────────────────────────┘
```

## Key Principles

### No Inter-Agent Messaging
Agents do not send messages to each other. All coordination is through game.json.

### Server Stays Dumb
The WebSocket server does ONE thing: polls action.json from each agent and forwards to frontend. Zero game logic.

### Identity from Directory Name
Agent ID comes from directory name, NOT from any agent-writable file:

```bash
AGENT_ID=$(basename "$AGENT_DIR")  # agent_001, agent_002, etc.
```

### Atomic State Mutations
```bash
TEMP=$(mktemp)
jq '... mutation ...' "$GAME_FILE" > "$TEMP" && mv "$TEMP" "$GAME_FILE"
```
mktemp + mv is atomic — either full new state or nothing.

## Agent Directory Structure

```
agent_mmorpg/gptrpg/agents/
├── agent_001/
│   ├── action.json      # Pending action for server pickup
│   ├── game_state.json  # Local view of world state
│   ├── crafted/         # Skills made by this agent
│   ├── memory/          # Zettelkasten (persists across seasons)
│   └── .claude/skills/  # Agent's skill set
└── agent_002/
    └── ...
```

## Spawning

Each agent is a separate Claude Code instance. Spawn with:
- Working directory set to their agent directory
- CLAUDE.md as their prompt
- Skills copied into their .claude/skills/

## game.json Structure

```json
{
  "game_id": "world_name",
  "tick": 0,
  "season": { "number": 1 },
  "agents": {},
  "trade_board": [],
  "quest_log": {},
  "achievements": {}
}
```

## execute.sh Actions

| Action | What it does |
|--------|---------------|
| quest_accept | Accept a quest from the board |
| quest_complete | Submit a crafted skill, earn gold |
| trade_post | List a skill for sale |
| trade_buy | Buy a skill from another agent |
| learn | Record learning (adds XP) |
| achievement_claim | Claim an achievement |
