#!/usr/bin/env python3
"""Plan-restore SessionStart hook.

After an auto-compact, re-injects the project's `PLAN.md` so a running
`wisdom:smith` recovers its state. Acts whenever the file is a wisdom:plan
plan (a `## Units` table with a `Status` column and at least one row), whatever
its units' status; silent no-op otherwise.
"""
import json
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main() -> int:
    from _plan import is_plan

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
    if not is_plan(content):
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
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
