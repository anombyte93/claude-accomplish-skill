---
name: accomplish
description: Log an accomplishment to Daily_Accomplishments and session-context. Use when the user wants to record a win, milestone, or personal achievement.
triggers:
  - "/accomplish"
  - "log accomplishment"
  - "record accomplishment"
  - "add accomplishment"
user-invocable: true
allowed-tools:
  - Bash
  - Edit
  - Write
  - Read
  - AskUserQuestion
---

# Accomplish - Daily Accomplishment Logger

**Script**: `~/.claude/skills/accomplish/script.py` handles all file I/O.

## Usage

```
/accomplish <description of what was accomplished>
```

## Execution

### STEP 1 — Gather Input

If user provided a description, use it as `ACCOMPLISHMENT_TEXT`. Otherwise ask:

```yaml
question: "What did you accomplish?"
header: "Win"
options: []
multiSelect: false
```

### STEP 2 — Gather Context

```bash
python3 ~/.claude/skills/accomplish/script.py gather-context
```

Returns JSON with: `date_file`, `timestamp`, `daily_path`, `daily_exists`, `session_context_path`, `has_accomplishments_section`, `git_log`, `git_diff`.

### STEP 3 — Build the Entry (AI judgment)

Using `ACCOMPLISHMENT_TEXT`, `git_log`, `git_diff`, and session context, craft:

```markdown
### TIMESTAMP AEDT

**What**: Brief title (from ACCOMPLISHMENT_TEXT)
**Context**: Why this matters — connect to user's journey, business goals, or growth
**Details**: Specifics — repos, files, tools, metrics
**Reflection**: Mirror the user's sentiment genuinely
```

Keep tone authentic. If they're excited, let it show. If it was hard-won, note the struggle.
Include tables if the accomplishment involves structured data.

### STEP 4 — Write Daily File

```bash
python3 ~/.claude/skills/accomplish/script.py write-entry \
  --file "DAILY_PATH" \
  --entry "FORMATTED_ENTRY" \
  --create  # only if daily_exists is false
```

### STEP 5 — Mirror to Session Context

Only if `session_context_path` was found:

```bash
python3 ~/.claude/skills/accomplish/script.py write-mirror \
  --file "SESSION_CONTEXT_PATH" \
  --line "**TIMESTAMP AEDT** - One-liner summary"
```

### STEP 6 — Confirm

Output briefly:
```
Logged to ~/Hermes/Daily_Accomplishments/DATE_FILE.md
Mirrored to session-context/CLAUDE-activeContext.md
```

## Rules

- NEVER skip the timestamp
- NEVER overwrite existing entries — always APPEND
- Daily_Accomplishments lives at `~/Hermes/Daily_Accomplishments/` (FIXED)
- Session context mirroring is per-project (wherever `session-context/` lives relative to cwd)

## Script Reference

All commands output JSON. Run from any directory.

| Command | Purpose |
|---------|---------|
| `gather-context` | Get date/time (AEDT), git log/diff, file paths and existence flags |
| `write-entry --file PATH --entry TEXT [--create]` | Write/append formatted entry to daily file |
| `write-mirror --file PATH --line TEXT` | Append one-liner to Accomplishments section in session-context |
