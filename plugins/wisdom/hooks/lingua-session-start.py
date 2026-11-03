#!/usr/bin/env python3
"""Lingua SessionStart hook.

Reads the per-project language preference (`memory/lingua.md`) and injects it as
session context, so the user's chosen response language applies automatically
without typing a magic word. Silent no-op when no preference is configured.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main() -> None:
    from _lingua import emit, read_config, read_event, rule

    path, config = read_config(read_event())
    config = config.strip()
    if not config:
        return

    context = (
        f"A `lingua` language preference is configured for this project (from {path}). "
        f"Follow it for the rest of this session:\n\n{config}"
    )
    line = rule(config)
    if line:
        context += f"\n\n{line}"
    emit("SessionStart", context)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
