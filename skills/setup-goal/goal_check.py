#!/usr/bin/env python3
"""goal_check.py — the checksums of a goal file's conditions, recorded as the run goes and verified.

A goal file's `## §2` holds EVERY condition the run must meet, one per line:

    - C<n> · <the condition>                                              open
    - C<n> · <the condition> · proof: <file> · sha256: <16 hex digits>    met

<file> is the evidence the run wrote (a test's output, a command's output, a screenshot), relative to the goal
file's own directory; the sha256 is that file's, so anyone can re-check a met condition. The prompt in `## §0`
lists no condition — the file is the only list.

    goal_check.py <goal>                         verify; print each condition open or met
    goal_check.py <goal> --record C<n> <file>    record a met condition: its proof file and that file's checksum
    goal_check.py <goal> --add "<condition>"     add a condition the design requires and §2 lacked

The list only grows: every condition the goal file holds on the default branch (origin's HEAD, or --base <ref>)
must still be here with its words unchanged — a condition is never dropped or reworded.

EXIT 0 every condition met, every checksum right, nothing dropped · 2 conditions still open (the run is not
done) · 1 REFUSED: a dropped or reworded condition, a checksum that does not match its file, a prompt that
lists a condition, or a malformed §2.
"""
import hashlib
import os
import re
import subprocess
import sys

LINE = re.compile(r"^- (C\d+) · (.+?)(?: · proof: (\S+) · sha256: ([0-9a-f]{16}))?$")
CLOSERS = ("SHIPPED", "NEEDS-ASKING", "FIXPOINT")


def file_sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def section(lines, head):
    start = next((i for i, l in enumerate(lines) if l.startswith("## " + head)), None)
    if start is None:
        return None
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return start + 1, end


def conditions(lines):
    """[(line index, id, text, proof, sha)] for every `- C` line in §2; malformed lines as (i, None, line, ...)."""
    span = section(lines, "§2")
    if span is None:
        return None
    out = []
    for i in range(*span):
        if not lines[i].startswith("- C"):
            continue
        m = LINE.match(lines[i])
        out.append((i, *m.groups()) if m else (i, None, lines[i], None, None))
    return out


def baseline(path, ref):
    """The conditions this goal file holds at the default branch, as {id: text}; {} when it is not there yet."""
    d = os.path.dirname(os.path.abspath(path))
    git = lambda *a: subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)
    top = git("rev-parse", "--show-toplevel")
    if top.returncode:
        return {}
    if not ref:
        head = git("symbolic-ref", "--short", "refs/remotes/origin/HEAD")
        ref = head.stdout.strip() if head.returncode == 0 else "origin/main"
    rel = os.path.relpath(os.path.abspath(path), top.stdout.strip())
    shown = git("show", f"{ref}:{rel}")
    if shown.returncode:
        return {}
    conds = conditions(shown.stdout.rstrip("\n").split("\n")) or []
    return {c[1]: c[2] for c in conds if c[1]}


def write(path, lines):
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


def record(path, lines, cid, proof):
    goal_dir = os.path.dirname(os.path.abspath(path))
    full = proof if os.path.isabs(proof) else os.path.join(goal_dir, proof)
    if not os.path.isfile(full):
        sys.exit(f"REFUSED: no proof file at {full}")
    rel = os.path.relpath(os.path.abspath(full), goal_dir)
    for i, c, text, _, _ in conditions(lines) or []:
        if c == cid:
            lines[i] = f"- {c} · {text} · proof: {rel} · sha256: {file_sha(full)}"
            write(path, lines)
            return
    sys.exit(f"REFUSED: no condition {cid} in §2")


def add(path, lines, text):
    conds = conditions(lines)
    if conds is None:
        sys.exit("REFUSED: no `## §2` section")
    n = 1 + max([int(c[1][1:]) for c in conds if c[1]] or [0])
    at = (conds[-1][0] + 1) if conds else section(lines, "§2")[0]
    lines.insert(at, f"- C{n} · {text.strip()}")
    write(path, lines)


def verify(path, lines, ref):
    problems, open_ = [], []
    conds = conditions(lines)
    if conds is None:
        return ["no `## §2` section"], []
    if not conds:
        problems.append("§2 holds no condition")
    goal_dir = os.path.dirname(os.path.abspath(path))
    seen = {}
    for i, cid, text, proof, sha in conds:
        if cid is None:
            problems.append(f"line {i + 1}: not `- C<n> · <condition>` with an optional ` · proof: <file> · sha256: <16 hex>`")
            continue
        if cid in seen:
            problems.append(f"{cid} appears twice")
        seen[cid] = text
        if proof is None:
            open_.append(cid)
            print(f"{cid} open")
            continue
        full = os.path.join(goal_dir, proof)
        if not os.path.isfile(full):
            problems.append(f"{cid}: its proof {proof} does not exist")
            print(f"{cid} BAD  {proof} missing")
        elif file_sha(full) != sha:
            problems.append(f"{cid}: {proof} no longer matches its checksum {sha} — re-prove it and record it again")
            print(f"{cid} BAD  {proof}")
        else:
            print(f"{cid} met  {sha}  {proof}")
    for word in CLOSERS:
        if not any(t.startswith(word) for t in seen.values()):
            problems.append(f"no {word} condition — SHIPPED, NEEDS-ASKING and FIXPOINT are always in §2")
    for cid, text in baseline(path, ref).items():
        if cid not in seen:
            problems.append(f"{cid} was dropped — the default branch's goal file holds it; a condition is never removed")
        elif seen[cid] != text:
            problems.append(f"{cid} was reworded — the default branch's goal file says: {text}")
    span0 = section(lines, "§0")
    if span0 is not None:
        for i in range(*span0):
            if re.match(r"^\s*(\d+\.|- C\d+)\s", lines[i]):
                problems.append(f"line {i + 1}: the prompt lists a condition — conditions live only in §2")
    return problems, open_


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    path = args[0]
    ref = args[args.index("--base") + 1] if "--base" in args else None
    lines = open(path).read().rstrip("\n").split("\n")
    if "--record" in args:
        k = args.index("--record")
        record(path, lines, args[k + 1], args[k + 2])
    elif "--add" in args:
        add(path, lines, args[args.index("--add") + 1])
    lines = open(path).read().rstrip("\n").split("\n")
    problems, open_ = verify(path, lines, ref)
    for p in problems:
        print("REFUSED:", p)
    if problems:
        sys.exit(1)
    print(f"{len(open_)} open" if open_ else "ALL MET")
    sys.exit(2 if open_ else 0)


if __name__ == "__main__":
    main()
