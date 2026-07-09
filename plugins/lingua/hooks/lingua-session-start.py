#!/usr/bin/env python3
"""Lingua SessionStart hook.

Reads the per-project language preference (`memory/lingua.md`) and injects it as
session context, so the user's chosen response language applies automatically
without typing a magic word. Silent no-op when no preference is configured.
"""
import json
import os
import sys


def main() -> int:
    try:
        data = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    except (json.JSONDecodeError, ValueError):
        data = {}

    # The transcript lives at ~/.claude/projects/<slug>/<session>.jsonl, so its
    # parent directory is the project's memory root — the most robust way to
    # locate the config without reimplementing Claude Code's path-slug encoding.
    candidates = []
    transcript = data.get("transcript_path") or ""
    if transcript:
        candidates.append(os.path.join(os.path.dirname(transcript), "memory", "lingua.md"))

    # Fallback: derive the slug from cwd (path separators -> '-').
    cwd = data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    slug = cwd.replace("/", "-").replace(".", "-")
    candidates.append(
        os.path.join(os.path.expanduser("~"), ".claude", "projects", slug, "memory", "lingua.md")
    )

    path = next((p for p in candidates if os.path.isfile(p)), None)
    if not path:
        return 0  # No preference configured — nothing to inject.

    try:
        content = open(path, encoding="utf-8").read().strip()
    except OSError:
        return 0
    if not content:
        return 0

    context = (
        f"A `lingua` language preference is configured for this project (from {path}). "
        "Follow it for the rest of this session:\n\n"
        f"{content}\n\n"
        "Apply these rules: write every response in `respond_in`; keep code, identifiers, "
        "commands, and file paths verbatim in `keep_terms_in`; if `refine_question` is true, "
        "prepend a one-line cleaned restatement of the user's question before answering. "
        "The user may override at any time by saying `lingua off` or asking to change the "
        "language."
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
