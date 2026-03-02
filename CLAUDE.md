# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Wisdom is a Claude Code plugin marketplace — a collection of AI-agent skill plugins that extend Claude
Code's capabilities. Plugins are defined primarily through Markdown-based skill definitions (SKILL.md)
with YAML frontmatter, not traditional source code.

All the plugins are follow the PoLP (Principle of Least Power) principle, which means they are designed
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
- `allowed-tools`: explicit tool permissions the skill needs
- `metadata`: author and version

The body contains phase-by-phase instructions that guide the AI agent through a workflow.

### Skill Discovery (Three Tiers)

1. User-level: `~/.claude/skills/`, `~/.claude/commands/`
2. Project-level: `.claude/skills/`, `.claude/commands/`
3. Plugin-bundled: `plugins/*/skills/`
