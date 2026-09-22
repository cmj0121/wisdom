---
name: commit
description: Writes a conventional commit message for the staged change and commits it. Use when a finished change is ready to record in git.
license: MIT
metadata:
  shortcut: "commit it"
---

# Commit

Write the message for what is staged and commit it. Nothing else: no push, no tag.

## Steps

1. `git diff --cached --stat`, then the staged diff itself. Nothing staged: ask what to
   stage — never `git add -A` on your own.
2. If the repo has a commit template (`git config commit.template`) or a visible convention
   in `git log -10`, follow it. Otherwise use the format below.
3. Commit. If a hook fails, report its output and stop — never `--no-verify`, never amend a
   commit that is not yours.
4. Report the short hash and subject.

## Format

```text
<type>(<scope>): <subject>

<body>

<footer>
```

- `type`: feat, fix, docs, test, refactor, perf, build, chore.
- `subject`: imperative, ≤ 72 characters, no trailing period.
- `body`: why the change was made and what it trades off, wrapped at 72. Skip it when the
  subject says everything.
- `footer`: `Refs: <issue>` only when the work came from an issue; `Closes: <issue>` only
  on the commit that finishes it. Never infer an issue from a branch name.
