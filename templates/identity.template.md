## thread_id
- thread_name: <stable name — a filesystem-safe form of thread_id, e.g. 2026-09-15T13-04-00-04-00>
- thread_id: <the ISO 8601 timestamp of this thread's first user turn — determine and write this
  at turn 1, never recompute it later>

## purpose
<One sentence: what this thread exists to do.>

## reads
- <file or folder this thread treats as input>

## writes
- <file or folder this thread produces>

## typical_recipients
- <thread_name> via <send_message | agent_spawn | shared_file | broadcast>

## trigger
- human | cron: <expression, if automated>

<Note: `trigger: cron: <expression>` records intent only. This plugin does not create or manage
an actual scheduled job — wiring up real automation (e.g. via a scheduling tool) is a separate
step the human owns.>
