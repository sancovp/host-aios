#!/usr/bin/env python3
"""guard_mode.py — the host AIOS's mode guard (DESIGN.md §9.2): every request names its mode before the agent acts.

A Claude Code UserPromptSubmit hook. A mode stated for the start of a session does not fire at the next request in the
same session, so at every prompt this hook adds one general instruction to the turn, before the agent acts: name the
request's mode — DEV when it asks to fix, add, change or improve a project that exists, opening the
`how-to-develop-a-project` skill first; WORK when it asks to make, produce or do something with a project, calling that
project's starting skillchain, and anything that will live in a folder of its own — a tool, a program, a project — being
a new project, `aios-artifacts` opened before that folder's first file, and a new project being WORK whatever it is
made of, DEV only for a project that already exists — and write the mode line into that project's
scratchpad with the Write or Edit tool, as the first line of its section there, making the section, or the scratchpad,
where there is none, since a line said only in the reply is not there to be read again; the section is kept through
the task's last turn and rolled up only before the next task.

    stdin   the hook payload {prompt, …}
    stdout  {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": "…"}} · exit 0 always

It decides nothing and refuses nothing. Its blind spot, stated with it: only the agent can tell the mode; the hook
reminds it at the moment the request arrives. A payload it cannot read, or an empty prompt, adds nothing. Standard
library only.
"""
from __future__ import annotations

import json
import sys

INSTRUCTION = (
    "Before you act on this request, name its mode. DEV — it asks to fix, add, change or improve a project that exists: "
    "open the `how-to-develop-a-project` skill first. WORK — it asks to make, produce or do something with a project: "
    "call that project's starting skillchain, which its CLAUDE.md names. Anything that will live in a folder of its own "
    "— a tool, a program, a project, any piece of work bigger than one file — is a new project: open `aios-artifacts` "
    "before that folder's first file, and make it there. A new project is WORK, whatever it is made of, its code "
    "included: DEV is only for a project that already exists. Then write "
    "your MODE LINE — `MODE: DEV or WORK · <the project> · <where you work> · GOAL: <this request in one line>` — into "
    "that project's scratchpad with the Write or Edit tool, as the first line of your section there, making the section, "
    "or the scratchpad, where there is none: saying it in your reply records nothing. Keep the section through this "
    "task's last turn; roll it up only before your next task.")


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    if not isinstance(payload, dict) or not str(payload.get("prompt") or "").strip():
        return 0
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": INSTRUCTION}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
