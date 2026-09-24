# Installing ops-center

You need [Claude Code](https://claude.com/product/claude-code) installed and signed in. That's
the only requirement — ops-center doesn't need any extra accounts, API keys, or configuration.

## Through the marketplace

In any Claude Code chat:

```
/plugin marketplace add nickbenes/marketplace
/plugin install ops-center@nickbenes-marketplace
```

Confirm it worked by running `/ops-center` with no arguments — it should print the four
available commands (`create`, `run`, `export`, `import`) instead of saying it doesn't recognize
the command.

## Without the marketplace

Paste this into a Claude Code chat and it will fetch and install the plugin for you:

```
Please review and install the skill at github.com/nickbenes/ops-center
```

## What happens on first use

The very first time you run `/ops-center create`, it creates
`~/.claude/ops-center/registry.json` on your machine to keep track of the project you're
setting up. Nothing is sent anywhere else — that file just lives on your own computer, and
`/ops-center run/export/import <name>` read it to look projects up by the name you gave them.

## Updating or removing it

- **Update**: re-run `/plugin install ops-center@nickbenes-marketplace` (or ask Claude to check
  for an update) to pick up a newer version.
- **Remove**: `/plugin uninstall ops-center`. This only removes the plugin itself — any project
  folders you've already created with it, and `~/.claude/ops-center/registry.json`, are left
  alone.
