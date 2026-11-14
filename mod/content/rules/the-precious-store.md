# THE PRECIOUS STORE — never rebuild, never recreate, back up first

TARGET:[**THE PRECIOUS STORE** — the one store this installation binds as never-rebuilt ([[user_info]] THE BINDINGS:
its container, its ports, its volumes) · an installation that has bound none has no precious store: this rule does not
fire, and the absence is reported, never guessed]

LAWS:[
1. never remove, recreate, rebuild, `compose down` or prune the bound store, its image or its volumes · never "fix" it
   by rebuilding
2. never stop or restart it without *USER*'s explicit go in the same conversation (what writes to it is live; a stop is
   *USER*'s call, always)
3. any test, SaaS or box work needing the same kind of store gets its OWN — a different name, different ports,
   different volumes · pointing a test context's connection settings at the bound store's ports is a bug
4. a current backup exists before any risky operation near it (judge "risky" paranoid)
5. it is read by nothing but the reader its binding names — never a database driver, a shell client, `curl` or a raw
   port — and that reader only through its own interfaces: an agent through its MCP, code through its SDK by that SDK's
   own convention · one bounded read at a time, by name, never an agent's sweep of descriptions
]

TRIGGER:[any command naming the bound store, its image or its volumes · any read of the bound store (⇒ through its reader's interface only) · any docker stop/rm/prune · any edit to a
connection setting that could reach it · any test or box setup needing that kind of store (⇒ re-read this rule and the
binding first) · when in doubt: separate container, separate ports, separate volumes, backup recency checked]

→ The backup/restore HOW-TO for this installation's binding (commands, gotchas, cron): the `understand-user-rules` skill
(`## the-precious-store`).
