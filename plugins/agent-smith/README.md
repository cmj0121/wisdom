# Agent Smith Plugin

> Project Leader agent — plans, dispatches, coordinates the scrum team.

Agent Smith is the leader of the scrum team. Smith owns the full lifecycle: analyzing
project context, producing plans, dispatching to specialized agents, and coordinating
iterations. Smith does not write code, specs, or docs directly.

| Mode       | Trigger words                       | Checkpoints               | Iterations       |
| ---------- | ----------------------------------- | ------------------------- | ---------------- |
| Partner    | `develop`, `implement it`, `fix it` | 2 (plan approval + merge) | Single pass      |
| Autonomous | `smith`                             | 1 (merge only)            | Minimum 3 cycles |

## The Team

| Agent           | Role             | Responsibility                                  |
| --------------- | ---------------- | ----------------------------------------------- |
| **agent-smith** | Project Leader   | Plans, dispatches, coordinates the scrum team   |
| **agent-ward**  | Architect        | System design, API design, tech stack decisions |
| **agent-hale**  | Developer        | Writes code and tests                           |
| **agent-ellis** | QA               | Code review, test execution, acceptance check   |
| **agent-twain** | Technical Writer | User docs, API docs, migration guides           |
| **agent-page**  | SRE              | Observability, reliability, performance review  |
| **agent-ross**  | Release Manager  | CI/CD, Docker, cloud deploy, commits (optional) |

## Installation

Install via the wisdom marketplace:

```bash
/plugin install agent-smith
```

## How It Works

1. **Plan** — Analyzes context, produces plan, challenges via tenth-man
2. **Design** — Dispatches to agent-ward for architecture (if needed)
3. **Implement** — Dispatches to agent-hale, reviewed by agent-ellis
4. **Docs & Ops** — Dispatches to agent-twain and agent-page in parallel
5. **Release** — Dispatches to agent-ross (if installed)
6. **Merge** — Presents summary, waits for approval, merges

## Usage

### Magic Words

- `develop`, `implement it`, `fix it` → Partner mode
- `smith` → Autonomous mode

## License

MIT
