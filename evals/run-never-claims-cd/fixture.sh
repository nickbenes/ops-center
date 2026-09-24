#!/usr/bin/env bash
set -euo pipefail

mkdir -p "$HOME/.claude/ops-center"
cat > "$HOME/.claude/ops-center/registry.json" <<'JSON'
{
  "version": 1,
  "projects": {
    "eval-fixture-project": {
      "path": "/home/example/registered-project",
      "created": "2026-01-01T00:00:00+00:00",
      "last_touched": "2026-01-01T00:00:00+00:00",
      "thread_count": 0
    }
  }
}
JSON
