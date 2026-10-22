---
name: code
description: Implements one unit of work with its tests, following the project's conventions. Use when what to build is settled and the code is the task.
license: MIT
metadata:
  shortcut: "code it"
---

# Code

Implement one unit and its tests. Read Setup, the unit and the decisions it follows from
the prompt when it pastes them, else from `PLAN_DETAILS.md` at the path given or the repo
root; with neither, the prompt is the unit. In a fresh worktree, run Setup's `Install`
before anything else.

## Steps

1. **Understand.** Read the unit's `Files` in full. Take interfaces from the decisions it
   follows — do not open files to confirm what an Interface already defines. Read anything
   else by declaration lines, and only where the Interface is silent. Never re-read a file
   already in context. If the unit is ambiguous, ask — do not guess an interface.
2. **Baseline.** Skip when Setup records one. Otherwise run the project's tests once (the
   `test` skill, or Setup's command) so a failure afterwards is attributable.
3. **Build, test first**, running only the unit's tests through Setup's `Subset` template
   (the full suite when it has none):
   - Bug: failing regression test → minimal fix → green.
   - Feature: one test per acceptance criterion → implement → refactor only once green.
   - Refactor: green before, small steps, green after every step.
4. **Check.** Run those tests again — and the full suite once, unless the prompt says the
   caller runs it after merging. Exercise the change the way a user would when tests
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
Tests:    <added/changed>; <pass>/<total> via <command>, baseline <pass>/<total> or recorded
Verified: <what was exercised beyond tests, or "tests only">
Open:     <deferred items and why, or none>
```

Do not commit unless asked to run `wisdom:commit` — committing is that skill's job.
