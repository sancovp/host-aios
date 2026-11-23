#!/usr/bin/env python3
"""guard_design.py — the host AIOS's design guard (DESIGN.md §12): one string, once per window, before any work.

A Claude Code SessionStart hook, run at a session's start and again at every resume, clear and compaction — so once in
every window, the moment before the agent's first step there. It adds one string to the window and does nothing else:

    Read the target project's DESIGN.md if it has one and if not then run the ground truth protocol. If it has a HALO
    SEEM MAP refer to that during ground truth.

It blocks nothing. A string comes first; a block is the second-order answer, for when the string proves too loose, and
a block then comes with its own protocol, an action or a syntax.

    stdin   the hook payload {source, …} (ignored)
    stdout  {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": STRING}} · exit 0 always
    --text  the string alone, for a machine's session-start notice that runs it beside its own text

Standard library only.
"""
from __future__ import annotations

import json
import sys

STRING = ("Read the target project's DESIGN.md if it has one and if not then run the ground truth protocol. If it has a "
          "HALO SEEM MAP refer to that during ground truth.")


def main() -> int:
    if "--text" in sys.argv[1:]:  # the plain string, for a machine's session-start notice that prints it beside its own
        print(STRING)
        return 0
    try:
        sys.stdin.read()
    except OSError:
        pass
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": STRING}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
