---
name: design
description: Decides an architecture, API shape or technology choice by weighing the options and their trade-offs. Use before building, when how to build is still open.
license: MIT
metadata:
  shortcut: "design it"
---

# Design

Settle one design question and record the decision. Decide — do not write the code or the
full specification.

## Steps

1. **State the question** in one sentence, with the constraints that bind it: the purpose,
   the existing stack and conventions (`PLAN.md` Context, `CLAUDE.md`), scale, and what must
   stay compatible.
2. **List 2–4 real options.** Include the one the codebase already leans toward. An option
   nobody would pick is padding — drop it.
3. **Compare** them on what the purpose needs: complexity, fit with the existing code,
   reversibility, operational cost, new dependencies. Say which becomes hard to change later.
4. **Recommend one** and say why in two sentences. When the choice is hard to reverse
   (public API, data model, dependency, file format) or the options are close, ask the user
   to choose before recording it.
5. **Record** the decision (below). When `PLAN.md` exists, append a row to its Decisions
   table as well.

## Design rules

- Design for the stated purpose only: no layer, option or abstraction for a need nobody
  raised. Name what was deliberately left out.
- Prefer the boring choice the project already uses over a better one it would have to
  learn.
- Define interfaces by what callers need: inputs, outputs, errors — not internals.

## Output

```markdown
## Decision: <question>

| Option | Trade-off | Hard to change later |
| ------ | --------- | -------------------- |

**Chosen:** <option> — <why>
**Interface:** <signatures, routes, schema or format, when the decision defines one>
**Left out:** <what was not designed, and why>
```

A picture helps: hand the structure to `wisdom:diagram`. A spec is needed: hand the
decision to `wisdom:spec`.
