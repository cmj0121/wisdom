---
name: sec-review
description: Reviews source for security issues and maps each finding to a CWE — whole project by default, or the scope its caller states. Use when security is the question, not code review.
license: MIT
allowed-tools:
  - Bash(git ls-files:*)
  - Bash(grep:*)
  - Read
  - Glob
  - Grep
metadata:
  author: cmj@cmj.tw
  version: "2.1.0"
  shortcut: "sec-review, security review"
  verdict: "__SEC_REVIEW_RESULT__"
---

# Security Reviewer

Reviews the **whole project** source for potential security issues and maps each to a
related CWE — unlike diff-only reviewers (e.g. the built-in `/security-review`) that
only inspect the current branch diff.

## Shortcut

This skill is triggered when the user's prompt contains `sec-review` or `security review`.

## How It Works

Each phase below assumes an input: a scope to enumerate, files to read. When one is missing —
the caller named a scope that resolves to nothing, or enumeration returns no source at all —
report that and stop. `Status: CLEAN` is a claim about source that was examined, so source
that was never enumerated earns no status, least of all the reassuring one.

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
- **Scope comes from the caller**: whole project is the default, not the mandate. `agent-ellis`
  invokes this diff-scoped as part of a unit review; `agent-ross` invokes it at full scope once
  per release. Scan what the caller asked for, and state which scope was used.
- Be specific: file path, line number, and a concrete fix for each finding.
- Findings are **potential** issues to verify, not proof of exploitability.
- Prefer the most specific CWE that fits the weakness.

## Team Coordination

**Available to:** `agent-ellis` (diff scope, per unit) and `agent-ross` (whole project, once
per release). `agent-page` does not invoke this scan — it reads Ellis's findings, because two
agents scanning the same source produce the same findings at twice the cost. Always emit the
`__SEC_REVIEW_RESULT__` block when called by another agent; the caller decides how to act.
