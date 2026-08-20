---
name: shortcut
description: Auto-dispatch skills and commands when the user types a magic word.
license: MIT
model: haiku
allowed-tools: Read, Glob, Grep
metadata:
  author: cmj@cmj.tw
  version: 1.2.1
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
from lines matching `prompt contains \`{word}\``. A file may define multiple magic
words; multi-word phrases match as exact substrings.

### Authoring Rule

The rule above is what dispatch reads. It is not what a marketplace validator reads:
a collision check cannot afford to miss a declaration, so it deliberately treats
**every** backtick span inside a `## Shortcut` section — and under a plugin README's
Magic Words heading — as a magic word.

So when writing those two sections, put nothing in backticks that is not a magic word,
and write everything else plain. That is a constraint on authors; it does not widen the
extraction rule above.

## Dispatch Rules

- Match magic words against the user's prompt; invoke the matching skill or command.
- Multiple matches: prefer highest-priority source, then longest match.
- No match: do nothing.
- After dispatching, inform the user which shortcut was triggered.

## Direct Invocation

When called directly (`shortcut:shortcut`), scan all three sources and list discovered shortcuts as a table:

| Magic Word | Skill / Command | Source | Description |
| ---------- | --------------- | ------ | ----------- |
