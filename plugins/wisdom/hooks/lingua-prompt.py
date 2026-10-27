#!/usr/bin/env python3
"""Lingua UserPromptSubmit hook.

Repeats the per-project language rule (`memory/lingua.md`) as one line of context
on every prompt, so a long session does not drift back to the prompt's language
once the SessionStart context is far behind or compacted away. Silent no-op when
no preference is configured or the prompt is empty.
"""
import json
import os
import re
import sys


def frontmatter_value(block: str, key: str) -> str:
    match = re.search(rf"^[ \t]*{key}[ \t]*:[ \t]*(.*?)[ \t]*$", block, re.MULTILINE)
    if not match:
        return ""
    return re.sub(r"\s+#.*$", "", match.group(1)).strip().strip("\"'")


def main() -> int:
    try:
        data = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    except (json.JSONDecodeError, ValueError):
        data = {}
    if not isinstance(data, dict):
        data = {}

    if not (data.get("prompt") or "").strip():
        return 0

    candidates = []
    transcript = data.get("transcript_path") or ""
    if transcript:
        candidates.append(os.path.join(os.path.dirname(transcript), "memory", "lingua.md"))

    cwd = data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    slug = cwd.replace("/", "-").replace(".", "-")
    candidates.append(
        os.path.join(os.path.expanduser("~"), ".claude", "projects", slug, "memory", "lingua.md")
    )

    path = next((p for p in candidates if os.path.isfile(p)), None)
    if not path:
        return 0

    try:
        content = open(path, encoding="utf-8").read()
    except OSError:
        return 0

    match = re.match(r"\s*---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return 0
    block = match.group(1)

    respond_in = frontmatter_value(block, "respond_in")
    if not respond_in:
        return 0
    keep_terms_in = frontmatter_value(block, "keep_terms_in") or "en"
    refine = frontmatter_value(block, "refine_question").lower() == "true"

    context = (
        f"lingua: reply in {respond_in}; keep code, identifiers, commands and paths in "
        f"{keep_terms_in}"
    )
    if refine:
        context += "; restate the question in one line first"
    context += ". Skip if the user said `lingua off` this session."

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
