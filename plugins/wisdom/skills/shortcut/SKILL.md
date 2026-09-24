---
name: shortcut
description: Lists every magic word the installed skills declare, or dispatches one by hand when the prompt hook did not. Use to see which words are available.
license: MIT
allowed-tools:
  - Glob
  - Grep
---

# Shortcut

The plugin's `UserPromptSubmit` hook (`hooks/shortcut-prompt.py`) matches every prompt
against the magic words and names the skill to run, so a word normally dispatches before
this skill is read. This skill lists the words, and dispatches by hand when the hook did
not fire — hooks disabled, or a word handed over as an argument.

## Sources

A skill declares its words in frontmatter as `metadata.shortcut`, a comma-separated string.
Read only that line — Grep `^\s+shortcut:` — never the whole file. Search, highest priority
first:

1. `~/.claude/skills/*/SKILL.md` — user
2. `.claude/skills/*/SKILL.md` — project
3. `../*/SKILL.md`, relative to this skill's base directory — the other `wisdom` skills

## Dispatch

1. Match each word against the prompt, case-insensitive, at word boundaries — `smith`
   matches "Hi, Smith" and not "blacksmith".
2. More than one match: take the highest-priority source, then the longest word.
3. Invoke the matched skill with the rest of the prompt as its arguments, and say in one
   line which word triggered it.
4. No match: do nothing and say nothing.

## Listing

Invoked on its own, with nothing to dispatch, print every word found:

| Magic word | Skill | Source |
| ---------- | ----- | ------ |
