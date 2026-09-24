#!/usr/bin/env python3
"""Shortcut UserPromptSubmit hook.

Matches the prompt against every magic word the installed skills declare
(`metadata.shortcut` in their frontmatter) and, on a hit, tells the model which
skill to run. Dispatch therefore no longer depends on the model choosing to run
the `shortcut` skill, and no skill file is read at the model's expense.
Silent no-op when no word matches.
"""
import glob
import json
import os
import re
import sys

# Highest priority first, mirroring how Claude Code resolves a skill name.
# The wisdom skills are invoked as `wisdom:<name>`; user and project ones bare.
def sources(cwd, plugin_root):
    yield os.path.join(os.path.expanduser("~"), ".claude", "skills"), ""
    yield os.path.join(cwd, ".claude", "skills"), ""
    yield os.path.join(plugin_root, "skills"), "wisdom:"


def frontmatter(path):
    try:
        with open(path, encoding="utf-8") as handle:
            text = handle.read(8192)
    except OSError:
        return ""
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---", 4)
    return text[4:end] if end != -1 else ""


def words(skills_dir, prefix):
    for path in sorted(glob.glob(os.path.join(skills_dir, "*", "SKILL.md"))):
        match = re.search(r"^\s+shortcut:\s*(.+?)\s*$", frontmatter(path), re.M)
        if not match:
            continue
        skill = prefix + os.path.basename(os.path.dirname(path))
        for word in match.group(1).strip("\"'").split(","):
            word = word.strip()
            if word:
                yield word, skill


def main() -> int:
    try:
        data = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    except (json.JSONDecodeError, ValueError):
        data = {}

    prompt = data.get("prompt") or ""
    # A slash command already names its skill; matching its text would only
    # tell the model to run what it is running.
    if not prompt.strip() or prompt.lstrip().startswith("/"):
        return 0

    cwd = data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(os.path.dirname(__file__))

    # First source with a hit wins; within it, the longest word.
    for skills_dir, prefix in sources(cwd, plugin_root):
        hits = [
            (word, skill)
            for word, skill in words(skills_dir, prefix)
            if re.search(r"(?<!\w)" + re.escape(word) + r"(?!\w)", prompt, re.I)
        ]
        if hits:
            word, skill = max(hits, key=lambda hit: len(hit[0]))
            break
    else:
        return 0

    context = (
        f"The prompt contains the magic word `{word}`. Run the `{skill}` skill now with the "
        "rest of the prompt as its arguments, and say in one line which word triggered it."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
