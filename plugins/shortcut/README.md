# Shortcut Plugin

> Dispatches the skill or command whose declared magic word appears in the prompt. Use at the start of
> a turn to check whether the user typed a registered trigger phrase, and to list every shortcut
> available across personal, project and plugin skills.

The shortcut plugin enables magic-word dispatch for Claude Code. When a user's prompt contains
a recognized keyword, the agent automatically invokes the corresponding skill or command.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install shortcut
```

## How It Works

### Magic Word Registration

Any skill or command file can register a shortcut by declaring the words in its YAML
frontmatter, as a comma-separated string:

```yaml
metadata:
  shortcut: "review code, qa review"
```

A `## Shortcut` section in the body then spells the same words out for human readers. It is
documentation: once frontmatter declares the words, a backtick in that section is ordinary
prose and can name a file, a tool or another skill freely.

Files with no `metadata.shortcut` fall back to the older contract — backtick-quoted words on
a line reading "triggered when the user's prompt contains ..." inside the `## Shortcut`
section — so a skill written before this change keeps working.

### Three-Tier Scanning

The plugin scans three directory levels in priority order:

| Priority | Source         | Paths                                      |
| -------- | -------------- | ------------------------------------------ |
| 1        | User-level     | `~/.claude/skills/`, `~/.claude/commands/` |
| 2        | Project-level  | `.claude/skills/`, `.claude/commands/`     |
| 3        | Plugin-bundled | `plugins/*/skills/`, `plugins/*/commands/` |

Higher-priority sources win when the same magic word is defined in multiple places.

### Auto-Dispatch

When the user types a prompt containing a magic word, the shortcut skill automatically
invokes the matched skill and informs the user what was triggered.

## Usage

### List All Shortcuts

```text
/shortcut
```

Displays a table of all registered magic words, their skills, sources, and descriptions.

### Auto-Trigger Example

If a skill registers the magic word `review`, simply typing:

```text
Please review this code
```

The agent detects `review` and dispatches the code-review skill automatically.

## License

MIT
