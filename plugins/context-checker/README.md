# Context Checker Plugin

> The check policy to ensure the Agent understands the guidelines.

The context-checker plugin provides a checkpoint mechanism for Claude Code. It verifies that
the Agent is aware of and following all established guidelines and skill policies in the current
session. When triggered, the Agent reports its active context and emits an inspection token to
prove policy compliance.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install context-checker
```

## How It Works

### Context Verification

1. **Acknowledge** - The Agent confirms it is aware of the current guidelines
2. **Verify** - Reviews active skills and commands for correctness
3. **Report** - Provides a brief summary of the guidelines being followed
4. **Inspect** - Emits the `__CHOCOLATE INSPECTION__` token on the final line

### Inspection Token

The `__CHOCOLATE INSPECTION__` token serves as proof that the Agent has read and is following
the context-checker policy. It must always appear on the last line of the response when this
skill is invoked.

## Usage

### Slash Command

```text
/check
```

Triggers a full context verification directly.

### Magic Word

Typing a prompt that contains `check` will auto-dispatch this skill via the shortcut plugin.

## License

MIT
