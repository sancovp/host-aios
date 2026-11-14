#!/usr/bin/env python3
"""Generate a persona prompt from a spec file — composes block types + a cognition DSL block.

    python scripts/make_persona.py examples/persona_debugger.json
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "prompt_engineering"))
from persona import make_persona_file  # noqa: E402


def main(argv):
    if len(argv) != 2:
        print("usage: make_persona.py <spec.json>", file=sys.stderr)
        return 2
    print(make_persona_file(argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
