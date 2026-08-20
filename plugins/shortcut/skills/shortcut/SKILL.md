---
name: shortcut
description: Dispatches the skill or command whose declared magic word appears in the prompt. Use at the start of a turn to check whether the user typed a registered trigger phrase, and to list every shortcut available across personal, project and plugin skills.
license: MIT
model: haiku
allowed-tools:
  - Read
  - Glob
  - Grep
metadata:
  author: cmj@cmj.tw
  version: "2.0.0"
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

Read the file's YAML frontmatter and take `metadata.shortcut`, a comma-separated string:

```yaml
metadata:
  shortcut: "challenge this, tenth man"
```

A file may declare several words; multi-word phrases match as exact substrings.

### Files without a `metadata.shortcut`

Fall back to the older contract: find the `## Shortcut` section and take backtick-quoted
words from lines matching `prompt contains {word}`.

The fallback exists because this skill scans user-level and project-level directories as
well as plugin ones, and a skill written by someone else may still declare its words the
old way. A file that has `metadata.shortcut` is read only from frontmatter — its
`## Shortcut` section is prose for human readers, and a backtick there means nothing.

## Dispatch Rules

- Match magic words against the user's prompt; invoke the matching skill or command.
- Multiple matches: prefer highest-priority source, then longest match.
- No match: do nothing.
- After dispatching, inform the user which shortcut was triggered.

## Direct Invocation

When called directly (`shortcut:shortcut`), scan all three sources and list discovered shortcuts as a table:

| Magic Word | Skill / Command | Source | Description |
| ---------- | --------------- | ------ | ----------- |
