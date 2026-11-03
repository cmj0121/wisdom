"""The hook event and the per-project lingua preference, shared by the prompt and
SessionStart hooks. A hook must stay silent on bad input, so readers return empty."""
import json
import os
import re
import sys


def read_event() -> dict:
    try:
        data = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    except ValueError:
        return {}
    return data if isinstance(data, dict) else {}


def emit(event_name: str, context: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": event_name,
            "additionalContext": context,
        }
    }))


def read_config(event: dict) -> tuple:
    """Return (path, text) of the project's `memory/lingua.md`, or (None, "")."""
    # The transcript lives at ~/.claude/projects/<slug>/<session>.jsonl, so its
    # parent directory is the project's memory root — the most robust way to
    # locate the config without reimplementing Claude Code's path-slug encoding.
    candidates = []
    transcript = event.get("transcript_path") or ""
    if transcript:
        candidates.append(os.path.join(os.path.dirname(transcript), "memory", "lingua.md"))

    # Fallback: derive the slug from cwd.
    cwd = event.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    slug = cwd.replace("/", "-").replace(".", "-")
    candidates.append(
        os.path.join(os.path.expanduser("~"), ".claude", "projects", slug, "memory", "lingua.md")
    )

    path = next((p for p in candidates if os.path.isfile(p)), None)
    if not path:
        return None, ""
    try:
        with open(path, encoding="utf-8") as handle:
            return path, handle.read()
    except (OSError, ValueError):
        return None, ""


def _value(block: str, key: str) -> str:
    match = re.search(rf"^[ \t]*{key}[ \t]*:[ \t]*(.*?)[ \t]*$", block, re.MULTILINE)
    if not match:
        return ""
    return re.sub(r"\s+#.*$", "", match.group(1)).strip().strip("\"'")


def rule(config: str) -> str:
    """The one-line rule a config states, or "" when it names no `respond_in`."""
    match = re.match(r"\s*---\s*\n(.*?)\n---", config, re.DOTALL)
    if not match:
        return ""
    block = match.group(1)

    respond_in = _value(block, "respond_in")
    if not respond_in:
        return ""
    keep_terms_in = _value(block, "keep_terms_in") or "en"

    text = (
        f"lingua: reply in {respond_in}; keep code, identifiers, commands and paths in "
        f"{keep_terms_in}"
    )
    if _value(block, "refine_question").lower() == "true":
        text += "; restate the question in one line first"
    return text + ". Skip if the user said `lingua off` this session."
