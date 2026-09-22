---
name: shortcut
description: Dispatches the skill whose magic word appears in the prompt, or lists every magic word available. Use at the start of a turn that may contain one.
license: MIT
allowed-tools:
  - Glob
  - Grep
---

# Shortcut

Find the magic word in the prompt and run the skill that declares it.

## Sources

A skill declares its words in frontmatter as `metadata.shortcut`, a comma-separated string.
Read only that line — Grep `^\s+shortcut:` — never the whole file. Search, highest priority
first:

1. `~/.claude/skills/*/SKILL.md` — user
2. `.claude/skills/*/SKILL.md` — project
3. `../*/SKILL.md`, relative to this skill's base directory — the other `wisdom` skills

## Dispatch

1. Match each word against the prompt as a case-insensitive substring.
2. More than one match: take the highest-priority source, then the longest word.
3. Invoke the matched skill with the rest of the prompt as its arguments, and say in one
   line which word triggered it.
4. No match: do nothing and say nothing.

## Listing

Invoked on its own, with nothing to dispatch, print every word found:

| Magic word | Skill | Source |
| ---------- | ----- | ------ |
