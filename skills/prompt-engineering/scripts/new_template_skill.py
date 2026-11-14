#!/usr/bin/env python3
"""new_template_skill.py — scaffold a NEW Claude Code skill package for a prompt template.

Each prompt template can become its own skill: this writes a complete, self-contained skill directory
(the engine in lib/, a SKILL.md, a make_prompt.py, and templates/<name>/ with the blocks) so the new
template ships as an installable skill.

  # clone an existing template into a new skill:
  python scripts/new_template_skill.py --name my-reviewer --out ~/.claude/skills --from-template persona

  # build from your own block payload files:
  python scripts/new_template_skill.py --name my-reviewer --out DIR --blocks sys.json persona.json rules.json
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

ENGINE_LIB = Path(__file__).resolve().parent.parent / "prompt_engineering"
TEMPLATES = Path(__file__).resolve().parent.parent / "prompt_engineering" / "templates"

SKILL_MD = '''---
name: {name}
description: Renders the "{name}" prompt template deterministically (built from blocks). Use to produce the {name} prompt the same way every time.
when_to_use: Whenever you need the {name} prompt; same spec renders the same prompt every time.
---

# {name} — a prompt-template skill

This skill renders one prompt template, **{name}**, built from the blocks in `templates/{name}/`.

```python
import sys; sys.path.insert(0, "lib")     # or ${{CLAUDE_SKILL_DIR}}/lib
from prompt_engine import render_template
render_template("{name}")                 # → the {name} prompt (deterministic)
```

Or from the shell: `python scripts/make_prompt.py`

## Files (relative to this skill)
- `lib/prompt_engine.py`, `lib/blocks.py` — the deterministic engine (on pydantic-stack-core)
- `templates/{name}/template.json` + block payloads — the {name} prompt template
- `scripts/make_prompt.py` — render it from the command line
'''

MAKE_PROMPT = '''#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from prompt_engine import render_template
print(render_template("{name}"))
'''


def scaffold_skill(name, out_dir, from_template=None, block_paths=None):
    """Create a self-contained skill package for a prompt template. Returns the skill dir path."""
    out = Path(out_dir).expanduser() / name
    (out / "lib").mkdir(parents=True, exist_ok=True)
    (out / "templates" / name).mkdir(parents=True, exist_ok=True)
    (out / "scripts").mkdir(parents=True, exist_ok=True)

    shutil.copy(ENGINE_LIB / "blocks.py", out / "lib" / "blocks.py")
    shutil.copy(ENGINE_LIB / "prompt_engine.py", out / "lib" / "prompt_engine.py")

    if from_template:
        src = TEMPLATES / from_template
        block_files = json.loads((src / "template.json").read_text()).get("blocks", [])
        for bf in block_files:
            shutil.copy(src / bf, out / "templates" / name / bf)
    elif block_paths:
        block_files = []
        for bp in block_paths:
            bp = Path(bp)
            block_files.append(bp.name)
            shutil.copy(bp, out / "templates" / name / bp.name)
    else:
        raise ValueError("provide from_template or block_paths")

    (out / "templates" / name / "template.json").write_text(
        json.dumps({"name": name, "description": f"The {name} prompt template.", "blocks": block_files},
                   indent=2) + "\n")
    (out / "SKILL.md").write_text(SKILL_MD.format(name=name))
    (out / "scripts" / "make_prompt.py").write_text(MAKE_PROMPT.format(name=name))
    return str(out)


def main():
    ap = argparse.ArgumentParser(description="Scaffold a new skill package for a prompt template.")
    ap.add_argument("--name", required=True, help="skill / template name")
    ap.add_argument("--out", required=True, help="directory to create the skill in")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--from-template", help="clone an existing stored template's blocks")
    g.add_argument("--blocks", nargs="+", help="block payload JSON files to include")
    args = ap.parse_args()
    path = scaffold_skill(args.name, args.out, from_template=args.from_template, block_paths=args.blocks)
    print(f"Created skill package: {path}")


if __name__ == "__main__":
    main()
