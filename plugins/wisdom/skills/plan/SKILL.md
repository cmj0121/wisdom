---
name: plan
description: Turns an idea into PLAN.md — context, units of work and decisions — for later skills to build from. Use before non-trivial work starts.
license: MIT
metadata:
  shortcut: "plan it"
---

# Plan

Write `PLAN.md` at the repo root: the one place later skills read instead of rediscovering
the project. Plan only — do not design, code or commit.

## Steps

1. **Read, cheapest first, and stop once the question is answered:** `CLAUDE.md` and
   `README.md` → directory layout → declaration lines (grep) → the files the change touches.
   Never read a file already in context.
2. **Capture the issue** when the work came from one (`#123`, a URL, a ticket ID). Never
   invent one; with no issue the field is `—`.
3. **Ask before writing** when the idea has more than one reasonable reading, or a choice is
   hard to undo (public API, data model, dependency, package name). Offer 2–4 options with
   the trade-off, recommendation first. One question at a time.
4. **Split the work** into units small enough for one commit each, and mark which depend on
   which — units with no dependency can run in parallel.
5. **Write `PLAN.md`** in the shape below, then show the user the goal and the unit list.

## PLAN.md

```markdown
# PLAN — <goal in one line>

## Context

| Field    | Content                                     |
| -------- | ------------------------------------------- |
| Stack    | languages, frameworks, package manager      |
| Commands | exact test / lint / build invocations       |
| Baseline | test result before any change               |
| Map      | `path` → role, only files this work touches |
| Issue    | ref, or —                                   |

## Decisions

| # | Question | Options | Chosen | Why |

## Units

| # | Unit | Acceptance | Depends on | Status |
```

Keep Context under 30 lines. `Acceptance` is what `review` will check the unit against: one
testable sentence per unit.

## Rules

- `PLAN.md` is a working file: never commit it.
- Updating an existing `PLAN.md`: change the rows that moved, keep the rest.
- A unit that needs an interface decided first gets a `design` unit ahead of it.
