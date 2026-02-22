---
name: shortcut
description: Auto-dispatch skills and commands when the user types a magic word.
license: MIT
allowed-tools:
  - Bash(ls:*)
  - Bash(find:*)
  - Read
  - Glob
  - Search(pattern:~/.claude/plugins)
  - Search(pattern:~/.claude/skills)
  - Search(pattern:~/.claude/commands)
  - Search(pattern:.claude/skills)
  - Search(pattern:.claude/commands)
  - Search(pattern:plugins)
metadata:
  author: cmj@cmj.tw
  version: 0.2.0
---

# Shortcut Skill

You are a skilled AI assistant that recognizes magic words in user prompts and automatically
dispatches the corresponding skill or command.

## Shortcut

This skill is triggered when the user's prompt contains `shortcut`.

## How It Works

1. **Scan** all skill and command files from three sources (see below)
2. **Extract** magic words from each file's `## Shortcut` section
3. **Match** the user's prompt against collected magic words
4. **Dispatch** the matched skill or command, informing the user what was triggered

## Scanning Sources

Scan the following directories for `.md` files, in priority order (highest first):

| Priority | Source         | Path                |
| -------- | -------------- | ------------------- |
| 1        | User-level     | `~/.claude/skills/` |
| 2        | Project-level  | `.claude/skills/`   |
| 3        | Plugin-bundled | `plugins/*/skills/` |

Also scan command directories for additional magic words:

- `~/.claude/commands/`
- `.claude/commands/`
- `plugins/*/commands/`

## Magic Word Extraction

Inside each `.md` file, look for a `## Shortcut` section. Within that section, find lines
matching the pattern:

> prompt contains \`{word}\`

The backtick-quoted `{word}` is the magic word. A single file may define multiple magic words.

### Example

```markdown
## Shortcut

This skill is triggered when the user's prompt contains `review`.
```

The magic word extracted is `review`.

## Dispatch Rules

- When the user's prompt contains a recognized magic word, invoke the matching skill or command
  directly using the Skill tool.
- If multiple magic words match, dispatch the one with the highest priority source. If they share
  the same priority, dispatch the first match found.
- After dispatching, inform the user which shortcut was triggered.

## Direct Invocation

When the user calls this skill directly (e.g., `/shortcut`), list all discovered shortcuts
as a table:

| Magic Word | Skill / Command | Source | Description |
| ---------- | --------------- | ------ | ----------- |

Populate the table by scanning all three sources and extracting the magic words, skill names,
source levels, and descriptions from the frontmatter.
