---
name: smith
description: Drives a piece of work from idea to merge — plans it, then calls the wisdom skills to design, build, review and commit it. Use for substantial work.
license: MIT
metadata:
  shortcut: "smith"
---

# Smith

Coordinate; do not do the work. Every step below belongs to another skill, bar the suite run: call
it with the right input, read its result, decide what happens next.

## Ground rules

- **Two checkpoints.** Stop for the user to approve the plan, and the merge. Also stop when a skill
  asks what only the user can answer, or a choice is hard to undo.
- **The plan files are the memory.** `PLAN.md` is Smith's view; `PLAN_DETAILS.md` holds what a
  subagent needs. Neither is committed, so a worktree lacks both: paste Setup, the unit's section
  and its decisions into the prompt, with the main checkout's absolute path to both as a fallback.
  Subagents only read them; Smith writes them, itself or through an inline `wisdom:design`, and
  updates `PLAN.md` before each step: a hook re-injects it after compaction.
- **Delegate every unit step.** Each skill run on a unit — code, review, fix, commit — goes to a
  subagent through `Agent`. Ask each to return only its fixed result line, plus one line per finding
  or failure on `WARN` or `FAIL`, no prose summary; a code subagent adds its Report block and any
  worktree path and branch. Smith reads those lines, never a diff; once a unit is merged, drop its
  reports.
- **No missing input is filled in.** A skill Smith routes on that returns no fixed result line is a
  gap: retry it once, then stop and tell the user; a review still without one leaves its unit
  unreviewed. Never write a silent skill's result yourself.
- **Two failed rounds** on the same unit or the same suite: stop and bring it to the user.
- **Language.** Write both checkpoints and the report in `respond_in` from the `lingua` preference
  in context, else the user's language, whatever the skills returned. Keep prompts to skills and
  subagents in English.
- **Keep the branch** as simple and linear as possible.
- **Never tag, release or push** unless the user asks in this conversation; a release is
  `wisdom:release`.

## 1. Plan

Run `wisdom:plan` on the idea. Then have a subagent run `wisdom:challenge` on the plan:

- `challenge: GO` → note its top items as risks in `PLAN.md`.
- `challenge: PAUSE` → revise the named items, then `SendMessage` the same challenger to re-check
  once.
- `challenge: RECONSIDER` → bring the finding to the user first.

**Checkpoint 1:** show the goal, the units and the open risks, plus `Tests deferred`, recorded as a
decision, when the plan is large enough for tests to wait. Wait for approval.

## 2. Design

Run every `design` unit here, never in Build, and mark it `done` in `PLAN.md`. Run `wisdom:design`
also when the plan adds a public interface (API, route, CLI flag, schema, file format) or a
dependency, and `wisdom:spec` when the builder would otherwise have to guess. A unit that changes a
visual interface gets `frontend-design:frontend-design` if installed — say so when not. With no
`design` unit and an unchanged interface, skip this step.

## 3. Build

Create the branch first: `git checkout -b feat/<three-word-slug>`. Order the units into batches by
`Depends on`: a batch holds every unit whose dependencies are merged or `done`. For each batch:

1. **Code.** One subagent per unit, with `isolation: "worktree"` when the batch has several units.
   Its prompt: Setup, the unit's section, the plan paths, "run `wisdom:code`", and "the full suite
   runs after merge". Keep its agent ID, worktree path and branch: the same subagent fixes and
   commits the unit. Tightly coupled units run one at a time, no worktree. With `Tests deferred`,
   each prompt adds "tests deferred", and one final unit writes all the tests.
   - `code: BLOCKED` → stop and bring its reason to the user.
2. **Review.** One subagent per unit, the batch in parallel, each running `wisdom:review` on its
   unit's diff (in its worktree, if any) with the unit's `Acceptance` and the code report's `Tests`
   line, so the tests are not run again; under `Tests deferred`, say the final unit covers them.
   Keep each reviewer's agent ID: a re-review goes to it by `SendMessage`, to check only the fix;
   one that cannot be resumed is replaced, with the whole diff.
