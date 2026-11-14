"""skillpack.py — a markdown body → a publishable `<name>/SKILL.md` dir.

The canonical output of every *CC is a MARKDOWN FILE carrying the chain / instructions in its custom
syntax; wrapping it as `<name>/SKILL.md` is the easiest way to publish it so any agent auto-loads it.
This is the one place that wrapper is written, shared by ACCC / CORCC / SCCC.

Moved DOWN from `chaincompiler.skillpack` (REBUILD-SPEC.md §7) so the *CC import it from the base.

D4: `write_skill(..., coordinate=True)` and `cohere_skills(root)` place skills as COORDINATE-ADDRESSED
nodes via `skilltree` (rule 25) — ALL skill stuff is built on skilltree. The default (`coordinate=False`)
preserves the exact original behavior, so the *CC and their tests keep working unchanged.
"""
from __future__ import annotations

from pathlib import Path
import re


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "skill"


def skill_markdown(name: str, description: str, body: str, *, extra: dict[str, str] | None = None) -> str:
    """Render the SKILL.md text (frontmatter + body). This IS the artifact."""
    fm = [f"name: {slugify(name)}", f"description: {description}"]
    for k, v in (extra or {}).items():
        fm.append(f"{k}: {v}")
    front = "\n".join(fm)
    return f"---\n{front}\n---\n\n{body.rstrip()}\n"


def write_skill(
    name: str,
    description: str,
    body: str,
    *,
    out_dir: str | Path,
    extra: dict[str, str] | None = None,
    coordinate: bool = False,
) -> Path:
    """Write `<out_dir>/<slug>/SKILL.md` and return its path.

    D4 — if `coordinate=True`, the skill is written into skilltree's recursive `.claude/skills/` layout
    (`<out_dir>/.claude/skills/<slug>/SKILL.md`), ready to be COORDINATE-ADDRESSED (rule 25). Write all
    your skills with `coordinate=True`, then call `cohere_skills(out_dir)` ONCE: skilltree assigns each a
    hierarchical coordinate (e.g. `0.1`, `0.2`), rewrites breadcrumbs, and writes `skilltree.json`.
    (Cohering once over the finished forest is skilltree's idiom — emitting after every write would keep
    re-rooting the tree.) Default `False` keeps the plain loose-dir behavior.
    """
    slug = slugify(name)
    base = Path(out_dir)
    # coordinate mode → skilltree's `.claude/skills/` root; else the plain `<out_dir>/<slug>/` loose dir.
    parent = base / ".claude" / "skills" if coordinate else base
    pkg = parent / slug
    pkg.mkdir(parents=True, exist_ok=True)
    md = skill_markdown(name, description, body, extra=extra)
    skill_path = pkg / "SKILL.md"
    skill_path.write_text(md, encoding="utf-8")
    return skill_path


def cohere_skills(root: str | Path, *, forest_name: str | None = None) -> dict:
    """Place every skill under `root` as a COORDINATE-ADDRESSED node (D4, rule 25).

    Thin wrapper over `skilltree.emit(root, root_forest=True)`: assigns hierarchical coordinates,
    rewrites breadcrumbs, synthesizes a forest root, and writes `skilltree.json`. `skilltree` is imported
    lazily so the pure deterministic prompt engine carries no hard skilltree requirement. Returns
    skilltree's emit report: `{ok, nodes, synthesized_root, root, moves, journal}`.
    """
    from skilltree import emit
    return emit(str(root), root_forest=True, forest_name=forest_name)


__all__ = ["slugify", "skill_markdown", "write_skill", "cohere_skills"]
