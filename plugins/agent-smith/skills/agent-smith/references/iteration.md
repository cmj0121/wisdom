# Autonomous Iteration

Read this when Phase 5 runs, which is Autonomous mode only. Partner mode skips the phase and
never needs this file.

## Scoring

Self-assess: `git log`, `git diff main...HEAD`, run tests, identify issues. Optionally invoke
`agent-ellis` for full review. Score (1-10):

| Dimension     | Score | Notes |
| ------------- | ----- | ----- |
| Correctness   |       |       |
| Completeness  |       |       |
| Quality       |       |       |
| Test Coverage |       |       |

## Reporting the iteration

Update the Iteration Log in `PLAN.md`, writing the iteration as `N/target` — iteration `N` of
**at most** `target` (`1/3`, `2/3`). **Report that same `N/target` in Smith's own output to the
user** when each iteration starts and ends, so the user sees where the run stands without
opening `PLAN.md`. `target` is a ceiling, not a quota — say so when reporting, so `1/3` is
never read as two further rounds being owed.

Raising `target` mid-run is allowed when the work genuinely needs more rounds — say so
explicitly (`target 3 → 4, because …`) rather than silently renumbering.

## Stopping condition

Iterate until the work **converges**, not until a fixed count is reached. Stop at whichever
comes first:

- **Converged** — the iteration produced no new FAIL or WARN findings and opened no new units.
  One clean pass is the signal; a second pass exists to re-confirm a pass that followed fixes,
  not to re-audit work that was already clean. This is the normal exit, and it usually arrives
  before `N` reaches `target`.
- **Ceiling** — `target` iterations completed: 3 by default.
- **User-specified count** — always honored, in either direction; it sets `target`.

An iteration that finds nothing costs a full dispatch fan-out across every unit, so a fixed
floor buys re-reads rather than quality. If scores are low but iterations keep surfacing
nothing actionable, that is a planning gap, not an execution gap — return to Phase 1 instead
of spending another pass.
