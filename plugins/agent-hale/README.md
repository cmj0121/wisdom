# Agent Hale Plugin

> Developer agent — writes clean, robust, maintainable code and its tests from an agreed plan or
> design. Use when implementation is the task and the approach is already settled, or when the user
> asks for something to be coded, and prizes correctness over cleverness.

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

1. **Pre-flight** — Reads `CLAUDE.md`/`PLAN.md`, confirms scope, captures baseline test state
2. **Understand** — Reads target code end-to-end; names the root cause before fixing bugs
3. **Implement** — Test-first; minimal, focused changes following project conventions
4. **Self-check** — Diff sanity, lint, typecheck, tests vs baseline, own security scan, `/simplify`
5. **Verify** — Actually exercises the change (browser/request/dry-run), not just tests
6. **Report** — Structured report (files, assumptions, tests, verification) back to Smith

After two failed fix attempts at the same symptom, Hale escalates rather than thrashing —
see the **Stuck Protocol** in the skill.

## Usage

### Magic Words

- `code it` → Hale implements the requested change
- `hale` → Direct invocation

## License

MIT
