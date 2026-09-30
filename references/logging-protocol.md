# Logging protocol

This describes the per-turn logging protocol that a scaffolded ops-center project runs on every
ordinary turn, once `/ops-center create` has finished. It's documentation the created project's
own `AGENTS.md` points back to (via `_architecture/BOOTSTRAP_PROMPT.md`) — the `ops-center`
plugin's own job is only to (a) set this up correctly during `create` (establishing
`memory/project-logs.csv` with the right header) and (b) touch it once during `export` (updating
the current turn's log rows as part of the pre-export checklist). The plugin does not run this
loop on its own, unrelated turns — see `SKILL.md`'s cross-cutting rules.

**As of v1.1.0**: added `thread_id` and `comm_confirmed`, and redefined `comm_channel`'s values
to map onto real Claude Code mechanisms. `thread_dttm` is kept, not removed — see
"`thread_id` vs `thread_dttm`" below.

## Schema

Both `memory/project-logs.csv` (project-wide, every thread) and each thread's own
`memory/threads/<thread_id-or-thread_dttm>/session-log.csv` (that thread only) share this header,
from `templates/log-header.csv`:

```
turn_dttm,thread_name,thread_dttm,thread_id,user_prompt_summary,comm_to,comm_channel,comm_ref,comm_confirmed
```

Quick cheat sheet — the question each column answers:

| Column | Question |
|---|---|
| `turn_dttm` | What time was it? |
| `thread_name` | What was my nickname? |
| `thread_dttm` | *(superseded by `thread_id` — see below)* |
| `thread_id` | Who am I really, for logging purposes? |
| `user_prompt_summary` | What did I know? |
| `comm_to` | Who needed to know it? |
| `comm_channel` | How did I tell them? |
| `comm_ref` | How specifically did I tell them? |
| `comm_confirmed` | Have I told them? |

### Field definitions

- **turn_dttm** — ISO 8601 timestamp of the current user turn.
- **thread_name** — the thread's current display name at the time of this turn. Mutable — don't
  treat it as a stable identifier.
- **thread_dttm** — ISO 8601 timestamp of this thread's *first* user turn. Stable for the life of
  the thread even if it's renamed later.
- **thread_id** — the thread's stable identity, going forward: a session id/ref or agentId (the
  same kind of identifier `ListAgents` shows, e.g. the bracketed ref in `"this session is
  <name> [6dd6a6]"`, or an `agentId` for a subagent) — **optional for now**. See
  "`thread_id` vs `thread_dttm`" below for why, and how to populate it when you can.
- **user_prompt_summary** — one concise sentence summarizing what the user asked. Never copy the
  full prompt in.
- **comm_to** — the actual identifier used in the real call: the session name/ref or agentId you
  messaged (`send_message`, `agent_spawn`), the specific thread a `shared_file` was written for,
  or `none` (`broadcast`, or no communication this turn). You generally can't know a peer's stable
  identity in advance — record whatever `SendMessage`/`ListAgents`/the Agent tool actually gave
  you, not a guess.
- **comm_channel** — one of:
  - `send_message` — a live `SendMessage` call to an addressable peer session (same-machine
    socket or Remote Control relay).
  - `agent_spawn` — dispatched a subagent via the Agent/Task tool and got a hand-back report.
  - `shared_file` — wrote to an artifact meant for a specific other thread to read later (e.g. a
    turnover file).
  - `broadcast` — wrote to a project-wide artifact with no specific addressee (e.g.
    `PROJECT-STATUS.md`).
  - `none` — no communication this turn (paired only with `comm_to=none`).
- **comm_ref** — optional. The `msg_id` `SendMessage` returned (`send_message` rows), the
  `agentId` (`agent_spawn` rows), or the file path (`shared_file`/`broadcast` rows); blank or `-`
  otherwise.
- **comm_confirmed** — `yes` / `no` / `unknown`. Only meaningful on `send_message` rows; blank or
  `-` otherwise. A same-machine peer session sends back a `[Cross-session delivery notice]` if
  your message was held or refused — silence there means it went through (`yes`). A Remote
  Control or cloud peer never reports back at all — silence there is genuinely `unknown`, not
  success. Don't record `yes` just because the call itself didn't error.

Most turns are pure single-thread work: one row, `comm_to=none,comm_channel=none`. Don't invent
cross-thread relevance that isn't real.

### One row per communication event

A turn with zero communications is one row. A turn with *N* communications is *N* rows, all
sharing the same `turn_dttm`/`thread_name`/`thread_dttm`/`thread_id`/`user_prompt_summary` —
no positional pipe-delimited alignment between columns. This replaced an earlier pipe-delimited
list design that turned out to be fragile once a turn had more than one recipient.

### `thread_id` vs `thread_dttm`

`thread_id` is meant to eventually replace `thread_dttm` as the stable identity column, because a
harness-assigned session/agent id doesn't require reconstructing a precise first-turn timestamp
after the fact the way `thread_dttm` does — a real compliance gap in practice (a thread that
skips logging for its first several turns has no way to recover its true `thread_dttm`).

It's kept **optional and additive, not a replacement**, until two things are confirmed in
practice: that a session's id/ref actually stays stable across resumption, compaction, and
renaming, and that it's practical to obtain cheaply (a thread generally has to call `ListAgents`
to learn its own ref — do this once per thread and cache it, not on every turn). Until then,
`thread_dttm` remains the field you can always populate, and `thread_id` is filled in when known.
Once `thread_id`'s stability is confirmed project-wide, `thread_dttm` will be deprecated —
that migration isn't done yet.

## CSV escaping

Quote any field containing a comma, quote, or line break. Escape an embedded quote by doubling
it (standard CSV escaping — Python's `csv` module, or any language's standard CSV writer, does
this correctly by default; don't hand-roll string concatenation for this).

## The per-turn checklist (what a project's AGENTS.md asks every thread to do)

1. Determine the current Turn DTTM.
2. Determine the current thread display name.
3. Retain the stable Thread DTTM from this thread's first user turn (and, if already known for
   this thread, its `thread_id`).
4. Summarize the user's prompt in one concise sentence.
5. Append one CSV row per communication event this turn (or a single `comm_to=none` row if none)
   to `memory/project-logs.csv` AND to this thread's own `session-log.csv`.
6. Do the user's requested work.
7. If the work materially changed project state, durable knowledge, process, or cross-thread
   dependencies, update the relevant persistent artifact before finishing the turn.
8. Verify the writes actually happened, when that's checkable.

**This is a zero-judgment gate, separate from context-loading.** It fires before task-type is
even evaluated — a quick, meta, or test-feeling turn is not exempt. Don't let logging get bundled
in your head with the heavier "which files should I read for this task" judgment call; that
judgment stays proportional to the task, logging doesn't.

If the filesystem is temporarily unwritable, don't claim the turn was logged — say so and
continue the user's work if possible.

### Recovering from a missed-logging gap

If a thread discovers mid-stream that it never started logging (or stopped for a while): backfill
from the point of discovery forward, with an explicit gap note in the next row's
`user_prompt_summary` or in `PROJECT-STATUS.md` (e.g. "logging gap: turns before this one in this
thread were not recorded"). Never fabricate a precise historical `turn_dttm` or `thread_dttm` for
turns that weren't actually logged at the time — an approximate reconstruction is worse than an
honest gap, because it looks authoritative when it isn't.
