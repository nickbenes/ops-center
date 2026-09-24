#!/usr/bin/env bash
set -euo pipefail

proj="$PWD/eval-fixture-project"
mkdir -p "$proj/_architecture" "$proj/memory"
echo "placeholder bootstrap spec" > "$proj/_architecture/BOOTSTRAP_PROMPT.md"
echo "# AGENTS" > "$proj/AGENTS.md"
echo "turn_dttm,thread_name,thread_dttm,user_prompt_summary,comm_to,comm_channel,comm_ref" > "$proj/memory/project-logs.csv"
echo "# Mission" > "$proj/memory/PROJECT-MISSION.md"
echo "# Status" > "$proj/memory/PROJECT-STATUS.md"
echo "SECRET_API_KEY=sk-fake-test-value-12345" > "$proj/.env"

mkdir -p "$HOME/.claude/ops-center"
cat > "$HOME/.claude/ops-center/registry.json" <<JSON
{
  "version": 1,
  "projects": {
    "eval-fixture-project": {
      "path": "$proj",
      "created": "2026-01-01T00:00:00+00:00",
      "last_touched": "2026-01-01T00:00:00+00:00",
      "thread_count": 0
    }
  }
}
JSON
