# Agent Ellis Plugin

> QA agent — reviews code quality and security, runs the test suite, and verifies work against its
> acceptance criteria. Use when a change needs reviewing before it lands, when tests should be run and
> judged, or when the user asks whether something is actually done.

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

| Agent           | Role           | Ellis's Relationship                            |
| --------------- | -------------- | ----------------------------------------------- |
| **agent-smith** | Project Leader | Sends review requests, routes Ellis's findings  |
| **agent-hale**  | Developer      | Receives implementation fixes via Smith         |
| **agent-ward**  | Architect      | Receives design-level issues via Smith          |
| **test-runner** | Support Tool   | Re-runs the suite when Hale's report is missing |
| **dep-auditor** | Support Tool   | Audits dependencies for vulnerabilities         |
| **sec-review**  | Support Tool   | Scans the diff for CWE-mapped security issues   |

## How It Works

1. **Code review** — Scans for quality, style, complexity issues
2. **Security review** — Scans for secrets, insecure functions, input validation
3. **Test results** — Consumes Hale's test report; re-runs only when it is missing or stale
4. **Acceptance check** — Verifies implementation matches PLAN.md
5. **Dependency and security audit** — Audits deps if dependency files changed; scans
   source for CWE-mapped issues
6. **Verdict** — FAIL / WARN / PASS / SKIP with categorized findings

## Usage

### Magic Words

- `review code` → Full QA review of current changes
- `qa review` → Full QA review
- `ellis` → Direct invocation

## License

MIT
