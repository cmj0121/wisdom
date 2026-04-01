# Dependency Auditor Plugin

> Audits dependencies for vulnerabilities and outdated packages.

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
