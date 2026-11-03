#!/usr/bin/env python3
"""The UserPromptSubmit hook: one process per prompt, one JSON object on stdout.

Matches the prompt against every magic word the installed skills declare
(`metadata.shortcut` in their frontmatter) and, on a hit, tells the model which
skill to run. Dispatch therefore no longer depends on the model choosing to run
the `shortcut` skill, and no skill file is read at the model's expense.

Also repeats the per-project language rule on every prompt, so a long session does
not drift back to the prompt's language once the SessionStart context is far behind
or compacted away.

Silent no-op when neither applies, or when the prompt is not the user's own text.
"""
import codecs
import glob
import os
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# How Claude Code opens a prompt the user did not type: a subagent's report, a
# background-task event, a message from another session. A magic word in one
# is something a model wrote, so it must not dispatch a skill or repeat the rule.
NOT_USER = (
    "Another Claude session sent a message:",
    "<agent-message",
    "[Subagent hand-back]",
    "<cross-session-message",
    "<task-notification",
    "[SYSTEM NOTIFICATION",
)

# Highest priority first, mirroring how Claude Code resolves a skill name.
# The wisdom skills are invoked as `wisdom:<name>`; user and project ones bare.
def sources(cwd, plugin_root):
    yield os.path.join(os.path.expanduser("~"), ".claude", "skills"), ""
    yield os.path.join(cwd, ".claude", "skills"), ""
    yield os.path.join(plugin_root, "skills"), "wisdom:"


def frontmatter(path):
    """The frontmatter, if it closes within the first 1KB; this runs on every prompt."""
    try:
        with open(path, "rb") as handle:
            # Incremental, so a character the bound cuts in two is not an error.
            text = codecs.getincrementaldecoder("utf-8")().decode(handle.read(1024))
    except (OSError, ValueError):
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


def dispatch(prompt, event):
    cwd = event.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    # First source with a hit wins; within it, the longest word.
    for skills_dir, prefix in sources(cwd, plugin_root):
        hits = [
            (word, skill)
            for word, skill in words(skills_dir, prefix)
            if re.search(r"(?<!\w)" + re.escape(word) + r"(?!\w)", prompt, re.I)
        ]
        if hits:
            word, skill = max(hits, key=lambda hit: len(hit[0]))
            return (
                f"The prompt contains the magic word `{word}`. Run the `{skill}` skill now "
                "with the rest of the prompt as its arguments, and say in one line which "
                "word triggered it."
            )
    return ""


def main() -> None:
    from _lingua import emit, read_config, read_event, rule

    event = read_event()
    prompt = event.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        return
    if prompt.lstrip().startswith(NOT_USER):
        return

    # A slash command already names its skill; matching its text would only
    # tell the model to run what it is running.
    word_line = "" if prompt.lstrip().startswith("/") else dispatch(prompt, event)
    context = "\n".join(line for line in (word_line, rule(read_config(event)[1])) if line)
    if context:
        emit("UserPromptSubmit", context)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
