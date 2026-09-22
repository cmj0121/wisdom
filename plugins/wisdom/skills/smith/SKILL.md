---
name: smith
description: Drives a piece of work from idea to merge — plans it, then calls the wisdom skills to design, build, review and commit it. Use for substantial work.
license: MIT
metadata:
  shortcut: "smith"
---

# Smith

Coordinate; do not do the work. Every step below belongs to another skill, and Smith's job
is to call it with the right input, read its result, and decide what happens next.

## Ground rules

- **Two checkpoints.** Stop for the user to approve the plan, and to approve the merge.
  Also stop whenever a skill asks a question only the user can answer, or a choice is hard
  to undo — autonomy is about pacing, never about deciding such a fork for the user.
- **`PLAN.md` is the memory.** Point every skill and subagent at it instead of restating
  context in the prompt. Once a unit is merged, shrink its row to one line and drop its
  reports from what you carry forward.
- **No missing input is filled in.** A skill that returns no result, or a review with no
  `VERDICT` line, is a gap: retry it once, then stop and tell the user. A result Smith
  writes for a silent skill is indistinguishable from a real one.
- **Language.** Talk to the user in their `lingua` language if one is set; keep prompts to
  skills and subagents in English — they are read by a model, and they add up.
- **Never tag, release or push** unless the user asks in this conversation.

## 1. Plan

Run `wisdom:plan` on the idea. Then run `wisdom:challenge` on the resulting plan:

- `GO` → note its top items as risks in `PLAN.md`.
- `PAUSE` → revise the named items, then challenge again once.
- `RECONSIDER` → bring the finding to the user before anything else.

**Checkpoint 1:** show the goal, the units and the open risks. Wait for approval.

## 2. Design

Only when the plan adds a public interface (an exported API, a route, a CLI flag, a schema,
a file format) or a dependency: run `wisdom:design` for it, and `wisdom:spec` when the
design is large enough that the builder would otherwise have to guess. A unit that changes a
visual interface gets `frontend-design:frontend-design` if it is installed — say so when it
is not. Behind an unchanged interface, skip this step.

## 3. Build

Create the branch first: `git checkout -b feat/<three-word-slug>`.

Order the units into batches by `Depends on`: a batch holds every unit whose dependencies
are already merged. For each batch:

1. **Code.** One subagent per unit, via the `Agent` tool with `isolation: "worktree"` when
   the batch has more than one unit. Its prompt: the unit's row number, "read `PLAN.md`",
   and "run `wisdom:code`". Tightly coupled units run one at a time, no worktree.
2. **Review.** Run `wisdom:review` on each unit's diff, passing the unit's `Acceptance`
   and the test result from the code report, so the suite is not run twice.
3. **Route the verdict:**

   | Verdict | Next                                                              |
   | ------- | ----------------------------------------------------------------- |
   | `PASS`  | ready to merge                                                    |
   | `WARN`  | fix if cheap; otherwise accept and note it in `PLAN.md`           |
   | `FAIL`  | back to `wisdom:code` with the findings, then review again        |
   | no line | re-run the review once; still none → stop, the unit is unreviewed |

   A finding that says the design is wrong goes to `wisdom:design`, not to `code`. After two
   failed fix rounds on the same unit, stop and bring it to the user.

4. **Merge** each passing worktree branch into the feature branch, one at a time; resolve a
   conflict with a `wisdom:code` subagent, then review the result again.
5. **Commit** each unit with `wisdom:commit`, and mark it `done` in `PLAN.md`.

## 4. Check

Run only the checks the change calls for, in parallel:

- `wisdom:docs` — the change is user-visible.
- `wisdom:secure` on the branch diff — it touches auth, input handling, secrets or crypto.
- `wisdom:audit` — a manifest or lockfile changed.
- `wisdom:ops` — it changes how a service runs or deploys.

A `FAIL`, `FINDINGS` or `BLOCK` goes back through step 3 like a review failure. `INCOMPLETE`
or `CONCERN` is reported at the checkpoint, not silently accepted.

## 5. Merge

**Checkpoint 2:** show `git log --oneline main..HEAD`, the verdict of every unit and check,
and anything accepted with a warning. Wait for approval, then:

```bash
git checkout main
git merge --no-ff feat/<slug>   # message: what the branch delivers; Closes: <issue> if any
git branch -d feat/<slug>
rm PLAN.md
```

A merge conflict goes to a `wisdom:code` subagent, then `wisdom:review`.

## 6. Release

Only when the user asks: run `wisdom:release`.

## Report

End with at most five lines: what merged, what was deferred, and one thing the next run
should do differently — only if there is one.
