---
name: ops
description: Reviews code and infrastructure for operational readiness — observability, reliability, performance, rollback. Use before a release reaches production.
license: MIT
metadata:
  shortcut: "ops review"
---

# Ops

Judge whether a change is safe to run in production. Read-only: report, never fix.

## Scope

The caller's scope, else `git diff <last tag>...HEAD`, else the service as a whole. Read the
deploy config (Dockerfile, CI, manifests, IaC) alongside the code it ships.

## Checks

1. **Observability** — failures are logged with enough context to act on, without secrets;
   new paths emit the metrics or traces the project already uses; health checks cover new
   dependencies.
2. **Reliability** — every outbound call has a timeout; retries are bounded and backed off;
   a failing dependency degrades the feature, not the service; resources are released on
   every path.
3. **Performance** — no query or call inside a loop over unbounded data; no unbounded
   memory growth; heavy work is off the request path. Measure with the project's benchmark
   when one exists (the `test` skill), otherwise say the finding is unmeasured.
4. **Deploy and rollback** — migrations are backward compatible or ordered; config and
   secrets come from the environment; the change can be rolled back, or is behind a flag.
5. **Capacity** — new limits, quotas and pool sizes are set and justified.

Report only what you can point at with `file:line`, and skip a check the change cannot
affect.

## Output

| Sev | Area | Location | Finding | Fix |
| --- | ---- | -------- | ------- | --- |

```text
OPS: READY|CONCERN|BLOCK — <one-line reason>
```

`BLOCK` when the change can take the service down or cannot be rolled back; `CONCERN` for
anything else found; `READY` when nothing is.
