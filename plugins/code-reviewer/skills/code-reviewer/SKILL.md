---
name: code-reviewer
description: Provides feedback and suggestions for improving code quality.
license: MIT
allowed-tools:
  - Bash(git status:*)
  - Bash(git diff:*)
  - Read
  - Glob
  - Grep
metadata:
  author: cmj@cmj.tw
  version: 0.7.0
---

# Code Review Skill

## Shortcut

This skill is triggered when the user's prompt contains `review`.

### Phase 1: Code Stage Review

Run `git diff --staged` to review staged changes. If none, emit a _SKIP_ verdict.

### Phase 2: Quality Checklist

Use Grep to scan changed files. Flag matches as **Warning**.

- **Code style**: Inconsistent indentation, trailing whitespace, missing semicolons
- **Code smells**: Long methods, large classes, duplicated code
- **Complexity**: Deeply nested code, long parameter lists
- **Documentation gaps**: Public methods/classes without docstrings

### Phase 3: Security Review

Use Grep to scan changed files. Flag matches as **FAIL**.

- **Hardcoded secrets**: API keys, passwords, sensitive information in code
- **Insecure functions**: Functions with known security vulnerabilities
- **Input validation**: Missing validation for user input
- **Data exposure**: Logging or exposing sensitive data

### Phase 4: Generate Review Verdict

Only emit the verdict when called by other skills, not when called directly by users.

```txt
__REVIEW_VERDICT__
Verdict: FAIL
Warnings: 3
Smells: 2
Complexity: 1
Documentation: 4
__REVIEW_VERDICT__
```

When called directly by users, present findings in a brief table and discuss suggestions.

## Team Coordination

The `__REVIEW_VERDICT__` block is a machine-readable contract consumed by other skills (`agent-smith`, `spec-writer`).

**Contract rules:**

- Always emit `__REVIEW_VERDICT__` when called by other skills.
- Counts must reflect actual findings per category.
- Verdict: FAIL / WARN / PASS / SKIP.
- Never omit the block, even with zero findings.
- Respect the project's existing conventions and style, even if they differ from general best practices.
