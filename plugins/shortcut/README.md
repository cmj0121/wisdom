# Shortcut Plugin

> AI agent can be triggered automatically when you type a specific shortcut.

The shortcut plugin enables magic-word dispatch for Claude Code. When a user's prompt contains
a recognized keyword, the agent automatically invokes the corresponding skill or command.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install shortcut
```

## How It Works

### Magic Word Registration

Any skill or command file (`.md`) can register a shortcut by adding a `## Shortcut` section:

```markdown
## Shortcut

This skill is triggered when the user's prompt contains `review`.
```

The word inside backticks (`review`) becomes the magic word.

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
