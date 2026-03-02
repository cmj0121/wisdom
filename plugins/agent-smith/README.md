# Agent Smith Plugin

> Dual-mode development agent — partner or fully autonomous — that plans, implements, reviews, commits, and delivers.

The agent-smith plugin combines project analysis and code implementation into a single development
agent with two operating modes:

| Mode       | Trigger words                       | Checkpoints               | Iterations       |
| ---------- | ----------------------------------- | ------------------------- | ---------------- |
| Partner    | `develop`, `implement it`, `fix it` | 2 (plan approval + merge) | Single pass      |
| Autonomous | `smith`                             | 1 (merge only)            | Minimum 3 cycles |

**Partner mode** pauses at plan approval so you can review and edit `PLAN.md` before implementation
begins, then pauses again before merge. **Autonomous mode** proceeds directly from planning through
iterative self-assessment cycles with zero user confirmation until the final merge.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install agent-smith
```

## How It Works

### Shared Workflow

1. **Understand and Plan** — Analyzes the project and creates an implementation plan in `PLAN.md`
2. **Implement, Review, and Commit** — Implements each unit of work, reviews, and commits autonomously

### Autonomous Mode (additional phases)

1. **Assess** — Reviews all changes, scores quality, identifies improvements
2. **Re-Plan and Iterate** — Creates new units of work based on assessment, repeats (minimum 3 iterations)

### Final Phases (shared)

1. **Merge** — Presents summary and waits for user approval before merging into main
2. **Lessons Learned** — Reflects on the process and identifies takeaways

## Usage

### Slash Command

```text
/smith
```

Starts a fully autonomous development session.

### Magic Words

Typing a prompt that contains one of the trigger words will auto-dispatch this skill via the shortcut
plugin:

- `develop`, `implement it`, `fix it` → Partner mode
- `smith` → Autonomous mode

## License

MIT
