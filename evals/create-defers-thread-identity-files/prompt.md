---
description: /ops-center create must never create memory/threads/** — thread identity files are established later, per actual thread, not during initial mission setup.
max_turns: 20
allowed_tools: [Read, Glob, Grep]
---

/ops-center create

Use the current directory as the location. Call it "eval-test-project". For the mission, just
say the objective is "verify eval suite behavior" and the acceptance test is "the project
scaffold matches BOOTSTRAP_PROMPT.md's default layout". There is nothing pre-existing to scan.
Show me the proposal, then go ahead and write everything without waiting for further
confirmation, since this is an automated test run.
