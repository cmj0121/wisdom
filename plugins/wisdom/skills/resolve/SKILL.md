---
name: resolve
description: Works through a pull request's review comments one at a time, test first when behaviour changes. Use when a PR has feedback to address. Never merges.
license: MIT
allowed-tools:
  - Bash(gh pr view:*)
  - Bash(gh pr diff:*)
metadata:
  shortcut: "resolve pr"
---

# Resolve

Address a PR's open review feedback, item by item. GitHub through `gh`. Never merge.

## Steps

1. **Find the PR:** the number in the prompt, else `gh pr view --json number,url` for the
   current branch. None: stop and say so.
2. **Collect open items** from both sources, then number them:
   - reviews and comments: `gh pr view <n> --json reviews,comments`
   - inline threads: `gh api repos/{owner}/{repo}/pulls/<n>/comments`
     Skip resolved threads, outdated ones already addressed, and approvals with no request.
3. **For each item, in order,** decide one of:
   - **Fix** — behaviour changes: failing test first, then the fix, then green.
     Wording, naming or docs: just change it.
   - **Push back** — the request is wrong or out of the PR's scope: draft a reply giving
     the reason, and offer a follow-up issue for out-of-scope work.
   - **Ask** — the request is ambiguous: ask the user, not the reviewer.
     Show the decision and the change for each item before moving on.
4. **Commit** each fix on its own (`wisdom:commit`), referencing the comment it answers.
5. **Reply and push** only after the user approves: post the replies
   (`gh pr comment` or a thread reply) and push the branch.
6. **Report** a table: item, decision, commit or reply.

## Rules

- Every write to GitHub — a reply, a push — is a checkpoint.
- Never resolve a thread on the reviewer's behalf; replying is enough.
- Never `gh pr merge`.
