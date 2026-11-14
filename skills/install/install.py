#!/usr/bin/env python3
"""install.py — the host AIOS's install script (DESIGN.md §0.6, the install script): it lays a user's folders out as
the author's are, so the global home holds only a pointer down to the folder that holds the AIOS.

    python3 install.py --folder DIR [--global-home DIR]

What it writes, all from its resources beside it (`aios/`, which the plugin's build writes from the template, and
`starter/`):
  <folder>/CLAUDE.md                        the boot config
  <folder>/.claude/rules/<rule>             every rule — `user_info.md` placed only while absent: the installer fills it out
  <folder>/TOP-LEVEL-DESIGN.md              the starter top-level design, placed only while absent: the folder's own top
  <folder>/workspace/CLAUDE.md              the workspace's index, placed only while absent: THE WORKSPACE, where every
                                            project the AI works in is a folder, one line each; its .claude/ scaffold empty
  <folder>/.claude/skills/ · agents/        empty: the skills reach the folder from the plugin, turned on for it
  <folder>/.claude/settings.json            turns the plugin on for every session in the folder
  <folder>/.claude/host-aios-install.json   the record: the version, the global home, the map, every file placed and
                                            its sha256
  <global home>/CLAUDE.md                   one line — read the folder's CLAUDE.md before anything else; a line already
                                            pointing to another folder that holds an install is left as it is
  <global home>/rules/master-map.md         THE MASTER MAP: its title line, then one line linking each folder's top-level
                                            design — written with this folder's line, or this folder's line added to it
The global home is --global-home, else CLAUDE_CONFIG_DIR, else the home folder's `.claude`.

It refuses first, changing nothing and naming each file: a target holding a file it did not write (bytes that are
neither what it would write nor what its record says it placed), a file it placed that has since been changed, a map at
the map's place that does not open with the map's title line, and a folder whose map line would pass 200 characters. A
second run at the same version changes nothing; a run at a newer version replaces only its own unchanged files, removes
its own unchanged files the new version no longer holds, and keeps a filled-out `user_info.md`.

Standard library only. It prints one JSON report; exit 0 installed or already current, 1 refused.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESOURCES = HERE / "aios"
STARTER = HERE / "starter" / "TOP-LEVEL-DESIGN.md"
WS_STARTER = HERE / "starter" / "workspace-CLAUDE.md"
RECORD = ".claude/host-aios-install.json"
USER_INFO = ".claude/rules/user_info.md"
TOP = "TOP-LEVEL-DESIGN.md"
WS_INDEX = "workspace/CLAUDE.md"
INSTALLERS_OWN = (USER_INFO, TOP, WS_INDEX)           # placed only while absent; the installer's own once placed
EMPTY = (".claude/skills", ".claude/agents", "workspace/.claude/rules", "workspace/.claude/skills", "workspace/.claude/agents")
MAP = "rules/master-map.md"
MAP_TITLE = ("# THE MASTER MAP — every top-level design, one line and one link each; find the top that holds the work "
             "here and read only that top")
MAP_LINE_MAX = 200
POINTER = re.compile(r"^BEFORE ANYTHING ELSE, ALWAYS READ (.+)/CLAUDE\.md WITH READ\(\)$")
_LINK = re.compile(r"\[[^\]]+\]\(\s*<?([^)\s>]+)>?\s*\)")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def global_home(given: str | None) -> Path:
    """The configuration folder Claude Code uses: --global-home, else CLAUDE_CONFIG_DIR, else the home's `.claude`."""
    if given:
        return Path(given).expanduser().resolve()
    if os.environ.get("CLAUDE_CONFIG_DIR"):
        return Path(os.environ["CLAUDE_CONFIG_DIR"]).expanduser().resolve()
    return (Path.home() / ".claude").resolve()


def pointer(folder: Path) -> bytes:
    """The one line the global home's CLAUDE.md holds — the same order the author's global home holds."""
    return f"BEFORE ANYTHING ELSE, ALWAYS READ {folder / 'CLAUDE.md'} WITH READ()\n".encode("utf-8")


