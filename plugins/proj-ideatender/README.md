# Project Idea Tender Plugin

> The project idea tender to help you generate project ideas.

The proj-ideatender plugin analyzes your project to understand its structure, purpose, and codebase,
then generates actionable ideas for improvements or new features. It is a read-only skill that never
modifies files or writes code.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install proj-ideatender
```

## How It Works

### Two-Phase Approach

1. **Project analysis** - Reads documentation, entrypoint files, git history, and directory structure
   to build a comprehensive understanding of the project
2. **Idea generation** - Produces 5-10 actionable ideas across five categories: features, improvements,
   refactoring, documentation, and testing

### Output

The skill produces two sections:

- **Project Summary**: Purpose, tech stack, recent activity, and code quality observations
- **Ideas**: A numbered list with title, category, description, and effort estimate

## Usage

### Slash Command

```text
/analyze
```

Triggers the full project analysis and idea generation workflow.

### Magic Word

Typing a prompt that contains `analyze` will auto-dispatch this skill via the shortcut plugin.

## License

MIT
