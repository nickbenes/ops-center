#!/usr/bin/env python3
"""Get/set/list/touch entries in the ops-center global registry.

Storage: ~/.claude/ops-center/registry.json — maps a chosen ops-center project
name to its absolute folder path plus light metadata. Independent of any
working directory; this is what /ops-center run/export/import look up by name.

Usage:
    registry.py get <name>
    registry.py set <name> <path> [--force]
    registry.py list [--json]
    registry.py touch <name> [--thread-count N]

Exit codes:
    get:    0 found, 1 not found
    set:    0 success or no-op (same path already registered),
            2 name exists pointing at a DIFFERENT path and --force wasn't passed
    list:   0 always
    touch:  0 success, 1 not found
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

REGISTRY_DIR = os.path.expanduser("~/.claude/ops-center")
REGISTRY_PATH = os.path.join(REGISTRY_DIR, "registry.json")


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_registry():
    if not os.path.exists(REGISTRY_PATH):
        return {"version": 1, "projects": {}}
    with open(REGISTRY_PATH, "r") as f:
        return json.load(f)


def save_registry(registry):
    os.makedirs(REGISTRY_DIR, exist_ok=True)
    tmp_path = REGISTRY_PATH + ".tmp"
    with open(tmp_path, "w") as f:
        json.dump(registry, f, indent=2)
        f.write("\n")
    os.replace(tmp_path, REGISTRY_PATH)


def cmd_get(args):
    registry = load_registry()
    entry = registry["projects"].get(args.name)
    if entry is None:
        print(f"No registry entry named '{args.name}'", file=sys.stderr)
        return 1
    print(entry["path"])
    return 0


def cmd_set(args):
    registry = load_registry()
    new_path = os.path.abspath(os.path.expanduser(args.path))
    existing = registry["projects"].get(args.name)

    if existing is not None and existing["path"] == new_path:
        return 0  # already registered at this exact path — idempotent no-op

    if existing is not None and not args.force:
        print(
            f"'{args.name}' is already registered at: {existing['path']}\n"
            f"Pass --force to overwrite with: {new_path}",
            file=sys.stderr,
        )
        return 2

    entry = {
        "path": new_path,
        "created": existing["created"] if existing else now_iso(),
        "last_touched": now_iso(),
        "thread_count": existing["thread_count"] if existing else 0,
    }
    registry["projects"][args.name] = entry
    save_registry(registry)
    return 0


def cmd_list(args):
    registry = load_registry()
    if args.json:
        print(json.dumps(registry["projects"], indent=2))
        return 0
    if not registry["projects"]:
        print("(no registered ops-center projects)")
        return 0
    for name, entry in sorted(registry["projects"].items()):
        print(f"{name}\t{entry['path']}\tlast_touched={entry['last_touched']}\tthreads={entry['thread_count']}")
    return 0


def cmd_touch(args):
    registry = load_registry()
    entry = registry["projects"].get(args.name)
    if entry is None:
        print(f"No registry entry named '{args.name}'", file=sys.stderr)
        return 1
    entry["last_touched"] = now_iso()
    if args.thread_count is not None:
        entry["thread_count"] = args.thread_count
    save_registry(registry)
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_get = sub.add_parser("get")
    p_get.add_argument("name")
    p_get.set_defaults(func=cmd_get)

    p_set = sub.add_parser("set")
    p_set.add_argument("name")
    p_set.add_argument("path")
    p_set.add_argument("--force", action="store_true")
    p_set.set_defaults(func=cmd_set)

    p_list = sub.add_parser("list")
    p_list.add_argument("--json", action="store_true")
    p_list.set_defaults(func=cmd_list)

    p_touch = sub.add_parser("touch")
    p_touch.add_argument("name")
    p_touch.add_argument("--thread-count", type=int, default=None)
    p_touch.set_defaults(func=cmd_touch)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
