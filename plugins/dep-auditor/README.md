# Dependency Auditor Plugin

> Audits project dependencies for known vulnerabilities and outdated versions across npm, pip, go,
> cargo and bundler. Use before a release, when a lockfile changes, or when the user asks whether the
> dependencies are safe or current.

A shared support tool that scans project dependencies for known vulnerabilities
and flags outdated packages.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install dep-auditor
```

## Supported Package Managers

| Language   | Package Managers |
| ---------- | ---------------- |
| JavaScript | npm, yarn        |
| Python     | pip, pipenv      |
| Go         | go modules       |
| Rust       | cargo            |
| Ruby       | bundler          |

## Usage

### Magic Words

- `audit deps` → Audit all project dependencies
- `dep-auditor` → Direct invocation

## License

MIT
