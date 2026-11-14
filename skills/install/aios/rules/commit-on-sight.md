# COMMIT ON SIGHT — never report uncommitted work, commit it

SCOPE:[binds the developer agent's own world — THE WORLD DIR, its repositories and its sessions — never a product's agents (a JobWorld seat or box, OM) or a customer's repositories, which follow their own product's design]

TRIGGER:[any `git status` showing modified/untracked files · any unpushed commit · about to write
or say the words "uncommitted" / "not committed" / "not yet committed" / "untracked" / "not
pushed" / "still dirty" · finishing any edit · any stage/goal/task closing · any repo entered]

DO:[
- commit THAT INSTANT, before writing anything else, by the kind of change ([[top-level-session-worktree]]): WORK —
  documents, notes, records, boards, a project's `workspace/` outputs (`how-to-save-work`), everything made for one piece of work whatever it is made of — on the default branch of the copy in use, by its
  own paths (`git add -- <its paths>`, then `git commit -m "<message>" -- <its paths>`), and pushed the same turn; CODE — a change to what the next piece of work is made with — on its worktree's branch,
  staying local while the set of code is in progress
- commit work found in ANY repo, not only the one being worked in, by its own paths, the same turn — a sweep that finds
  dirt in a neighbouring checkout commits it there too · except in a copy in use where another session may be at work:
  there, commit only your own paths, and name the rest in one clause of the report — a file another session changed
  and has not committed is that session's · code found uncommitted in a copy in use is never committed onto its default
  branch: carry it into a worktree's branch, or name it
- commit first, then mention it in one clause of the report at most ("committed X found on sight")
- write a real message: what the change is, why it exists
- push WORK the same turn it is committed; push CODE only when a whole set of code is done (then ONE ready PR), or once
  before a session ends so nothing is lost — never after each edit, and NEVER to the default branch of a repository that
  has a merge queue (a push of code there runs agents and skips the queue); a repository whose own rules commit straight
  to its default branch pushes per set too
- respect the worktree law while doing it ([[subagent-worktree-isolation]], [[top-level-session-worktree]]) — WORK in
  the copy in use, CODE on its worktree's branch, never moved to another checkout to commit it
]

NOT:[
- push code to a merge-queue repository's default branch, ever — not for a "minor" edit
- `git add -A` in a copy in use several sessions save into, or commit a path you did not change
- push code, open a PR, or ask for the queue, per edit — one push and one PR per finished set of code
- report uncommitted state as a finding, a status line, a residue row, or a "flag"
- leave dirt for a later stage / a later window / the human
- ask whether to commit
- describe the dirty state in prose instead of clearing it
]

NOTE:[reporting dirt instead of clearing it costs a full roundtrip to produce an instruction that
was already standing — the fix is always the same action, so take it]