def resources() -> tuple[dict[str, bytes], dict]:
    """What the folder holds, relative to it, from the resources beside this script; and their manifest."""
    manifest = json.loads((RESOURCES / "manifest.json").read_text(encoding="utf-8"))
    files = {"CLAUDE.md": (RESOURCES / "CLAUDE.md").read_bytes()}
    for p in sorted((RESOURCES / "rules").glob("*.md")):
        files[f".claude/rules/{p.name}"] = p.read_bytes()
    files[".claude/settings.json"] = (json.dumps({"enabledPlugins": {manifest["plugin"]: True}}, indent=2)
                                      + "\n").encode("utf-8")
    files[TOP] = STARTER.read_bytes()
    files[WS_INDEX] = WS_STARTER.read_bytes()
    return files, manifest


def pointed_elsewhere(home: Path, folder: Path) -> Path | None:
    """The other AIOS folder the global home's one line already points to — one holding an install record — or None."""
    p = home / "CLAUDE.md"
    if not p.is_file() or p.is_symlink():
        return None
    lines = [line for line in p.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip()]
    found = POINTER.match(lines[0]) if len(lines) == 1 else None
    if not found:
        return None
    other = Path(found.group(1))
    return other if other != folder and (other / RECORD).is_file() else None


def map_line(folder: Path, map_dir: Path) -> str:
    """This folder's line on the master map: what the top is, and one link to its top-level design — the link a
    `~/` path where the folder is under the home folder, else its absolute path, and a path relative to the map's own
    folder where that line would pass the map's limit."""
    top, home = folder / TOP, Path.home().resolve()
    links = [f"~/{top.relative_to(home)}"] if home in top.parents else []
    links += [str(top), os.path.relpath(top, map_dir)]
    lines = [f"- the AIOS in {folder.name} — [its top-level design]({link})" for link in links]
    return next((x for x in lines if len(x) <= MAP_LINE_MAX), min(lines, key=len))


def links_to(line: str, target: Path, base: Path) -> bool:
    for t in _LINK.findall(line):
        p = Path(os.path.expanduser(t))
        if (p if p.is_absolute() else base / p).resolve() == target.resolve():
            return True
    return False


def map_plan(home: Path, folder: Path) -> tuple[dict | None, dict | None]:
    """The master map's action — written with this folder's line, the line added, or nothing — or its refusal."""
    m = home / MAP
    line = map_line(folder, m.parent)
    if len(line) > MAP_LINE_MAX:
        return None, {"path": str(m), "why": f"this folder's map line would be {len(line)} characters, over the "
                                             f"{MAP_LINE_MAX} a map line holds — install into a folder with a shorter path"}
    if m.is_symlink() or (m.exists() and not m.is_file()):
        return None, {"path": str(m), "why": "is there and is not a file it wrote"}
    if not m.exists():
        return {"do": "place", "path": str(m), "data": f"{MAP_TITLE}\n\n{line}\n".encode("utf-8")}, None
    text = m.read_text(encoding="utf-8", errors="replace")
    first = next((x for x in text.splitlines() if x.strip()), None)
    if first != MAP_TITLE:
        return None, {"path": str(m), "why": "a file is at the master map's place without the map's title line — a "
                                             "file this install did not write"}
    if any(links_to(x, folder / TOP, m.parent) for x in text.splitlines() if x.startswith("- ")):
        return {"do": "unchanged", "path": str(m), "data": None}, None
    return {"do": "add-line", "path": str(m),
            "data": (text if text.endswith("\n") else text + "\n").encode("utf-8") + f"{line}\n".encode("utf-8")}, None


