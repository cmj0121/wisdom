---
name: spec
description: Writes a technical specification — requirements, interfaces, data model — for a design already decided. Use when a design must be recorded before it is built.
license: MIT
metadata:
  shortcut: "write spec"
---

# Spec

Write down a decided design so someone else can build it. Record — do not re-decide. An
open design question goes back to `wisdom:design`.

## Steps

1. **Collect the decision:** the prompt, `PLAN.md` Decisions, the output of `design`. Read
   only the code the spec's interfaces touch.
2. **Ask** about any gap that would force the builder to guess — an unstated error case, a
   missing field, an unclear limit. Do not fill it in yourself.
3. **Write** the spec in the shape below, to the path the user gives or
   `docs/specs/<topic>.md`. Omit a section that does not apply rather than writing "N/A".

## Shape

```markdown
# <Topic> Specification

## Goal

One paragraph: the problem and who has it.

## Non-goals

What this deliberately does not do.

## Requirements

Numbered, each testable: "The API rejects a request without a token with 401."

## Interfaces

Signatures, routes, CLI flags or file formats — inputs, outputs, errors.

## Data model

Entities, fields, types, constraints.

## Flow

The main path step by step; a diagram when a picture is clearer (`wisdom:diagram`).

## Open questions

Anything still undecided, with who decides.
```

## Rules

- Every requirement must be checkable by a test or a reviewer; rewrite vague ones.
- Use the project's own names for things.
- Keep it as short as the design allows — a spec is read before building, not admired.
