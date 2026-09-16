---
name: dep-auditor
description: Audits dependencies for known vulnerabilities and outdated versions across npm, pip, go, cargo and bundler. Use before a release or when a lockfile changes.
license: MIT
model: haiku
context: fork
background: false
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
  version: "2.0.0"
  shortcut: "audit deps, dep-auditor"
  verdict: "__AUDIT_RESULT__"
---

# Dependency Auditor

Used by agent-page (SRE) and agent-ellis (QA).

## Shortcut

This skill is triggered when the user's prompt contains `audit deps` or `dep-auditor`.

## How It Works

Each phase assumes the one before it produced something to work on. When it did not, report
that and stop rather than reporting nothing found — the two are not the same, and only one of
them is good news.

### Phase 1: Detect Package Manager

Auto-detect by checking lock/config files. If multiple managers detected, audit all. If none
is detected, report that and stop — do not fall through to Phase 4. The table below is a
closed list, so a project outside it is the routine case, and an audit that ran no command
would otherwise emit `Status: CLEAN` and be read as a project with no vulnerable dependencies.

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
