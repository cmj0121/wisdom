---
name: ascii-grapher
description: Draws ASCII diagrams for architecture, data flows, state machines and concepts. Use when a structure is easier to see than to read, or must survive in a terminal.
license: MIT
model: haiku
context: fork
background: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
metadata:
  author: cmj@cmj.tw
  version: "2.0.0"
  shortcut: "draw a graph, draw a diagram, ascii diagram"
---

# ASCII Grapher Skill

## Shortcut

This skill is triggered when the user's prompt contains `draw a graph`, `draw a diagram`,
or `ascii diagram`.

## How It Works

Each phase assumes the one before it produced something: a subject to draw, a layout to
render. When it did not, say what is missing and ask rather than inventing structure to fill
the frame. A diagram is read as a statement of fact about the system, so a guessed box is a
claim nobody made and nobody can trace.

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
