# Tear down BY PID — `pkill -f` hits processes you did not launch

PRINCIPLE:[`pkill -f <pattern>` matches EVERY process on the host whose command line contains the
pattern · your own dev instance and the user's long-running daemon are launched by the SAME command,
so any pattern that finds yours finds theirs · the blast is invisible in the command's own output
(pkill prints nothing) and the damage shows up later as "the port is closed"]

TRIGGER:[tearing down anything started this session · about to type `pkill`/`killall`/`kill $(pgrep …)`
· any cleanup step at the end of a proof run]

DO:[
- CAPTURE THE PID AT LAUNCH (`nohup … & echo $!`) and kill THAT: `kill <pid>` → verify → `kill -9 <pid>`
- when the pid was lost, resolve the ONE process by its own port: `lsof -nP -iTCP:<myport> -sTCP:LISTEN -t`
- **BASELINE THE USER'S PROCESSES AT SESSION START** (`lsof -nP -iTCP:<their port>` + a `/health` curl)
  so a later "it is down" claim can be attributed instead of guessed at
- verify the teardown with an `lsof`/`ps` receipt, and verify THEIR daemon is still serving too
]
NOT:[
- `pkill -f` on any pattern naming a module/script the user also runs (`om_cave`, `server.py`,
  `uvicorn`, `vite`, `node`) — the pattern cannot tell your instance from theirs
- assume a SIGTERM is harmless because the process survives: it can close its LISTENER and keep
  running, so the process list still shows it while nothing is served
- restart the user's daemon to "fix" what you broke — a restart picks up every code change since it
  launched, which is a MATERIAL change to their environment and their call to make
  ([[canonical-source-dirs]]'s never-touch discipline). Report it, hand them the exact command, stop · the one restart
  that is the agent's: installing a released version into a program that stays running, as the last step of the git
  loop ([[top-level-session-worktree]] point 12) — by its pid, then checked to answer, with the user's other daemons
  checked still answering; THE PRECIOUS STORE never ([[the-precious-store]])
- report "my port is closed" as the whole teardown — check that THEIR daemon still answers too
]
