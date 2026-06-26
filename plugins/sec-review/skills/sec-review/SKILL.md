---
name: sec-review
description: Whole-project security reviewer mapping findings to CWE.
license: MIT
allowed-tools:
  - Bash(git ls-files:*)
  - Bash(grep:*)
  - Read
  - Glob
  - Grep
metadata:
  author: cmj@cmj.tw
  version: 1.0.0
---

# Security Reviewer

Reviews the **whole project** source for potential security issues and maps each to a
related CWE — unlike diff-only reviewers (e.g. the built-in `/security-review`) that
only inspect the current branch diff.

## Shortcut

This skill is triggered when the user's prompt contains `sec-review` or `security review`.

## How It Works

### Phase 1: Scope

Enumerate source files with `git ls-files` (fall back to Glob). Skip vendored/generated
code, `node_modules`, build output, and lockfiles. Identify the languages in use and the
entry points (CLI mains, HTTP handlers, request routers, message consumers).

### Phase 2: Review for Weakness Classes

Grep/read source for common weakness classes. Map each to its example CWE:

| Issue Class                        | Example CWE       |
| ---------------------------------- | ----------------- |
| Injection — SQLi                   | CWE-89            |
| Injection — command                | CWE-77 / CWE-78   |
| Injection — template               | CWE-94            |
| Cross-site scripting (XSS)         | CWE-79            |
| Hardcoded secrets                  | CWE-798           |
| Broken / missing authentication    | CWE-287           |
| Broken access control              | CWE-862 / CWE-285 |
| Insecure deserialization           | CWE-502           |
| Path traversal                     | CWE-22            |
| Server-side request forgery (SSRF) | CWE-918           |
| Weak cryptography                  | CWE-327           |
| Sensitive data exposure            | CWE-200           |
| Missing input validation           | CWE-20            |
| Insecure randomness                | CWE-330           |
| XML external entity (XXE)          | CWE-611           |
| Open redirect                      | CWE-601           |

### Phase 3: Triage

For each finding assign a severity (Critical / High / Medium / Low) and the most
specific CWE ID that applies.

### Phase 4: Report

**Inline by default.** Present a findings table:

| File:Line | Issue | Severity | CWE | Suggested Fix |
| --------- | ----- | -------- | --- | ------------- |

Write a report file (e.g. `SECURITY-REVIEW.md`) **only** when the user explicitly asks.
Default is inline — write nothing.

When called by another agent, also emit a structured block:

```txt
__SEC_REVIEW_RESULT__
Status: CLEAN / WARN / CRITICAL
Findings: <n>
  Critical: <n>
  High: <n>
  Medium: <n>
  Low: <n>
__SEC_REVIEW_RESULT__
```

## Constraints

- **Read-only**: MUST NOT modify project files. Only review and report.
- Be specific: file path, line number, and a concrete fix for each finding.
- Findings are **potential** issues to verify, not proof of exploitability.
- Prefer the most specific CWE that fits the weakness.

## Team Coordination

**Available to:** agent-page, agent-ellis. Always emit the `__SEC_REVIEW_RESULT__` block
when called by another agent; caller decides how to act.
