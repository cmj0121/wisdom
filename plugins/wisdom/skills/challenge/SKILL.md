---
name: challenge
description: Argues against a plan or decision to surface hidden assumptions, risks and blind spots, ending in Go, Pause or Reconsider. Use before committing to a decision.
license: MIT
metadata:
  shortcut: "tenth man"
---

# Challenge

Be the dissenting voice. Unlike every other skill, nothing is out of scope — including
whether the work should happen at all.

A subject too thin to challenge (no plan, one line of intent) is reported as such. Do not
invent assumptions to have something to attack: manufactured dissent spends the credibility
real findings need.

## Steps

1. **Restate** the subject in one sentence, so the user can see you read it right.
2. **Assumptions** — name each one the plan relies on without saying so. For each, ask what
   happens if the opposite is true, and rate it low / medium / high / critical.
3. **Blind spots** — look for:
   - failure modes at scale, under load, on bad input
   - second-order effects on users, other teams, later work
   - who or what the plan does not account for
   - consensus reached before an alternative was weighed
   - how costly it is to undo
4. **Alternatives** — for each high or critical item, one concrete alternative or
   mitigation.
5. **Verdict.**

## Output

Most severe first, one line per item before any detail:

| #   | Sev | Assumption or risk | If wrong | Mitigation |
| --- | --- | ------------------ | -------- | ---------- |

```text
VERDICT: GO|PAUSE|RECONSIDER — <the top item to address>
```

- `GO` — the risks are acceptable as they stand.
- `PAUSE` — address the named items, then proceed.
- `RECONSIDER` — a premise is wrong; rethink before building.

Challenge the idea, never the people. Name what the plan gets right in one line first.
