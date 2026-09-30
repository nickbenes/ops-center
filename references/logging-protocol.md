# Logging protocol

This describes the per-turn logging protocol that a scaffolded ops-center project runs on every
ordinary turn, once `/ops-center create` has finished. It's documentation the created project's
own `AGENTS.md` points back to (via `_architecture/BOOTSTRAP_PROMPT.md`) — the `ops-center`
plugin's own job is only to (a) set this up correctly during `create` (establishing
`memory/project-logs.csv` with the right header) and (b) touch it once during `export` (updating
the current turn's log rows as part of the pre-export checklist). The plugin does not run this
loop on its own, unrelated turns — see `SKILL.md`'s cross-cutting rules.

**As of v1.2.0**: `thread_id` is the thread's single stable identity column again, timestamp-based
(what v1.1.0 briefly called `thread_dttm`). v1.1.0 tried making `thread_id` a harness-assigned
session/agent ref instead, kept alongside `thread_dttm` while that was unproven — two independent
sessions then observed their own ref change mid-session with no rename, so that approach is
dropped. See "Why `thread_id` is timestamp-based" below. This does **not** affect `comm_to` —
addressing a *peer* still uses whatever session ref/agentId a real call to that peer actually
returns; only a thread's *own* identity column changed.

## Schema

Both `memory/project-logs.csv` (project-wide, every thread) and each thread's own
`memory/threads/<thread_id>/session-log.csv` (that thread only) share this header, from
`templates/log-header.csv`:

```
turn_dttm,thread_name,thread_id,user_prompt_summary,comm_to,comm_channel,comm_ref,comm_confirmed
```

Quick cheat sheet — the question each column answers:

| Column | Question |
|---|---|
| `turn_dttm` | What time was it? |
| `thread_name` | What was my nickname? |
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
- **thread_id** — ISO 8601 timestamp of this thread's *first* user turn. Stable for the life of
  the thread even if it's renamed later — **required**, always populate it (not an optional
  field; see the history note below for why it isn't harness-assigned).
- **user_prompt_summary** — one concise sentence summarizing what the user asked. Never copy the
  full prompt in.
- **comm_to** — the actual identifier used in the real call: the session name/ref or agentId you
  messaged (`send_message`, `agent_spawn`), the specific thread a `shared_file` was written for,
  or `none` (`broadcast`, or no communication this turn). You generally can't know a peer's stable
  identity in advance — record whatever `SendMessage`/`ListAgents`/the Agent tool actually gave
  you, not a guess. (This is about addressing a *peer* — unrelated to how you determine your own
  `thread_id` above.)
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
sharing the same `turn_dttm`/`thread_name`/`thread_id`/`user_prompt_summary` — no positional
pipe-delimited alignment between columns.

### Why `thread_id` is timestamp-based

v1.1.0 tried making `thread_id` a harness-assigned session id/ref (e.g. the bracketed ref
`ListAgents` shows), reasoning that it wouldn't require reconstructing a precise first-turn
timestamp after the fact the way a timestamp-based identifier does. Two independent sessions then
observed their own `ListAgents` ref change mid-session with no rename — confirmed via separate
`ListAgents` calls, not inferred from a secondary signal like a changed transport socket path
(which is a distinct, lower-level artifact and only suggestive on its own). A session ref that can
silently change under the thread it's supposed to identify isn't a usable stable identifier, so
v1.2.0 dropped that approach and went back to what actually worked: an ISO timestamp set once, at
the thread's first user turn, and never recomputed.

### Record it immediately, and don't trust memory to hold it

Two rules that follow directly from the instability above:

1. **Determine `thread_id` at the thread's very first turn**, right after reading `AGENTS.md` and
   internalizing this protocol — not deferred until "whenever it's convenient."
2. **Write it to `identity.md` immediately, and re-read it from there when you need it later** —
   don't rely on conversational memory to hold a value set early in a long session. Compaction can
   lose or paraphrase away a specific value set many turns ago; a file doesn't have that problem.

## CSV escaping

Quote any field containing a comma, quote, or line break. Escape an embedded quote by doubling
it (standard CSV escaping — Python's `csv` module, or any language's standard CSV writer, does
this correctly by default; don't hand-roll string concatenation for this).

## The per-turn checklist (what a project's AGENTS.md asks every thread to do)

1. Determine the current Turn DTTM.
2. Determine the current thread display name.
3. Retain the stable `thread_id` — read it from this thread's `identity.md` (don't trust
   conversational memory for it), or determine and write it there now if this is the thread's
   first turn.
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
thread were not recorded"). Never fabricate a precise historical `turn_dttm` or `thread_id` for
turns that weren't actually logged at the time — an approximate reconstruction is worse than an
honest gap, because it looks authoritative when it isn't.
