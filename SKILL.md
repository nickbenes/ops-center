---
name: ops-center
description: Create, run, export, and import a persistent multi-thread project workspace under the ops-center bootstrap architecture — a shared filesystem (AGENTS.md, memory/, per-turn CSV logs, thread identity files) that lets independently-scoped Claude Code threads coordinate without shared conversational memory. Invoked explicitly via /ops-center create|run|export|import; not intended for automatic invocation from conversation.
disable-model-invocation: true
argument-hint: create | run <name> | export <name> | import <path-to-zip>
---

# ops-center

Route on the first word of `$ARGUMENTS`. **Read the matching reference file in full before doing
anything else for that subcommand** — don't act from this file's summary alone, the detail that
matters is in the reference doc.

- No arguments, or an unrecognized first word: print the four subcommands below with a one-line
  description of each, and stop. Don't guess which one was meant.
- `create` → read `references/create.md`, then follow it step by step.
- `run <name>` → read `references/run.md`. Requires a `<name>`; if it's missing, ask for it.
- `export <name>` → read `references/export.md`. Requires a `<name>`.
- `import <path>` → read `references/import.md`. Requires a path to a `.zip` file.

The four subcommands, for the no-args summary:

- **create** — bootstrap a new ops-center project in a folder you choose.
- **run \<name\>** — look up a registered project and tell you where it lives.
- **export \<name\>** — package a registered project into a zip, after checking for anything
  that shouldn't leave the machine.
- **import \<path-to-zip\>** — restore an exported project into a folder you choose.

## Cross-cutting rules (apply to every subcommand)

- Never claim a write, zip, unzip, or registry update succeeded without verifying it actually
  happened.
- Never claim to have changed the working directory — a session can't `cd` itself. `run` always
  reports a path and asks the human to move there; it never says "I've switched into...".
- Never delete or reorganize a user's existing files without their explicit approval.
- This skill only acts on an explicit `/ops-center` invocation — never infer an ops-center
  action from ordinary conversation (that's what `disable-model-invocation` is for).
- All four workflows use `${CLAUDE_PLUGIN_ROOT}` to find this plugin's own `scripts/` and
  `templates/` regardless of where it's installed — never hardcode a path to them.
