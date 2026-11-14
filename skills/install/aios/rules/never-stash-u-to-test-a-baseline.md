# `git stash -u` DELETES EMPTY UNTRACKED DIRS — and `pop` never brings them back

PRINCIPLE:[`git stash push -u` runs a `git clean -fd`-shaped sweep · untracked FILES are saved and
restored · **an empty untracked DIRECTORY is deleted and stored nowhere**, because git has no object
for an empty dir · so `stash -u` → `stash pop` is NOT round-trip-safe on directory structure]

TRIGGER:[about to run `git stash -u` / `git stash push -u` / `git clean -fd` · about to "stash to
check whether an error is pre-existing" · any temporary-revert to compare a baseline]

DO:[
- scope the stash to the paths under test: `git stash push -- <path> [<path>…]` (no `-u`)
- or compare in a THROWAWAY WORKTREE off the ref (`git worktree add --detach <ref>`) and run the
  check there — the working tree is never disturbed ([[subagent-worktree-isolation]], same law)
- or just read the config: a `tsc`/lint error naming a compilerOption or a missing type package is
  pre-existing by inspection; no revert needed
- if `-u` already ran: report it immediately ([[user_comms]]) — say that empty dirs were removed,
  that the loss is directory EXISTENCE only (no file content), and name what depended on them
]
NOT:[
- `git stash -u` in a repo whose empty dirs are LOAD-BEARING — and in this ecosystem they are:
  [[00-every-dir-has-a-claude-and-projects-nest]] mandates `.claude/{rules,skills,agents}` in every
  dir and says they MAY BE EMPTY, and any dir-scanning feature (the woom devdir walk, the AIOS
  roster, the onion tree) reads a dir's devdirs as its identity — so deleting an empty `.claude/`
  silently deletes that dir's membership in the world
- assume `pop` restored everything because `git status` came back clean — status never shows an
  empty dir, so the loss is INVISIBLE to the check you would naturally run
- count on recovering a deleted empty dir — git holds no object for it
]
