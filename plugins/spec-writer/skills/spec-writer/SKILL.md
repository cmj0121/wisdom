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

Support tool that produces technical specifications. Invoked by agent-ward (architecture/design specs),
agent-twain (structured technical documents), and ascii-grapher (architecture diagrams).

## Shortcut

This skill is triggered when the user's prompt contains `write spec`, `draft spec`, or `spec-writer`.

### Phase 1: Understand

1. Read `PLAN.md` (if present) for context and goals.
2. Review README.md, CONCEPTS.md, and related docs.
3. Understand scope from the caller's request or user prompt.

### Phase 2: Draft and Review

Draft technical specs covering:

- Project overview and goals
- Functional and non-functional requirements
- System architecture and design
- Implementation details and constraints
- Open questions and future considerations

Invoke `ascii-grapher:ascii-grapher` for system architecture, data flow, and sequence diagrams.
Embed diagrams as fenced code blocks. Split into `docs/` with cross-references if a spec
exceeds one file. When called directly by user, present drafts for review.

### Phase 3: Finalize

Keep each document under 5000 words / 800 lines. Loop back to Phase 2 if review feedback requires refinement.

## Team Coordination

- Called by **agent-ward**: produce architecture/design specs. Report back to Ward.
- Called by **agent-twain**: produce structured technical documents. Report back to Twain.
- Called by **agent-smith**: produce specs for units of work in `PLAN.md`. Report back to Smith.
- Called **directly by user**: full workflow with user review.
