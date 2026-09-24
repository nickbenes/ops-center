# `/ops-center import <path-to-zip>`

Restores a previously exported ops-center project from its zip archive.

## Step 0 — Resolve the destination

Use the exact same ask-never-assume location logic as `references/create.md` step 1 (current
directory vs. a different/new one; same harness-support caveats). Don't restate that logic here —
just apply it.

## Step 1 — Unzip

Use Python's stdlib `zipfile` module, preserving relative paths:

```python
import zipfile

with zipfile.ZipFile("<path-to-zip>") as zf:
    zf.extractall("<destination-directory>")
```

Afterward, verify the extraction actually produced the expected top-level files (at minimum,
something resembling `AGENTS.md` and a `memory/` folder) before reporting success. If it looks
like a bare filesystem export rather than a nested single-folder zip, adjust the destination path
accordingly rather than nesting it one level deeper than intended.

## Step 2 — Read the restored project's own files

In order: `_architecture/BOOTSTRAP_PROMPT.md`, `AGENTS.md`, `memory/PROJECT-MISSION.md`,
`memory/PROJECT-STATUS.md`, and the migration handoff from `references/export.md` step 7 — if one
exists. **The handoff may be absent** (an older export, or a project that was never exported
through this plugin) — handle that gracefully, don't treat it as a failure.

## Step 3 — Check for environment differences

Compare what this environment offers against what the project's files assume: tools,
filesystem behavior, skills, automations, connectors, permissions, context handling. **Propose**
any compatibility changes that seem necessary — never apply them silently. Show the proposal and
wait for a decision.

## Step 4 — Preserve history exactly

Don't rewrite anything in `memory/project-logs.csv`, any thread's `session-log.csv`,
`memory/turnover/`, `memory/lessons-learned/`, or thread DTTMs/identity files. They came out of
the zip as they were; leave them that way.

## Step 5 — Update the registry

Choose a name for this restored project (ask, unless the user already gave one), then:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/registry.py" set <name> <destination-path>
```

- Exit code `0`: done.
- Exit code `2`: that name is already registered pointing at a *different* path. Show the
  existing path and ask before re-running with `--force`. Never silently overwrite an existing
  registry entry.

## Step 6 — Don't resume work prematurely

Only start substantive work in the restored project once enough state has actually been read and
understood (steps 2–3) — don't jump straight into a task the moment the unzip finishes.
