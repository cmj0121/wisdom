---
name: diagram
description: Draws ASCII diagrams of architecture, flows, states and sequences. Use when a decided structure is easier to see than read, or must render in a terminal.
license: MIT
metadata:
  shortcut: "draw a diagram"
---

# Diagram

Draw a structure that is already decided. Deciding it is `wisdom:design`'s job; a missing
piece of the structure is a question to ask, not a box to invent.

## Steps

1. **Name the subject and the kind** — pick the one form that fits:

   | Kind         | Shows                               |
   | ------------ | ----------------------------------- |
   | Architecture | components and who calls whom       |
   | Flow         | data or control moving step to step |
   | State        | states and the events between them  |
   | Sequence     | messages between actors over time   |
   | Tree         | hierarchy — directories, ownership  |

2. **List the nodes and edges** from the source (the prompt, `PLAN.md`, the code) before
   drawing. Only what the source states.
3. **Draw** in a ` ```text ` fence with the characters below.
4. **Check** every line is the same width where boxes stack, no edge crosses a label, and
   the diagram fits in 100 columns. Past 12 nodes, split it into two diagrams.

## Characters

```text
Boxes     ┌───┐ │   │ └───┘        Arrows    ──>  <──  │  ▼  ▲
Branches  ├── └── ┬ ┴ ┼           Labels    ──label──>  on the edge
```

Use plain ASCII (`+ - | > v`) instead when the caller asks or the output target cannot
render box-drawing characters.

## Rules

- Flow reads left-to-right or top-to-bottom; never both in one diagram.
- One label per edge, three words at most.
- Same kind of thing, same shape of box.
- No legend unless a shape or line style carries a meaning the labels do not.
