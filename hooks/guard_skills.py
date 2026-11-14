#!/usr/bin/env python3
"""guard_skills.py — the host AIOS's skill guard (DESIGN.md §8.7): a skill is opened where its trigger fires.

A Claude Code PreToolUse hook on Write, Edit and MultiEdit. Every kind of file whose making a skill holds, at a place a
program can tell, is written only after that skill is opened by the agent that writes it: it refuses the write while
that agent's transcript shows the skill not yet opened — no Skill call naming it, no Read of its SKILL.md — and names
the skill to open; once it is opened, every later write of that kind passes. The agent is the session itself, or a
helper agent: for a helper agent's tool call Claude Code names it in the payload (`agent_id`) while `transcript_path`
stays the session's, and keeps the helper's own events beside it, in `<session>/subagents/agent-<agent_id>.jsonl` — so
that is the transcript read, and a skill only the session opened does not count, since the helper's context never held
it.

    a `DESIGN.md`                                   the `design-md` skill and the `design-toc` skill
    a design's table of contents, `design_toc.md`   the `design-toc` skill
    a board, `*_states.md`                          the `state-file` skill
    an architecture map, `21-architecture-diagrams.md`   the `archi-diagram` skill
    a top-level design, `TOP-LEVEL-DESIGN.md`      the `top-level-design` skill
    the master map, `rules/master-map.md`          the `top-level-design` skill
    a goal file, `.claude/goals/<name>.md`         the `setup-goal` skill
    a ground truth, `GROUND_TRUTH_<datetime>.md`   the `ground-truth` skill
    a file in the rule-draft box — inside a place the nearest `.claude/rules/user_info.md` above the file, or above the
      session's folder, binds to THE RULE-DRAFT BOX                                 the `rule-draft-box` skill
    a project's own output — a file under the `workspace/` of a folder holding a `DESIGN.md`, or under the
      `<project>-workspace/` beside such a folder                                   the `how-to-save-work` skill

    stdin   the hook payload {tool_name, tool_input, transcript_path, cwd, and agent_id for a helper agent's call}
    exit 0  allowed · exit 2 refused, the skill to open on stderr, which Claude Code hands back to the agent

Its blind spot, stated with it: a file written through the shell is not seen here — the rules bind it. A payload, a
transcript or a binding file it cannot read passes, because a guard that fails closed on its own error would stop every
write. Standard library only.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

TOOLS = {"Write", "Edit", "MultiEdit"}
KINDS = [
    (re.compile(r"(^|/)DESIGN\.md$"), "a DESIGN.md", ("design-md", "design-toc"), "rule 26-canonical-design"),
    (re.compile(r"(^|/)design_toc\.md$"), "a design's table of contents", ("design-toc",),
     "rule design-docs-keep-a-toc"),
    (re.compile(r"(^|/)[^/]*_states\.md$"), "a board", ("state-file",), "rule 28-distributed-state"),
    (re.compile(r"(^|/)21-architecture-diagrams\.md$"), "an architecture map", ("archi-diagram",),
     "rule 23-architecture-layer"),
    (re.compile(r"(^|/)TOP-LEVEL-DESIGN\.md$"), "a top-level design", ("top-level-design",),
     "rule 00-top-level-design-is-an-lfp-rollup"),
    (re.compile(r"(^|/)rules/master-map\.md$"), "the master map", ("top-level-design",), "rule 00-canonical-doc-paths"),
    (re.compile(r"(^|/)\.claude/goals/[^/]+\.md$"), "a goal file", ("setup-goal",), "rule 22-seq-write-a-goal"),
    (re.compile(r"(^|/)GROUND_TRUTH_[^/]*\.md$"), "a ground truth", ("ground-truth",), "rule 00-samaya §V"),
]
BOX = ("a draft in the rule-draft box", ("rule-draft-box",), "the boot config's THE RULESET")
OUTPUT = ("a project's own output", ("how-to-save-work",), "rule top-level-session-worktree, THE TWO KINDS OF CHANGE")
BOX_ROW = re.compile(r"^\|\s*\*\*THE RULE-DRAFT BOX\*\*")


def opened(transcript: str) -> set[str] | None:
    """The skills the session has opened — by a Skill call, or a Read of a skill's SKILL.md — or None if unreadable."""
    try:
        lines = Path(transcript).expanduser().read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    found: set[str] = set()
    for line in lines:
        if '"tool_use"' not in line:
            continue
        try:
            e = json.loads(line)
        except ValueError:
            continue
        for b in (e.get("message") or {}).get("content") or []:
            if not isinstance(b, dict) or b.get("type") != "tool_use":
                continue
            inp = b.get("input") or {}
            if b.get("name") == "Skill":
                name = str(inp.get("skill") or inp.get("command") or "").split(":")[-1].strip("/ ")
                if name:
                    found.add(name)
            elif b.get("name") == "Read" and str(inp.get("file_path") or "").endswith("/SKILL.md"):
                found.add(Path(str(inp["file_path"])).parent.name)
    return found


