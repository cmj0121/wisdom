---
name: test-runner
description: Detects test framework and runs the project test suite.
license: MIT
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
  version: 1.0.0
---

# Test Runner

A shared support tool that detects the project's test framework and runs the test suite.
Used by agent-hale (self-check), agent-ellis (QA verification), and agent-page (pre-release).

## Shortcut

This skill is triggered when the user's prompt contains `run tests` or `test-runner`.

## How It Works

### Phase 1: Detect Test Framework

Auto-detect the test runner by checking for configuration files:

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

If multiple frameworks are detected, run all of them. If none are detected, report
that no test framework was found and stop.

### Phase 2: Run Tests

Execute the detected test command(s). Capture output including:

- Total tests run
- Tests passed / failed / skipped
- Error messages for failures
- Test duration

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

If tests fail, include the failure details (file, test name, error message).

## Team Coordination

**Available to:** agent-hale, agent-ellis, agent-page, agent-ross

When invoked by other agents, always emit the `__TEST_RESULT__` block.
The calling agent decides how to act on the results.
