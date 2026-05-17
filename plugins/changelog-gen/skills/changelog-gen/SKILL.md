---
name: changelog-gen
description: Generates changelog from git history using conventional commits.
license: MIT
allowed-tools:
  - Bash(git log:*)
  - Bash(git tag:*)
  - Bash(git diff:*)
  - Read
  - Glob
  - Grep
  - Write
  - Edit
metadata:
  author: cmj@cmj.tw
  version: 1.0.0
---

# Changelog Generator

Support tool that generates changelog entries from git commit history using conventional commits.

## Shortcut

This skill is triggered when the user's prompt contains `changelog` or `changelog-gen`.

## How It Works

### Phase 1: Determine Scope

1. Find latest git tag: `git tag --sort=-v:refname | head -1`
2. If no tags, use full history
3. Collect commits since last tag: `git log <tag>..HEAD --oneline`

### Phase 2: Parse Commits

Parse each commit as `<type>(scope): <description>`. Group by type:

| Type     | Section          |
| -------- | ---------------- |
| feat     | Features         |
| fix      | Bug Fixes        |
| docs     | Documentation    |
| refactor | Refactoring      |
| test     | Tests            |
| chore    | Chores           |
| perf     | Performance      |
| ci       | CI/CD            |
| BREAKING | Breaking Changes |

Non-conventional commits go into "Other Changes."

### Phase 3: Generate Changelog

Output in Keep a Changelog format:

```markdown
## [<version>] - <date>

### Breaking Changes

- ...

### Features

- ...

### Bug Fixes

- ...
```

Prepend to existing `CHANGELOG.md`, or create one with a header.

### Phase 4: Write or Return

- Called by another agent: return the changelog text
- Called directly: write to `CHANGELOG.md` in project root

## Team Coordination

**Available to:** agent-ross, agent-twain. Always return formatted changelog text; caller decides placement.
