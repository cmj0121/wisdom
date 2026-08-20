# Briefing Plugin

> Output style for planning and review agents — keeps results compact, summarises each question before
> answering it, and drives discussion one numbered topic at a time. Use when running agent-smith or
> tenth-man, or when the user asks for shorter output or to decide one thing at a time.

A shared output style for the agents that talk to you the most. It governs shape, not
content: it makes results shorter and decisions sequential, and never licenses dropping a
finding or skipping a checkpoint.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install briefing
```

## How It Works

1. **Lead with the result** — outcome first, tables over prose, no process narration
2. **Summarise questions** — one-line question, options table, a recommendation and why
3. **Detail on request** — depth is granted per question, then it returns to step 2
4. **One topic at a time** — every topic numbered against the total, `Topic (1/4): ...`

## Usage

### Magic Words

- `briefing` → Apply the briefing output style
- `brief me` → Apply the briefing output style

## Applies To

agent-smith and tenth-man, for output addressed to the user. Agent-to-agent reports are
unaffected.

## License

MIT
