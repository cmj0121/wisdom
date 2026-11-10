---
name: architecture
description: Decides an architecture, API or technology choice, preferring vetted libraries over hand-rolled code. Use before building, when how to build is still open.
license: MIT
metadata:
  shortcut: "architect it"
---

# Architecture

Settle one architecture question and record the decision. Decide — do not write the code, the
full specification or the ordered units (those are `wisdom:plan`'s).

## Steps

1. **State the question** in one sentence, with the constraints that bind it: the purpose,
   the existing stack and conventions (`PLAN.md` Context, `CLAUDE.md`), scale, and what must
   stay compatible.
2. **List 2–4 real options.** Include the one the codebase already leans toward and, when the
   question involves parsing or security, the vetted library that covers it. An option nobody
   would pick is padding — drop it.
3. **Compare** them on the criteria below that the question turns on. Say which becomes hard
   to change later.
4. **Recommend one** and say why in two sentences. When the choice is hard to reverse
   (public API, data model, dependency, file format) or the options are close, ask the user
   to choose before recording it.
5. **Record** the decision (below). When the plan files exist, add `Question | Chosen | Why`
   to `PLAN.md` Decisions, its Interface and Left out under the matching `D<n>` in
   `PLAN_DETAILS.md`, and correct the `Files` of the units it changes. Write the Interface
   verbatim: `code` builds against it without reopening the files it describes.

## Criteria

Weigh only the ones the question turns on — this is not a checklist.

- **Robustness and security:** how it fails on bad input, and who has already found its bugs.
- **Maintainability:** who can change it in a year, and how much they must learn first.
- **Focus:** it serves the stated target, not a neighbouring one.
- **Reversibility and room to extend:** what it locks in, and where it can grow.
- **Cost:** complexity, operations, new dependencies.

## Rules

- **Vetted over hand-rolled.** Reject building your own when a vetted, maintained library or
  standard exists: parsers (JSON, YAML, CSV, HTML, URL, dates…), crypto, auth, sanitising,
  protocol or serialisation code. Build one only when no vetted option fits, or the
  dependency costs more than the risk (a tiny fixed-format read in a no-dependency script);
  then name it as a risk, with the reason.
- **Precedence.** For parsing untrusted or structured input and anything security-sensitive,
  a vetted library beats the choice the project already uses. Among vetted options, the one
  the project already uses wins. An existing hand-rolled piece is flagged, not extended.
- **Direction, not steps.** The decision states what it commits the project to and where it
  can grow. Settle one decision at a time; splitting work into ordered units stays with
  `wisdom:plan`.
- **Flexible by seams, not layers.** Keep interfaces clean and add a seam only where change
  is already foreseen. No layer, option or plugin point for a need nobody raised; name what
  was deliberately left out.
- **Interfaces by what callers need:** inputs, outputs, errors — not internals.

## Output

```markdown
## Decision: <question>

| Option | Trade-off | Hard to change later |
| ------ | --------- | -------------------- |

**Chosen:** <option> — <why>
**Commits to:** <what the project is now bound to, and where it can grow>
**Interface:** <signatures, routes, schema or format, when the decision defines one>
**Risks:** <a hand-rolled piece kept or flagged, and why — omit when none>
**Left out:** <what was not decided, and why>
```

A picture helps: hand the structure to `wisdom:diagram`. A spec is needed: hand the
decision to `wisdom:spec`.