def writers_transcript(payload: dict) -> str:
    """The transcript of the agent making the call: the session's, or a helper agent's own beside it."""
    session = str(payload.get("transcript_path") or "")
    agent = str(payload.get("agent_id") or "")
    if not (session and agent):
        return session
    s = Path(session)
    return str(s.parent / s.stem / "subagents" / f"agent-{agent}.jsonl")


def boxes(*starts: Path) -> list[Path]:
    """Each place bound to THE RULE-DRAFT BOX by the nearest `.claude/rules/user_info.md` above each start."""
    found: list[Path] = []
    for start in starts:
        for d in (start, *start.parents):
            f = d / ".claude" / "rules" / "user_info.md"
            if not f.is_file():
                continue
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                break
            for line in text.splitlines():
                if BOX_ROW.match(line):
                    cell = line.rstrip().rstrip("|").rsplit("|", 1)[-1]
                    found += [Path(os.path.expanduser(p)).resolve() for p in re.findall(r"`([^`]+)`", cell)
                              if p.startswith(("/", "~"))]
            break
    return found


def is_output(path: Path) -> bool:
    """A file under a project's own `workspace/`, or under the `<project>-workspace/` beside the project's folder."""
    for d in path.parents:
        if d.name == "workspace" and (d.parent / "DESIGN.md").is_file():
            return True
        stem = d.name[: -len("-workspace")] if d.name.endswith("-workspace") else ""
        if stem and (d.parent / stem / "DESIGN.md").is_file():
            return True
    return False


def kind_of(raw: str, cwd: str) -> tuple[str, tuple[str, ...], str] | None:
    """What kind of file a write of `raw` makes, or None for a file no skill holds the making of."""
    named = next(((k[1], k[2], k[3]) for k in KINDS if k[0].search(raw)), None)
    if named:
        return named
    path = Path(raw)
    starts = [path.parent] + ([Path(cwd)] if cwd else [])
    try:
        resolved = path.resolve()
        if any(resolved == b or b in resolved.parents for b in boxes(*starts)):
            return BOX
        if is_output(path):
            return OUTPUT
    except (OSError, RuntimeError, ValueError):
        return None
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    if not isinstance(payload, dict) or payload.get("tool_name") not in TOOLS:
        return 0
    raw = str((payload.get("tool_input") or {}).get("file_path") or "")
    if not raw:
        return 0
    kind = kind_of(raw, str(payload.get("cwd") or ""))
    if not kind:
        return 0
    have = opened(writers_transcript(payload))
    if have is None:
        return 0
    what, skills, law = kind
    missing = [s for s in skills if s not in have]
    if not missing:
        return 0
    names = " and ".join(f"`{s}`" for s in missing)
    print(f"⛔ REFUSED — this writes {what} ({Path(raw).name}), and the {names} skill{'s' if len(missing) > 1 else ''} "
          f"that hold{'' if len(missing) > 1 else 's'} how {what} is made and the gate it passes "
          f"{'are' if len(missing) > 1 else 'is'} not opened by this agent ({law}).\n"
          f"Remedy: open {names} with the Skill tool, by name, read what {'they say' if len(missing) > 1 else 'it says'}, "
          f"then make the file through {'them' if len(missing) > 1 else 'it'}; its gate is the script in the folder Claude "
          f"Code names as the skill's base directory when it loads — never searched for on disk.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
