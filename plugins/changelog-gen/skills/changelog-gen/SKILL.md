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

A shared support tool that generates changelog entries from git commit history.
Parses conventional commit messages and groups them by type.

## Shortcut

This skill is triggered when the user's prompt contains `changelog` or `changelog-gen`.

## How It Works

### Phase 1: Determine Scope

1. Find the latest git tag: `git tag --sort=-v:refname | head -1`
2. If no tags exist, use the full git history
3. Collect commits since the last tag: `git log <tag>..HEAD --oneline`

### Phase 2: Parse Commits

Parse each commit using conventional commit format:

```txt
<type>(scope): <description>
```

Group commits by type:

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

Commits that don't follow conventional format go into "Other Changes."

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

If an existing `CHANGELOG.md` exists, prepend the new section.
If not, create it with a header.

### Phase 4: Write or Return

- If called by another agent: return the changelog text
- If called directly: write to `CHANGELOG.md` in the project root

## Team Coordination

**Available to:** agent-ross, agent-twain

When invoked by other agents, return the formatted changelog text.
The calling agent decides where to place it.
