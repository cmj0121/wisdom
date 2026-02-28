# Agent Smith Plugin

> Fully autonomous development agent: give it an idea, it plans, implements, iterates, and delivers.

The agent-smith plugin combines project analysis and code implementation into a single fully autonomous
agent. Give it a brief idea and it handles everything — planning, implementing, reviewing, committing,
and then iterating at least 3 times to self-assess, re-plan, and improve. All iterations are automatic
with zero user confirmation until the final merge.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install agent-smith
```

## How It Works

### Fully Autonomous Workflow

1. **Understand and Plan** — Analyzes the project and creates an implementation plan in `PLAN.md`
2. **Implement, Review, and Commit** — Implements each unit of work, reviews, and commits autonomously
3. **Assess** — Reviews all changes, scores quality, identifies improvements
4. **Re-Plan and Iterate** — Creates new units of work based on assessment, repeats (minimum 3 iterations)
5. **Merge** — Presents summary and waits for user approval before merging into main
6. **Lessons Learned** — Reflects on the process and identifies takeaways

### Key Design Principles

- **One checkpoint only** — the final merge into main
- **Minimum 3 iterations** — self-assessment and improvement cycles
- **PLAN.md as a living document** — updated each iteration with new work and an iteration log
- **No user intervention** — fully autonomous from idea to merge-ready code

## Usage

### Slash Command

```text
/smith
```

Starts a fully autonomous development session.

### Magic Word

Typing a prompt that contains `smith` will auto-dispatch this skill via the shortcut plugin.

## License

MIT
