#!/usr/bin/env python3
"""Afk notification hook, and the switch for the mode it serves.

`afk-notify.py on` / `off` writes or removes this session's marker,
`~/.claude/wisdom/afk/<session_id>`. With no argument it is a hook: while the
marker exists, `Stop` and a permission `Notification` ring the terminal (BEL +
OSC 9, plus a Notification Center message under Terminal.app, which shows no
OSC 9), and `SessionEnd` removes the marker.
Silent no-op when the mode is off or the terminal cannot be reached.
"""
import json
import os
import re
import subprocess
import sys

LIMIT = 120
TITLE = "Claude Code"
# The message and title arrive as argv, so no text is ever parsed as AppleScript.
OSASCRIPT = (
    "osascript",
    "-e", "on run argv",
    "-e", "display notification (item 1 of argv) with title (item 2 of argv)",
    "-e", "end run",
)


def marker(session_id):
    # The id becomes a file name; anything else is not an id.
    if not isinstance(session_id, str) or not re.fullmatch(r"[\w-]+", session_id):
        return ""
    return os.path.join(os.path.expanduser("~"), ".claude", "wisdom", "afk", session_id)


def switch(turn_on):
    path = marker(os.environ.get("CLAUDE_CODE_SESSION_ID"))
    if not path:
        print("afk: no session id in CLAUDE_CODE_SESSION_ID, mode unchanged")
        return
    try:
        if turn_on:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, "w").close()
        elif os.path.exists(path):
            os.remove(path)
    except OSError as error:
        print(f"afk: mode unchanged, {error}")
        return
    print("afk: on" if turn_on else "afk: off")


def clean(text):
    # An escape or a BEL in the text would end the OSC sequence it is sent in.
    text = "".join(char for char in text if char.isprintable()).strip()
    return text if len(text) <= LIMIT else text[: LIMIT - 1] + "…"


def last_message(data):
    message = data.get("last_assistant_message")
    if isinstance(message, str) and message.strip():
        return message
    try:
        with open(str(data.get("transcript_path") or ""), "rb") as handle:
            handle.seek(0, os.SEEK_END)
            handle.seek(max(0, handle.tell() - 65536))
            lines = handle.read().decode("utf-8", "replace").splitlines()
    except OSError:
        return ""
    for line in reversed(lines):
        try:
            entry = json.loads(line)
            if entry.get("type") != "assistant":
                continue
            content = entry["message"]["content"]
        except (ValueError, AttributeError, KeyError, TypeError):
            continue
        if isinstance(content, str):
            return content
        return "\n".join(
            block.get("text") or ""
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    return ""


def verdict(message):
    lines = [line.strip(" \t`*_") for line in message.splitlines() if line.strip()]
    last = lines[-1] if lines else ""
    if last == "AFK: DONE":
        return "done"
    ask = re.fullmatch(r"AFK: ASK\b[\s—–:-]*(.*)", last)
    if ask:
        return clean("needs you: " + clean(ask.group(1))).rstrip(": ")
    # A missing line still pings: silence would read as "still working".
    return "stopped"


def tty():
    override = os.environ.get("AFK_NOTIFY_TTY")
    if override:
        return override
    # /dev/tty is not openable from a hook's child process; ask for the TUI's.
    pid = os.environ.get("CLAUDE_PID") or str(os.getppid())
    try:
        name = subprocess.run(
            ["ps", "-o", "tty=", "-p", pid],
            capture_output=True, text=True, timeout=5,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""
    return "/dev/" + name if re.fullmatch(r"[\w/]+", name) else ""


def notify(text):
    path = tty()
    if path:
        try:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(f"\a\x1b]9;{text}\a")
        except OSError:
            pass
    if os.environ.get("TERM_PROGRAM") == "Apple_Terminal":
        try:
            subprocess.run(
                [*OSASCRIPT, text, TITLE],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5,
            )
        except (OSError, subprocess.SubprocessError):
            pass


def main() -> int:
    if len(sys.argv) > 1:
        if sys.argv[1] in ("on", "off"):
            switch(sys.argv[1] == "on")
        return 0

    try:
        data = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    except (json.JSONDecodeError, ValueError):
        data = {}
    if not isinstance(data, dict):
        return 0

    # The marker was written under the environment's id; a hook that does not
    # see that variable, or sees another, still has the payload's.
    for session_id in (os.environ.get("CLAUDE_CODE_SESSION_ID"), data.get("session_id")):
        path = marker(session_id)
        if path and os.path.exists(path):
            break
    else:
        return 0

    event = data.get("hook_event_name")
    if event == "SessionEnd":
        try:
            os.remove(path)
        except OSError:
            pass
    elif event == "Stop":
        notify(verdict(last_message(data)))
    elif event == "Notification":
        message = data.get("message") if isinstance(data.get("message"), str) else ""
        kind = data.get("notification_type")
        # Only known noise is skipped, so an unknown needs-you event still
        # pings: the idle reminder would ring again a minute after Stop did.
        noise = kind in ("idle_prompt", "auth_success") if kind else "waiting for" in message.lower()
        if not noise:
            notify(clean("needs you: " + clean(message)).rstrip(": "))
    return 0


if __name__ == "__main__":
    sys.exit(main())
