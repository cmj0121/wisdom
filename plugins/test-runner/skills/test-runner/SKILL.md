---
name: test-runner
description: Detects the project's test framework, runs its suite, and reports what passed, what failed and why. Use when a change needs verifying, when the user asks to run the tests, or when an agent needs the current state of the suite before judging finished work.
license: MIT
model: haiku
context: fork
background: false
allowed-tools:
  - Bash(npm test:*)
  - Bash(npm run:*)
  - Bash(npx:*)
  - Bash(pytest:*)
  - Bash(python -m pytest:*)
  - Bash(go test:*)
  - Bash(make test:*)
  - Bash(cargo test:*)
  - Bash(mvn test:*)
  - Bash(gradle test:*)
  - Bash(bundle exec:*)
  - Bash(mix test:*)
  - Read
  - Glob
  - Grep
metadata:
  author: cmj@cmj.tw
  version: "2.0.0"
  shortcut: "run tests, test-runner"
---

# Test Runner

Used by agent-hale (self-check), agent-ellis (QA), agent-page (pre-release).

## Shortcut

This skill is triggered when the user's prompt contains `run tests` or `test-runner`.

## How It Works

### Phase 1: Detect Test Framework

Auto-detect by checking config files. If multiple detected, run all. If none, report and stop.

| Config File                         | Runner  | Command             |
| ----------------------------------- | ------- | ------------------- |
| `package.json` with `test` script   | npm     | `npm test`          |
| `pytest.ini` / `pyproject.toml`     | pytest  | `pytest`            |
| `setup.cfg` with `[tool:pytest]`    | pytest  | `python -m pytest`  |
| `go.mod`                            | go test | `go test ./...`     |
| `Makefile` with `test` target       | make    | `make test`         |
| `Cargo.toml`                        | cargo   | `cargo test`        |
| `pom.xml`                           | maven   | `mvn test`          |
| `build.gradle` / `build.gradle.kts` | gradle  | `gradle test`       |
| `Gemfile` with `rspec` / `minitest` | bundler | `bundle exec rspec` |
| `mix.exs`                           | mix     | `mix test`          |

### Phase 2: Run Tests

Execute detected command(s). Capture: total/passed/failed/skipped counts,
failure error messages, duration.

### Phase 3: Report Results

Return a structured report:

```txt
__TEST_RESULT__
Framework: <name>
Command: <command>
Status: PASS / FAIL
Total: <n>
Passed: <n>
Failed: <n>
Skipped: <n>
Duration: <time>
__TEST_RESULT__
```

If tests fail, include failure details (file, test name, error message).

## Team Coordination

**Available to:** agent-hale, agent-ellis, agent-page, agent-ross. Always emit the
`__TEST_RESULT__` block when invoked; caller decides how to act.
