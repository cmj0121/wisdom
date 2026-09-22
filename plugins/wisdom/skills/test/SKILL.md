---
name: test
description: Detects the project's test framework, runs the suite and reports what passed and failed. Use to run tests; it does not review or fix code.
license: MIT
metadata:
  shortcut: "run tests"
---

# Test

Run the test suite and report the result. Never edit code or tests.

## Steps

1. **Find the command**, first match wins: `PLAN.md` Context → `Makefile` `test` target →
   the manifest (`package.json` scripts, `pyproject.toml`, `go.mod`, `Cargo.toml`,
   `Gemfile`) → the framework's default runner.
2. **Run it** once, with any path or filter the caller gave. Do not retry a failing suite.
3. **Report** in the format below. For each failure give the test, the assertion or error in
   one line, and `file:line`. Do not guess a fix.

## Report

```text
RESULT: PASS|FAIL|ERROR
Command: <exact command>
Counts:  <passed> passed, <failed> failed, <skipped> skipped
Failures:
- <test> — <message> (<file:line>)
```

`ERROR` means the suite could not run (no framework found, command missing, build broke);
say which. No framework found is `ERROR`, never `PASS`.
