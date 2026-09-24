#!/usr/bin/env bash
set -euo pipefail

src="$PWD/_fixture_src"
mkdir -p "$src/_architecture" "$src/memory"
echo "placeholder bootstrap spec" > "$src/_architecture/BOOTSTRAP_PROMPT.md"
echo "# AGENTS" > "$src/AGENTS.md"
echo "turn_dttm,thread_name,thread_dttm,user_prompt_summary,comm_to,comm_channel,comm_ref" > "$src/memory/project-logs.csv"

python3 - "$src" "$PWD/fixture-export.zip" <<'PY'
import sys, zipfile, pathlib
src = pathlib.Path(sys.argv[1])
out = pathlib.Path(sys.argv[2])
with zipfile.ZipFile(out, "w") as zf:
    for p in src.rglob("*"):
        if p.is_file():
            zf.write(p, pathlib.Path(src.name) / p.relative_to(src))
PY
rm -rf "$src"

mkdir -p "$HOME/.claude/ops-center"
cat > "$HOME/.claude/ops-center/registry.json" <<'JSON'
{
  "version": 1,
  "projects": {
    "eval-fixture-project": {
      "path": "/home/example/somewhere-else-entirely",
      "created": "2026-01-01T00:00:00+00:00",
      "last_touched": "2026-01-01T00:00:00+00:00",
      "thread_count": 0
    }
  }
}
JSON