def read_record(folder: Path) -> dict:
    p = folder / RECORD
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def plan(folder: Path, home: Path, want: dict[str, bytes], record: dict) -> tuple[list[dict], list[dict]]:
    """Every action the install takes, and every refusal — decided before anything is written."""
    placed = record.get("files", {})                     # path (folder-relative, or the global CLAUDE.md's) -> sha256
    targets = {str(folder / rel): data for rel, data in want.items()}
    if not pointed_elsewhere(home, folder):
        targets[str(home / "CLAUDE.md")] = pointer(folder)
    own = {str(folder / rel) for rel in INSTALLERS_OWN}
    actions, refused = [], []
    for path, data in sorted(targets.items()):
        p = Path(path)
        if p.is_symlink() or (p.exists() and not p.is_file()):
            refused.append({"path": path, "why": "is there and is not a file it wrote"})
            continue
        if not p.exists():
            actions.append({"do": "place", "path": path, "data": data})
            continue
        have = sha(p.read_bytes())
        if have == sha(data):
            actions.append({"do": "unchanged", "path": path, "data": data})
        elif path in own and path in placed:
            actions.append({"do": "keep", "path": path, "data": None})       # the installer's own, filled out
        elif placed.get(path) == have:
            actions.append({"do": "replace", "path": path, "data": data})     # its own, at an older version
        elif path in placed:
            refused.append({"path": path, "why": "it placed this file and it has been changed since"})
        else:
            refused.append({"path": path, "why": "it holds a file this install did not write"})
    for path, recorded in sorted(placed.items()):
        if path in targets or path == str(home / "CLAUDE.md"):           # the global home's line is never removed
            continue
        p = Path(path)
        if not p.exists():
            continue
        if p.is_file() and sha(p.read_bytes()) == recorded:
            actions.append({"do": "remove", "path": path, "data": None})      # its own, no longer in this version
        else:
            refused.append({"path": path, "why": "it placed this file, this version no longer holds it, and it has "
                                                 "been changed since"})
    return actions, refused


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="install the host AIOS into a folder of its own")
    ap.add_argument("--folder", required=True, help="the folder that holds the AIOS")
    ap.add_argument("--global-home", help="Claude Code's configuration folder (default: CLAUDE_CONFIG_DIR, else ~/.claude)")
    a = ap.parse_args(argv)
    folder = Path(a.folder).expanduser().resolve()
    home = global_home(a.global_home)
    want, manifest = resources()
    try:
        record = read_record(folder)
    except (OSError, ValueError) as e:
        print(json.dumps({"ok": False, "refused": [{"path": str(folder / RECORD), "why": f"unreadable: {e}"}]},
                         indent=2))
        return 1
    if folder == home or home in folder.parents:
        print(json.dumps({"ok": False, "refused": [{"path": str(folder), "why": "the folder is inside the global home; "
                          "the global home holds only the pointer down to it"}]}, indent=2))
        return 1
    actions, refused = plan(folder, home, want, record)
    map_act, map_refused = map_plan(home, folder)
    if map_refused:
        refused.append(map_refused)
    if refused:
        print(json.dumps({"ok": False, "folder": str(folder), "global_home": str(home), "refused": refused}, indent=2))
        return 1

    files = {}
    for act in actions:
        p = Path(act["path"])
        if act["do"] in ("place", "replace"):
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(act["data"])
        elif act["do"] == "remove":
            p.unlink()
            continue
        files[act["path"]] = sha(p.read_bytes())
    for rel in EMPTY:
        (folder / rel).mkdir(parents=True, exist_ok=True)
    if map_act["do"] in ("place", "add-line"):
        mp = Path(map_act["path"])
        mp.parent.mkdir(parents=True, exist_ok=True)
        mp.write_bytes(map_act["data"])
    new_record = {"version": manifest["version"], "plugin": manifest["plugin"], "global_home": str(home),
                  "map": map_act["path"], "files": dict(sorted(files.items()))}
    text = json.dumps(new_record, indent=2) + "\n"
    rp = folder / RECORD
    if not rp.is_file() or rp.read_text(encoding="utf-8") != text:
        rp.write_text(text, encoding="utf-8")
    by = lambda kind: [act["path"] for act in actions if act["do"] == kind]
    print(json.dumps({"ok": True, "version": manifest["version"], "folder": str(folder), "global_home": str(home),
                      "placed": by("place"), "replaced": by("replace"), "removed": by("remove"), "kept": by("keep"),
                      "unchanged": len(by("unchanged")), "map": {"path": map_act["path"], "do": map_act["do"]},
                      "global_line": "points to this folder" if str(home / "CLAUDE.md") in files else
                                     "left pointing to another folder that holds an install"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
