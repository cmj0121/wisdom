---
name: agent-smith
description: Dual-mode development agent — partner or fully autonomous — that plans, implements, reviews, commits, and delivers.
license: MIT
allowed-tools:
  - Bash(git status:*)
  - Bash(git checkout -b:*)
  - Bash(git checkout:*)
  - Bash(git log:*)
  - Bash(git stash)
  - Bash(git restore:*)
  - Bash(git diff:*)
  - Bash(git merge:*)
  - Bash(git branch:*)
  - Bash(rm PLAN.md)
  - Read
  - Glob
  - Grep
  - Write
  - Edit
metadata:
  author: cmj@cmj.tw
  version: 0.8.0
---

# Agent Smith — Development Agent

| Mode       | Trigger words                       | Checkpoints               | Iterations       |
| ---------- | ----------------------------------- | ------------------------- | ---------------- |
| Partner    | `develop`, `implement it`, `fix it` | 2 (plan approval + merge) | Single pass      |
| Autonomous | `smith`                             | 1 (merge only)            | Minimum 3 cycles |

If both trigger types appear, prefer **Autonomous** mode.

**Plan file:** `PLAN.md` in project root — living document, not committed, removed after merge.

## Shortcut

This skill is triggered when the user's prompt contains `develop`, `implement it`, `fix it`, or `smith`.

## How It Works

### Phase 1: Understand and Plan

Invoke `proj-ideatender:proj-ideatender` to analyze the project context.

**[Partner]** Evaluate scope; discuss with user if vague. Use `proj-ideatender` to break down broad
requests into manageable tasks.

Create an implementation plan and write it to `PLAN.md`:

```markdown
# PLAN.md

## Idea

<user's original idea>

## Design

<high-level design and approach>

## Units of Work

| #   | Unit | Description | Status  |
| --- | ---- | ----------- | ------- |
| 1   | ...  | ...         | pending |

## Planned Commits

| #   | Commit | Description |
| --- | ------ | ----------- |
| 1   | ...    | ...         |

## Iteration Log

| Iteration | Correctness | Completeness | Quality | Test Coverage | Summary |
| --------- | ----------- | ------------ | ------- | ------------- | ------- |
```

> **Note:** Iteration Log is for Autonomous mode. In Partner mode it may remain empty.

**[Partner]** Save `PLAN.md` and **WAIT** for user approval. The user may edit the file or invoke
`proj-ideatender` to refine. Do NOT proceed until confirmed.

**[Autonomous]** Proceed directly to Phase 2.

### Phase 2: Implement, Review, and Commit

**Fully autonomous** — do not stop or ask for confirmation.

Read `PLAN.md` as **source of truth** (user may have edited it after Phase 1).

**Before the first commit**, create a feature branch from the idea summary:
`git checkout -b feat/<slugified-3-word-summary>` (e.g., `feat/add-user-auth`)

For each unit of work:

#### Implementation

Write clean, focused code with proper tests and error handling.

For bug fixes: reproduce → write regression test → hypothesize root cause →
isolate and fix (one minimal change) → verify test passes.

#### Review

Pass the linter first, then invoke `code-reviewer:code-reviewer`. Fix all Critical, Warning, and
FAIL-verdict issues. On security FAIL, fix and re-invoke automatically.

#### Commit

Invoke `git-committer:git-committer` for each unit. Update the unit's Status in `PLAN.md` to `done`.

### Phase 3: Assess [Autonomous mode only]

**[Partner]** Skip — go directly to Phase 5.

After all units complete, self-assess: review changes (`git log`, `git diff main...HEAD`), run tests,
identify issues and enhancement opportunities, then score (1-10):

| Dimension     | Score | Notes |
| ------------- | ----- | ----- |
| Correctness   |       |       |
| Completeness  |       |       |
| Quality       |       |       |
| Test Coverage |       |       |

Update the Iteration Log in `PLAN.md`.

### Phase 4: Re-Plan and Iterate [Autonomous mode only]

**[Partner]** Skip — go directly to Phase 5.

Add new units of work to `PLAN.md` addressing issues from Phase 3. Return to **Phase 2**.

**Repeat Phases 2–4 for at least 3 iterations** (honor user-specified count). Stop early if all
scores reach 9+. Each iteration must produce meaningful improvements — no trivial busywork.

### Phase 5: Merge

**[Autonomous]** Show the Iteration Log from `PLAN.md` first.

1. Show `git log --oneline main..HEAD`
2. Invoke `git-committer:git-committer` to generate a merge commit message

**[CHECKPOINT]** Present summary to user. Wait for approval.

After approval: `git checkout main` → `git merge --no-ff <branch>` →
`git branch -d <branch>` → `rm PLAN.md`

If the merge produces conflicts, resolve them, then invoke `code-reviewer:code-reviewer`
to verify the resolution before completing the merge commit.

### Phase 6: Lessons Learned

Share a brief reflection: what went well, what could improve, surprising findings, and patterns for
future sessions.
