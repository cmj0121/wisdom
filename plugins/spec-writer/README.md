# Spec Writer Plugin

> Write technical specifications for software projects.

The spec-writer plugin helps you create detailed technical specifications for your software projects.
It reads your project's README, understands the codebase structure, and produces clear documents
covering concepts, architecture, design principles, and implementation details.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install spec-writer
```

## How It Works

### Specification Workflow

1. **README check** - Verifies that a `README.md` exists in the project root
2. **Project scan** - Reads the README and scans the project structure to understand context
3. **Scope confirmation** - Asks what kind of specification you need
4. **Draft documents** - Writes specification files following size and formatting guidelines
5. **User confirmation** - Presents drafts and waits for approval before writing files

### Document Types

| Document      | Location     | Content                                           |
| ------------- | ------------ | ------------------------------------------------- |
| `README.md`   | Project root | High-level overview, purpose, features, examples  |
| `CONCEPTS.md` | Project root | Core concepts, architecture, design principles    |
| `docs/*.md`   | `docs/`      | Implementation details and technical requirements |

All documents are kept under 5000 words or 800 lines. Larger specifications are split into multiple
files inside the `docs/` directory with cross-reference links.

## Usage

### Slash Command

```text
/spec
```

Triggers the full specification writing workflow.

### Magic Word

Typing a prompt that contains `spec` will auto-dispatch this skill via the shortcut plugin.

## License

MIT
