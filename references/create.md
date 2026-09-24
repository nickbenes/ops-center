# `/ops-center create`

Bootstraps a new ops-center project: a persistent, filesystem-backed workspace that lets
independent Claude Code threads coordinate over time. Follow these steps in order. Full
background and rationale for every artifact created here is in
`templates/BOOTSTRAP_PROMPT.md` §4–§14 — this doc is the operational checklist; that file is the
spec it implements.

## Step 1 — Ask for a location

Ask whether to use the current working directory, or a different/new one. **Never assume** —
even "use the current directory" needs an explicit yes, because this step also determines whether
the harness supports the rest of this flow at all:

- Claude Code desktop, terminal, or IDE extension: always running from some working directory —
  ask whether to use it (and scan it) or point to/create a different one. Suggest "the current
  directory" as the default answer, but still ask.
- Claude Code cloud-remote: treat identically to desktop/terminal, since it also has a persistent
  working directory.
- Claude.ai, or any other harness with a Project + connected filesystem instead of a real working
  directory: this is out of scope for `/ops-center`. Say so plainly and suggest running this
  inside a Claude Code working directory instead of guessing at a substitute.

Once the location is settled, read and write every file for the rest of this flow using paths
**relative to that location** (e.g. `AGENTS.md`, `memory/PROJECT-MISSION.md`) rather than
resolving and reusing an absolute path everywhere. The one exception is the registry entry in
step 3, which genuinely needs an absolute path since it's looked up later from other working
directories.

## Step 2 — Ask for a name

This becomes the registry key and, by default, the top-level folder/project name.

## Step 3 — Register immediately

Before scanning, before drafting anything, run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/registry.py" set <name> <absolute-location>
```

- Exit code `0`: done, continue to step 4.
- Exit code `2`: the name is already registered pointing at a *different* path. Tell the user
  the existing path and ask whether to pick a different name or confirm overwriting (in which
  case re-run with `--force`). Don't silently overwrite — the spec is explicit about this for
  `/ops-center import`, and it's treated the same way here for consistency.

Registering this early means even an abandoned setup stays findable — that's the whole point of
doing it before any other step.

## Step 4 — Scan (silently)

Look at whatever already exists at the chosen location — files, folders, existing docs, code,
anything that hints at what this project is for. **Don't narrate this as it happens** ("let me
look around...") — it's a quiet step. Its *findings* surface in step 5, not here.

## Step 5 — Draft the mission

State your understanding of the project's mission, shaped like `templates/PROJECT-MISSION.template.md`
expects: objective, source-of-truth hierarchy, workflow, and a proposed one-sentence acceptance
test.

- If the scan turned up real material to draw on: draft from it, and **explicitly label it as a
  draft/guess** — don't present scan-derived content as already-confirmed fact.
- If the scan found little to go on: run a short, targeted interview asking only what the scan
  couldn't answer — typically the audience/beneficiary, and what "done" or "handoff" looks like.
  Don't ask about things the scan already answered.

## Step 6 — Confirm the acceptance-test sentence specifically

Ask about the one-sentence acceptance test by name, not a generic "does this look right?" — that
sentence is the real gate on whether the mission is correctly scoped, so it needs its own
explicit confirmation.

## Step 7 — Propose the filesystem structure

Default to `templates/BOOTSTRAP_PROMPT.md` §4's layout. Omit or add directories when this
specific project actually warrants it — don't create empty structure merely for symmetry. Note
any deviation; it'll go into `AGENTS.md` §10 in step 10.

## Step 8 — Identify inputs and workstreams

Note the authoritative input material and the likely initial workstreams/threads.

## Step 9 — Draft `memory/PROJECT-MISSION.md`

Fill `templates/PROJECT-MISSION.template.md` with what steps 5–8 established.

## Step 10 — Draft `AGENTS.md`

Fill `templates/AGENTS.template.md`. Link to `memory/PROJECT-MISSION.md` rather than repeating
its contents; record any layout deviations from step 7 in its §10.

## Step 11 — Draft `memory/PROJECT-STATUS.md`

Fill `templates/PROJECT-STATUS.template.md` — the compact, cheap-to-read orientation entry point.

## Step 12 — Establish `memory/project-logs.csv`

Create it with the header row from `templates/log-header.csv`. See
`references/logging-protocol.md` for what the columns mean — no need to re-derive that here,
just create the file correctly.

## Step 13 — Save the bootstrap spec

Copy `templates/BOOTSTRAP_PROMPT.md` byte-for-byte to `_architecture/BOOTSTRAP_PROMPT.md` in the
new project. Verbatim — don't paraphrase or regenerate it.

## Step 14 — Identify initial playbooks/templates/tools

Note anything obvious the project should start with under `playbooks/`, `templates/`, `tools/`.
Don't invent structure the project doesn't need yet.

## Step 15 — Explain cross-thread communication

Explain, in the proposal, how independent threads will exchange information: via
`memory/turnover/` (shared_file), broadcast artifacts, or direct messages — and how that maps to
the `comm_to`/`comm_channel`/`comm_ref` log columns described in `references/logging-protocol.md`.

## Step 16 — Identify what should NOT be persisted

Call out anything (secrets, huge generated artifacts, ephemeral scratch work) that shouldn't be
written into this project's durable filesystem.

## Step 17 — Note platform capabilities/limitations

Anything about this specific harness/environment that affects the design (e.g. no real
scheduler available for a `cron`-triggered thread — see `references/thread-identity.md`).

## Step 18 — Show the proposal, then write

Show the full proposed bootstrap — the file tree and the drafted contents from steps 9–13 — before
making any broad or destructive change. Wait for approval before writing.

## Explicitly deferred (do not do these here)

Per-thread `identity.md`, `starter-prompt.md`, and `session-log.csv` are **not** created during
`/ops-center create`. They're created later, per actual thread, as described in
`references/thread-identity.md`. Don't create `memory/threads/` at all during this flow.

## Never

Never delete or reorganize a user's existing files without their explicit approval — this
applies throughout, especially during the silent scan in step 4, which must only read.
