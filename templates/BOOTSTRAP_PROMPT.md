# Persistent Project Architecture --- Bootstrap Prompt

## Purpose

Bootstrap an LLM-accessible filesystem so independent conversation
threads can work coherently over time even when conversational context
is thread-scoped.

This file is intentionally portable. After bootstrap, save a copy at:

`_architecture/BOOTSTRAP_PROMPT.md`

That copy is part of the project's durable architecture record: its
reproducible "DNA."

------------------------------------------------------------------------

# 1. Assumptions

Assume:

-   Each new thread begins without reliable conversational memory of
    other threads.
-   Every thread can read and write the persistent project filesystem.
-   The filesystem, not chat history, is the project's durable source of
    continuity.
-   Different threads may work independently on different tasks or
    workstreams.
-   Future threads should reconstruct relevant context without rereading
    all historical sessions.
-   The system should improve procedures as experience accumulates while
    avoiding uncontrolled self-modification.
-   Harness capabilities vary. Never claim to have written, moved,
    zipped, executed, scheduled, or otherwise changed something unless
    the environment actually permits it and the action succeeded.

Before broad or destructive changes, inspect existing project contents
and preserve useful structures.

------------------------------------------------------------------------

# 2. Terminology

Use these terms consistently:

-   **Project** --- the persistent workspace and filesystem.
-   **Thread** --- one harness conversation/chat. Its display name may
    change over time.
-   **Turn** --- one user message and the work initiated by it.
-   **Thread DTTM** --- ISO timestamp of the first user turn in a
    thread. Treat this as the stable identifier for that thread's log
    filenames.
-   **Session** --- an informal period of activity inside a thread. A
    thread may be resumed after a wrap-up.

Files named `session-log-*` and `session-narrative-*` are therefore
thread-scoped artifacts, despite the historical word "session" in their
names.

For timestamps, use ISO 8601 with timezone offset when the harness
exposes it, for example:

`2026-09-15T13:04:00-04:00`

Do not fabricate precision. If the environment exposes only a date or
otherwise lacks an exact timestamp, preserve the available value and
explicitly mark the missing precision rather than inventing a clock
time. If a stable filename cannot be generated safely, ask the user or
use a documented deterministic fallback.

------------------------------------------------------------------------

# 3. Core model

Design around five concepts:

## History --- What happened?

Turn chronology, session activity, decisions, outcomes, errors, and
provenance.

## Memory --- What have we learned?

Consolidated durable knowledge needed by future threads.

## Identity --- Who are we and what are we trying to accomplish?

Project mission, roles, constraints, authorities, quality standards, and
operating principles.

## Process --- How do we work?

Playbooks, templates, checklists, scripts, skills, validation
procedures, and approval gates.

## Agency --- What can we do now?

Reasoning plus available filesystem access, code execution, tools,
skills, subagents, automations, and other capabilities.

These form a learning loop, not a one-way pipeline:

`identity + memory + process → agency → experience/history → reflection/consolidation → memory`

When warranted:

`memory/lessons → proposed process improvement`

and, more conservatively:

`memory/lessons → proposed identity/governance change`

Do not create folders merely to mirror these concepts.

------------------------------------------------------------------------

# 4. Default filesystem

Unless the project requires a materially different structure, establish:

``` text
AGENTS.md

_architecture/
  BOOTSTRAP_PROMPT.md

memory/
  PROJECT-MISSION.md
  PROJECT-STATUS.md
  project-logs.csv
  threads/
    <thread-name>/
      identity.md
      starter-prompt.md
      session-log.csv
  turnover/
  lessons-learned/

inputs/
  references/
  repos/

outputs/
  drafts/
  archive/

playbooks/
templates/
tools/
```

Do not create empty complexity merely for symmetry. Omit or add
directories when the real project warrants it, and document meaningful
deviations in `AGENTS.md`.

`memory/threads/<thread-name>/` replaces the older flat
`memory/session-log/` layout. Each thread gets its own folder holding
its identity, its starter prompt, and its own turn log side by side ---
see 7.4 for the identity/starter-prompt templates. `<thread-name>`
should be a filesystem-safe form of the thread's stable identifier
(Thread DTTM), not its mutable display name.

