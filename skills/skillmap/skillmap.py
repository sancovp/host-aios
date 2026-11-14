#!/usr/bin/env python3
"""skillmap — turn a flat pile of skills into a navigable, coordinate-addressed map
your AI agent can actually read.

Point it at a folder of skills (or any folder of markdown). It gives every skill a
hierarchical coordinate (0.1, 0.1.2, ...), reads each one's description, and writes a
single CLAUDE.md: a Folder Map tree + an addressable Index + branch summaries — so the
agent can do *progressive disclosure* (open a branch, descend to the coordinate it needs)
instead of drowning in a flat list.

Zero dependencies (Python stdlib only). Non-destructive: it only writes one file,
CLAUDE.md, in the folder you point it at.

    python3 skillmap.py ~/.claude/skills            # print the map
    python3 skillmap.py ~/.claude/skills --write     # write CLAUDE.md into the folder

The coordinate engine (assign_coords / skill_name / compose_summary) is vendored from
ChainCompiler's `skilltree` package (MIT) so the addressing matches the canonical scheme.
"""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path

# ───────────────────────── vendored from skilltree/model.py (MIT, chaincompiler) ──────────
@dataclass
class Node:
    name: str
    path: Path
    description: str = ""
    coord: str | None = None
    children: list["Node"] = field(default_factory=list)

    def walk(self):
        yield self
        for c in self.children:
            yield from c.walk()


def assign_coords(root: "Node", base: str = "0") -> "Node":
    """Give every node a hierarchical coordinate: root=base, child i (1-based)=parent.i."""
    def w(n: "Node", coord: str) -> None:
        n.coord = coord
        for i, c in enumerate(n.children, 1):
            w(c, f"{coord}.{i}")
    w(root, base)
    return root


def skill_name(n: "Node") -> str:
    """`<coord>-<name>` so a flat, coord-sorted list reveals the tree and is addressable."""
    return f"{n.coord}-{n.name}" if n.coord else n.name


def compose_summary(n: "Node") -> str:
    """Deterministic branch summary (the RAPTOR 'internal node carries a summary' win, no LLM)."""
    kids = ", ".join(c.name for c in n.children) or "(leaf)"
    return f"opens to {len(n.children)} branch(es): {kids}"
# ───────────────────────── end vendored ──────────────────────────────────────────────────

_DESC = re.compile(r"^description:\s*(.+)$", re.I | re.M)


def read_description(d: Path) -> str:
    """Best-effort one-line description: SKILL.md/README frontmatter `description:`,
    else the first real line/heading of any markdown in the dir."""
    for fn in ("SKILL.md", "README.md"):
        f = d / fn
        if f.is_file():
            txt = f.read_text(encoding="utf-8", errors="ignore")
            m = _DESC.search(txt)
            if m:
                return m.group(1).strip().strip("\"'")[:160]
            for line in txt.splitlines():
                s = line.strip()
                if s and not s.startswith("---"):
                    return s.lstrip("# ").strip()[:160]
    for f in sorted(d.glob("*.md")):
        for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
            s = line.strip()
            if s and not s.startswith("---"):
                return s.lstrip("# ").strip()[:160]
    return ""


def build_tree(root_path: Path) -> "Node":
    """Mirror the directory nesting as a tree. A node = a subdirectory; a leaf = a dir with
    no subdirs. Hidden dirs (dotfiles) are skipped."""
    root = Node(name=root_path.name, path=root_path, description="(root)")

    def add(parent: "Node") -> None:
        subdirs = sorted(
            p for p in parent.path.iterdir()
            if p.is_dir() and not p.name.startswith(".")
        )
        for d in subdirs:
            child = Node(name=d.name, path=d, description=read_description(d))
            parent.children.append(child)
            add(child)

    add(root)
    return root


def render_folder_map(root: "Node") -> str:
    lines = [f"{root.coord}  {root.name}/"]

    def rec(node: "Node", prefix: str) -> None:
        n = len(node.children)
        for i, c in enumerate(node.children):
            last = i == n - 1
            branch = "└─ " if last else "├─ "
            desc = f"  — {c.description}" if c.description else ""
            lines.append(f"{prefix}{branch}{c.coord}  {c.name}{desc}")
            rec(c, prefix + ("   " if last else "│  "))

    rec(root, "")
    return "\n".join(lines)


def render_index(root: "Node") -> str:
    rows = ["| Coord | Skill | What it does | Path |", "|---|---|---|---|"]
    for n in root.walk():
        if n.coord == root.coord:
            continue
        rel = n.path.relative_to(root.path)
        rows.append(f"| `{n.coord}` | {n.name} | {n.description or '—'} | `{rel}/` |")
    return "\n".join(rows)


def render_branches(root: "Node") -> str:
    rows = []
    for n in root.walk():
        if n.children:
            rows.append(f"- `{n.coord}` **{n.name}** → {compose_summary(n)}")
    return "\n".join(rows) or "_(flat — every skill is a leaf at depth 1)_"


def build_map(root_path: Path) -> str:
    root = assign_coords(build_tree(root_path))
    n_skills = sum(1 for _ in root.walk()) - 1
    depth = max((n.coord.count(".") for n in root.walk()), default=0)
    return f"""# {root.name} — skill map

*Auto-generated by [skillmap](https://github.com/). {n_skills} skills, depth {depth}. Each skill
has a coordinate address — open a branch, descend to the coordinate you need. Don't load the
whole pile; navigate it.*

## Folder Map

```
{render_folder_map(root)}
```

## Index (addressable)

{render_index(root)}

## Branches (what each opens to)

{render_branches(root)}
"""


def main() -> None:
    ap = argparse.ArgumentParser(description="Map a folder of skills into a navigable, coordinate-addressed CLAUDE.md.")
    ap.add_argument("folder", help="folder of skills (e.g. ~/.claude/skills)")
    ap.add_argument("--write", action="store_true", help="write CLAUDE.md into the folder (default: print to stdout)")
    args = ap.parse_args()

    root_path = Path(args.folder).expanduser().resolve()
    if not root_path.is_dir():
        ap.error(f"not a folder: {root_path}")

    out = build_map(root_path)
    if args.write:
        dest = root_path / "CLAUDE.md"
        dest.write_text(out, encoding="utf-8")
        print(f"wrote {dest}")
    else:
        print(out)


if __name__ == "__main__":
    main()
