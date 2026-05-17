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

Used by agent-page (SRE) and agent-ellis (QA).

## Shortcut

This skill is triggered when the user's prompt contains `audit deps` or `dep-auditor`.

## How It Works

### Phase 1: Detect Package Manager

Auto-detect by checking lock/config files. If multiple managers detected, audit all.

| Config File         | Package Manager | Audit Command       |
| ------------------- | --------------- | ------------------- |
| `package-lock.json` | npm             | `npm audit`         |
| `yarn.lock`         | yarn            | `npm audit`         |
| `requirements.txt`  | pip             | `pip audit`         |
| `Pipfile.lock`      | pipenv          | `pip audit`         |
| `go.sum`            | go modules      | `govulncheck ./...` |
| `Cargo.lock`        | cargo           | `cargo audit`       |
| `Gemfile.lock`      | bundler         | `bundle audit`      |

### Phase 2: Vulnerability Scan

Run audit command(s). For each vulnerability capture: package+version, ID (CVE/GHSA),
severity, description, fix version.

### Phase 3: Outdated Package Check

- npm: `npm outdated`
- pip: `pip list --outdated`
- go: `go list -u -m all`
- cargo: `cargo outdated`

Flag packages more than 2 major versions behind.

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

If vulnerabilities found, include details for each.

## Team Coordination

**Available to:** agent-page, agent-ellis. Always emit the `__AUDIT_RESULT__` block when invoked;
caller decides how to act.