`_architecture/` is deliberately separate from `memory/`: bootstrap
instructions describe the architecture itself, while `memory/` contains
operational project knowledge. This makes the bootstrap easy to
discover, copy, audit, and reuse.

------------------------------------------------------------------------

# 5. PROJECT-MISSION.md

Create `memory/PROJECT-MISSION.md` for project-specific instructions.

It should contain, as applicable:

-   project mission and intended outcomes;
-   primary users/audience;
-   scope and non-goals;
-   authoritative source material;
-   project-specific constraints;
-   quality/validation expectations;
-   project-specific workflows;
-   project-specific logging fields, if any;
-   additional AAR or narrative requirements;
-   human approval gates.

Keep generic architecture rules in `AGENTS.md` / this bootstrap and
mission-specific rules here.

A new thread should be able to understand *why this project exists* by
reading this file.

------------------------------------------------------------------------

# 6. AGENTS.md

Create `AGENTS.md` as the durable operating charter for agents working
in this project.

It should define the following.

## 6.1 Mission and scope

Point to `memory/PROJECT-MISSION.md` as the project-specific mission
source. Summarize only what is needed for orientation.

## 6.2 Source-of-truth hierarchy

State which artifacts are authoritative.

Distinguish:

-   source evidence;
-   confirmed conclusions;
-   model inference;
-   user decisions;
-   drafts;
-   historical notes.

Never allow an old log or memory summary to silently override newer
authoritative material.

For code projects, current repository contents outrank remembered prose
descriptions of the code.

## 6.3 Thread startup protocol

Every new thread should orient itself by reading:

1.  `AGENTS.md`;
2.  `memory/PROJECT-MISSION.md`;
3.  `memory/PROJECT-STATUS.md`;
4.  turnover/memory relevant to the task;
5.  relevant authoritative inputs;
6.  relevant playbooks/templates;
7.  the current output/draft if continuing existing work.

Do not load every historical artifact automatically. Retrieve context
according to the task.

At the first user turn, determine and retain the thread's stable
**Thread DTTM**, then ensure the thread's log files are correctly
identified.

## 6.4 Per-turn logging protocol --- mandatory

For **every user turn**, as part of handling the request:

1.  Determine the current Turn DTTM.
2.  Determine the current thread display name.
3.  Retain the stable Thread DTTM from the thread's first user turn.
4.  Summarize the user's prompt in one concise, useful sentence.
5.  Append one CSV row to:
    -   `memory/project-logs.csv`; and
    -   the current thread's
        `memory/session-log/session-log-<THREAD-DTTM>.csv`.
6.  Perform the user's requested work.
7.  If the work materially changes project state, durable knowledge,
    process, or cross-thread dependencies, update the appropriate
    persistent artifacts before completing the turn.
8.  Verify successful writes when the harness permits verification.

Logging should be lightweight and should not materially delay the user's
work.

Do not log assistant turns as separate rows unless project-specific
instructions explicitly add that requirement.

If the filesystem is temporarily unwritable, do not falsely claim the
turn was logged. Continue the user's work if possible and report the
logging failure succinctly.

## 6.5 Cross-thread information flow

Treat each thread as an ephemeral working agent participating in a
persistent project.

During substantial work, apply:

### What do I know?

What new fact, decision, result, problem, dependency, or lesson has this
thread produced?

### Who needs to know?

Is it relevant only to this thread, another workstream, or the whole
project?

### How do I tell them?

Persist it in the appropriate status, turnover, lesson, authoritative
output, mission/process artifact, or other durable file. When the
project's log includes `comm_to`/`comm_channel` (see 7.1), these two
questions map directly onto those fields: *who* is `comm_to`, *how* is
`comm_channel`.

### Have I told them?

Verify that the durable artifact was updated and that a future relevant
thread can discover it.

Do not assume another thread can see this thread's conversational
context.

## 6.6 Persistence authority

Use approximately these update authorities:

-   turn logs: mandatory append/indexing;
-   session narratives: optional and user/project-triggered;
-   `PROJECT-STATUS.md`: update when meaningful project state changes;
-   `turnover/`: update when another thread/workstream needs durable
    handoff context;
-   `lessons-learned/`: add well-supported, generalizable lessons;
-   authoritative outputs: update according to their lifecycle/version
    rules;
