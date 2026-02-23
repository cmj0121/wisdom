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
  version: 0.3.3
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

## Dispatch Result

After processing a user prompt, emit a machine-readable result block:

```text
__DISPATCH_RESULT__
matched: true | false
magic_word: <word or none>
skill: <skill name or none>
source: user | project | plugin | none
status: DISPATCHED | NO_MATCH | ERROR
__DISPATCH_RESULT__
```

- **DISPATCHED**: A magic word was matched and the corresponding skill was invoked.
- **NO_MATCH**: No magic word matched the user's prompt.
- **ERROR**: A magic word matched but the dispatch failed (e.g., skill not found).

## Team Coordination

The `shortcut` skill is a meta-dispatcher in the wisdom plugin suite. It routes user prompts
to the correct skill based on magic words but does not chain into multi-skill workflows itself.

**Contract rules:**

- Always emit the `__DISPATCH_RESULT__` block after processing, whether or not a match was found.
- The dispatched skill is responsible for its own output contracts -- `shortcut` does not
  aggregate or relay downstream result blocks.
- This skill does not invoke `context-checker:check` or any other workflow skills. It is a routing layer only.

## Direct Invocation

When the user calls this skill directly (e.g., `shortcut:shortcut`), list all discovered shortcuts
as a table:

| Magic Word | Skill / Command | Source | Description |
| ---------- | --------------- | ------ | ----------- |

Populate the table by scanning all three sources and extracting the magic words, skill names,
source levels, and descriptions from the frontmatter.
