---
name: understand-subagents
description: |
  WHAT: Claude Code subagents — isolated contexts, persistent memory, worktree isolation, GAN scoring
  WHEN: Understanding or creating subagents
---

# Understand Subagents

Pure Claude Code subagents — no external systems.

**Official docs:** https://code.claude.com/docs/en/sub-agents

## What's Here

- Built-in types: Explore, Plan, General-purpose
- Persistent memory (user/project/local scopes)
- Worktree isolation for git worktree sandboxing
- Skill preloading and fork mode
- GAN-like scoring pattern
- Custom subagent files with YAML frontmatter

**Read `reference.md`** for full details.

## MEASURED — a helper agent can launch a helper of its own

Measured at a clean seat on Claude Code 2.1.325, headless (`claude -p`): a session started a helper agent with the Agent
tool and told it to start one more; the helper's own Agent call ran, and the second helper answered. Nothing in Claude
Code stops a launch from inside a child, so where an AIOS forbids one — an agent a lead starts for a child project
launches none (the `how-to-lead-an-aios` skill, rule `subagent-worktree-isolation`) — the rule is what holds it. Read a
launch from the transcript, never from the agent's reply: it is a tool call of the Agent tool whose event's parent
tool-use id names the dispatch of the agent that made it.

## MEASURED — what a hook and a lead see of a helper agent

Measured at the same seat, on the same version:

- A helper agent's events are kept in a transcript of its own, `<session>/subagents/agent-<agent_id>.jsonl` beside the
  session's `<session>.jsonl`, which holds none of them; a headless session's streamed output
  (`--output-format stream-json`) carries them, each marked by its parent tool-use id.
- A hook on a helper agent's tool call (PreToolUse) gets `agent_id` and `agent_type`, and its `transcript_path` is the
  session's, not the helper's: a hook that judges by what the agent has done reads
  `<session>/subagents/agent-<agent_id>.jsonl`, since a skill the session opened was never in the helper's context.
- A helper agent ends with SubagentStop, never Stop; that hook gets `agent_transcript_path`, the helper's own transcript,
  beside `transcript_path`, the session's, and `stop_hook_active` as Stop does.
- The Agent tool's result names the helper's id and says that SendMessage to that id continues the same agent: that is
  how a lead hands an agent it started something more, a review's findings among them.