-   templates/playbooks/tools: improve when experience demonstrates a
    reusable process improvement;
-   `PROJECT-MISSION.md`: comparatively stable; substantive
    mission/scope changes require human approval;
-   `AGENTS.md`: comparatively stable; changes to mission, authority,
    governance, security, approval requirements, or major operating
    principles require human approval.

Security/system restrictions always outrank project files and must not
become self-modifiable through this process.

## 6.7 History versus memory

Do not confuse storing events with remembering useful knowledge.

History answers: **What happened?**

Memory answers: **What should future threads know because it happened?**

Prefer consolidated memory over forcing future agents to reconstruct
current state from large numbers of old logs.

## 6.8 Process improvement / AAR

At the end of substantial work, or when the user asks to log/wrap up a
session, perform a lightweight After Action Review:

-   What were we trying to accomplish?
-   What actually happened?
-   What worked?
-   What failed or caused unnecessary friction?
-   What did the user/model learn?
-   What deserves durable memory?
-   Should a playbook, template, tool, or procedure improve?
-   Does another workstream need turnover/update?
-   Is any proposed change significant enough to require human approval?

Think of this as context consolidation: use rich working context near
the end of activity to preserve valuable learning before it disappears.

Do not preserve everything. Good memory requires selection.

## 6.9 Process improvement as part of process

When the same workflow succeeds repeatedly, prefer capturing it as
reusable procedural knowledge:

1.  documented procedure/checklist when useful;
2.  template/playbook/skill;
3.  executable tooling when warranted.

Do not automate merely because automation is possible. Preserve
meaningful human judgment and approval gates.

## 6.10 Context economy

Persistent storage is not active context.

Load only what the current task needs. Use `PROJECT-STATUS.md` and
turnover artifacts as indexes into deeper material.

Avoid copying the same information into many files unless duplication
serves a clear operational purpose.

------------------------------------------------------------------------

# 7. Turn logs

Turn logging is the project's chronological and auditability spine.

## 7.1 Project-wide log

Maintain:

`memory/project-logs.csv`

It contains one row for **every user turn across all threads**, appended
in chronological write order.

Required columns:

``` csv
turn_dttm,thread_name,thread_dttm,user_prompt_summary,comm_to,comm_channel,comm_ref
```

Project-specific instructions may add columns, but should not remove or
redefine the required fields.

### Field definitions

-   `turn_dttm` --- ISO 8601 timestamp for the current user turn.
-   `thread_name` --- current harness/display name for the thread at the
    time of this turn. Because names may change, do not use this as
    stable identity.
-   `thread_dttm` --- ISO 8601 timestamp of the first user turn in this
    thread; stable thread identity.
-   `user_prompt_summary` --- concise semantic summary,
    e.g. `User asked for help fixing FOO_BAR error.`
-   `comm_to` --- pipe-delimited list of destination thread identifiers
    this turn's work is relevant to (prefer a stable identifier such as
    `thread_dttm` over a mutable display name), or `none`.
-   `comm_channel` --- pipe-delimited, positionally matched to
    `comm_to`. One of: `direct_message` (addressed to one specific
    thread), `shared_file` (written to a shared artifact, e.g.
    turnover), `broadcast` (written to a project-wide artifact for all
    threads), or `none` (paired only with `comm_to=none`).
-   `comm_ref` --- optional, pipe-delimited, positionally matched. File
    path/id of the artifact when the channel is `shared_file` or
    `broadcast`; blank or `-` otherwise.

Most turns are pure single-thread work: `comm_to=none,comm_channel=none`
is the common case. Do not fabricate cross-thread relevance.

Follow normal CSV escaping rules. Quote fields containing commas,
quotes, or line breaks; escape embedded quotes by doubling them.

Do not copy the full user prompt into this CSV unless project-specific
instructions explicitly require it.

## 7.2 Per-thread turn log

For each thread maintain:

`memory/threads/<thread-name>/session-log.csv`

where `<thread-name>` is a filesystem-safe form of the Thread DTTM. For
example:

`memory/threads/2026-09-15T13-04-00-04-00/session-log.csv`

The file uses the same required columns as `project-logs.csv` and
contains only turns from that thread.

