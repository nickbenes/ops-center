# Thread identity and starter prompt

This describes how a project thread gets its own identity files. **`/ops-center create` does not
do this** — thread identity files are created per thread, as threads are actually named, not as
part of initial mission setup (BOOTSTRAP_PROMPT.md §13.1 note after step 18). This doc is for
whenever a thread is actually established afterward — whether a human asks the `ops-center` skill
to hand-build one, or (more commonly) a project's own `AGENTS.md` governs that moment on its own
without re-invoking `/ops-center` at all.

**As of v1.2.0**: a thread determines its `thread_id` (an ISO 8601 timestamp, set once at its
first user turn) immediately, and writes it to `identity.md` right away rather than deferring —
see "Record it immediately" below. This replaced a v1.1.0 attempt at a harness-assigned
session/agent-ref identifier, which turned out to be unstable in practice; see
`references/logging-protocol.md`'s "Why `thread_id` is timestamp-based."

## Where these files live

`memory/threads/<thread_id>/`, where `<thread_id>` is a filesystem-safe form of the thread's
`thread_id` (its stable identity — the ISO timestamp of its first user turn), not its mutable
display name. Colons in the ISO timestamp become hyphens, e.g. `thread_id` of
`2026-09-15T13:04:00-04:00` becomes folder name `2026-09-15T13-04-00-04-00`.

Each thread folder holds three sibling files:

- `identity.md` — see `templates/identity.template.md`, six fields:
  - **thread_id** — a section grouping `thread_name` (mutable display name) with the thread's
    actual `thread_id` value (the stable first-turn timestamp) — the section and one of its two
    fields share a name deliberately, since the section is about the thread's identity overall.
  - **purpose** — one sentence: what this thread exists to do.
  - **reads** — files/folders this thread treats as input.
  - **writes** — files/folders this thread produces.
  - **typical_recipients** — a *declared default* (thread + channel), not a per-turn fact. The
    log's `comm_to`/`comm_channel` columns record what actually happened on a given turn.
  - **trigger** — `human`, or `cron: <expression>` if this thread is meant to run on a schedule.
    A cron-triggered thread needs no special-casing elsewhere in the architecture — it's just a
    thread whose trigger happens to be automated. **This plugin does not create or manage the
    actual scheduled job** — recording `trigger: cron: ...` here documents intent only; wiring up
    real automation (e.g. via a scheduling tool) is a separate step the human owns.
- `starter-prompt.md` — see `templates/starter-prompt.template.md`. The literal copy-paste text a
  human pastes into a fresh session to bootstrap it as this thread. Restates the identity fields
  in **second person**, not a link to `identity.md`, so a new session becomes this identity in one
  paste with zero ambiguity about which role it's playing.
- `session-log.csv` — this thread's own turn log, same header as `memory/project-logs.csv` (see
  `references/logging-protocol.md`), containing only rows from this thread.

## Record it immediately

Determine `thread_id` at the thread's very first turn — right after reading `AGENTS.md`, before
anything else — and write `identity.md` (at minimum its `thread_id` section) then, not whenever
it becomes convenient. Re-read `thread_id` from `identity.md` whenever you need it later in the
session rather than trusting conversational memory to still hold it accurately; long sessions get
compacted, and a value set at turn 1 can get lost or paraphrased away by the time it matters again
much later. A file doesn't have that problem.

## Renames

If a thread is renamed, keep writing to the same `<thread_id>` folder (it's keyed on the stable
`thread_id`, not the display name). The changing `thread_name` values in the log rows create an
auditable rename trail.

## Updates

Create both `identity.md` and `starter-prompt.md` when a thread is first established; update
them if the thread's role changes materially later.
