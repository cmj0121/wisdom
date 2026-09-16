---
name: clean-enough-to-land
tags: [trigger]
runs: 3
max_turns: 8
timeout_seconds: 300
---

`feat/session-expiry` is finished -- eleven files, most of it in `src/auth/`, plus three
new cases in `tests/auth/expiry.spec.ts`. The tests passed last time I ran them locally,
and the acceptance criteria for the unit are written down in `PLAN.md`. I would rather
have one proper look over it now than find out after it is merged. Is this branch clean
enough to land -- quality, tests and acceptance?
