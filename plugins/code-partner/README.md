# Code Parner Plugin

> The code partner to help you code together with the AI agent.

The code-partner plugin provides an AI pair programming experience. It reads your project's
documentation, discusses the design with you, presents a step-by-step plan, and implements
the code collaboratively with your approval at every stage.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install code-partner
```

## How It Works

### Pair Programming Workflow

1. **Understand** - Reads README.md and relevant docs to learn the project
2. **Discuss** - Proposes a high-level design and approach
3. **Plan** - Presents an implementation plan in table format for your approval
4. **Implement** - Writes code step by step, confirming at each stage
5. **Test** - Reviews changes and adds tests where applicable
6. **Commit** - Follows the project's commit template or conventional commit format

### Development Guidelines

The plugin follows best practices including:

- Clean, concise code with proper naming conventions
- Short, focused functions and methods
- Modular design with reusable components
- Comprehensive tests and documentation
- Proper error handling and input validation

### Git Workflow

Each feature or fix gets its own branch. Commits are structured incrementally:

1. Top-down implementation scaffold
2. Incremental improvements and refactoring
3. Unit tests and integration tests

## Usage

### Slash Command

```text
/develop
```

Starts a pair programming session directly.

### Magic Word

Typing a prompt that contains `develop` will auto-dispatch this skill via the shortcut plugin.

## License

MIT
