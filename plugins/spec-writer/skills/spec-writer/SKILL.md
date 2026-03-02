---
name: spec-writer
description: Write technical specifications for software projects.
license: MIT
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
metadata:
  author: cmj@cmj.tw
  version: 0.8.1
---

# Spec Writer Skill

## Shortcut

This skill is triggered when the user's prompt contains `spec`.

### Phase 1: Understand

Review the project's README.md, CONCEPTS.md, and relevant documentation. Optionally invoke
`proj-ideatender:proj-ideatender` for additional project insights.

### Phase 2: Draft and Review

Draft technical specifications covering:

- Project overview and goals
- Functional and non-functional requirements
- System architecture and design
- Implementation details and constraints
- Open questions and future considerations

If a spec exceeds a single file, split into `docs/` with cross-reference links.

Invoke `code-reviewer:code-reviewer` to review drafts. Refine based on feedback.

### Phase 3: Finalize

Ensure each document stays under 5000 words / 800 lines. Loop back to _Phase 2_ if review feedback
requires further refinement.

## Team Coordination

Other skills may invoke this skill to produce specifications for specific features or components.
Write specs based on the context and requirements provided by the caller.
