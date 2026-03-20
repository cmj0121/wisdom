# Spec Writer Plugin

> Writes technical specifications with architecture diagrams, collaborating with proj-ideatender and ascii-grapher.

The spec-writer plugin produces detailed technical specifications for the development team. It
collaborates with `proj-ideatender` for project context and `ascii-grapher` for architecture
diagrams and flow charts embedded directly in spec documents.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install spec-writer
```

## How It Works

### Specification Workflow

1. **Understand** - Invokes `proj-ideatender` for project context, reads existing docs
2. **Draft and review** - Writes specs with embedded architecture diagrams (via `ascii-grapher`),
   then invokes `agent-ellis` for review (when part of the agent team)
3. **Finalize** - Ensures documents stay under 5000 words / 800 lines

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

### Slash Command

```text
/spec
```

Triggers the full specification writing workflow.

### Magic Word

Typing a prompt that contains `write spec`, `draft spec`, or `spec-writer` will
auto-dispatch this skill via the shortcut plugin.

## License

MIT
