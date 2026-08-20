# Changelog Generator Plugin

> Generates changelog entries from git history, grouping conventional commits by type. Use when a
> release needs notes, when the user asks what changed since a tag, or when a CHANGELOG has fallen
> behind the commits it is supposed to describe.

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

- `generate changelog` → Generate changelog from recent commits
- `changelog-gen` → Direct invocation

## License

MIT
