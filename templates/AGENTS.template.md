# AGENTS.md — Operating Charter for `<project-name>`

<Fill in during `/ops-center create`. This file is the durable operating charter every thread in
this project should read at startup. It carries the generic architecture rules from
`_architecture/BOOTSTRAP_PROMPT.md`, made concrete for this specific project. Keep
project-specific mission/scope details in `memory/PROJECT-MISSION.md` instead of duplicating them
here — link to it.>

## 1. Mission and scope

See [`memory/PROJECT-MISSION.md`](memory/PROJECT-MISSION.md) for the full mission, scope, and
non-goals. In one sentence: <restate the mission for quick orientation>.

## 2. Source-of-truth hierarchy

<State which artifacts are authoritative for this project, most authoritative first. Typical
order, adjust as needed:>

1. Current repository / filesystem contents (never an old log or memory summary overriding
   newer authoritative material).
2. Explicit user decisions.
3. Confirmed conclusions recorded in `memory/PROJECT-STATUS.md` or `memory/turnover/`.
4. Source evidence in `inputs/`.
5. Drafts in `outputs/drafts/` (not yet authoritative).
6. Historical notes / old session narratives (context only, never override anything above).
7. Model inference (lowest — always verify against the above before treating as fact).

## 3. Thread startup protocol

Every new thread working in this project should read, in order:

1. This file (`AGENTS.md`).
2. `memory/PROJECT-MISSION.md`.
3. `memory/PROJECT-STATUS.md`.
4. Any `memory/turnover/` file relevant to the task at hand.
5. Relevant authoritative inputs under `inputs/`.
6. Relevant `playbooks/`/`templates/`.
7. The current output/draft under `outputs/drafts/`, if continuing existing work.

Do not load every historical artifact automatically — retrieve context according to the task.

At the first user turn, determine and retain the thread's stable **Thread DTTM** (the ISO
timestamp of that first turn), then make sure the thread's own log files
(`memory/threads/<thread-name>/`) are correctly identified. See
[`_architecture/BOOTSTRAP_PROMPT.md`](_architecture/BOOTSTRAP_PROMPT.md) §2 and §7.4 for exactly
how `<thread-name>` is derived and how a thread's `identity.md`/`starter-prompt.md`/
`session-log.csv` are created the first time that thread does real work.

## 4. Per-turn logging protocol — mandatory

For every user turn: determine the Turn DTTM, the thread's current display name, and its stable
Thread DTTM; write a one-sentence summary of the prompt; append one CSV row to
`memory/project-logs.csv` AND to this thread's own `memory/threads/<thread-name>/session-log.csv`;
then do the work; then update status/turnover/lessons if the work materially changed project
state. Full field definitions and CSV escaping rules are in
[`_architecture/BOOTSTRAP_PROMPT.md`](_architecture/BOOTSTRAP_PROMPT.md) §6.4 and §7 — don't
re-derive them, just follow them. If the filesystem is temporarily unwritable, say so rather than
claiming the turn was logged.

## 5. Cross-thread information flow

When this thread learns something another thread or workstream needs, ask: what do I know, who
needs to know, how do I tell them (`comm_to`/`comm_channel` on the log row, plus a durable
artifact — turnover, status, or a broadcast file), and have I told them (verify the artifact
actually reflects it and is discoverable). Never assume another thread can see this thread's
conversational context — only the filesystem is shared.

## 6. Persistence authority

- Turn logs: mandatory, append-only.
- Session narratives: optional, user/project-triggered.
- `memory/PROJECT-STATUS.md`: update when project state meaningfully changes.
- `memory/turnover/`: update when another thread/workstream needs durable handoff context.
- `memory/lessons-learned/`: add well-supported, generalizable lessons; avoid duplicates.
- Authoritative outputs: update per their own lifecycle/version rules.
- `playbooks/`/`templates/`/`tools/`: improve when experience shows a reusable process win.
- `memory/PROJECT-MISSION.md`: comparatively stable — substantive scope changes need human
  approval.
- This file (`AGENTS.md`): comparatively stable — changes to mission, authority, governance,
  security, approval requirements, or major operating principles need human approval.

## 7. History versus memory

History (turn logs) answers "what happened." Memory (status, turnover, lessons) answers "what
should a future thread know because it happened." Prefer consolidated memory over forcing a
future thread to reconstruct current state from a pile of old logs.

## 8. Process improvement / AAR

At the end of substantial work, or when asked to log/wrap up: what were we trying to do, what
actually happened, what worked, what didn't, what's worth remembering, and does a playbook or
another workstream need updating. Be selective — good memory requires leaving things out.

## 9. Context economy

Persistent storage is not active context. Load only what the current task needs; use
`memory/PROJECT-STATUS.md` and `memory/turnover/` as indexes into deeper material rather than
copying the same information into many files.

## 10. Deviations from the default filesystem layout

<List anything this project's structure omits or adds versus BOOTSTRAP_PROMPT.md §4's default
layout, and why. Leave as "none" if the default layout was used as-is.>
