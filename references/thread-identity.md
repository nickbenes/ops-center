# Thread identity and starter prompt

This describes how a project thread gets its own identity files. **`/ops-center create` does not
do this** — thread identity files are created per thread, as threads are actually named, not as
part of initial mission setup (BOOTSTRAP_PROMPT.md §13.1 note after step 18). This doc is for
whenever a thread is actually established afterward — whether a human asks the `ops-center` skill
to hand-build one, or (more commonly) a project's own `AGENTS.md` governs that moment on its own
without re-invoking `/ops-center` at all.

## Where these files live

`memory/threads/<thread-name>/`, where `<thread-name>` is a filesystem-safe form of the thread's
`thread_dttm` (its stable identity — the ISO timestamp of its first user turn), not its mutable
display name. Colons in the ISO timestamp become hyphens, e.g. `thread_dttm` of
`2026-09-15T13:04:00-04:00` becomes folder name `2026-09-15T13-04-00-04-00`.

Each thread folder holds three sibling files:

- `identity.md` — see `templates/identity.template.md`, six fields:
  - **thread_id** — thread_name + thread_dttm.
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
  in **second person**, not a link to `identity.md` — a new session should become this identity
  in one paste with zero ambiguity about which role it's playing.
- `session-log.csv` — this thread's own turn log, same header as `memory/project-logs.csv` (see
  `references/logging-protocol.md`), containing only rows from this thread.

## Renames

If a thread is renamed, keep writing to the same `<thread-name>` folder (it's keyed on the
stable `thread_dttm`, not the display name). The changing `thread_name` values in the log rows
create an auditable rename trail.

## Updates

Create both `identity.md` and `starter-prompt.md` when a thread is first established; update
them if the thread's role changes materially later.
