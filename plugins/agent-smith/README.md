# Agent Smith Plugin

> Team leader agent — dispatches planning, spec-writing, coding, and review jobs to specialized agents.

Agent Smith is the leader of the development team. Smith does not write code or specs directly —
instead, Smith dispatches jobs to specialized agents and coordinates their work through a layered
skill architecture.

| Mode       | Trigger words                       | Checkpoints               | Iterations       |
| ---------- | ----------------------------------- | ------------------------- | ---------------- |
| Partner    | `develop`, `implement it`, `fix it` | 2 (plan approval + merge) | Single pass      |
| Autonomous | `smith`                             | 1 (merge only)            | Minimum 3 cycles |

## The Team

| Agent               | Role          | Responsibility                                     |
| ------------------- | ------------- | -------------------------------------------------- |
| **agent-smith**     | Leader        | Dispatches jobs, coordinates workflow, manages git |
| **proj-ideatender** | Project Owner | Analyzes project context, produces brief plans     |
| **spec-writer**     | Spec Writer   | Writes technical specs with architecture diagrams  |
| **agent-hale**      | Programmer    | Writes code based on plan and spec                 |
| **agent-ellis**     | Code Reviewer | Reviews code, finds bugs, reports findings         |
| **git-committer**   | Commit Gen    | Generates commit messages                          |

## Installation

Install via the wisdom marketplace:

```bash
/plugin install agent-smith
```

## How It Works

### Phase 1: Understand and Plan

Smith dispatches to `proj-ideatender` to analyze the project and produce a brief plan.
In Partner mode, the plan is presented to the user. In Autonomous mode, Smith reviews it directly.

### Phase 2: Spec (if needed)

For non-trivial features, Smith dispatches to `spec-writer` to produce technical specifications
with architecture diagrams (via `ascii-grapher`).

### Phase 3: Implement, Review, and Commit

For each unit of work, Smith dispatches:

1. **agent-hale** — writes the code
2. **agent-ellis** — reviews the code (PASS/WARN/FAIL)
3. **git-committer** — commits on PASS

On FAIL, Smith re-dispatches to Hale with Ellis's findings, then back to Ellis.

### Autonomous Mode (additional phases)

1. **Assess** — Smith reviews all changes, scores quality
2. **Re-Plan** — Smith invokes `proj-ideatender` to reassess, adds new units, loops back

### Final Phases

1. **Merge** — Presents summary, waits for user approval, merges into main
2. **Lessons Learned** — Reflects and persists insights

## Usage

### Slash Command

```text
/smith
```

Starts a fully autonomous development session.

### Magic Words

- `develop`, `implement it`, `fix it` → Partner mode
- `smith` → Autonomous mode

## License

MIT
