---
name: proj-ideatender
description: Analyze your project and generate ideas for improvements or new features.
license: MIT
allowed-tools:
  - Bash(git log:*)
  - Bash(git show:*)
  - Read
  - Glob
  - Grep
  - WebFetch
  - WebSearch
  - Write
  - Edit
metadata:
  author: cmj@cmj.tw
  version: 0.8.1
---

# Project Idea Tender Skill

ALWAYS enter `plan mode` when called. Do not leave until the user explicitly asks.

## Shortcut

This skill is triggered when the user's prompt contains `analyze`, `plan it` or `review and refine it`.

**Cache dir**: All persistent files (`PROJECT.md`, `IDEAS.md`) MUST be written to
`~/.claude/projects/<project-path>/memory/`, never to the project directory.

### Phase 1: Project Analysis

1. **Project overview**: Read `README.md` and relevant docs. If missing, use Glob for
   `docs/`, `CONTRIBUTING.md`; read key source files; use WebSearch as last resort.
2. **Git history**: `git log` (last 20 commits or 3 months). Use `git show` for significant commits.
3. **Project structure**: Glob to map directory layout. Identify key components and areas needing improvement.

Persist analysis to `PROJECT.md` in cache dir. Update on re-analysis.

### Phase 2: Idea Generation

Generate actionable ideas based on the user's prompt and Phase 1 analysis. Without a prompt,
ask the user what to improve. Categories: features, improvements, refactoring, docs, testing.

Persist ideas to `IDEAS.md` in cache dir.

### Phase 3: Handoff

Present ideas from `IDEAS.md` in table format:

    | Priority | Description | Estimated Time Commitment (AI) |
    | -------- | ----------- | ----------------------------- |
    | High     | Add a new module to support login. | 2 mins |

Do not generate new ideas here. If the user requests refinements, return to _Phase 2_.
The user has final say on which ideas to pursue.

## Team Coordination

When called by other skills, ONLY read cache files (`PROJECT.md`, `IDEAS.md`). Do not generate new
ideas or modify analysis unless explicitly asked.

## Constraints

- **Read-only**: MUST NOT modify project files. Only write `PROJECT.md` and `IDEAS.md` in cache dir.
- Do not implement ideas — analyze and ideate only.
- Aim for 5-10 realistic, well-thought-out ideas aligned with the project's direction.
- Incorporate roadmap or issue tracker references when available.
