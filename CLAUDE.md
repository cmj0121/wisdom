# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Wisdom is a Claude Code plugin marketplace — a collection of AI-agent skill plugins that extend Claude
Code's capabilities. Plugins are defined primarily through Markdown-based skill definitions (SKILL.md)
with YAML frontmatter, not traditional source code.

All plugins follow the PoLP (Principle of Least Power) principle, which means they are designed
to be as simple and declarative as possible, relying on Claude's natural language understanding rather
than complex code logic. This makes them more maintainable and easier to extend by the community.

## Architecture

### Plugin Structure

Every plugin lives under `plugins/<name>/` and must contain:

```text
plugins/<name>/
├── .claude-plugin/plugin.json   # Metadata: name, version, license, author
├── skills/<name>/SKILL.md       # AI agent instructions with YAML frontmatter
├── README.md
└── LICENSE
```

### Skill Definitions (SKILL.md)

Each SKILL.md has YAML frontmatter declaring:

- `name`, `description`, `license`
- `model`: which model tier runs the skill — `fable` / `opus` / `sonnet` / `haiku`, a full
  model ID, or omitted to inherit the session default. Pin only where it matters: the
  strongest model for high-stakes, hard-to-reverse reasoning, a cheaper one for mechanical
  high-frequency work. Read at session start, so changes take effect on the next session.
- `allowed-tools`: explicit tool permissions the skill needs
- `metadata`: author and version

The body contains phase-by-phase instructions that guide the AI agent through a workflow.

### Skill Discovery (Three Tiers)

1. User-level: `~/.claude/skills/`, `~/.claude/commands/`
2. Project-level: `.claude/skills/`, `.claude/commands/`
3. Plugin-bundled: `plugins/*/skills/`

## Checks

Run `make test` before handing work back: it runs `scripts/test` (structure),
`scripts/check-version-sync` (versions) and `scripts/validate` (semantics), and reports all
three rather than stopping at the first failure. Those same three run on every commit,
ungated — pre-commit's candidate list excludes deletions, so a path-gated hook sees nothing on
a deletion-only commit and is skipped. After editing `scripts/validate`, also run
`scripts/validate-fixtures` — its negative-fixture self-test, and the one hook still gated
(on `^scripts/`), which the commit path runs but `make test` does not.

What that means for edits here:

- A plugin version bump touches three files at once: `.claude-plugin/marketplace.json`, the
  plugin's `plugin.json`, and the skill's `metadata.version`. Never change one alone.
- A release also bumps the **top-level** `version` in `.claude-plugin/marketplace.json`, which
  must not lag the latest `v*` git tag. That is a fourth location and a separate check.
- A plugin's `description` must read identically in `.claude-plugin/marketplace.json`, its
  `plugin.json` and its `SKILL.md` frontmatter.
- Every skill needs a `## Shortcut` section declaring its magic words in backticks; `shortcut`
  itself is the sole exception. Magic words must be unique across all plugins.
- A plugin README must document exactly the magic words its skill declares — no extras, none
  missing — and keep its H1, `## Installation` and `## License` sections.
- Inside a `## Shortcut` section, and under a plugin README's Magic Words heading, EVERY
  backtick span is read as a magic word. Write anything else there — filenames, tool names,
  skill references — without backticks. Elsewhere in the same file backticks are normal.
  Such a section ends only at a heading of the same or higher level, so its subsections are
  still inside it, and a code fence there is rejected outright rather than read as prose.
- A plugin registered in `.claude-plugin/marketplace.json` must also be named in the
  top-level `README.md` prose; a mention only inside a code fence does not count.
- Write a `<plugin>:<skill>` reference only when both halves exist in this repo.
- `model:` must be a known tier or a full `claude-*` ID; to inherit the session default, omit
  the field — `inherit` is not a valid value.

Passing checks only prove nothing mechanically checkable is broken. Prose accuracy — a stale
table row, a wrong command name — is not covered and still needs review.
