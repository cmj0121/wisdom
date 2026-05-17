---
name: ascii-grapher
description: Draw ASCII diagrams for architecture, flows, and concepts.
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

# ASCII Grapher Skill

## Shortcut

This skill is triggered when the user's prompt contains `graph` or `diagram` or `ascii`.

### Phase 1: Understand the Subject

Determine what to visualize: code architecture, concept/data flow, sequence diagram, or custom.
Ask clarifying questions only when scope is genuinely ambiguous.

### Phase 2: Plan the Layout

Plan nodes, edges (with direction/labels), layout direction (top-to-bottom, left-to-right, hybrid),
and size budget (max 120 columns; prefer compact).

### Phase 3: Draw the ASCII Diagram

Use plain-text characters. Conventions:

#### Box style

```text
┌──────────────┐
│  Component   │
└──────────────┘
```

#### Arrows

- Horizontal: `───>`, `<───`, `<──>`
- Vertical: `│` with `▼` or `▲` at endpoints
- Avoid diagonals; use L-shaped connectors

#### Labels

Place edge labels inline on the arrow or above/below:

```text
        request
  ────────────────>
```

#### Grouping

Use solid boxes for logical groups:

```text
┌─── Service Layer ───┐
│                     │
│  ┌───┐    ┌───┐     │
│  │ A │    │ B │     │
│  └───┘    └───┘     │
│                     │
└─────────────────────┘
```

### Phase 4: Present and Refine

Output inside a fenced code block. Add a brief legend if labels aren't self-explanatory.
Loop back to Phase 2 if user requests changes.

### Phase 5: Save (optional)

Embed diagrams inside the target document (e.g., `README.md`, `CONCEPTS.md`, spec file)
within a fenced code block — do not create a separate file. Use `Write`/`Edit` in place.

## Diagram Types Cheat Sheet

| Type             | When to use                                  |
| ---------------- | -------------------------------------------- |
| Block diagram    | Module/component relationships, layered arch |
| Flowchart        | Decision trees, process flows                |
| Sequence diagram | Request/response between actors over time    |
| Tree             | File structures, hierarchies, org charts     |
| Data flow        | ETL pipelines, event streams                 |

## Team Coordination

Other skills invoke this skill to produce diagrams. Draw based on caller's context and requirements.
