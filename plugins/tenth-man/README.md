# Tenth Man Plugin

> Devil's advocate that challenges assumptions and surfaces risks to prevent groupthink.

Named after the "tenth man rule" — if nine people agree, the tenth must argue the opposite.
This plugin systematically challenges plans, proposals, designs, and code changes to surface
hidden risks and blind spots before they become real problems.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install tenth-man
```

## How It Works

### Challenge Workflow

1. **Understand** — reads and summarizes the subject under review
2. **Challenge assumptions** — surfaces and stress-tests implicit assumptions, rated by severity
3. **Surface risks** — identifies failure modes, second-order effects, missing perspectives, and reversibility concerns
4. **Suggest alternatives** — proposes concrete mitigations for high-severity items
5. **Verdict** — delivers a Go / Pause / Reconsider recommendation with top action items

## Usage

### Slash Command

```text
/tenth-man
```

### Magic Words

Typing a prompt that contains `challenge this` or `tenth man` will auto-dispatch this skill
via the shortcut plugin.

### Examples

```text
/tenth-man Review our plan to migrate from REST to GraphQL
```

```text
Here's our proposal for the new auth system. challenge this
```

## License

MIT
