---
name: dep-auditor
description: Audits dependencies for vulnerabilities and outdated packages.
license: MIT
allowed-tools:
  - Bash(npm audit:*)
  - Bash(npm outdated:*)
  - Bash(pip audit:*)
  - Bash(pip list --outdated:*)
  - Bash(go list:*)
  - Bash(govulncheck:*)
  - Bash(cargo audit:*)
  - Bash(cargo outdated:*)
  - Bash(bundle audit:*)
  - Bash(gh api:*)
  - Read
  - Glob
  - Grep
metadata:
  author: cmj@cmj.tw
  version: 1.0.0
---

# Dependency Auditor

A shared support tool that audits project dependencies for known vulnerabilities
and outdated packages. Used by agent-page (SRE review) and agent-ellis (QA).

## Shortcut

This skill is triggered when the user's prompt contains `audit deps` or `dep-auditor`.

## How It Works

### Phase 1: Detect Package Manager

Auto-detect the package manager by checking for lock/config files:

| Config File         | Package Manager | Audit Command       |
| ------------------- | --------------- | ------------------- |
| `package-lock.json` | npm             | `npm audit`         |
| `yarn.lock`         | yarn            | `npm audit`         |
| `requirements.txt`  | pip             | `pip audit`         |
| `Pipfile.lock`      | pipenv          | `pip audit`         |
| `go.sum`            | go modules      | `govulncheck ./...` |
| `Cargo.lock`        | cargo           | `cargo audit`       |
| `Gemfile.lock`      | bundler         | `bundle audit`      |

If multiple package managers are detected, audit all of them.

### Phase 2: Vulnerability Scan

Run the appropriate audit command(s). For each vulnerability found, capture:

- Package name and version
- Vulnerability ID (CVE, GHSA, etc.)
- Severity (critical, high, medium, low)
- Description
- Fix version (if available)

### Phase 3: Outdated Package Check

Check for outdated packages:

- npm: `npm outdated`
- pip: `pip list --outdated`
- go: `go list -u -m all`
- cargo: `cargo outdated`

Flag packages that are more than 2 major versions behind.

### Phase 4: Report

Return a structured report:

```txt
__AUDIT_RESULT__
Status: CLEAN / WARN / CRITICAL
Vulnerabilities: <n>
  Critical: <n>
  High: <n>
  Medium: <n>
  Low: <n>
Outdated: <n>
__AUDIT_RESULT__
```

If vulnerabilities are found, include details for each one.

## Team Coordination

**Available to:** agent-page, agent-ellis

When invoked by other agents, always emit the `__AUDIT_RESULT__` block.
The calling agent decides how to act on the results.
