# ASCII Grapher Plugin

> Draws ASCII diagrams for architecture, data flows, state machines and concepts. Use when a structure
> is easier to see than to read, when the user asks for a diagram in plain text, or when a design
> needs a picture that survives in a terminal or a commit message.

The ascii-grapher plugin creates plain-text diagrams directly in your terminal — no external tools
needed. Describe what you want to visualize (or point it at your code) and get a clean ASCII diagram
using box-drawing characters.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install ascii-grapher
```

## How It Works

1. **Understand** — Reads your codebase or listens to your description to identify components and relationships.
2. **Plan** — Determines nodes, edges, layout direction, and size constraints.
3. **Draw** — Renders a diagram using Unicode box-drawing characters inside a code block.
4. **Refine** — Iterates on the diagram based on your feedback.
5. **Save** — Optionally writes the diagram to a file.

## Supported Diagram Types

| Type             | Example use case                           |
| ---------------- | ------------------------------------------ |
| Block diagram    | Module relationships, layered architecture |
| Flowchart        | Decision trees, process flows              |
| Sequence diagram | Request/response between actors over time  |
| Tree             | File structures, hierarchies               |
| Data flow        | ETL pipelines, event streams               |

## Usage

### Slash Command

```text
/ascii-grapher
```

### Magic Words

Typing a prompt that contains `draw a graph`, `draw a diagram`, or `ascii diagram` will
auto-dispatch this skill via the shortcut plugin. These are magic words, not slash commands —
the plugin ships a skill, so the slash form is the skill's own name.

### Examples

```text
draw an ascii diagram of the plugin architecture
draw a graph of the request flow from client to database
draw a diagram of the module dependencies
```

## License

MIT
