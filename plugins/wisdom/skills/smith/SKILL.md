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
- **The plan files are the memory.** `PLAN.md` is Smith's view; `PLAN_DETAILS.md` holds
  what a subagent needs. Neither is committed, so a worktree lacks both: paste Setup, the
  unit's section and the decisions it follows into the prompt, and give the main
  checkout's absolute path to both files as a fallback. Subagents only read them; Smith
  writes them, itself or through the `wisdom:design` it runs inline.
- **Delegate every unit step.** Each skill run on a unit — code, review, fix, commit, test
  — goes to a subagent through `Agent`. Ask it to return its fixed result line, plus one
  line per finding on `WARN` or `FAIL`. Smith reads those lines, never a diff, and writes
  the verdict into `PLAN.md`; once a unit is merged, drop its reports from what you carry.
- **No missing input is filled in.** A skill that returns no result, or a review with no
  `VERDICT` line, is a gap: retry it once, then stop and tell the user. A result Smith
  writes for a silent skill is indistinguishable from a real one.
- **Language.** Before step 1, take `respond_in` from the `lingua` preference in context,
  else from `~/.claude/projects/<project-path>/memory/lingua.md`; with neither, use the
  user's language. Write both checkpoints and the report in it, whatever the skills
  returned. Keep prompts to skills and subagents in English — a model reads them, and
  they add up.
- **Never tag, release or push** unless the user asks in this conversation.

## 1. Plan

Run `wisdom:plan` on the idea. Then have a subagent run `wisdom:challenge` on the plan:

- `GO` → note its top items as risks in `PLAN.md`.
- `PAUSE` → revise the named items, then challenge again once.
- `RECONSIDER` → bring the finding to the user before anything else.

**Checkpoint 1:** show the goal, the units and the open risks. Wait for approval.

## 2. Design

Run every `design` unit in the plan here, never in Build, and mark it `done` in `PLAN.md`.
Run `wisdom:design` also when the plan adds a public interface (an exported API, a route, a
CLI flag, a schema, a file format) or a dependency, and `wisdom:spec` when the design is
large enough that the builder would otherwise have to guess. A unit that changes a visual
interface gets `frontend-design:frontend-design` if it is installed — say so when it is
not. With no `design` unit and an unchanged interface, skip this step.

## 3. Build

Create the branch first: `git checkout -b feat/<three-word-slug>`.

Order the units into batches by `Depends on`: a batch holds every unit whose dependencies
are already merged or `done`. For each batch:

1. **Code.** One subagent per unit, with `isolation: "worktree"` when the batch has more
   than one unit. Its prompt: Setup, the unit's section, the plan paths, "run
   `wisdom:code`", and "the full suite runs after merge". Keep its agent ID, and the
   worktree path and branch its result names: the same subagent fixes and commits the
   unit. Tightly coupled units run one at a time, no worktree.
2. **Review.** One subagent per unit, the whole batch in parallel, each running
   `wisdom:review` on its unit's diff — in the worktree path, when it has one — with the
   unit's `Acceptance` and the code report's `Tests` line, so the tests are not run again.
3. **Route the verdict**, and write it to the unit's `Verdict` in `PLAN.md`:

   | Verdict | Next                                                                 |
   | ------- | -------------------------------------------------------------------- |
   | `PASS`  | commit                                                               |
   | `WARN`  | fix if the finding lines show it is cheap; else accept, note `WARN`  |
   | `FAIL`  | `SendMessage` the findings to the unit's code subagent, review again |
   | no line | re-run the review once; still none → stop, the unit is unreviewed    |

   A finding that says the design is wrong: run `wisdom:design` inline, then `SendMessage`
   the new Interface to the unit's code subagent. After two failed fix rounds on the same
   unit, stop and bring it to the user.

4. **Commit.** `SendMessage` the unit's code subagent to run `wisdom:commit` in its
   worktree — an uncommitted branch cannot be merged. If it cannot be resumed, a new
   subagent commits in that worktree. Mark the unit `done`.
5. **Merge** each committed worktree branch into the feature branch, one at a time; resolve
   a conflict with a `wisdom:code` subagent, then review and commit the result again.
6. **Test.** Once the batch is merged, a subagent runs `wisdom:test` on the feature branch
   — the one full-suite run per batch. `PASS` → set `PLAN_DETAILS.md` Baseline to
   `PASS at <short SHA>` before the next batch. `FAIL` → a new code subagent on the feature
   branch gets the failures and the units whose `Files` they touch; review, commit and run
   the suite again. Two failed rounds → stop and bring it to the user.

## 4. Check

Run only the checks the change calls for, each in its own subagent, in parallel:

- `wisdom:docs` — the change is user-visible.
- `wisdom:secure` on the branch diff — it touches auth, input handling, secrets or crypto.
- `wisdom:audit` — a manifest or lockfile changed.
- `wisdom:ops` — it changes how a service runs or deploys.

A `FAIL`, `FINDINGS` or `BLOCK` goes to a new code subagent on the feature branch, then
review and commit as in step 3. `INCOMPLETE` or `CONCERN` is reported at the checkpoint,
not silently accepted.

## 5. Merge

**Checkpoint 2:** show `git log --oneline main..HEAD`, the verdict of every unit (from
`PLAN.md`) and check, and anything accepted with a warning. Wait for approval, then:

```bash
git checkout main
git merge --no-ff feat/<slug>   # message: what the branch delivers; Closes: <issue> if any
git branch -d feat/<slug>
rm PLAN.md PLAN_DETAILS.md
```

A merge conflict goes to a `wisdom:code` subagent, then `wisdom:review`.

## 6. Release

Only when the user asks: run `wisdom:release`.

## Report

End with at most five lines: what merged, what was deferred, and one thing the next run
should do differently — only if there is one.
