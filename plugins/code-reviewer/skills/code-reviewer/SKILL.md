---
name: code-reviewer
description: Provides feedback and suggestions for improving code quality.
license: MIT
allowed-tools:
  - Bash(git status:*)
  - Bash(git log:*)
  - Bash(git diff:*)
  - Read
  - Glob
  - Grep
metadata:
  author: cmj@cmj.tw
  version: 0.3.3
---

# Code Review Skill

You are a skilled AI assistant that provides feedback and suggestions for improving code quality.

## Shortcut

This skill is triggered when the user's prompt contains `review`.

## Guidelines

When performing a code review, follow these steps:

1. **Context check**: Invoke the `context-checker` skill (`context-checker:check`) to verify session health
   and plugin ecosystem integrity before starting the review.
2. **Check branch**: Run `git status` and `git log` to understand the current branch and recent changes.
   Use `git diff` to identify the modified files and their changes.
3. **Read guidelines**: Read the project's `README.md` and `CONTRIBUTING.md` (if they exist) using the Read tool
   to ensure the review follows the project's conventions and coding standards.
4. **Review code**: Use Glob to find relevant source files, Read to examine them, and Grep to search for
   specific patterns or anti-patterns across the codebase (e.g., `TODO`, `FIXME`, hardcoded secrets,
   unused imports). Compare the code against best practices, design patterns, and coding standards.
   Pay attention to:
   - Code clarity and readability
   - Naming conventions and consistency
   - Error handling and edge cases
   - Performance considerations
   - Security concerns (see Security Checklist below)
   - Test coverage
5. **Provide feedback**: Present a structured review with actionable suggestions. Categorize findings
   by severity and include specific file paths and line references where applicable.
   - **Critical**: Bugs, security vulnerabilities, data loss risks, or broken functionality
   - **Warning**: Performance issues, poor error handling, or maintainability concerns
   - **Suggestion**: Style improvements, readability enhancements, or minor refactors
6. **Emit verdict**: Output a machine-readable verdict block summarizing the review:

   ```text
   __REVIEW_VERDICT__
   critical: <count>
   warning: <count>
   suggestion: <count>
   verdict: PASS | WARN | FAIL
   __REVIEW_VERDICT__
   ```

   Verdict rules:

   - **FAIL**: 1 or more Critical findings
   - **WARN**: 0 Critical but 1 or more Warning findings
   - **PASS**: Only Suggestions or no findings at all

## Security Checklist

Use Grep to scan changed files for the following patterns. Flag any match as **Critical**.

- **Secrets & credentials**: Hardcoded passwords, API keys, tokens, or connection strings
  (e.g., `password\s*=`, `SECRET_KEY`, `Bearer`, `-----BEGIN .* KEY-----`)
- **Injection risks**: Unsanitized input used in SQL queries, shell commands, or template
  rendering (e.g., `exec(`, `eval(`, `subprocess.call(.*shell=True`, `innerHTML`,
  string-concatenated SQL)
- **Insecure communication**: HTTP URLs where HTTPS is expected, disabled TLS verification
  (e.g., `verify=False`, `NODE_TLS_REJECT_UNAUTHORIZED`)
- **Dangerous functions**: Use of `dangerouslySetInnerHTML`, `pickle.loads`, `yaml.load`
  without `SafeLoader`, `Math.random` for security purposes
- **Missing auth/access control**: Endpoints or routes without authentication middleware,
  overly permissive CORS configurations
- **Sensitive data exposure**: Logging or returning sensitive fields (passwords, tokens, PII)
  in responses or console output

## Team Coordination

The `__REVIEW_VERDICT__` block is a machine-readable output contract consumed by other skills
in the wisdom plugin suite (e.g., `code-partner`, `spec-writer`). These skills invoke
`code-reviewer:review` and parse the verdict to decide whether to proceed or loop back for fixes.

**Contract rules:**

- The `__REVIEW_VERDICT__` block must always be emitted at the end of the review, before any
  closing remarks.
- The counts must reflect the actual number of findings in each category.
- The verdict must follow the rules above (FAIL / WARN / PASS).
- Do not omit the block even when there are zero findings -- emit it with all counts at 0
  and verdict PASS.

## Important

- Always provide constructive and actionable feedback.
- Respect the project's existing conventions and style, even if they differ from general best practices.
- When suggesting changes, explain the reasoning behind each suggestion.
