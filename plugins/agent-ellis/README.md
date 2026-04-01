# Agent Ellis Plugin

> QA agent — code review, test execution, and acceptance verification.

Agent Ellis is the QA agent of the scrum team. Ellis reviews code for quality and
security, runs the test suite, verifies acceptance criteria against `PLAN.md`, and
audits dependencies. Findings route to `agent-hale` (fixes) or `agent-ward` (redesign)
via `agent-smith`.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install agent-ellis
```

## Role in the Team

| Agent           | Role           | Ellis's Relationship                           |
| --------------- | -------------- | ---------------------------------------------- |
| **agent-smith** | Project Leader | Sends review requests, routes Ellis's findings |
| **agent-hale**  | Developer      | Receives implementation fixes via Smith        |
| **agent-ward**  | Architect      | Receives design-level issues via Smith         |
| **test-runner** | Support Tool   | Runs the project test suite for Ellis          |
| **dep-auditor** | Support Tool   | Audits dependencies for vulnerabilities        |

## How It Works

1. **Code review** — Scans for quality, style, complexity issues
2. **Security review** — Scans for secrets, insecure functions, input validation
3. **Test execution** — Runs test suite via test-runner
4. **Acceptance check** — Verifies implementation matches PLAN.md
5. **Dependency audit** — Audits deps if dependency files changed
6. **Verdict** — FAIL / WARN / PASS / SKIP with categorized findings

## Usage

### Magic Words

- `review code` → Full QA review of current changes
- `qa` → Full QA review
- `ellis` → Direct invocation

## License

MIT
