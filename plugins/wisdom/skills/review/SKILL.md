---
name: review
description: Reviews a diff for correctness, quality and fit to its acceptance criteria, ending in a one-line verdict. Use before a change is committed or merged.
license: MIT
metadata:
  shortcut: "review it"
---

# Review

Review a change and return findings with a verdict. Read-only: never edit files.

## Scope

The caller's diff, else `git diff` plus `git diff --cached`, else `git diff main...HEAD`.
Nothing to review: `VERDICT: SKIP`. Judge the change against its purpose — the unit's
acceptance in `PLAN.md`, or the prompt — not against work nobody asked for.

## Checks

1. **Correctness** — logic errors, unhandled edge cases, broken error paths, races.
2. **Acceptance** — each criterion met; nothing outside the unit's scope slipped in.
3. **Tests** — the change is covered; a bug fix has a regression test. Use a result the
   caller passed; otherwise run the `test` skill once.
4. **Security** — hardcoded secrets, unvalidated input at a boundary, injection, sensitive
   data in logs. Flag here; a full audit is the `secure` skill's job.
5. **Quality** — duplication, needless complexity, dead code, comments that restate code,
   drift from the project's conventions.

Report only what you can point at with `file:line`. No style nits a formatter would fix.

## Verdict

- `FAIL` — a correctness bug, failing test, security finding or unmet acceptance criterion.
- `WARN` — quality findings only.
- `PASS` — nothing found.

## Output

One finding per row, most severe first, then the verdict as the last line:

| Sev | Location | Finding | Fix |
| --- | -------- | ------- | --- |

```text
VERDICT: PASS|WARN|FAIL|SKIP — <one-line reason>
```

Always end with the `VERDICT` line, even with zero findings: a caller reads its absence as
a review that never ran.
