# GAN-Like Pattern (Critic-Revise Loop)

A team configuration where two agents iterate on the same work product — one produces, one critiques, until the critic passes the output.

## When to Use

- Writing drafts (prose, code, scripts)
- Code review against explicit criteria
- Compliance or safety checking
- Iterative refinement with clear acceptance criteria

## The Configuration

```
PRODUCER ───────────────────────────────┐
  │ Produces the work                       │
  │ Receives critique                      │
  │ Revises and resubmits                  │
  ▼                                        │
CRITIC ◄──────────────────────────────────┘
  │ Evaluates against criteria               │
  │ Returns specific critique               │
  │ Passes → done                         │
```

## How It Works

1. PRODUCER generates initial output
2. CRITIC evaluates against checklist
3. If fail: CRITIC messages PRODUCER with critique, PRODUCER revises
4. Repeat until CRITIC passes
5. CRITIC messages lead with "passed"

## Example: Code Review

```
PRODUCER → generates function
  ↓
CRITIC → checks:
  - No SQL injection?
  - Types correct?
  - Error handling?
  - Tests present?
  ↓ fail → "Line 23: SQL injection. Line 45: missing error handling."
  ↓ pass → "LGTM"
```

## Spawning

```javascript
Agent: { name: "producer", prompt: "You are the producer. Write code that meets the criteria. Wait for critique before revising." }
Agent: { name: "critic", prompt: "You are the critic. Evaluate output against checklist. Give specific, actionable critique. Pass when acceptable." }
```

Critic messages producer directly with critique. Lead only receives final "passed" message.

## Compounding

Critic accumulates failure patterns → fewer rounds needed over time.

## Key Difference from Metacog Shell

Metacog Shell: observer extracts skills from executor's work (executor doesn't change behavior mid-cycle)

GAN-Like: critic and producer iterate on the SAME artifact until critic passes it
