---
name: agent-smith
description: Team leader agent — dispatches planning, spec-writing, coding, and review jobs to specialized agents.
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
  version: 0.9.0
---

# Agent Smith — Team Leader

Agent Smith is the leader of the development team. Smith does not write code or specs directly —
instead, Smith dispatches jobs to specialized agents and coordinates their work.

| Mode       | Trigger words                       | Checkpoints               | Iterations       |
| ---------- | ----------------------------------- | ------------------------- | ---------------- |
| Partner    | `develop`, `implement it`, `fix it` | 2 (plan approval + merge) | Single pass      |
| Autonomous | `smith`                             | 1 (merge only)            | Minimum 3 cycles |

If both trigger types appear, prefer **Autonomous** mode.

**Plan file:** `PLAN.md` in project root — living document, not committed, removed after merge.

## Shortcut

This skill is triggered when the user's prompt contains `develop`, `implement it`, `fix it`, or `smith`.

## The Team

| Agent               | Role             | Responsibility                                               |
| ------------------- | ---------------- | ------------------------------------------------------------ |
| **agent-smith**     | Leader           | Dispatches jobs, coordinates workflow, manages git lifecycle |
| **proj-ideatender** | Project Owner    | Analyzes project context, produces brief plans               |
| **spec-writer**     | Spec Writer      | Writes technical specs with architecture diagrams            |
| **agent-hale**      | Programmer       | Writes code based on plan and spec                           |
| **agent-ellis**     | Code Reviewer    | Reviews code, finds bugs, reports to ideatender or hale      |
| **frontend-design** | UI Designer      | Designs and implements production-grade frontend interfaces  |
| **git-committer**   | Commit Generator | Generates commit messages                                    |

## How It Works

### Phase 1: Understand and Plan

Invoke `proj-ideatender:proj-ideatender` to analyze the project context and produce a brief plan.

**[Partner]** `proj-ideatender` presents the plan to the **user** for approval. The user may
refine or redirect. Smith waits for the user to confirm before proceeding.

**[Autonomous]** `proj-ideatender` presents the plan to **Smith**. Smith reviews it and proceeds.

Once the plan is approved, Smith writes `PLAN.md`:

```markdown
# PLAN.md

## Idea

<user's original idea>

## Design

<high-level design from proj-ideatender>

## Spec

<reference to spec documents if spec-writer was invoked>

## Units of Work

| #   | Unit | Description | Assignee   | Status  |
| --- | ---- | ----------- | ---------- | ------- |
| 1   | ...  | ...         | agent-hale | pending |

## Planned Commits

| #   | Commit | Description |
| --- | ------ | ----------- |
| 1   | ...    | ...         |

## Iteration Log

| Iteration | Correctness | Completeness | Quality | Test Coverage | Summary |
| --------- | ----------- | ------------ | ------- | ------------- | ------- |
```

### Phase 2: Spec (if needed)

For non-trivial features, invoke `spec-writer:spec-writer` to produce technical specifications.
The spec-writer will collaborate with `proj-ideatender` for context and use `ascii-grapher` for
architecture diagrams and flow charts.

Smith reviews the spec output before proceeding. Skip this phase for simple bug fixes or
small changes.

### Phase 2.5: UI Design (if needed)

For tasks involving frontend/UI work, invoke `frontend-design:frontend-design` to design and
implement the user interface. The frontend-design skill produces production-grade, visually
distinctive code (HTML/CSS/JS, React, Vue, etc.).

Smith should dispatch to frontend-design when:

- The plan includes UI components, pages, or web interfaces
- The user explicitly requests frontend work
- `proj-ideatender`'s plan identifies UI-related units of work

If the `frontend-design` plugin is not installed, **inform the user** that the frontend-design
plugin is required for UI tasks and suggest they install it and reload their plugins before
proceeding.

Smith reviews the frontend-design output before passing it to `agent-hale` for integration
with the rest of the codebase.

### Phase 3: Implement, Review, and Commit

**Before the first commit**, create a feature branch:
`git checkout -b feat/<slugified-3-word-summary>`

For each unit of work:

#### Dispatch to agent-hale

Invoke `agent-hale:agent-hale` with the unit of work, referencing `PLAN.md` and any specs.
Agent Hale writes clean, focused code with proper tests and error handling.

#### Dispatch to agent-ellis

After Hale completes a unit, invoke `agent-ellis:agent-ellis` to review the changes.
Agent Ellis reviews code quality and security, then reports findings:

- **PASS** → proceed to commit
- **WARN** → Smith decides: fix or accept. If fix, re-dispatch to Hale then back to Ellis
- **FAIL** → must fix. Re-dispatch to Hale with Ellis's findings, then re-review

#### Commit

Once Ellis passes, invoke `git-committer:git-committer` for the commit.
Update the unit's Status in `PLAN.md` to `done`.

### Phase 4: Assess [Autonomous mode only]

**[Partner]** Skip — go directly to Phase 6.

After all units complete, Smith self-assesses: review changes (`git log`, `git diff main...HEAD`),
run tests, identify issues. Optionally invoke `agent-ellis` for a full-branch review.

Score (1-10):

| Dimension     | Score | Notes |
| ------------- | ----- | ----- |
| Correctness   |       |       |
| Completeness  |       |       |
| Quality       |       |       |
| Test Coverage |       |       |

Update the Iteration Log in `PLAN.md`.

### Phase 5: Re-Plan and Iterate [Autonomous mode only]

**[Partner]** Skip — go directly to Phase 6.

Invoke `proj-ideatender` to reassess based on current state. Add new units to `PLAN.md`.
Return to **Phase 3**.

**Repeat Phases 3–5 for at least 3 iterations** (honor user-specified count). Stop early if all
scores reach 9+. Each iteration must produce meaningful improvements — no trivial busywork.

