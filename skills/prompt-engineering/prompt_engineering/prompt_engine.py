"""
prompt_engine.py — the deterministic prompt builder, on `pydantic-stack-core` blocks.

A block (data) → a prompt chunk; a stored template (ordered blocks) → one full prompt. SAME inputs give
the SAME output every time — no model call, no randomness, pure composition. That determinism is the point.

Vocabulary
  block            — a `RenderablePiece` (see blocks.py): typed fields + a pure render() → a prompt chunk.
                     Declarative form: `{"type": <RegistryName>, **fields}`.
  prompt           — a `MetaStack` of blocks (built with blocks.prompt / blocks.render_prompt).
  prompt template  — a stored, ordered set of block files (a folder under templates/) → one full prompt.

Top-level API
  render(spec)                    → prompt chunk for ONE declarative block spec
  render_file(path)               → render a block spec from a JSON file
  list_templates()                → names of stored prompt templates
  load_template(name)             → {name, description, blocks:[spec...], block_files:[...]}
  render_template(name)           → ONE prompt (the template's blocks, composed in order, as a MetaStack)
  render_template_blocks(name)    → {block_name: prompt} (each block rendered separately)
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

try:
    from .blocks import block_from_dict, render_prompt, RenderablePiece
except ImportError:  # loaded standalone (package dir on sys.path)
    from blocks import block_from_dict, render_prompt, RenderablePiece


def render(spec: Union[Dict[str, Any], RenderablePiece]) -> str:
    """One block (a declarative `{"type": ..., ...}` spec or a RenderablePiece) → its prompt chunk."""
    block = spec if isinstance(spec, RenderablePiece) else block_from_dict(spec)
    return block.render()


def render_file(path: Union[str, Path]) -> str:
    """Render a block spec from a JSON file."""
    return render(json.loads(Path(path).read_text()))


# ── prompt templates: a stored, ordered set of BLOCKS (add one by DROPPING A FOLDER) ───────────────
#   templates/
#     {template_name}/
#       template.json   — manifest: {name, description, blocks: ["block1.json", "block2.json", ...]}
#       {block}.json    — a declarative block spec: {"type": <RegistryName>, **fields}
# To add a prompt template: create the folder + template.json + block specs in the project's own templates folder, and
# pass it as `base`. The `templates/` beside this file holds the shipped ones and is read only.

def templates_root(base: Optional[Union[str, Path]] = None) -> Path:
    return Path(base) if base else (Path(__file__).resolve().parent / "templates")


def list_templates(base: Optional[Union[str, Path]] = None) -> List[str]:
    """Discover prompt templates by the folder convention (any dir with a template.json)."""
    root = templates_root(base)
    if not root.exists():
        return []
    return sorted(p.name for p in root.iterdir() if (p / "template.json").exists())


def load_template(name: str, base: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """Load a prompt template: manifest + each ordered block spec."""
    root = templates_root(base)
    manifest = json.loads((root / name / "template.json").read_text())
    block_files = manifest.get("blocks", [])
    blocks = [json.loads((root / name / f).read_text()) for f in block_files]
    return {"name": manifest.get("name", name), "description": manifest.get("description", ""),
            "blocks": blocks, "block_files": block_files}


def render_template(name: str, base: Optional[Union[str, Path]] = None) -> str:
    """Render a stored prompt template → ONE prompt (its blocks composed in order as a MetaStack)."""
    t = load_template(name, base)
    return render_prompt(*t["blocks"])


def render_template_blocks(name: str, base: Optional[Union[str, Path]] = None) -> Dict[str, str]:
    """Render each block of a prompt template separately → {block_name: prompt}."""
    t = load_template(name, base)
    return {Path(f).stem: render(b) for f, b in zip(t["block_files"], t["blocks"])}


__all__ = ["render", "render_file", "templates_root",
           "list_templates", "load_template", "render_template", "render_template_blocks"]
