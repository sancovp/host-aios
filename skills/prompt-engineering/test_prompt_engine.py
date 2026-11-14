#!/usr/bin/env python3
"""prompt-engineering skill — proves: deterministic render; blocks compose into prompt templates; a
prompt template is a stored folder of blocks (add by dropping a folder); example block types render; a
persona stacks blocks; and a template scaffolds its OWN skill package. Pure stdlib, no API."""
import glob
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "prompt_engineering"))
sys.path.insert(0, str(HERE / "scripts"))
from prompt_engine import (  # noqa: E402
    render, render_file, list_templates, render_template, render_template_blocks,
)
from new_template_skill import scaffold_skill  # noqa: E402


def main():
    # 1. DETERMINISM — same block payload → same prompt, every time
    payload = json.loads((HERE / "examples" / "deity_template.json").read_text())
    a, b = render(payload), render(payload)
    assert a == b and a.startswith("# Worldsmith") and "domain of otters" in a
    print("  deterministic   same block → same prompt ✓")

    # 2. PROMPT TEMPLATE — a stored, ordered set of BLOCKS → one prompt
    five = render_template("five_level")
    for level in ("WORLD", "EGREGORE", "DEITY", "PROGENITOR", "AGENT"):
        assert level in five
    assert five.index("WORLD") < five.index("AGENT"), "blocks join in manifest order"
    assert set(render_template_blocks("five_level")) == {"world", "egregore", "deity", "progenitor", "agent"}
    print("  template        blocks compose into one prompt, in order ✓")

    # 3. ADD-BY-FOLDER — discovered by convention
    names = list_templates()
    assert {"five_level", "simple_agent", "persona"} <= set(names), names
    assert render_template("simple_agent").startswith("You are a Helper")
    print(f"  add-by-folder   templates discovered: {names} ✓")

    # 4. BLOCK TYPES — each example block renders to a non-empty chunk
    block_files = sorted(glob.glob(str(HERE / "examples" / "block_*.json")))
    assert len(block_files) >= 6
    for bf in block_files:
        assert len(render_file(bf)) > 5, bf
    print(f"  block types     {len(block_files)} example blocks render (system/persona/rules/few-shot/…) ✓")

    # 5. PERSONA — a worked persona stacks block types into one prompt
    persona = render_template("persona")
    for section in ("## Persona", "## Rules", "## Output format"):
        assert section in persona, section
    assert "Ada" in persona
    print("  persona         system+persona+rules+output → one persona prompt ✓")

    # 6. ENGINE — declarative blocks render deterministically (NO exec); a prompt IS a MetaStack of pieces
    from blocks import Role, BulletList, prompt as make_prompt, render_prompt
    from pydantic_stack_core import MetaStack
    assert render({"type": "Template", "template": "{x}!", "values": {"x": "hi"}}) == "hi!"
    composed = render_prompt(Role(role="a helper"), BulletList(title="Rules", items=["Be terse."]))
    assert composed == "You are a helper.\n\n## Rules\n- Be terse.", composed
    assert isinstance(make_prompt(Role(role="a helper")), MetaStack)   # every prompt IS a MetaStack
    print("  engine          declarative blocks → MetaStack of RenderablePieces (no exec) ✓")

    # 7. SKILL GENERATOR — a prompt template scaffolds its OWN skill package
    tmp = tempfile.mkdtemp()
    skill_dir = Path(scaffold_skill("my-reviewer", tmp, from_template="persona"))
    assert (skill_dir / "SKILL.md").exists()
    assert (skill_dir / "lib" / "prompt_engine.py").exists()   # generated skills keep a self-contained lib/
    assert (skill_dir / "templates" / "my-reviewer" / "template.json").exists()
    # the generated package's template renders (point the engine at the generated templates dir)
    gen_prompt = render_template("my-reviewer", base=skill_dir / "templates")
    assert "Ada" in gen_prompt and "## Rules" in gen_prompt
    print("  skill-gen       a template scaffolds its OWN skill package (renders standalone) ✓")

    print("PROMPT-ENGINEERING PASS — engine · blocks → templates · block types · persona · skill generator")


if __name__ == "__main__":
    main()
