---
name: shortcut
description: Lists every magic word the installed skills declare, or dispatches one by hand when the prompt hook did not. Use to see which words are available.
license: MIT
allowed-tools:
  - Glob
  - Grep
---

# Shortcut

The plugin's `UserPromptSubmit` hook normally dispatches a magic word before this skill is
read. This skill lists the words, and dispatches by hand when the hook did not fire — hooks
disabled, a skill's frontmatter over 1KB, or a word handed over as an argument.

## Sources

A skill declares its words in frontmatter as `metadata.shortcut`, a comma-separated string.
Read only that line — Grep `^\s+shortcut:` — never the whole file. Search, highest priority
first:

1. `~/.claude/skills/*/SKILL.md` — user
2. `.claude/skills/*/SKILL.md` — project
3. `../*/SKILL.md`, relative to this skill's base directory — the other `wisdom` skills

## Dispatch

1. Match the words as the hook does: Grep `def dispatch` with 20 lines of context in
   [`shortcut-prompt.py`](../../hooks/shortcut-prompt.py), the one statement of that rule.
2. Invoke the matched skill with the rest of the prompt as its arguments, and say in one
   line which word triggered it.
3. No match: do nothing and say nothing.

## Listing

Invoked on its own, with nothing to dispatch, print every word found:

| Magic word | Skill | Source |
| ---------- | ----- | ------ |
