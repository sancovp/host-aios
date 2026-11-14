#!/usr/bin/env python3
"""guard_dispatch.py — the host AIOS's dispatch guard (DESIGN.md §8.1): one agent holds a body of code.

A Claude Code PreToolUse hook on the Agent tool (and its older name, Task) and the Workflow tool. It reads an Agent
call's prompt and a Workflow call's script — the script given inline, or the file its `scriptPath` names — and refuses
a dispatch whose text orders a worktree on a new branch (`git worktree add … -b <branch>`, or `-B`): that is the setup
a dispatch needs to build or change the work's own code, which the session that read the code does itself (the rules
`subagent-worktree-isolation` and `00-explore-reads-everything`). A worktree added detached (`--detach`) — the setup
for a test, a review or a try-out in a throwaway copy — passes, and so does a dispatch that adds no worktree.

    stdin   the hook payload {tool_name, tool_input}
    exit 0  allowed · exit 2 refused, the reason and the remedy on stderr, which Claude Code hands back to the agent

Its blind spot, stated with it: a dispatch that has an agent edit the copy in use without any worktree, or that sets a
branch up another way (`git switch -c`, `git checkout -b`), is not seen here — the rules bind it. A payload it cannot
read passes, because a guard that fails closed on its own error would stop every dispatch. Standard library only.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

TOOLS = {"Agent", "Task", "Workflow"}
_ADD = re.compile(r"\bgit\b(?:\s+-C\s+\S+|\s+-c\s+\S+|\s+--git-dir(?:=|\s+)\S+)*\s+worktree\s+add\b([^\n;&|]*)")
_NEW_BRANCH = re.compile(r"(?:^|\s)-[bB](?:\s+|=)['\"]?[\w${}<>@./+-]*[\w$}>]")

REASON = (
    "⛔ REFUSED — this dispatch orders a worktree on a new branch (`git worktree add … -b`): the setup for handing "
    "an agent the work's own code to build or change. The session that read a body of code is the one that changes "
    "it, in its own worktree, through the project's own system (rules subagent-worktree-isolation and "
    "00-explore-reads-everything).\n"
    "Remedy: make the change yourself, in your own worktree. Dispatch an agent only to locate, test, review or try "
    "something, in a throwaway copy of its own — `git -C <repo> worktree add --detach <its ignored scratch "
    "folder>/worktrees/<task> <ref>` — and read its output yourself."
)


def orders_a_new_branch(text: str) -> str | None:
    """The `git worktree add … -b` command the text orders, or None."""
    for m in _ADD.finditer(text or ""):
        args = m.group(1)
        if "--detach" in args.split():
            continue
        if _NEW_BRANCH.search(args):
            return m.group(0).strip()
    return None


def dispatch_text(tool: str, ti: dict) -> str:
    if tool in ("Agent", "Task"):
        return str(ti.get("prompt") or "")
    script = str(ti.get("script") or "")
    path = ti.get("scriptPath")
    if path:
        try:
            script += "\n" + Path(str(path)).expanduser().read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass
    return script


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    tool = payload.get("tool_name") or ""
    if tool not in TOOLS:
        return 0
    found = orders_a_new_branch(dispatch_text(tool, payload.get("tool_input") or {}))
    if not found:
        return 0
    print(f"{REASON}\nThe command it orders: {found[:200]}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
