#!/usr/bin/env python3
"""Plan-compact PreCompact hook.

Before a compaction, tells the summary what to keep when the project's
`PLAN.md` is a wisdom:plan plan: the plan itself is re-injected from disk
afterwards, so the summary keeps only what the file lacks. Plain stdout on a
PreCompact hook becomes instructions for the summary. Silent no-op otherwise.
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
    if not isinstance(data, dict):
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

    print(
        f"If you are running wisdom:smith, its plan is in {plan}; otherwise ignore this. "
        "PLAN.md is re-injected from disk after compaction, so do not restate it. "
        "Keep only what it lacks: the current step, any question awaiting the user, "
        "and decisions not yet written to it. Drop merged units' reports and diffs. "
        "The user's own /compact instructions, if any, take precedence."
    )
    return 0


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
