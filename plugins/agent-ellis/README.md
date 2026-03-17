# Agent Ellis Plugin

> Code reviewer agent — reviews code quality and security, reports findings to proj-ideatender or agent-hale.

Agent Ellis is the code reviewer of the development team. Ellis reviews code for quality and
security issues, then reports findings through the team's reporting chain: implementation fixes
go to `agent-hale`, design-level issues escalate to `proj-ideatender` — all routed by `agent-smith`.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install agent-ellis
```

## Role in the Team

| Agent               | Role          | Ellis's Relationship                               |
| ------------------- | ------------- | -------------------------------------------------- |
| **agent-smith**     | Leader        | Sends review requests, routes Ellis's findings     |
| **agent-hale**      | Programmer    | Receives implementation fixes from Ellis via Smith |
| **proj-ideatender** | Project Owner | Receives design-level issues from Ellis via Smith  |
| **spec-writer**     | Spec Writer   | Ellis may review spec drafts                       |

## How It Works

### Review Workflow

1. **Check changes** - Runs `git diff --staged` or `git diff` to find changes
2. **Quality checklist** - Scans for code style, smells, complexity, documentation gaps
3. **Security review** - Scans for hardcoded secrets, insecure functions, input validation
4. **Generate verdict** - FAIL / WARN / PASS / SKIP with categorized findings
5. **Report** - Routes findings to Smith (who forwards to Hale or ideatender)

### Severity Levels

| Level      | Meaning                                                   |
| ---------- | --------------------------------------------------------- |
| Critical   | Must be fixed: bugs, security vulnerabilities, data loss  |
| Warning    | Should be addressed: error handling, performance concerns |
| Suggestion | Nice to have: readability, naming, style improvements     |

### Finding Categories

| Category             | Routed to       |
| -------------------- | --------------- |
| Implementation-level | agent-hale      |
| Design-level         | proj-ideatender |

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
