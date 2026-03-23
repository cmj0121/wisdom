---
name: shortcut
description: Auto-dispatch skills and commands when the user types a magic word.
license: MIT
allowed-tools:
  - Read
  - Glob
  - Grep
metadata:
  author: cmj@cmj.tw
  version: 0.8.1
---

# Shortcut Skill

Recognize magic words in user prompts and dispatch the matching skill or command.

## Scanning Sources

Scan these directories for `.md` files, in priority order (highest first):

| Priority | Source         | Path                |
| -------- | -------------- | ------------------- |
| 1        | User-level     | `~/.claude/skills/` |
| 2        | Project-level  | `.claude/skills/`   |
| 3        | Plugin-bundled | `plugins/*/skills/` |

Also scan command directories:

- `~/.claude/commands/`
- `.claude/commands/`
- `plugins/*/commands/`

## Magic Word Extraction

In each `.md` file, find the `## Shortcut` section and extract backtick-quoted words
from lines matching:

> prompt contains \`{word}\`

A single file may define multiple magic words. Multi-word phrases (e.g.,
`commit it`, `review and refine it`) are matched as exact substrings, not
individual words.

## Dispatch Rules

- Match magic words against the user's prompt; invoke the matching skill or command.
- Multiple matches: prefer the highest-priority source, then longest match.
- No match: do nothing — let Claude handle the prompt with its default behavior.
- After dispatching, inform the user which shortcut was triggered.

## Direct Invocation

When called directly (`shortcut:shortcut`), scan all three sources and list discovered shortcuts as a table,
extracting magic words, skill names, source levels, and descriptions from frontmatter:

| Magic Word | Skill / Command | Source | Description |
| ---------- | --------------- | ------ | ----------- |
