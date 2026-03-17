---
name: spec-writer
description: Writes technical specifications with architecture diagrams, collaborating with proj-ideatender and ascii-grapher.
license: MIT
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
metadata:
  author: cmj@cmj.tw
  version: 0.9.0
---

# Spec Writer Skill

## Shortcut

This skill is triggered when the user's prompt contains `spec`.

## Role in the Team

The spec-writer produces technical specifications for the development team. It collaborates with:

- **proj-ideatender**: for project context and the brief plan
- **ascii-grapher**: for architecture diagrams and flow charts
- **agent-ellis**: to review spec drafts (when called by agent-smith)

### Phase 1: Understand

1. Invoke `proj-ideatender:proj-ideatender` for project context. Read its cache files
   (`PROJECT.md`, `IDEAS.md`) for existing analysis.
2. Review the project's README.md, CONCEPTS.md, and relevant documentation.
3. Understand the scope from the brief plan or user request.

### Phase 2: Draft and Review

Draft technical specifications covering:

- Project overview and goals
- Functional and non-functional requirements
- System architecture and design
- Implementation details and constraints
- Open questions and future considerations

**Architecture diagrams**: Invoke `ascii-grapher:ascii-grapher` to produce:

- System architecture diagrams showing component relationships
- Data flow diagrams for key processes
- Sequence diagrams for critical interactions

Embed diagrams directly in the spec documents as fenced code blocks.

If a spec exceeds a single file, split into `docs/` with cross-reference links.

Invoke `agent-ellis:agent-ellis` to review drafts (when called by agent-smith).
When called directly by user, present drafts for user review instead.

### Phase 3: Finalize

Ensure each document stays under 5000 words / 800 lines. Loop back to _Phase 2_ if review feedback
requires further refinement.

## Team Coordination

- When called by **agent-smith**: produce specs for the units of work in `PLAN.md`. Report
  completed specs back to Smith.
- When called by **proj-ideatender**: produce specs based on the brief plan context provided.
- When called **directly by user**: full specification workflow with user review.
- Other skills may invoke this skill to produce specifications for specific features or components.
