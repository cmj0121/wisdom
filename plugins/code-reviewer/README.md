# Code Reviewer Plugin

> Provides feedback and suggestions for improving code quality.

The code-reviewer plugin helps you review your code by analyzing the current branch, reading project
guidelines, and providing structured feedback with actionable suggestions. It checks for best practices,
design patterns, coding standards, and potential issues.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install code-reviewer
```

## How It Works

### Review Workflow

1. **Check branch** - Runs `git status`, `git log`, and `git diff` to understand the current changes
2. **Read guidelines** - Reads `README.md` and `CONTRIBUTING.md` for project conventions
3. **Review code** - Examines changed files against best practices and coding standards
4. **Provide feedback** - Presents a structured report with categorized findings

### Severity Levels

| Level      | Meaning                                                   |
| ---------- | --------------------------------------------------------- |
| Critical   | Must be fixed: bugs, security vulnerabilities, data loss  |
| Warning    | Should be addressed: error handling, performance concerns |
| Suggestion | Nice to have: readability, naming, style improvements     |

## Usage

### Slash Command

```text
/review
```

Triggers the full code review workflow directly.

### Magic Word

Typing a prompt that contains `review` will auto-dispatch this skill via the shortcut plugin.

## License

MIT
