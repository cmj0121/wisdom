# Agent Hale Plugin

> Programmer agent — writes clean, focused code based on plan and spec from the team.

Agent Hale is the programmer of the development team. Hale receives units of work from
`agent-smith`, reads the plan and specs, and writes clean, focused implementation code
with proper tests and error handling.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install agent-hale
```

## Role in the Team

| Agent               | Role          | Hale's Relationship                           |
| ------------------- | ------------- | --------------------------------------------- |
| **agent-smith**     | Leader        | Assigns work to Hale, forwards review results |
| **proj-ideatender** | Project Owner | Provides project context via cache files      |
| **spec-writer**     | Spec Writer   | Provides technical specs Hale implements from |
| **agent-ellis**     | Code Reviewer | Reviews Hale's code, findings sent via Smith  |

## How It Works

1. **Understand** — Reads `PLAN.md`, specs, and existing code to understand the unit of work
2. **Implement** — Writes clean, focused code following project conventions
3. **Self-check** — Reviews own changes, runs `/simplify`, verifies scope
4. **Report** — Reports completed work back to Smith (or user if called directly)

### Handling Review Feedback

When `agent-ellis` finds issues, Smith re-dispatches to Hale with the findings. Hale fixes
FAIL items (must fix) and WARN items (fix unless Smith says otherwise), then reports back.

## Usage

### Slash Command

```text
/hale
```

### Magic Words

- `code it` → Hale implements the requested change
- `hale` → Direct invocation

## License

MIT
