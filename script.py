#!/usr/bin/env python3
"""Accomplish skill - deterministic operations for daily accomplishment logging."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

DAILY_DIR = Path.home() / "Hermes" / "Daily_Accomplishments"


def _out(data):
    print(json.dumps(data, indent=2))


def _run(cmd, cwd=None):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=10, cwd=cwd)
        return r.stdout.strip()
    except Exception:
        return ""


def cmd_gather_context(args):
    """Gather all context needed for building an accomplishment entry."""
    # Date/time in AEDT
    date_file = _run(["date", "+%-d-%b-%y"], cwd=None)
    timestamp = _run(["date", "+%H:%M"], cwd=None)

    # Override with AEDT
    date_file = _run(["env", "TZ=Australia/Sydney", "date", "+%-d-%b-%y"])
    timestamp = _run(["env", "TZ=Australia/Sydney", "date", "+%H:%M"])

    # Git context
    git_log = _run(["git", "log", "--oneline", "-10"])
    git_diff = _run(["git", "diff", "--stat", "HEAD~5..HEAD"])

    # Daily file
    daily_path = DAILY_DIR / f"{date_file}.md"
    daily_exists = daily_path.exists()

    # Session context - search order
    session_context_path = None
    candidates = [
        Path.cwd() / "session-context" / "CLAUDE-activeContext.md",
        Path.home() / "Hermes" / "chris" / "session-context" / "CLAUDE-activeContext.md",
    ]
    for c in candidates:
        if c.exists():
            session_context_path = str(c)
            break

    # Check if session-context has accomplishments section
    has_accomplishments_section = False
    if session_context_path:
        try:
            content = Path(session_context_path).read_text()
            has_accomplishments_section = "## Accomplishments" in content
        except Exception:
            pass

    _out({
        "status": "ok",
        "date_file": date_file,
        "timestamp": timestamp,
        "daily_path": str(daily_path),
        "daily_exists": daily_exists,
        "session_context_path": session_context_path,
        "has_accomplishments_section": has_accomplishments_section,
        "git_log": git_log,
        "git_diff": git_diff,
    })


def cmd_write_entry(args):
    """Write or append an accomplishment entry to the daily file."""
    path = Path(args.file)
    entry = args.entry

    # Ensure directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    if args.create:
        # New file with header
        date_label = path.stem  # e.g. "10-Feb-26"
        content = f"# Accomplishments - {date_label}\n\n---\n\n{entry}\n"
        path.write_text(content)
    else:
        # Append to existing
        existing = path.read_text()
        if not existing.endswith("\n"):
            existing += "\n"
        content = existing + f"\n---\n\n{entry}\n"
        path.write_text(content)

    _out({"status": "ok", "path": str(path), "mode": "create" if args.create else "append"})


def cmd_write_mirror(args):
    """Append a one-liner to the Accomplishments section in session-context."""
    path = Path(args.file)
    if not path.exists():
        _out({"status": "error", "message": f"File not found: {path}"})
        sys.exit(1)

    content = path.read_text()
    line = args.line

    if "## Accomplishments" in content:
        # Append to existing section - find the section and add after last bullet
        lines = content.split("\n")
        insert_idx = None
        in_section = False
        for i, l in enumerate(lines):
            if l.strip() == "## Accomplishments":
                in_section = True
                continue
            if in_section:
                if l.startswith("## ") and l.strip() != "## Accomplishments":
                    # Hit next section, insert before it
                    insert_idx = i
                    break
                if l.strip():
                    insert_idx = i + 1  # After last non-empty line in section

        if insert_idx is None:
            insert_idx = len(lines)

        lines.insert(insert_idx, f"- {line}")
        content = "\n".join(lines)
    else:
        # Create new section at end
        if not content.endswith("\n"):
            content += "\n"
        content += f"\n## Accomplishments\n\n- {line}\n"

    path.write_text(content)
    _out({"status": "ok", "path": str(path), "mode": "appended"})


def main():
    parser = argparse.ArgumentParser(description="Accomplish skill operations")
    sub = parser.add_subparsers(dest="command")

    # gather-context
    sub.add_parser("gather-context", help="Get date, time, git context, file paths")

    # write-entry
    p_write = sub.add_parser("write-entry", help="Write/append entry to daily file")
    p_write.add_argument("--file", required=True, help="Path to daily accomplishments file")
    p_write.add_argument("--entry", required=True, help="Formatted markdown entry")
    p_write.add_argument("--create", action="store_true", help="Create new file (vs append)")

    # write-mirror
    p_mirror = sub.add_parser("write-mirror", help="Append one-liner to session-context")
    p_mirror.add_argument("--file", required=True, help="Path to CLAUDE-activeContext.md")
    p_mirror.add_argument("--line", required=True, help="One-liner summary to append")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmds = {
        "gather-context": cmd_gather_context,
        "write-entry": cmd_write_entry,
        "write-mirror": cmd_write_mirror,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
