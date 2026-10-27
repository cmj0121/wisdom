#!/usr/bin/env python3
"""Plan-restore SessionStart hook.

After an auto-compact, re-injects the project's `PLAN.md` so a running
`wisdom:smith` recovers its state. Acts only when the plan has wisdom:plan's
`## Units` table with a `Status` column and at least one unit not `done`;
silent no-op otherwise.
"""
import json
import os
import sys


def cells(line: str) -> list:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def has_open_unit(content: str) -> bool:
    lines = content.splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == "## Units")
    except StopIteration:
        return False

    table = []
    for line in lines[start + 1:]:
        if line.strip().startswith("|"):
            table.append(line)
        elif table or line.startswith("#") or line.strip():
            break
    if len(table) < 3:
        return False

    header = cells(table[0])
    if "Status" not in header:
        return False
    col = header.index("Status")
    for row in table[2:]:
        row_cells = cells(row)
        if col < len(row_cells) and row_cells[col] != "done":
            return True
    return False


def main() -> int:
    try:
        data = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    except (json.JSONDecodeError, ValueError):
        return 0
    if not isinstance(data, dict) or data.get("source") != "compact":
        return 0

    cwd = data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    plan = os.path.join(cwd, "PLAN.md")
    try:
        with open(plan, encoding="utf-8") as f:
            content = f.read()
    except (OSError, ValueError):
        return 0
    if not has_open_unit(content):
        return 0

    details = os.path.join(cwd, "PLAN_DETAILS.md")
    context = (
        f"Context was compacted. If you are running wisdom:smith, its state is below "
        f"(from {plan}); builders' details are in {details}. Otherwise ignore it.\n\n"
        f"{content}"
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
