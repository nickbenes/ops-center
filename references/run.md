# `/ops-center run <name>`

Look up `<name>` in the registry and tell the human where it lives — that's the entire job.

## Steps

1. If `<name>` is missing from the command, ask for it — don't guess.
2. Look it up:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/registry.py" get <name>
   ```

   - Found (exit 0): the path is printed. Report it to the human and instruct them to `cd` there,
     or reopen Claude Code in that folder. **A session cannot change its own working directory
     mid-conversation** — never say or imply that you've "switched into" or are "now in" that
     project. State the path, and say what the human needs to do next.
   - Not found (exit 1): run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/registry.py" list` to show
     what *is* registered, and ask which one they meant rather than guessing at a close match.

## Design note (not behavior — just context)

The registry's shape is deliberately kept simple and stable so it could later support
cross-ops-center coordination (one project's thread telling another project's thread that
something relevant happened). That's out of scope for this command today — `run` only resolves a
name to a path.
