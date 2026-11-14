---
name: understand-user-rules
description: "WHAT: the procedures and relations that sit behind the user-level rules — the neo4j backup and restore procedure, how the maximized-version operator pairs with the feature-close CoR, and how per-dir state relates to DESIGN.md. WHEN: backing up or restoring the precious store, running the maximized-version operator, or deciding whether a fact belongs in DESIGN.md or a `_states.md`."
---

# Understand the user-level rules — the procedures behind them

A rule says WHAT must hold. This skill carries the HOW a rule points at when the how is too long to sit in the
rule. Each section is named for the rule it serves.

## the-precious-store — backing up and restoring it

The precious store is the container an installation binds in `user_info.md` (THE PRECIOUS STORE).

**Back up — online, no stop, no touch.** Run a throwaway helper that shares the store's network namespace and
writes to the HOST disk, never into the Docker VM:
```
mkdir -p <world dir>/backups/neo4j
docker run --rm --network container:<precious container> \
  -v <world dir>/backups/neo4j:/backup neo4j:5-enterprise \
  neo4j-admin database backup --from=localhost:6362 --to-path=/backup --type=full <every database>
```
- `SHOW DATABASES` first, and back up EVERY database it lists — the store holds more than `neo4j` and `system`.
- The backup service is Enterprise's default-on port 6362; confirm it answers before relying on it.
- Keep beside the artifacts: the logs, a `SHA256SUMS`, and a `README.md` with the node and relationship counts,
  the checksums and the restore command.
- An artifact is far smaller than the live store (compression of a hollow store); a restore inflates it back to
  the full size — plan disk for the full store.

**Restore — into a FRESH container, never onto the precious one.**
```
neo4j-admin database restore --from-path=/backup/<artifact> --overwrite-destination=true <database>
```
- Put the restored `/data` on a HOST bind mount, never inside the Docker VM: the VM's free space is smaller than
  the inflated store, and filling it endangers the precious container itself.
- Stage the artifact in a writable directory — the tool extracts temporary files next to it.
- A backup is proven only by a restore whose counts match the backup's `README.md`.

**Not built:** a recurring backup as a cave CronAutomation, with restore-verify into a scratch container.

## maximized-version-operator — where it sits against the feature-close CoR

Run the maximized-version operator at DESIGN time; it catches a target anchored to the current setup's shape.
Close with the feature-close CoR, which catches forgotten alignment at CLOSURE time. Repeating the same
iteration a third time is the lagging signal that the operator was skipped; run the operator before that.

## 28-distributed-state — DESIGN.md and `_states.md` together

`DESIGN.md` states the STRUCTURAL truth of the whole project, central and stable. Each dir's `_states.md` states
the OPERATIONAL truth — which deliverables sit at which phase, here. They never compete. Both ride progressive
disclosure: entering a dir loads its `.claude/rules/`, so its state and architecture are seen on arrival.
