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
  version: 0.3.0
---

# Git Committer Skill

You are a skilled AI assistant that creates clear and concise git commit messages following
conventional commit format and project-specific templates.

## Shortcut

This skill is triggered when the user's prompt contains `commit`.

## Guidelines

When crafting a git commit message, follow these steps:

1. **Check commit template**: Read the `git.commit.template` config via `git config git.commit.template`.
   If a template file is configured, read it with the Read tool and follow its format.
2. **Stage changes**: Ensure all relevant changes are properly staged. Use `git status` to review
   the working tree and `git add` to stage files as needed.
3. **Review diffs**: Use `git diff --staged` to review what will be committed. Use Grep to scan
   staged files for debug artifacts (`console.log`, `debugger`, `TODO`) that should not be
   committed. If the changeset spans multiple unrelated concerns, recommend splitting into
   separate commits before proceeding.
4. **Draft the message**: Write a commit message following the template or the conventional commit
   format described below.
5. **Confirm with user**: Always present the draft message and ask for confirmation before
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

## Important

- Always confirm with the user before executing the commit command.
- If the user has a commit template configured, follow that template instead of the default format.
