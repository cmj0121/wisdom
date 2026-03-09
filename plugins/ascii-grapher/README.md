# ASCII Grapher Plugin

> Draw ASCII diagrams for architecture, flows, and concepts.

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
/graph
```

### Magic Words

Typing a prompt that contains `graph`, `diagram`, or `ascii` will auto-dispatch this skill via the
shortcut plugin.

### Examples

```text
draw an ascii diagram of the plugin architecture
graph the request flow from client to database
show me a diagram of the module dependencies
```

## License

MIT
