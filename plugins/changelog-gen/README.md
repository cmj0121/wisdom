# Changelog Generator Plugin

> Generates changelog from git history using conventional commits.

A shared support tool that parses conventional commit messages and generates
structured changelogs in Keep a Changelog format.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install changelog-gen
```

## How It Works

1. Finds the latest git tag to determine scope
2. Parses commits using conventional commit format
3. Groups by type (features, fixes, docs, etc.)
4. Outputs in Keep a Changelog format

## Usage

### Magic Words

- `changelog` → Generate changelog from recent commits
- `changelog-gen` → Direct invocation

## License

MIT
