#!/usr/bin/env python3
"""make_prompt.py — render a prompt from the command line (the universal prompt-maker).

  python scripts/make_prompt.py --list                          # list stored prompt templates
  python scripts/make_prompt.py --template persona              # render a stored prompt template
  python scripts/make_prompt.py --template five_level --blocks  # render each block separately
  python scripts/make_prompt.py --block examples/block_system.json   # render one block payload
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "prompt_engineering"))
from prompt_engine import render_file, render_template, render_template_blocks, list_templates  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="Render a prompt deterministically.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--template", help="name of a stored prompt template (templates/<name>/)")
    g.add_argument("--block", help="path to a single block payload JSON")
    g.add_argument("--list", action="store_true", help="list stored prompt templates")
    ap.add_argument("--blocks", action="store_true", help="with --template: print each block separately")
    args = ap.parse_args()

    if args.list:
        names = list_templates()
        print("\n".join(names) if names else "(no templates)")
    elif args.template:
        if args.blocks:
            for name, prompt in render_template_blocks(args.template).items():
                print(f"# ── block: {name} ──\n{prompt}\n")
        else:
            print(render_template(args.template))
    else:
        print(render_file(args.block))


if __name__ == "__main__":
    main()
