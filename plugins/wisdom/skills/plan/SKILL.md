---
name: plan
description: Turns an idea into PLAN.md and PLAN_DETAILS.md — units, decisions and the context to build them — for later skills. Use before non-trivial work starts.
license: MIT
metadata:
  shortcut: "plan it"
---

# Plan

Write two files at the repo root, so later skills read instead of rediscovering the project:
`PLAN.md`, the short view a coordinator reads, and `PLAN_DETAILS.md`, what a builder needs to
start cold. Plan only — do not design, code or commit.

## Steps

1. **Read, cheapest first, and stop once the question is answered:** `CLAUDE.md` and
   `README.md` → directory layout → declaration lines (grep) → the files the change touches.
   Never read a file already in context.
2. **Capture the issue** when the work came from one (`#123`, a URL, a ticket ID). Never
   invent one; with no issue the field is `—`.
3. **Ask before writing** when the idea has more than one reasonable reading, or a choice is
   hard to undo (public API, data model, dependency, package name). Offer 2–4 options with
   the trade-off, recommendation first. One question at a time.
4. **Record the setup:** what turns a fresh checkout (a new worktree) into a testable one,
   the full-suite command and its result now, and how to run only some tests.
5. **Split the work** into units small enough for one commit each, and mark which depend on
   which — units with no dependency can run in parallel. List the files each unit touches.
6. **Write both files** in the shapes below, then show the user the goal and the unit list.

## PLAN.md

```markdown
# PLAN — <goal in one line>

## Context

| Field | Content                                |
| ----- | -------------------------------------- |
| Stack | languages, frameworks, package manager |
| Issue | ref, or —                              |

## Decisions

| # | Question | Chosen | Why |

## Units

| # | Unit | Depends on | Status | Verdict |

## Risks

- <open risk, from `challenge` — or none>
```

Keep it under 60 lines: it is re-read on every step. `Verdict` stays empty until a review
returns one.

## PLAN_DETAILS.md

```markdown
# PLAN_DETAILS — <goal in one line>

## Setup

| Field    | Content                                                        |
| -------- | -------------------------------------------------------------- |
| Install  | commands that make a fresh checkout testable, or —             |
| Test     | exact full-suite command; lint / build commands if any         |
| Subset   | template that runs only some tests, e.g. `pytest <path>`, or — |
| Baseline | full-suite result and the commit it ran on                     |

## Decisions

### D<n> — <question>

- Interface: <signatures, routes, schema or format, verbatim — or —>
- Left out: <what was deliberately not designed>

## Units

### U<n> — <unit>

- Files: `<path>` — <role>, one per line
- Acceptance: <one testable sentence; what `review` checks>
- Follows: <D1, D3 — the decisions this unit must obey, or —>
```

No line budget: a builder reads only its unit and the decisions it follows.

## Rules

- Both files are working files: never commit them.
- Updating existing files: change the rows that moved, keep the rest.
- A unit that needs an interface decided first gets a `design` unit ahead of it; leave its
  decision's Interface as `—` for `design` to fill.
