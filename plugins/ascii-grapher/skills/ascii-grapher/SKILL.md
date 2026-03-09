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
  version: 0.8.2
---

# ASCII Grapher Skill

## Shortcut

This skill is triggered when the user's prompt contains `graph` or `diagram` or `ascii`.

### Phase 1: Understand the Subject

Determine what the user wants to visualize. This may be:

- **Code architecture**: read the codebase to understand module relationships, layers, and dependencies.
- **Concept flow**: understand a process, data flow, or decision tree from the user's description.
- **Sequence diagram**: capture interactions between components over time.
- **Custom**: any other structure the user describes.

If the user references code, read the relevant files with `Read`, `Glob`, and `Grep` to gather context.
Ask clarifying questions only if the scope is genuinely ambiguous.

### Phase 2: Plan the Layout

Before drawing, plan:

1. **Nodes** — identify every box, actor, or component.
2. **Edges** — identify connections, their direction, and optional labels.
3. **Layout direction** — top-to-bottom, left-to-right, or hybrid based on what fits best.
4. **Size budget** — aim for max 120 columns wide and a reasonable height. Prefer compact diagrams.

### Phase 3: Draw the ASCII Diagram

Render the diagram using only plain-text characters. Follow these conventions:

#### Box style

```text
┌──────────────┐
│  Component   │
└──────────────┘
```

#### Arrows

- Horizontal: `───>`, `<───`, `<──>`
- Vertical: `│` with `▼` or `▲` at endpoints
- Diagonal: avoid when possible; use L-shaped connectors instead

#### Connectors and junctions

- Corner: `┌ ┐ └ ┘`
- Tee: `├ ┤ ┬ ┴`
- Cross: `┼`

#### Labels

Place edge labels inline on the arrow or directly above/below:

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

1. Output the diagram inside a fenced code block so it renders with a monospace font.
2. Add a brief legend or description below the diagram if labels alone are not self-explanatory.
3. If the user asks for changes, loop back to _Phase 2_ and redraw.

### Phase 5: Save (optional)

When saving, embed the diagram directly inside the target document (e.g., `README.md`, `CONCEPTS.md`,
or a spec file) within a fenced code block — do not create a separate standalone file for the diagram.
Use the `Write` or `Edit` tool to insert or update the diagram in place.

## Diagram Types Cheat Sheet

| Type             | When to use                                  |
| ---------------- | -------------------------------------------- |
| Block diagram    | Module/component relationships, layered arch |
| Flowchart        | Decision trees, process flows                |
| Sequence diagram | Request/response between actors over time    |
| Tree             | File structures, hierarchies, org charts     |
| Data flow        | ETL pipelines, event streams                 |

## Team Coordination

Other skills may invoke this skill to produce diagrams for documentation or specifications.
Draw diagrams based on the context and requirements provided by the caller.
