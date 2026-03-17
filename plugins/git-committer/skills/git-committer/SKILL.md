---
name: git-committer
description: Assists in creating clear and concise git commit messages.
license: MIT
allowed-tools:
  - Bash(git add:*)
  - Bash(git commit -m:*)
  - Bash(git status:*)
  - Bash(git log:*)
  - Bash(git diff:*)
  - Bash(git config:*)
  - Read
metadata:
  author: cmj@cmj.tw
  version: 0.8.1
---

# Git Committer Skill

## Shortcut

This skill is triggered when the user's prompt contains `commit it`.

### Phase 1: Check the commit template

Check `.git/COMMIT_TEMPLATE` or `git config commit.template`. Follow the project template if it exists;
otherwise fall back to the conventional commit format below.

### Phase 2: Analyze the changes

Run `git status` and `git diff --cached` to review staged changes. If there are no staged
changes, inform the user and stop — do not create an empty commit. Classify changes using
the project template categories or conventional commit types (`feat`, `fix`, `docs`,
`refactor`, `test`, `chore`). Identify the scope (affected module/component).

### Phase 3: Generate the commit message

Generate a commit message following the template or conventional format. Include a short description,
optional body, and footer with issue references or breaking changes.

### Phase 4: Merged Commit Message

For merge commits, summarize commit messages from both branches into a single message reflecting the
combined changes. Return the message to the caller — the orchestrator (e.g., `agent-smith`) executes
the actual merge and branch cleanup.

## Conventional Commit Format

If no template is configured, use the following format. Indent body/itemize/footer 4 spaces, wrap at 72 chars.

```txt
<type>(scope): <Short description of the change>

    <body: Detailed explanation of the change, if necessary.>
    <itemize: If the change includes multiple parts, list them here with bullet points.>

    <footer: Any relevant issue references or breaking changes, listed here.>

    Committer: <model name>
```

## Team Coordination

**Contract rules:**

- When invoked by `agent-smith`, skip `agent-ellis:agent-ellis` quality gate.
- When invoked directly by the user, always run `agent-ellis:agent-ellis` quality gate.