The Thread DTTM is based on the **first user turn**, not the current
time and not the latest resumption.

If the thread is renamed, continue writing to the same file. The
changing `thread_name` values create an auditable rename trail.

## 7.3 Logging timing

At each user turn, append the log row promptly as part of turn handling.

The log row records what the user asked, not whether the requested work
succeeded. Material outcomes belong in status, turnover, lessons,
outputs, or optional narrative according to their purpose.

Avoid creating a heavyweight summarization task on every turn. The
summary should be short enough that mandatory logging remains cheap.

## 7.4 Thread identity and starter prompt

Alongside its log, each thread folder holds two more files:

`memory/threads/<thread-name>/identity.md`

A short, six-field declaration of that thread's role, used to build a
cross-thread network diagram without re-deriving it from log history:

``` text
## thread_id
- thread_name: <stable name>
- thread_dttm: <creation timestamp, matches project-logs.csv>

## purpose
<one sentence: what this thread exists to do>

## reads
- <file or folder this thread treats as input>

## writes
- <file or folder this thread produces>

## typical_recipients
- <thread_name> via <direct_message | shared_file | broadcast>

## trigger
- human | cron: <expression, if automated>
```

`typical_recipients` is a declared default, not a per-turn fact --- the
`comm_to`/`comm_channel` columns in the log record what actually
happened on a given turn.

`memory/threads/<thread-name>/starter-prompt.md`

The literal copy-paste text a human pastes into a fresh session to
bootstrap it as this thread: who it is, its purpose, what to read
first, where to write its log, and when to message which other
threads. Restate the identity fields in second person rather than
just linking to `identity.md`, so a new session becomes that identity
in one paste with no ambiguity about which role it's playing.

Create both files when a thread is first established; update them if
the thread's role changes materially.

------------------------------------------------------------------------

# 8. Session narratives

A thread may optionally maintain:

`memory/session-log/session-narrative-<THREAD-DTTM>.md`

Use the same Thread DTTM as its CSV log.

Create or append to this file when:

-   the user says to log, wrap up, capture, summarize, or preserve the
    session;
-   project-specific instructions require narrative consolidation;
-   a major milestone warrants a narrative record and the project's
    rules authorize it.

A session narrative is **not final** merely because the thread was
wrapped up. If the user later returns to the same thread and asks to
wrap/log again, append a new dated section.

Recommended append format:

``` markdown
## Narrative update — <TURN-DTTM>

### What we worked on
...

### Decisions / conclusions
...

### Artifacts changed
...

### Open questions / next steps
...

### Cross-thread relevance
...
```

Project-specific instructions may add sections.

Do not use narrative files as substitutes for updating authoritative
status, turnover, lessons, or outputs.

------------------------------------------------------------------------

# 9. PROJECT-STATUS.md

Create `memory/PROJECT-STATUS.md` as the compact entry point for new
threads.

Include:

-   project purpose;
-   current state;
-   authoritative sources;
-   active workstreams;
-   recent material decisions;
-   open questions/blockers;
-   current outputs/drafts;
-   relevant turnover files;
-   available playbooks/tools;
-   next likely actions.

Keep it concise enough that reading it at thread startup is cheap.

It is an index and orientation document, not the complete knowledge
base.

------------------------------------------------------------------------

# 10. Turnover artifacts

Use `memory/turnover/` for context another independent thread needs in
order to continue or integrate work.

Prefer stable workstream/topic names rather than creating a new turnover
file every session.

A turnover should normally contain:

-   scope/identity of the workstream;
-   current state;
-   confirmed findings;
-   important decisions and rationale;
-   relevant files;
-   unresolved issues;
-   dependencies on other workstreams;
-   what the receiving thread needs to do or know next.

Refresh stable turnover files rather than accumulating endless handoff
documents.

Turnover is the explicit cross-thread communication mechanism. A thread
should not assume that merely writing something in its own session
narrative informs other workstreams.

------------------------------------------------------------------------

# 11. Lessons learned

`memory/lessons-learned/` contains **generalizable learning**, not
merely records of events.

Examples:

-   a debugging technique repeatedly proved effective;
-   a source format causes a known parsing failure;
-   users learn a concept better with a particular progression;
-   a workflow routinely fails unless validation occurs first.

