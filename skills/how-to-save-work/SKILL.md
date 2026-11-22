---
name: how-to-save-work
description: WHEN you are about to save an output of USING a project — an essay a compiler wrote, a render, a generated asset, a report, the notes or minutes of a meeting, a record of a run — save it in that project's own workspace folder, workspace/<kind>/<piece>/, making each folder that does not exist yet with its CLAUDE.md, then commit it by its own paths in the copy in use and push it. Everything made for one piece of work is saved with it, whatever it is made of, the code that makes one film's assets included. Not for a change to the project's program, what its next piece of work is made with (that is code, changed in a dev space), and not for a note about undone work — progress, a pending check, a reminder (that goes to the project's scratchpad).
---

# how-to-save-work — an output of using a project, saved where it belongs

You are holding something a project made while it was being used — whatever it is made of: the code that makes one
film's assets is part of that film, and is saved with it — and it is about to be saved. This skill says where
it goes, which folders you make on the way, and how it is saved. It is the procedure the always-loaded rules point to
when they name a project's `workspace/` (`top-level-session-worktree` THE TWO KINDS OF CHANGE, WORK).

## 1 — THE PLACE

The workspace is hierarchical. An AIOS's own work is its projects, each a folder in THE WORKSPACE (`user_info` binds
it), and everything the AI does happens in one of them; what a project produces goes in that project's own workspace:

```
<project>/workspace/<kind>/<piece>/
```

- `<project>` — the project whose use made the output: the folder whose `CLAUDE.md` and rules the work ran under.
- `<kind>` — one folder per kind of thing the project makes, named for that kind: an essay compiler's `homework/`;
  a Blender compiler's `trees/` and `characters/`.
- `<piece>` — inside a kind, its pieces arranged the way that kind needs: homework in dated folders
  (`homework/2026-11-12/`), assets one folder each (`trees/oak/`). A kind decides its arrangement the first time it
  is made, writes it in its own `CLAUDE.md`, and every later piece follows it.

## 2 — MAKE WHAT IS MISSING, AS THE WORK GOES

Check each level before the save. A level that does not exist, you make now — never in a pass over the projects, and
never ahead of an output that needs it. Each folder you make gets its `CLAUDE.md` and an empty
`.claude/{rules,skills,agents}`:

| folder | its `CLAUDE.md` says |
|---|---|
| `workspace/` | it holds the project's outputs, sorted by kind — one line per kind folder |
| `<kind>/` | what that kind of thing is and how its pieces are arranged — one line per piece |
| `<piece>/` | what that work is — and one line for every file in it, written the turn the file lands |

Copy nothing else in: a session working in the folder already loads every `CLAUDE.md`, rule and skill of the project
above it. A `CLAUDE.md` says what its folder is for and what is in it; how the work is going is a note, and a note goes
to the project's scratchpad (`the-host-aios-scratchpad`), never into a `CLAUDE.md`.

## 3 — SAVE IT AS WORK

An output is WORK: saved in THE COPY IN USE, on the default branch, by its own paths, and pushed the same turn — no
worktree, no pull request:

```
git add -- <the output> <every CLAUDE.md you made>
git commit -m "<what the output is, and what made it>" -- <the same paths>
git push
```

Git keeps no empty folder, so the empty `.claude/` folders live on disk only. A push refused because the default branch moved is met by a pull that only adds (`top-level-session-worktree` point
12), then a push again.

## 4 — WHEN THE WORKSPACE IS A WORK PATH

A project's `workspace/` is a work path only where nothing that acts when the default branch moves reaches into it:

- a project nothing publishes or deploys: its `workspace/` is a work path at once;
- a project a publisher or a deploy reaches: its `workspace/` is a work path once that system leaves the project's own
  `workspace/` out — of its copy, its change check and its choice of what a change touches — as that system's own
  design states and its own board shows that part built. Read that design and that board before the save. Until it does, the project's work is
  saved beside its folder, never inside it: the same `workspace/<kind>/<piece>/` shape, in a folder named
  `<project>-workspace/` next to the project's folder, outside every folder that publishes or deploys.

## 5 — PUBLISHING SOMETHING FROM A WORKSPACE

Nothing inside a workspace is ever published, except a folder named on purpose as a published artifact in the
installation's publisher's list — one piece, or a whole kind when every piece of that kind is meant to be public —
copied after a scan for secrets, since a workspace also holds private records. Where the publisher has no artifact kind
of entry yet, nothing in a workspace is published. Whether something is published is *USER*'s decision alone. An
artifact is not a release: it is something made by using a program, and it does not have to install and run.

## 6 — NEVER

- the project's program changed in a workspace — what its next piece of work is made with is code, changed in a dev
  space (`top-level-session-worktree`, CODE); code made for this one piece is the piece's own, saved with it
- a folder made in a pass ahead of the work, or a folder without its `CLAUDE.md`
- a file in a piece without its line in that piece's `CLAUDE.md`
- `git add -A`, or a path you did not change, in a copy several sessions save into
- an output saved inside a published or deployed project's `workspace/` before that project's publisher or deploy
  leaves the folder out

## NEXT

The output is on the default branch: `git log origin/<default>..<default>` is empty and the piece's `CLAUDE.md` names
it. A note the work left goes to the project's scratchpad now; a wish to make the output public is *USER*'s to rule,
then named as an artifact; the next output of the same kind goes into the same kind folder, arranged as its
`CLAUDE.md` says.
