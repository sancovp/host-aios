#!/usr/bin/env python3
"""hook.py — THE TOP-LEVEL-DESIGN GATE on every write (a Claude Code PreToolUse hook).

Runs `check_top_level_design.check_text` — the one gate, imported, never a second copy — on the
document AS IT WOULD READ AFTER the Edit / MultiEdit / Write, and on the document as it reads
now. An edit that adds a finding the document did not already carry is REFUSED (exit 2, the new
findings on stderr, which Claude Code hands back to the agent). An edit that only removes
findings passes, so a document can be repaired one edit at a time; once it is clean, every
finding an edit would add is refused.

WHICH FILE: every top THE MASTER MAP names (the global rule at `<global home>/rules/master-map.md`, the global
home CLAUDE_CONFIG_DIR, else the home folder's `.claude`), and the map itself, which gets the map check; where no
map is there, the role THE TOP-LEVEL DESIGN, read from the installation's `user_info.md` (the gate's own binding
reader: the nearest `.claude/rules/user_info.md` above the edited file or the working directory). When neither
names a top, the hook says so on every edit (exit 1, which Claude Code shows and does not block), because a gate
that cannot find its document checks nothing. A file in another checkout of the same repository — a worktree — is the same document
when it sits at the same path inside the repository. Every other file passes untouched.

INSTALL — in the project settings of the repository that holds the top-level design:

    {"hooks": {"PreToolUse": [{"matcher": "Edit|MultiEdit|Write",
        "hooks": [{"type": "command",
                   "command": "f=\"<the AIOS's skills folder>/top-level-design/hook.py\"; if [ -f \"$f\" ]; then python3 \"$f\"; else echo \"the top-level-design gate is missing at $f, so this edit is not checked\" >&2; exit 1; fi"}]}]}}

CONTRACT (Claude Code PreToolUse): stdin = the hook payload {tool_name, tool_input}; exit 0 =
allow; exit 2 = block, stderr fed back to the agent. A payload it cannot read, or an edit whose
old text is not in the file, passes: the tool reports its own failure, and a broken hook never
blocks unrelated work.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import check_top_level_design as gate  # noqa: E402


def _repo(path: str) -> tuple[str, str] | None:
    """(git common dir, path relative to the worktree top) — or None outside git."""
    d = os.path.dirname(path) or "."
    try:
        top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, timeout=5).stdout.strip()
        common = subprocess.run(["git", "-C", d, "rev-parse", "--path-format=absolute", "--git-common-dir"],
                                capture_output=True, text=True, timeout=5).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None
    if not top or not common:
        return None
    return os.path.realpath(common), os.path.relpath(os.path.realpath(path), os.path.realpath(top))


def is_the_design(path: str, bound: str) -> bool:
    if os.path.realpath(path) == os.path.realpath(bound):
        return True
    a, b = _repo(path), _repo(bound)
    return bool(a and b and a == b)


def after_edit(before: str, tool: str, ti: dict) -> str | None:
    if tool == "Write":
        return ti.get("content")
    edits = ti.get("edits") if tool == "MultiEdit" else [ti]
    text = before
    for e in edits or []:
        old, new = e.get("old_string"), e.get("new_string")
        if old is None or new is None or old not in text:
            return None
        text = text.replace(old, new) if e.get("replace_all") else text.replace(old, new, 1)
    return text


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    tool = payload.get("tool_name") or ""
    ti = payload.get("tool_input") or {}
    path = ti.get("file_path") or ""
    if tool not in ("Edit", "MultiEdit", "Write") or not path:
        return 0
    the_map = gate.map_path()
    is_map = os.path.realpath(path) == os.path.realpath(the_map)
    if not is_map:
        tops, from_map = gate.tops(start=path)
        if not tops:
            where = (f"the master map at {from_map} names no top-level design that exists" if from_map else
                     f"no master map, and no user_info.md binding THE TOP-LEVEL DESIGN above {path} or the working "
                     "directory")
            print(f"⚠ the top-level-design gate found {where}, so this edit is not checked", file=sys.stderr)
            return 1
        if not any(is_the_design(path, t) for t in tops):
            return 0
    try:
        before = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        before = ""
    after = after_edit(before, tool, ti)
    if after is None:
        return 0

    if is_map:
        base = os.path.dirname(os.path.realpath(path))
        check = lambda text: gate.check_map(text, base)
    else:
        binding = gate.read_binding(start=path)
        check = lambda text: gate.check_text(text, binding)
    had = Counter(f.key for f in check(before)) if before else Counter()
    found = check(after)
    new, budget = [], Counter(had)
    for f in found:
        if budget[f.key] > 0:
            budget[f.key] -= 1
        else:
            new.append(f)
    if not new:
        return 0
    what = "THE MASTER MAP" if is_map else "THE TOP-LEVEL DESIGN"
    print(f"⛔ REFUSED — this edit adds to {what} what it may never carry:\n", file=sys.stderr)
    for f in new[:40]:
        print(f"   line {f.line:>5} · {f.kind:<14} · {f.snippet}  — {f.why}", file=sys.stderr)
    if len(new) > 40:
        print(f"   … and {len(new) - 40} more", file=sys.stderr)
    if is_map:
        print("\nThe master map holds its title line and one line per top-level design — what the top is and one "
              "link that resolves — and nothing more (law: rule 00-canonical-doc-paths).", file=sys.stderr)
    else:
        print("\nThe top-level design states only the design: no date, no quote, no replaced reading, no "
              "history, no patch block, no moved stub, no state of construction, no detail past a bridge. "
              "Rewrite the edit so it states the design itself (law: rule 00-top-level-design-is-an-lfp-rollup).",
              file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