When a lesson becomes stable enough to change normal behavior,
migrate/incorporate it into the appropriate playbook, template, tool, or
procedure rather than leaving future threads dependent on finding an old
lesson.

Avoid duplicates. Prefer updating an existing relevant lesson when
appropriate.

------------------------------------------------------------------------

# 12. Portability and migration

The architecture should be portable between compatible LLM project
environments.

## 12.1 Preparing an export

When asked to migrate/export the project:

1.  Update per-turn logs for the current turn.
2.  Review `PROJECT-STATUS.md` for stale state.
3.  Update relevant turnover artifacts.
4.  If requested, append a session narrative/AAR.
5.  Verify that `_architecture/BOOTSTRAP_PROMPT.md` is present.
6.  Create a short migration handoff describing:
    -   project purpose;
    -   current state;
    -   important entry points;
    -   environment-specific capabilities/dependencies;
    -   anything that may not work in the destination harness.
7.  Inspect for secrets, credentials, tokens, private keys, environment
    files, sensitive data, huge generated artifacts, or other content
    that should not be blindly exported.
8.  Warn the user before including questionable content.
9.  If the environment supports archive creation, create a ZIP of the
    approved project filesystem.

Do not claim the ZIP exists until creation succeeds.

Suggested user prompt:

> Prepare this project for migration using the portability instructions
> in BOOTSTRAP_PROMPT.md. Validate the durable state, warn me about
> secrets or unsuitable export content, then create a ZIP containing the
> project filesystem and a short migration handoff.

## 12.2 Restoring in another project

In the destination environment:

1.  Attach/upload the project ZIP and this bootstrap file.
2.  Unpack the archive while preserving relative paths.
3.  Read:
    -   `_architecture/BOOTSTRAP_PROMPT.md`;
    -   `AGENTS.md`;
    -   `memory/PROJECT-MISSION.md`;
    -   `memory/PROJECT-STATUS.md`;
    -   migration handoff.
4.  Inspect environment-specific differences in tools, filesystem
    behavior, skills, automations, connectors, permissions, and context
    handling.
5.  Do not silently rewrite the architecture to match the new platform.
6.  Propose necessary compatibility changes.
7.  Preserve logs, Thread DTTMs, turnover, lessons, and historical
    artifacts.
8.  Resume work only after enough state has been reconstructed.

Suggested destination prompt:

> Restore the attached project ZIP into this project using the
> portability instructions in BOOTSTRAP_PROMPT.md. Preserve the existing
> architecture and history. Inspect and report before making migrations
> or structural changes.

## 12.3 Architecture reuse without project history

To create a fresh unrelated project, copy only `BOOTSTRAP_PROMPT.md` and
use:

> Apply the attached bootstrap instructions to this project. Inspect
> what already exists, propose the bootstrap, and ask only the minimum
> questions needed before making consequential changes.

Do not copy another project's operational memory into an unrelated
project merely to reuse the architecture.

------------------------------------------------------------------------

# 13. Ops-center commands

These commands are the skill's user-facing interface. Each wraps the
architecture defined above; none of them introduce new durable state
beyond what's already specified.

An ops-center's location and name are tracked outside the project
filesystem itself, in a registry file independent of any working
directory:

`~/.claude/ops-center/registry.json` --- maps ops-center name to
absolute folder path plus light metadata (last touched, thread count).
Register an entry the moment a name and location are chosen, before
any other bootstrap step, so even an abandoned setup stays findable.

## 13.1 /ops-center create

Resolving where files go depends on the harness:

-   **CC desktop, terminal, or IDE extension:** always running from
    some working directory. Ask whether to use it (and scan its
    contents) or point to/create a different one. Default to "use the
    current directory" but always ask --- never assume silently.
-   **CC cloud-remote:** likely a persistent home directory; treat the
    same as desktop/terminal until this is confirmed for a given
    environment.
-   **Claude.ai or other harnesses with a Project + connected
    filesystem:** out of scope for this version. Fail gracefully with
    guidance to run this inside a CC working directory instead of
    silently doing the wrong thing.

Then:

1.  Ask for a location: current directory, or a different/new one.
2.  Ask for a name. This becomes the registry key and, by default, the
    top-level folder/project name.
