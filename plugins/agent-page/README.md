# Agent Page Plugin

> SRE agent — observability, reliability, and performance review.

Named after Larry Page — co-founder of Google, where SRE originated.

Agent Page is the SRE of the development team. Page reviews code and infrastructure
for operational readiness before release.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install agent-page
```

## Role in the Team

| Agent             | Role           | Page's Relationship                                             |
| ----------------- | -------------- | --------------------------------------------------------------- |
| **agent-smith**   | Project Leader | Assigns ops review tasks                                        |
| **agent-hale**    | Developer      | Fixes ops issues flagged by Page                                |
| **agent-ellis**   | QA             | Owns the dependency and security scans; Page reads its findings |
| **test-runner**   | Support Tool   | Runs a dedicated performance suite only                         |
| **ascii-grapher** | Support Tool   | Produces infrastructure diagrams                                |

## How It Works

1. **Understand** — Reads plan and changed files
2. **Observability** — Checks logging, metrics, tracing, alerting
3. **Reliability** — Checks error handling, timeouts, circuit breakers
4. **Performance** — Checks queries, memory, concurrency, caching
5. **Security** — Reads Ellis's dependency and security findings; checks secrets, access control
6. **Infrastructure** — Reviews Docker, CI/CD, K8s, Terraform
7. **Verdict** — Reports READY / CONCERN / BLOCK

## Usage

### Magic Words

- `ops review` → Page reviews changes for operational readiness
- `reliability review` → Page focuses on reliability concerns
- `page it` → Direct invocation

## License

MIT
