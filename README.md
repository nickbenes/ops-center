# ops-center

Normally, every time you start a new conversation with Claude, it starts from zero — it has no
memory of what you talked about yesterday, or what a different conversation window figured out
five minutes ago. **ops-center gives Claude a shared notebook on your computer** so that any new
conversation can read what earlier ones wrote down, and pick up where things left off, instead of
starting over.

You don't need to install anything to try this. The whole system is just a set of written
instructions for Claude to follow — you can download that instruction file right now:
[`templates/BOOTSTRAP_PROMPT.md`](templates/BOOTSTRAP_PROMPT.md). Paste its contents into a new
chat with Claude and ask it to follow the directions, and you're using ops-center with no install
step at all.

## Installing it (optional)

Installing turns this into a proper add-on ("plugin") for
[Claude Code](https://claude.com/product/claude-code) — Anthropic's coding assistant — so you can
just type `/ops-center create` instead of pasting the instructions file every time. Pick whichever
of these is easiest:

**Option 1 — through the marketplace.** In a Claude Code chat, paste:
```
/plugin marketplace add nickbenes/marketplace
/plugin install ops-center@nickbenes-marketplace
```

**Option 2 — ask Claude to install it for you.** In a Claude Code chat, paste:
```
Please review and install the skill at github.com/nickbenes/ops-center
```

**Option 3 — skip installing anything.** Use
[`templates/BOOTSTRAP_PROMPT.md`](templates/BOOTSTRAP_PROMPT.md) as described above instead.

## What it actually does

ops-center creates a folder of plain files — mostly Markdown notes and a couple of spreadsheets
(CSV files) — that describe a project: what it's for, what's been decided, what's happened so
far, and who's supposed to do what next. Any Claude conversation that opens that folder can read
those files and understand the project without you having to re-explain it.

It also keeps a small list, on your own computer, of every project you've set up this way and
where its folder is — so you can ask for one by name later instead of remembering the path.

## The four commands

Once installed, these are typed directly into a Claude Code chat:

- **`/ops-center create`** — sets up a new project folder. Asks you where to put it and what to
  call it, looks at anything already there, proposes a one-sentence description of what "done"
  looks like for the project, and confirms that with you before writing anything.
- **`/ops-center run <name>`** — reminds you where a project you set up earlier lives, so you can
  open a fresh chat there. (A single conversation can't jump to a different folder on its own —
  this just tells you the path so you can go there yourself.)
- **`/ops-center export <name>`** — packages a project folder into a single `.zip` file you can
  move somewhere else, after checking for anything (like a password or API key) that probably
  shouldn't leave your machine, and warning you before including it.
- **`/ops-center import <path-to-zip>`** — unpacks a `.zip` created by `export` into a folder you
  choose, and picks up its history without rewriting anything.

## For developers

- The plugin's full behavior is written out in `SKILL.md` and `references/*.md`.
- `scripts/registry.py` manages the project list, stored at `~/.claude/ops-center/registry.json`.
- Test locally with `claude --plugin-dir ./ops-center` before opening a PR.
- `claude plugin validate ./ops-center --strict` runs the same structural check CI runs — free,
  no API key needed.
- `claude plugin eval .` runs the behavioral eval suite under `evals/` — also free (it only uses
  graders that don't call a judge model), but not run automatically in CI; run it yourself before
  opening a PR that changes behavior.

## Known limitations

- Only tested with Claude Code running from a real working directory (desktop, terminal, or IDE
  extension). Claude.ai-style harnesses with a "Project" instead of a filesystem aren't
  supported — `/ops-center create` will say so rather than guessing at a substitute.
- `export`/`import` archive the project folder as-is; they don't reformat or compress anything
  beyond a standard zip, and they don't understand version control history beyond whatever files
  happen to be in the folder.
- The registry (`~/.claude/ops-center/registry.json`) is local to one machine — it isn't synced
  or shared between computers.
- Recording a `cron:` trigger in a thread's `identity.md` documents intent only. This plugin
  doesn't create or manage an actual scheduled job.
