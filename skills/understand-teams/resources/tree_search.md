# Tournament Pattern (Tree Search)

A team configuration where N agents independently attempt the same task. A judge evaluates their outputs and selects the best. Branching explored in parallel, best path selected.

## When to Use

- Exploring solution space
- Competitive selection
- Finding the optimal approach among alternatives
- Research with multiple hypotheses

## The Configuration

```
         ┌─────────────────┐
         │     JUDGE        │
         │  (lead agent)   │
         └────────┬────────┘
                  │ evaluates
    ┌────────────┼────────────┐
    ▼            ▼            ▼
 AGENT_1       AGENT_2       AGENT_3
  solve         solve         solve
    │             │             │
    ▼             ▼             ▼
 output_1      output_2      output_3
    │             │             │
    └─────────────┴─────────────┘
                  │
                  ▼
              JUDGE selects best
```

## How It Works

1. JUDGE creates N identical task definitions (different agents get same brief)
2. AGENTS independently solve (may use different approaches)
3. AGENTS write outputs to shared files
4. JUDGE reads all outputs, scores against criteria
5. JUDGE selects winner, may prompt for refinement on top entry

## Spawning

```javascript
Agent: { name: "judge", prompt: "You are the judge. Create task definitions. After agents submit, evaluate and select the best." }
Agent: { name: "agent-1", prompt: "Solve the task independently. Write output to shared/agent-1/output.md." }
Agent: { name: "agent-2", prompt: "Solve the task independently. Write output to shared/agent-2/output.md." }
Agent: { name: "agent-3", prompt: "Solve the task independently. Write output to shared/agent-3/output.md." }
```

Judge monitors shared directory, reads all outputs when agents signal done.

## Variants

### Single-Round Tournament
N agents, one submission each, judge picks best.

### Multi-Round with Refinement
Best entry from round 1 is shared with all agents for round 2 improvement. Judge picks from refined entries.

### Hierarchical Tournament
Quarter-finals → Semi-finals → Finals. Reduces judge's load with many agents.

## Scoring Criteria

Judge evaluates against explicit criteria:
- Correctness
- Efficiency
- Novelty
- Clarity

Can weight criteria differently based on task type.

## Key Difference from GAN-Like

GAN-Like: two agents iterate on same artifact until critic passes

Tournament: N agents independently produce artifacts, judge selects best
