# `/ops-center export <name>`

Prepares an ops-center project for migration and produces a literal zip archive of it — not a
reformatted export, an as-is copy of the filesystem.

## Step 1 — Look up the project

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/registry.py" get <name>
```

Fail clearly and stop if `<name>` isn't registered — don't guess a path.

## Step 2 — Update the current turn's logs

Append this turn's row to `memory/project-logs.csv` and to the current thread's own
`memory/threads/<thread-name>/session-log.csv`, per `references/logging-protocol.md`. (This is
the one point where `/ops-center` itself participates in the logging protocol, since exporting is
itself a loggable turn in that project.)

## Step 3 — Review `memory/PROJECT-STATUS.md` for staleness

Read it. If it no longer reflects reality, update it before exporting.

## Step 4 — Update relevant turnover artifacts

If any `memory/turnover/` file needs refreshing so a thread in the destination environment can
pick up where this one left off, update it now.

## Step 5 — Optional session narrative

Only if the user asks: append a narrative/AAR entry (see `templates/BOOTSTRAP_PROMPT.md` §8).
Don't add one unprompted.

## Step 6 — Verify the bootstrap copy is present

Check `_architecture/BOOTSTRAP_PROMPT.md` exists in the project. If it's missing, that's a defect
in how this project was created — flag it rather than silently patching it in with the plugin's
current template (which may have drifted from whatever version the project was actually built
against).

## Step 7 — Draft a migration handoff

Write a short handoff (in `memory/turnover/` or as a note you show the user — whichever fits the
project) covering: project purpose, current state, important entry points, environment-specific
capabilities/dependencies, and anything that may not work in the destination environment.

## Step 8 — Scan for anything that shouldn't be exported

Check for secrets, credentials, tokens, private keys, `.env*` files, and unusually large generated
artifacts (binaries, dependency trees, media). **Warn before including any hit** — don't silently
include it, and don't silently exclude it either (exclusion is also a decision the human should
see and agree to). Wait for a decision before zipping.

## Step 9 — Zip the approved folder

Use Python's stdlib `zipfile` module (always available — don't assume a `zip` CLI binary is
installed on whatever platform this runs on):

```python
import zipfile, pathlib

project_dir = pathlib.Path("<absolute-project-path>")
out_path = project_dir.parent / f"{project_dir.name}.zip"

with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for path in project_dir.rglob("*"):
        if path.is_file():
            zf.write(path, path.relative_to(project_dir.parent))
```

Adjust the file list to reflect whatever was excluded in step 8. **Verify the zip file actually
exists on disk afterward before telling the user it's done** — don't claim success before
checking.

## Step 10 — Update the registry (optional)

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/registry.py" touch <name>
```
