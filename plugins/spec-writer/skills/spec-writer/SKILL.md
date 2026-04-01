---
name: spec-writer
description: Writes technical specifications with architecture diagrams.
license: MIT
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
metadata:
  author: cmj@cmj.tw
  version: 1.0.0
---

# Spec Writer Skill

## Shortcut

This skill is triggered when the user's prompt contains `write spec`, `draft spec`, or `spec-writer`.

## Role in the Team

The spec-writer is a support tool that produces technical specifications. It is invoked by:

- **agent-ward** (Architect): for formal architecture and design specs
- **agent-twain** (Technical Writer): for structured technical documents
- **ascii-grapher**: for architecture diagrams and flow charts

### Phase 1: Understand

1. Read `PLAN.md` (if present) to understand the project context and goals.
2. Review the project's README.md, CONCEPTS.md, and relevant documentation.
3. Understand the scope from the caller's request or user prompt.

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

When called directly by user, present drafts for user review.

### Phase 3: Finalize

Ensure each document stays under 5000 words / 800 lines. Loop back to _Phase 2_ if review feedback
requires further refinement.

## Team Coordination

- When called by **agent-ward**: produce architecture and design specs. Report back to Ward.
- When called by **agent-twain**: produce structured technical documents. Report back to Twain.
- When called by **agent-smith**: produce specs for the units of work in `PLAN.md`. Report
  completed specs back to Smith.
- When called **directly by user**: full specification workflow with user review.
