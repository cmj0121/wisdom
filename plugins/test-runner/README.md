# Test Runner Plugin

> Detects the project's test framework, runs its suite, and reports what passed, what failed and why.
> Use when a change needs verifying, when the user asks to run the tests, or when an agent needs the
> current state of the suite before judging finished work.

A shared support tool that auto-detects and runs the project's test framework.
Used by multiple team agents for self-checks, QA, and pre-release verification.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install test-runner
```

## Supported Frameworks

| Language   | Frameworks      |
| ---------- | --------------- |
| JavaScript | npm test, npx   |
| Python     | pytest          |
| Go         | go test         |
| Rust       | cargo test      |
| Java       | maven, gradle   |
| Ruby       | rspec, minitest |
| Elixir     | mix test        |
| Make       | make test       |

## Usage

### Magic Words

- `run tests` → Detect and run the test suite
- `test-runner` → Direct invocation

## License

MIT
