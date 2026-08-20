# Spec Writer Plugin

> Writes technical specifications — requirements, interfaces, data models and architecture diagrams.
> Use when a design needs recording before it is built, when the user asks for a spec, RFC or design
> document, or when another agent needs a written contract to work from.

The spec-writer plugin produces detailed technical specifications for the development team.
It is invoked by `agent-ward` (Architect) and `agent-twain` (Technical Writer), and uses
`ascii-grapher` for architecture diagrams and flow charts.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install spec-writer
```

## How It Works

### Specification Workflow

1. **Understand** — Reads `PLAN.md`, project docs, and caller's context
2. **Draft** — Writes specs with embedded architecture diagrams (via `ascii-grapher`)
3. **Finalize** — Ensures documents stay under 5000 words / 800 lines

### Document Types

| Document      | Location     | Content                                           |
| ------------- | ------------ | ------------------------------------------------- |
| `README.md`   | Project root | High-level overview, purpose, features, examples  |
| `CONCEPTS.md` | Project root | Core concepts, architecture, design principles    |
| `docs/*.md`   | `docs/`      | Implementation details and technical requirements |

### Diagrams

The spec-writer automatically invokes `ascii-grapher` to produce:

- System architecture diagrams
- Data flow diagrams
- Sequence diagrams for critical interactions

## Usage

### Magic Words

- `write spec` → Full specification workflow
- `draft spec` → Full specification workflow
- `spec-writer` → Direct invocation

## License

MIT
