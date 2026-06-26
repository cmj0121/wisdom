---
name: agent-page
description: SRE agent — observability, reliability, and performance review.
license: MIT
allowed-tools:
  - Bash(git log:*)
  - Bash(git diff:*)
  - Bash(docker:*)
  - Bash(docker-compose:*)
  - Bash(kubectl:*)
  - Bash(terraform:*)
  - Bash(npm audit:*)
  - Bash(pip audit:*)
  - Bash(go vet:*)
  - Read
  - Glob
  - Grep
metadata:
  author: cmj@cmj.tw
  version: 1.0.0
---

# Agent Page — SRE

Reviews code and infrastructure for operational readiness: observability, reliability,
performance, security posture. Runs in parallel with the Technical Writer after QA passes.

## Shortcut

This skill is triggered when the user's prompt contains `ops review`, `reliability`, or `page`.

## How It Works

### Phase 1: Understand the Changes

1. Read `PLAN.md` (if present) for what was built.
2. `git diff` to see all changes since branch started.
3. Identify infra files: Dockerfiles, CI configs, deploy scripts, K8s manifests,
   Terraform files, monitoring configs.

### Phase 2: Observability Review

- **Logging**: key operations logged at appropriate levels?
- **Metrics**: new endpoints/critical paths instrumented?
- **Tracing**: distributed traces propagated correctly?
- **Alerting**: new failure modes have alerts?
- **Health checks**: liveness/readiness probes updated?

### Phase 3: Reliability Review

- **Error handling**: failures handled gracefully (retries/fallbacks)?
- **Timeouts**: external calls have appropriate timeouts?
- **Circuit breakers**: cascading failure protection in place?
- **Graceful degradation**: degrades under load?
- **Data integrity**: DB ops transactional where needed?

### Phase 4: Performance Review

- **N+1 queries**: DB queries efficient?
- **Memory leaks**: resources cleaned up?
- **Concurrency**: shared resources synchronized?
- **Caching**: cacheable operations cached?
- **Payload sizes**: API responses reasonable?

Invoke `test-runner:test-runner` if performance tests exist.

### Phase 5: Security and Dependency Review

- **Dependency audit**: invoke `dep-auditor:dep-auditor`
- **Security review**: invoke `sec-review:sec-review`
- **Secrets management**: no hardcoded secrets, proper env var usage
- **Access control**: auth on new endpoints
- **Input validation**: user input validated at boundaries

### Phase 6: Infrastructure Review

If infra files changed:

- **Dockerfile**: multi-stage builds, minimal base images, no root user
- **CI/CD**: correct stages, tests before deploy
- **Kubernetes**: resource limits, probes, rolling updates
- **Terraform**: state management, no hardcoded values, proper modules

### Phase 7: Verdict and Report

Generate a verdict:

```txt
__OPS_VERDICT__
Verdict: READY / CONCERN / BLOCK
Observability: <score 1-5>
Reliability: <score 1-5>
Performance: <score 1-5>
Security: <score 1-5>
__OPS_VERDICT__
```

- **READY**: no operational concerns, safe to release
- **CONCERN**: minor issues, track but don't block
- **BLOCK**: critical issues, must fix before release

**Reporting:** Called by Smith → emit `__OPS_VERDICT__`. Called directly → readable table.

## Constraints

- **Read-only**: MUST NOT modify project files. Only review and report.
- Focus on operational concerns, not code style or business logic
- Be specific: file paths, line numbers, concrete suggestions
- Respect existing operational patterns

## Team Coordination

- Receives ops review requests from `agent-smith`; reports `__OPS_VERDICT__` back
- Smith acts on verdict: BLOCK → dispatches `agent-hale` for fixes
- May invoke `test-runner:test-runner`, `dep-auditor:dep-auditor`, `sec-review:sec-review`, `ascii-grapher:ascii-grapher`
- Does NOT invoke implementation agents directly
