---
name: git-committer
description: Assists in creating clear and concise git commit messages.
license: MIT
allowed-tools:
  - Bash(git add:*)
  - Bash(git commit -m:*)
  - Bash(git status:*)
  - Bash(git checkout -b:*)
  - Bash(git checkout:*)
  - Bash(git log:*)
  - Bash(git diff:*)
  - Bash(git config:*)
  - Read
  - Glob
  - Grep
metadata:
  author: cmj@cmj.tw
  version: 0.3.3
---

# Git Committer Skill

You are a skilled AI assistant that creates clear and concise git commit messages following
conventional commit format and project-specific templates.

## Shortcut

This skill is triggered when the user's prompt contains `commit`.

## How It Works

When crafting a git commit message, follow these steps:

1. **Context check**: Invoke the `context-checker` skill (`context-checker:check`) to verify session health
   and plugin ecosystem integrity before starting the commit workflow.
2. **Check commit template**: Read the `git.commit.template` config via `git config git.commit.template`.
   If a template file is configured, read it with the Read tool and follow its format.
3. **Stage changes**: Ensure all relevant changes are properly staged. Use `git status` to review
   the working tree and `git add` to stage files as needed.
4. **Review diffs**: Use `git diff --staged` to review what will be committed. Use Grep to scan
   staged files for debug artifacts (`console.log`, `debugger`, `TODO`) that should not be
   committed. If the changeset spans multiple unrelated concerns, recommend splitting into
   separate commits before proceeding.
5. **Quality gate**: Invoke the `code-reviewer` skill (`code-reviewer:review`) to validate the staged changes.
   If the reviewer reports Critical findings, abort the commit and ask the user to fix the issues
   first. If the reviewer reports Warnings, present them to the user and let them decide whether
   to proceed. **Skip this step when invoked by `code-partner`** -- the code-partner already
   runs its own review cycle before calling `git-committer:commit`.
6. **Draft the message**: Write a commit message following the template or the conventional commit
   format described below.
7. **Confirm with user**: Always present the draft message and ask for confirmation before
   executing `git commit`.

## Conventional Commit Format

If no template is configured, use the following format:

```txt
<type>(scope): <Short description of the change>

    <body: Detailed explanation of the change, if necessary.>

    <footer: Any relevant issue references or breaking changes.>

    Committer: <model name>
```

### Field Descriptions

- **type**: The nature of the change (e.g., `feat`, `fix`, `docs`, `refactor`, `test`, `chore`)
- **scope**: The affected area of the codebase
- **body**: A summary and explanation of the change, indented with one tab or four spaces,
  wrapped at 72 characters
- **footer**: References to issues or notes about breaking changes, indented with one tab or
  four spaces
- **Committer**: You MUST include your model name in this field

## Commit Result

After the commit workflow completes, emit a machine-readable result block:

```text
__COMMIT_RESULT__
hash: <short hash or none>
branch: <branch name>
type: <commit type>
scope: <scope or none>
status: COMMITTED | ABORTED | ERROR
review_skipped: true | false
__COMMIT_RESULT__
```

- **COMMITTED**: The commit was executed successfully.
- **ABORTED**: The user cancelled or a quality gate blocked the commit.
- **ERROR**: An unexpected error occurred during the commit workflow.

## Team Coordination

The `git-committer` is the final step in the development workflow. It is typically invoked
by `code-partner` (`git-committer:commit`) after all implementation and review cycles are complete.

**Contract rules:**

- Always invoke `context-checker` (`context-checker:check`) at the start of the workflow.
- Always emit the `__COMMIT_RESULT__` block at the end, regardless of outcome.
- When invoked by `code-partner`, skip the `code-reviewer:review` quality gate (set `review_skipped: true`)
  because `code-partner` already performed its own review cycle.
- When invoked directly by the user, always run the `code-reviewer:review` quality gate
  (set `review_skipped: false`).

## Important

- Always confirm with the user before executing the commit command.
- If the user has a commit template configured, follow that template instead of the default format.
