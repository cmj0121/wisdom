# Project Idea Tender Plugin

> Project owner agent — analyzes project context and produces brief plans for the team.

The proj-ideatender plugin serves as the project owner in the agent team. It analyzes your project
to understand its structure, purpose, and codebase, then produces brief plans and actionable ideas.
It is a read-only skill that never modifies project files.

## Role in the Team

- **With agent-smith (Autonomous)**: Analyzes and reports the brief plan to Smith
- **With agent-smith (Partner)**: Presents the plan to the user for approval
- **With spec-writer**: Provides project context for specification writing
- **With agent-ellis**: Receives design-level issue reports
- **Standalone**: Full analysis and idea generation for the user

## Installation

Install via the wisdom marketplace:

```bash
/plugin install proj-ideatender
```

## How It Works

### Three-Phase Approach

1. **Project analysis** - Reads documentation, entrypoint files, git history, and directory structure
2. **Idea generation and brief plan** - Produces a brief plan with goal, approach, units of work,
   and risks; or 5-10 actionable ideas across categories
3. **Handoff** - Reports plan to Smith (autonomous) or presents to user (partner/standalone)

### Output

- **PROJECT.md**: Project analysis persisted to cache directory
- **IDEAS.md**: Ideas and plans persisted to cache directory

## Usage

### Slash Command

```text
/analyze
```

Triggers the full project analysis and idea generation workflow.

### Magic Word

Typing a prompt that contains `analyze`, `plan it`, or `review and refine it` will auto-dispatch
this skill via the shortcut plugin.

## License

MIT