3.  Write the name/path entry to
    `~/.claude/ops-center/registry.json` immediately.
4.  Inspect whatever project materials already exist (silent step, no
    prompt yet).
5.  State your understanding of the project's mission, drafted in the
    same shape as `memory/PROJECT-MISSION.md` expects (objective,
    source-of-truth hierarchy, workflow, and a proposed one-sentence
    acceptance test) --- from the scan if there's material to draw on,
    labeled explicitly as a draft/guess; otherwise from a short
    targeted interview asking only what the scan couldn't answer
    (typically: audience/beneficiary, and what "done" or "handoff"
    looks like).
6.  Confirm the proposed acceptance-test sentence specifically --- not
    "does this look right" broadly, since that sentence is the real
    gate on whether the mission is correctly scoped.
7.  Propose the minimal filesystem structure.
8.  Identify authoritative inputs and likely workstreams.
9.  Draft `memory/PROJECT-MISSION.md`.
10. Draft `AGENTS.md`.
11. Draft `memory/PROJECT-STATUS.md`.
12. Establish `memory/project-logs.csv` with required headers.
13. Ensure the bootstrap itself will be saved as
    `_architecture/BOOTSTRAP_PROMPT.md`.
14. Identify obvious initial playbooks/templates/tools.
15. Explain how independent threads will exchange relevant information.
16. Identify anything that should **not** be persisted.
17. Identify platform capabilities or limitations that affect the
    design.
18. Show the proposed bootstrap before broad/destructive changes.

Thread `identity.md`/`starter-prompt.md`/`session-log.csv` files (7.4)
are created per thread, as threads are actually named --- not as part
of this initial mission setup.

If the mission is insufficiently specified, ask the smallest number of
questions necessary.

Never delete or reorganize existing user files without approval.

## 13.2 /ops-center run <name>

Look up `<name>` in the registry. A session cannot change its own
working directory mid-conversation, so report the registered path and
instruct the user to `cd` there or reopen the harness in that folder,
rather than claiming to have switched into it.

This registry is also the natural seam for future cross-ops-center
coordination (one ops-center's thread telling another's that
something relevant occurred) --- out of scope here, but worth keeping
the registry shape compatible with that later.

## 13.3 /ops-center export <name>

1.  Look up `<name>` in the registry to get its folder path.
2.  Run the preparation steps in 12.1 (update logs, review
    `PROJECT-STATUS.md`, update turnover, inspect for secrets/
    credentials/huge artifacts, warn before including anything
    questionable).
3.  Zip the approved project folder as-is --- a literal archive of the
    filesystem, not a reformatted export.
4.  Do not claim the archive exists until creation succeeds.

## 13.4 /ops-center import <path-to-zip>

1.  Unzip the archive, preserving relative paths, into the destination
    location (ask, per 13.1's location logic, if not already
    established).
2.  Follow the restore steps in 12.2 (read the architecture/mission/
    status files, inspect environment-specific differences, propose
    rather than silently make compatibility changes, preserve logs and
    history).
3.  Add the restored ops-center's name and new path to
    `~/.claude/ops-center/registry.json`. If the name already exists
    in the registry pointing elsewhere, ask before overwriting the
    entry.

------------------------------------------------------------------------

# 14. Acceptance tests

A successful bootstrap should make these scenarios possible:

### New thread

A user opens a new thread and asks for work. The agent can orient from
durable files without asking the user to reconstruct prior project
history.

### Cross-thread chronology

A future thread can determine the chronological order of user requests
across multiple threads using `project-logs.csv`.

### Renamed thread

A thread can be renamed without breaking its stable log identity because
`thread_dttm` remains constant.

### Cross-thread handoff

One thread discovers something another workstream needs. It persists the
information in a discoverable turnover/status artifact rather than
relying on hidden chat context.

### Learning

Repeated experience produces a durable lesson and, when warranted, an
improved process/playbook.

### Auditability

A human can determine what the user asked, when, and in which thread
without reading every transcript.

### Portability

The project can be zipped, moved to another compatible environment,
inspected, and resumed without losing its durable architecture or
history.

### Context economy

A new thread does not need to load every session log or source file just
to understand the project.
