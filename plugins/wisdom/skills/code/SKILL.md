---
name: code
description: Implements one unit of work with its tests, following the project's conventions. Use when what to build is settled and the code is the task.
license: MIT
metadata:
  shortcut: "code it"
---

# Code

Implement one unit and its tests. Read the unit's row and Context in `PLAN.md` when one
exists; otherwise the prompt is the unit.

## Steps

1. **Understand.** Read only what the unit touches: the files it edits in full, everything
   else by declaration lines. Never re-read a file already in context. If the unit is
   ambiguous, ask — do not guess an interface.
2. **Baseline.** Run the project's tests once (the `test` skill, or Context's command) so a
   failure afterwards is attributable.
3. **Build, test first:**
   - Bug: failing regression test → minimal fix → green.
   - Feature: one test per acceptance criterion → implement → refactor only once green.
   - Refactor: green before, small steps, green after every step.
4. **Check.** Run the tests again; exercise the change the way a user would when tests
   cannot (a request, a CLI run, a page load).
5. **Report** in the format below.

## Code rules

- Build what the unit asks for — no speculative options, layers or abstractions.
- Follow the project's existing conventions over general best practice.
- Validate at system boundaries only; trust internal invariants.
- No comments that restate the code; no `TODO`s or dead fallbacks left behind.
- Stuck after two attempts at the same failure: stop and report what was tried.

## Report

```text
Unit:     <id or one line>
Files:    <path> — <why>, one per line
Tests:    <added/changed>; <pass>/<total>, baseline <pass>/<total>
Verified: <what was exercised beyond tests, or "tests only">
Open:     <deferred items and why, or none>
```

Do not commit — that is `commit`'s job.