3. **Route the verdict**, and write it to the unit's `Verdict` in `PLAN.md`:

   | Verdict        | Next                                                                   |
   | -------------- | ---------------------------------------------------------------------- |
   | `review: PASS` | commit                                                                 |
   | `review: WARN` | fix if the finding lines show it is cheap; else accept, note `WARN`    |
   | `review: FAIL` | `SendMessage` the findings to the unit's code subagent, then re-review |
   | `review: SKIP` | the unit left no diff: stop and tell the user; it is not `done`        |

   A finding that says the design is wrong: run `wisdom:design` inline, then `SendMessage` the new
   Interface to the code subagent.

4. **Commit.** `SendMessage` the code subagent to `git add` the `Files` its report names, then run
   `wisdom:commit` in its worktree; a new subagent does so there, told those files, if it cannot be
   resumed. Only `COMMIT: <hash>` marks the unit `done`.
   - `commit: FAILED` → `SendMessage` it the reason: fix, re-review if code changed, recommit.
5. **Merge** each committed worktree branch into the feature branch, one at a time. A conflict goes
   to a `wisdom:code` subagent, told the conflicted paths to fix and `git add`; then review and
   commit again.
6. **Test.** Once the batch is merged, Smith itself runs Setup's `Test` through Bash on the feature
   branch, with a timeout the suite fits, reading only
   `log=$(mktemp); ( set -e; <Test> ) >"$log" 2>&1; echo "exit $?"; tail -n 20 "$log"`. A one-unit
   batch built on the feature branch, whose `Tests` line is already a full-suite run, takes that
   instead.
   - Exit 0 → set `PLAN_DETAILS.md` Baseline to `PASS at <short SHA>` before the next batch.
   - No `exit N` line, or a suite beyond Bash's foreground limit → it could not run: stop and tell
     the user.
   - Non-zero → a subagent runs `wisdom:test` to name the failures.
   - `test: FAIL` → a new code subagent on the feature branch gets the failures and the `Files` of
     the units they touch; review, `git add` its report's `Files` and commit, run the suite again.
   - `test: ERROR` → the suite could not run; `test: PASS` → the runs disagree. Nothing is proven:
     stop and tell the user why.

## 4. Check

Run only the checks the change calls for, each in its own subagent, in parallel:

- `wisdom:docs` — the change is user-visible.
- `wisdom:secure` on the branch diff — it touches auth, input handling, secrets or crypto.
- `wisdom:audit` — a manifest or lockfile changed.
- `wisdom:ops` — it changes how a service runs or deploys.

Then route each result:

- `docs: BLOCKED`, `secure: FINDINGS`, `audit: FINDINGS`, `ops: BLOCK` → a new code subagent on the
  feature branch, then review and commit as in step 3; after `docs: BLOCKED`, re-run `wisdom:docs`.
- `docs: DONE` or `docs: SKIP`, no file changed → continue.
- `docs: DONE`, files changed → `SendMessage` that docs subagent to `git add` the files its report
  names and run `wisdom:commit`; if it cannot be resumed, a new subagent commits them.
  `commit: FAILED` with changes → a new code subagent, then commit again.
- `audit: INCOMPLETE`, `ops: CONCERN` → report at the checkpoint, never silently accept.

## 5. Shape

A subagent runs `wisdom:history` on the feature branch, base `main`: it classifies as that skill's
body says and passes its script the manifest. Take its `HISTORY:` line.

- `history: SHAPED` → reviews still hold; do not re-run them.
- `history: UNCHANGED` → continue.
- `history: ABORTED` → the branch did not move; show the reason at Checkpoint 2.

Then run the suite as in step 3's Test, since step 4's commits are untested; a fix commits, then
returns here.

## 6. Merge

**Checkpoint 2:** show `git log --oneline main..HEAD`, the `HISTORY:` result, the verdict of every
unit (from `PLAN.md`) and check, and anything accepted with a warning. A commit made after this goes
through `wisdom:review` and step 5 before it is re-shown. Wait for approval, then (a conflict goes
as in step 3's Merge):

```bash
git checkout main
git merge --no-ff feat/<slug>   # message: what the branch delivers; Closes: <issue> if any
git branch -d feat/<slug>
rm PLAN.md PLAN_DETAILS.md
```

## Report

End with at most five lines: what merged, what was deferred, and one thing the next run should do
differently, if any.