### Phase 6: Merge

**[Autonomous]** Show the Iteration Log from `PLAN.md` first.

1. Show `git log --oneline main..HEAD`
2. Invoke `git-committer:git-committer` to generate a merge commit message

**[CHECKPOINT]** Present summary to user. Wait for approval.

After approval: `git checkout main` → `git merge --no-ff <branch>` →
`git branch -d <branch>` → `rm PLAN.md`

If the merge produces conflicts, dispatch to `agent-hale` to resolve them, then invoke
`agent-ellis` to verify the resolution.

### Phase 7: Lessons Learned

Share a brief reflection: what went well, what could improve, surprising findings,
and patterns for future sessions. Append the reflection to `LESSONS.md` in the
`proj-ideatender` cache dir (`~/.claude/projects/<project-path>/memory/`).

## Workflow Overview

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                      Agent Smith (Leader)                               │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ Phase 1: Understand and Plan                                      │  │
│  │  smith ──dispatch──> proj-ideatender ──> brief plan               │  │
│  │  [Partner] ideatender reports to USER                             │  │
│  │  [Autonomous] ideatender reports to SMITH                         │  │
│  └──────────────────────────┬────────────────────────────────────────┘  │
│                              │                                          │
│                              ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ Phase 2: Spec (if needed)                                         │  │
│  │  smith ──dispatch──> spec-writer ──> technical spec + diagrams    │  │
│  │                      (uses proj-ideatender + ascii-grapher)       │  │
│  └──────────────────────────┬────────────────────────────────────────┘  │
│                              │                                          │
│                              ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ Phase 2.5: UI Design (if needed)                                  │  │
│  │  smith ──dispatch──> frontend-design ──> UI code + assets         │  │
│  │  (hint user to install plugin if missing)                         │  │
│  └──────────────────────────┬────────────────────────────────────────┘  │
│                              │                                          │
│                              ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ Phase 3: Implement, Review, and Commit                            │  │
│  │  For each unit of work:                                           │  │
│  │    smith ──dispatch──> agent-hale (code)                          │  │
│  │          ──dispatch──> agent-ellis (review)                       │  │
│  │          ──dispatch──> git-committer (commit)                     │  │
│  │                                                                   │  │
│  │    ┌───────────┐     ┌───────────┐     ┌──────────────┐           │  │
│  │    │ agent-hale│────>│agent-ellis│────>│ git-committer│           │  │
│  │    │ (code)    │<────│ (review)  │     │ (commit)     │           │  │
│  │    └───────────┘ fix └───────────┘     └──────────────┘           │  │
│  └──────────────────────────┬────────────────────────────────────────┘  │
│                              │                                          │
│               ┌──────────────┴──────────────┐                           │
│               │                             │                           │
│          [Partner]                    [Autonomous]                      │
│               │                             │                           │
│               ▼                             ▼                           │
│  ┌──────────────────┐      ┌─────────────────────────────────────┐      │
│  │ Phase 6: Merge   │      │ Phase 4: Assess                     │      │
│  │  CHECKPOINT      │      │  Score correctness, completeness,   │      │
│  │  merge + cleanup │      │  quality, test coverage             │      │
│  └────────┬─────────┘      └──────────────┬──────────────────────┘      │
│           │                                │                            │
│           │                                ▼                            │
│           │               ┌─────────────────────────────────────┐       │
│           │               │ Phase 5: Re-Plan and Iterate        │       │
│           │               │  proj-ideatender reassess           │       │
│           │               │  Add new units ──> loop to Phase 3  │       │
│           │               │  (min 3 iterations, stop at 9+)     │       │
│           │               └──────────────┬──────────────────────┘       │
│           │                              │                              │
│           │                              ▼                              │
│           │               ┌─────────────────────────────────────┐       │
│           │               │ Phase 6: Merge                      │       │
│           │               │  Show iteration log, CHECKPOINT     │       │
│           │               │  merge + cleanup                    │       │
│           │               └──────────────┬──────────────────────┘       │
│           │                              │                              │
│           └──────────┬───────────────────┘                              │
│                      ▼                                                  │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ Phase 7: Lessons Learned                                          │  │
│  │  Reflect ──> append to LESSONS.md                                 │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Team Coordination

**Smith's dispatch contracts:**

- Invokes `proj-ideatender:proj-ideatender` in Phase 1 for project analysis and brief planning.
  In Partner mode, ideatender reports to user. In Autonomous mode, ideatender reports to Smith.
- Invokes `spec-writer:spec-writer` in Phase 2 for technical specifications. The spec-writer
  collaborates with `proj-ideatender` for context and `ascii-grapher` for diagrams.
- Invokes `frontend-design:frontend-design` in Phase 2.5 for UI/frontend work. Reviews the
  output before passing to Hale for integration. If the plugin is not installed, hints the user
  to install and reload it.
- Invokes `agent-hale:agent-hale` in Phase 3 for code implementation. Hale receives the unit
  of work, plan, and spec references.
- Invokes `agent-ellis:agent-ellis` in Phase 3 after each unit. Acts on the `__REVIEW_VERDICT__`
  block: re-dispatches to Hale on FAIL, decides on WARN, proceeds on PASS.
- Invokes `git-committer:git-committer` in Phase 3 for commit messages. The git-committer skips
  its own review gate when called by agent-smith (already reviewed by Ellis).
- Invokes `ascii-grapher:ascii-grapher` via spec-writer when documentation needs diagrams.

**Reporting chain:**

- `agent-hale` reports completed work to Smith
- `agent-ellis` reports review findings to Smith, who may forward to `proj-ideatender` (for
  design-level issues) or back to `agent-hale` (for implementation fixes)
- `proj-ideatender` reports plans to Smith (autonomous) or user (partner)
