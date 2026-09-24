# Logging protocol

This describes the per-turn logging protocol that a scaffolded ops-center project runs on every
ordinary turn, once `/ops-center create` has finished. It's documentation the created project's
own `AGENTS.md` points back to (via `_architecture/BOOTSTRAP_PROMPT.md`) — the `ops-center`
plugin's own job is only to (a) set this up correctly during `create` (establishing
`memory/project-logs.csv` with the right header) and (b) touch it once during `export` (updating
the current turn's log rows as part of the pre-export checklist). The plugin does not run this
loop on its own, unrelated turns — see `SKILL.md`'s cross-cutting rules.

## Schema

Both `memory/project-logs.csv` (project-wide, every thread) and each thread's own
`memory/threads/<thread-name>/session-log.csv` (that thread only) share this header, from
`templates/log-header.csv`:

```
turn_dttm,thread_name,thread_dttm,user_prompt_summary,comm_to,comm_channel,comm_ref
```

- **turn_dttm** — ISO 8601 timestamp of the current user turn.
- **thread_name** — the thread's current display name at the time of this turn. Mutable — don't
  treat it as a stable identifier.
- **thread_dttm** — ISO 8601 timestamp of this thread's *first* user turn. Stable for the life of
  the thread even if it's renamed later; this is the real identity.
- **user_prompt_summary** — one concise sentence summarizing what the user asked. Never copy the
  full prompt in.
- **comm_to** — pipe-delimited list of destination thread identifiers this turn's work is
  relevant to (prefer `thread_dttm` over a display name), or `none`.
- **comm_channel** — pipe-delimited, positionally matched to `comm_to`. One of
  `direct_message` (addressed to one specific thread), `shared_file` (written to a shared
  artifact such as a turnover file), `broadcast` (written to a project-wide artifact for all
  threads), or `none` (paired only with `comm_to=none`).
- **comm_ref** — optional, pipe-delimited, positionally matched. File path/id of the artifact
  when the channel is `shared_file` or `broadcast`; blank or `-` otherwise.

Most turns are pure single-thread work: `comm_to=none,comm_channel=none`. Don't invent
cross-thread relevance that isn't real.

## CSV escaping

Quote any field containing a comma, quote, or line break. Escape an embedded quote by doubling
it (standard CSV escaping — Python's `csv` module, or any language's standard CSV writer, does
this correctly by default; don't hand-roll string concatenation for this).

## The per-turn checklist (what a project's AGENTS.md asks every thread to do)

1. Determine the current Turn DTTM.
2. Determine the current thread display name.
3. Retain the stable Thread DTTM from this thread's first user turn.
4. Summarize the user's prompt in one concise sentence.
5. Append one CSV row to `memory/project-logs.csv` AND to this thread's own
   `memory/threads/<thread-name>/session-log.csv`.
6. Do the user's requested work.
7. If the work materially changed project state, durable knowledge, process, or cross-thread
   dependencies, update the relevant persistent artifact before finishing the turn.
8. Verify the writes actually happened, when that's checkable.

If the filesystem is temporarily unwritable, don't claim the turn was logged — say so and
continue the user's work if possible.
