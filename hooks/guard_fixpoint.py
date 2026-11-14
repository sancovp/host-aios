#!/usr/bin/env python3
"""guard_fixpoint.py — the host AIOS's fixpoint guard (DESIGN.md §8.8): a turn that changed a file ends on a re-read
that finds nothing wrong.

A Claude Code Stop and SubagentStop hook. At the first stop of a turn — the payload's `stop_hook_active` false — it
reads the transcript of the agent stopping from the turn's prompt on, and when the turn wrote or edited a file (a Write,
Edit or MultiEdit), it holds the stop once: the reason names each file the turn changed and gives the boot config's
FIXPOINT as one instruction — re-read what it changed and everything that states the same things or points to it, as a
fresh reviewer of the whole would; change what is wrong, never what is only worded otherwise; end on a pass that finds
nothing wrong. At the stop after that pass (`stop_hook_active` true) it lets the turn end, so it can never loop. A turn
that changed no file ends at once. The agent stopping is the session, at Stop, or a helper agent, at SubagentStop: Claude
Code ends a helper agent with SubagentStop and never Stop, and names its own transcript there
(`agent_transcript_path`) beside the session's, so a helper's turn is read from its own events.

    stdin   the hook payload {transcript_path, stop_hook_active, and agent_transcript_path at a helper agent's stop}
    stdout  {"decision": "block", "reason": "…"} to hold the stop · nothing to let it end · exit 0 always

Its blind spot, stated with it: a file changed through the shell is not counted here — the boot config's FIXPOINT binds
it. A payload or a transcript it cannot read lets the turn end, because a guard that fails closed on its own error would
hold every turn. Standard library only.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

WRITES = {"Write", "Edit", "MultiEdit"}
INSTRUCTION = ("Before the turn ends, re-read what it changed, and everything that states the same things or points to "
               "it, as a fresh reviewer of the whole would. Change what is wrong, never what is only worded otherwise "
               "than you would word it now; then end the turn on a pass that finds nothing wrong (the boot config's "
               "FIXPOINT). This is asked once per turn.")


def is_prompt(e: dict) -> bool:
    """A user's own prompt: a user message whose content is text, never a tool's result."""
    if e.get("type") != "user" or e.get("isMeta"):
        return False
    content = (e.get("message") or {}).get("content")
    if isinstance(content, str):
        return bool(content.strip())
    if isinstance(content, list):
        return any(isinstance(b, dict) and b.get("type") == "text" for b in content) and not any(
            isinstance(b, dict) and b.get("type") == "tool_result" for b in content)
    return False


def changed_this_turn(transcript: str) -> list[str] | None:
    """The files the turn's Write, Edit and MultiEdit calls named, in order — or None if the transcript is unreadable."""
    try:
        lines = Path(transcript).expanduser().read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    events = []
    for line in lines:
        try:
            events.append(json.loads(line))
        except ValueError:
            continue
    start = max((i for i, e in enumerate(events) if is_prompt(e)), default=-1)
    files: list[str] = []
    for e in events[start + 1:]:
        if e.get("type") != "assistant":
            continue
        for b in (e.get("message") or {}).get("content") or []:
            if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") in WRITES:
                p = str((b.get("input") or {}).get("file_path") or "")
                if p and p not in files:
                    files.append(p)
    return files


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    if payload.get("stop_hook_active"):
        return 0
    files = changed_this_turn(str(payload.get("agent_transcript_path") or payload.get("transcript_path") or ""))
    if not files:
        return 0
    shown = "\n".join(f"  - {f}" for f in files[:40]) + (f"\n  … and {len(files) - 40} more" if len(files) > 40 else "")
    print(json.dumps({"decision": "block", "reason": f"FIXPOINT — this turn changed {len(files)} file(s):\n{shown}\n"
                                                     f"{INSTRUCTION}"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
