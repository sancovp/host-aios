#!/usr/bin/env python3
"""check.py — the host AIOS's check hook (DESIGN.md §0.6, the check hook), run at every session start.

The AIOS folder it checks is the one the session works in — the nearest folder at or above the session's working
folder that holds the install's record — else the one the global home's CLAUDE.md names in the one line the install
script writes. It compares that folder's CLAUDE.md and `.claude/rules/` with the install skill's resources
(`skills/install/aios/` in this plugin) by sha256 — `user_info.md` checked only to be there, since the installer fills
it out — and reads the master map at the global home (`rules/master-map.md`), naming each line whose top-level design is
missing. It prints one line: the folder whole, or each file missing, changed or extra; or that nothing is installed;
then what the map holds. It exits 0 every time and never refuses the session. The global home is CLAUDE_CONFIG_DIR, else
the home folder's `.claude`, as the install script finds it; the plugin's folder is CLAUDE_PLUGIN_ROOT, else the folder
above this file's; the session's working folder is the `cwd` the session-start payload names, else this process's.

    python3 check.py
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import select
import sys
from pathlib import Path

POINTER = re.compile(r"^BEFORE ANYTHING ELSE, ALWAYS READ (.+)/CLAUDE\.md WITH READ\(\)$")
USER_INFO = "user_info.md"
RECORD = Path(".claude") / "host-aios-install.json"
MAP = Path("rules") / "master-map.md"
_LINK = re.compile(r"\[[^\]]+\]\(\s*<?([^)\s>]+)>?\s*\)")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def global_home() -> Path:
    if os.environ.get("CLAUDE_CONFIG_DIR"):
        return Path(os.environ["CLAUDE_CONFIG_DIR"]).expanduser()
    return Path.home() / ".claude"


def plugin_root() -> Path:
    return Path(os.environ.get("CLAUDE_PLUGIN_ROOT") or Path(__file__).resolve().parent.parent)


def session_cwd() -> Path:
    """The session's working folder: the `cwd` of the session-start payload on stdin, when one is there, else ours."""
    try:
        if not sys.stdin.isatty() and select.select([sys.stdin], [], [], 0.2)[0]:
            cwd = json.loads(sys.stdin.read() or "{}").get("cwd")
            if cwd:
                return Path(cwd)
    except (OSError, ValueError, AttributeError):
        pass
    return Path.cwd()


def session_folder(cwd: Path) -> Path | None:
    """The nearest folder at or above `cwd` that holds the install's record."""
    for d in (cwd, *cwd.parents):
        if (d / RECORD).is_file():
            return d
    return None


def map_text() -> str:
    """What the master map at the global home says: every line names a top-level design that exists, or which do not."""
    m = global_home() / MAP
    if not m.is_file():
        return "no master map at the global home"
    missing, n = [], 0
    for line in m.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("- "):
            continue
        n += 1
        for t in _LINK.findall(line)[:1]:
            p = Path(os.path.expanduser(t))
            if not (p if p.is_absolute() else m.parent / p).is_file():
                missing.append(t)
    if missing:
        return f"the master map: {len(missing)} of its {n} line(s) name a top-level design that is missing — {', '.join(missing)}"
    return f"the master map: each of its {n} line(s) names a top-level design that exists"


def check(cwd: Path | None = None) -> str:
    folder = session_folder(cwd or Path.cwd())
    if folder is None:
        pointer_file = global_home() / "CLAUDE.md"
        if not pointer_file.is_file():
            return ("host AIOS: nothing installed — the global home holds no CLAUDE.md pointing to an AIOS folder; run "
                    "the install skill")
        lines = [line for line in pointer_file.read_text(encoding="utf-8").splitlines() if line.strip()]
        found = POINTER.match(lines[0]) if len(lines) == 1 else None
        if not found:
            return ("host AIOS: nothing installed — the global home's CLAUDE.md holds other instructions, not the one "
                    "line the install skill writes")
        folder = Path(found.group(1))
    res = plugin_root() / "skills" / "install" / "aios"
    version = json.loads((res / "manifest.json").read_text(encoding="utf-8")).get("version", "?")
    want = {"CLAUDE.md": res / "CLAUDE.md"}
    want.update({f".claude/rules/{p.name}": p for p in sorted((res / "rules").glob("*.md"))})
    rules = folder / ".claude" / "rules"
    have = {f".claude/rules/{p.name}" for p in rules.glob("*.md")} if rules.is_dir() else set()
    missing, changed = [], []
    for rel, src in want.items():
        target = folder / rel
        if not target.is_file():
            missing.append(rel)
        elif Path(rel).name != USER_INFO and sha(target) != sha(src):
            changed.append(rel)
    extra = sorted(have - set(want))
    if not (missing or changed or extra):
        return (f"host AIOS: whole — {folder} holds the boot config and all {len(want) - 1} rules of version {version} "
                f"· {map_text()}")
    parts = [f"{label}: {', '.join(items)}" for label, items in
             (("missing", missing), ("changed", changed), ("extra", extra)) if items]
    return (f"host AIOS: {folder} is not whole against version {version} — " + " · ".join(parts)
            + f" (the install skill restores what it placed; a changed file it refuses to overwrite) · {map_text()}")


def main() -> int:
    try:
        print(check(session_cwd()))
    except Exception as e:                                  # the hook never refuses a session
        print(f"host AIOS: the check could not run — {type(e).__name__}: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
