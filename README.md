# host-aios

<!-- SCALABLE-PUBLISHING:AUTOGEN START (managed block — do not edit between these markers) -->

[ChainCompiler](https://github.com/sancovp/chaincompiler) • [skilltree](https://github.com/sancovp/skilltree)

📦 Auto-published from the monorepo • [CHANGELOG](./CHANGELOG.md) • [sancovp/host-aios](https://github.com/sancovp/host-aios)

<!-- SCALABLE-PUBLISHING:AUTOGEN END -->

The host AIOS for Claude Code: a configuration that Claude takes on by reading it, so that every session works the
same way. Each project gets a design, a board of where its work stands, an architecture map and notes. Every piece of
knowledge goes to one home, and every change is checked before it leaves the machine.

## What is in it

- **The skills.** The thirteen construction stations and the workflow they make up. The skills that write a project's
  `DESIGN.md`, its board, its architecture map and a ground truth of an existing project. The skill that starts a new
  project (`aios-artifacts`). The skills that start development work and work on a project, save what a project makes,
  settle a question only you can answer, and make a kind's abstraction before its second piece. Goal writing, and the
  checks a project's documents pass.
- **The install skill.** A plugin install loads no `CLAUDE.md`, so the `install` skill lays the AIOS out in a folder of
  its own: its boot instructions, its rules, a starter top-level design and its workspace of projects. It adds one line
  to your global Claude folder pointing down to that folder, and that folder's line to the master map.
- **The hooks.** A check at every session start says whether the AIOS's folder is whole. Each prompt gets one
  instruction: name the request's mode and start it from the right skill. Anything that will live in a folder of its
  own is started as a new project. Two guards refuse mistakes before they happen, and one holds a turn open:
  - one refuses a write of a design, a board or a map while the skill that makes it is unopened;
  - one refuses an agent dispatch that would hand code to another agent;
  - one holds a turn's first stop once, for a re-read of what it changed.
- **The mod** (`host-aios-mod`, a second plugin in this marketplace). It adds the boot instructions and rules to a
  session that has none loaded.

## How to use it

1. Install it from its marketplace, this repository, in one step:

   ```
   /plugin install host-aios --marketplace sancovp/host-aios
   ```

   Or add the marketplace with `/plugin marketplace add sancovp/host-aios`, then install `host-aios` from it.
2. Ask Claude to install the host AIOS, or run the `install` skill. Name the folder it should live in, then fill out
   the one file it asks you to, `user_info.md`: who you are, and where your work lives.
3. Start Claude Code in that folder. Ask for anything. A new project is made in the folder's workspace with its design,
   board and map, and every project after it the same way.

## License

MIT, see `LICENSE`.
