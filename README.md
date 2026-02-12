# claude-accomplish-skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/anombyte93/claude-accomplish-skill)](https://github.com/anombyte93/claude-accomplish-skill/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/anombyte93/claude-accomplish-skill)](https://github.com/anombyte93/claude-accomplish-skill/commits/main)
[![GitHub Issues](https://img.shields.io/github/issues/anombyte93/claude-accomplish-skill)](https://github.com/anombyte93/claude-accomplish-skill/issues)

A Claude Code skill that logs rich accomplishments to a daily journal and mirrors summaries to your project's session context.

## The Problem

You ship features, fix bugs, hit milestones — but never write them down. By the end of the week you can't remember what you did. Progress feels invisible.

## The Solution

`/accomplish` captures what you did with full context: git history, session activity, and your own words. It writes a rich, timestamped entry to your daily log and mirrors a one-liner to your active project context.

```
/accomplish Shipped the authentication feature to production
```

That's it. One command. Rich entry with reflection, context, and details — written to `~/Hermes/Daily_Accomplishments/` and mirrored to `session-context/`.

## Installation

### One-liner (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/anombyte93/claude-accomplish-skill/main/install.sh | bash
```

### Manual

```bash
mkdir -p ~/.claude/skills/accomplish
cd ~/.claude/skills/accomplish
curl -fsSL -O https://raw.githubusercontent.com/anombyte93/claude-accomplish-skill/main/SKILL.md
curl -fsSL -O https://raw.githubusercontent.com/anombyte93/claude-accomplish-skill/main/script.py
chmod +x script.py
```

### Update

```bash
curl -fsSL https://raw.githubusercontent.com/anombyte93/claude-accomplish-skill/main/install.sh | bash
```

Or check for updates without installing:

```bash
bash ~/.claude/skills/accomplish/install.sh --check-update
```

## Usage

```
/accomplish <what you accomplished>
/accomplish                           # prompts you to describe it
```

### Examples

```
/accomplish Shipped the authentication feature to production
/accomplish Just hit $33k AUD revenue from vibe-coding in 3 months
/accomplish Fixed the race condition in the payment queue
```

## How It Works

1. **Gathers context** — date/time (AEDT), recent git log, file changes
2. **Builds a rich entry** — AI crafts a reflection connecting your accomplishment to your journey
3. **Writes to daily file** — `~/Hermes/Daily_Accomplishments/12-Feb-26.md`
4. **Mirrors to session context** — one-liner appended to `session-context/CLAUDE-activeContext.md`

### Entry Format

```markdown
### 14:30 AEDT

**What**: Shipped authentication feature
**Context**: Key milestone for the Atlas AI platform launch
**Details**: Implemented OAuth2 with JWT, 3 files changed, 2 new tests
**Reflection**: Hard-won after debugging the token refresh loop for 2 hours
```

## Architecture

The skill uses a **codified architecture** — deterministic file I/O is handled by `script.py`, while AI handles the creative writing (entry composition, reflection, sentiment).

```
SKILL.md (AI judgment)          script.py (deterministic I/O)
├── Ask user what happened      ├── gather-context
├── Build rich entry            ├── write-entry
└── Craft one-liner summary     └── write-mirror
```

### Script Reference

All commands output JSON. Run from any directory.

| Command | Purpose |
|---------|---------|
| `gather-context` | Get date/time (AEDT), git log/diff, file paths and existence flags |
| `write-entry --file PATH --entry TEXT [--create]` | Write/append formatted entry to daily file |
| `write-mirror --file PATH --line TEXT` | Append one-liner to Accomplishments section in session-context |

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| Daily directory | `~/Hermes/Daily_Accomplishments/` | Fixed location for all daily logs |
| Session context | `./session-context/CLAUDE-activeContext.md` | Per-project mirror location |
| Timezone | `Australia/Sydney` (AEDT) | Timestamps use AEDT |

## Requirements

- [Claude Code](https://claude.ai/claude-code) CLI
- Python 3.8+
- Git (for context gathering)

## License

MIT — see [LICENSE](LICENSE)
