# Agent Hale Plugin

> Developer agent — writes clean, robust and maintainable code.

Agent Hale is the developer of the scrum team. Hale receives units of work from
`agent-smith`, reads the plan and designs from `agent-ward`, and writes clean,
focused implementation code with proper tests.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install agent-hale
```

## Role in the Team

| Agent           | Role           | Hale's Relationship                           |
| --------------- | -------------- | --------------------------------------------- |
| **agent-smith** | Project Leader | Assigns work to Hale, forwards review results |
| **agent-ward**  | Architect      | Provides designs Hale implements from         |
| **agent-ellis** | QA             | Reviews Hale's code, findings sent via Smith  |
| **test-runner** | Support Tool   | Runs the project test suite for Hale          |

## How It Works

1. **Understand** — Reads `PLAN.md`, designs, and existing code
2. **Implement** — Writes clean, focused code following project conventions
3. **Self-check** — Reviews changes, runs tests via test-runner, runs `/simplify`
4. **Report** — Reports completed work back to Smith (or user if called directly)

## Usage

### Magic Words

- `code it` → Hale implements the requested change
- `hale` → Direct invocation

## License

MIT
