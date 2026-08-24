---
name: pr-flow
description: Walks a pull request from its issue to merge-ready — verifies the originating issue exists, checks the diff against the issue body for missing and over-engineered parts, and works each reviewer comment test-first within issue scope. Use when the user asks to open a PR, resolve review comments, or check a PR against its issue; merging stays with the user.
license: MIT
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(git status:*)
  - Bash(git diff:*)
  - Bash(git log:*)
  - Bash(git branch:*)
  - Bash(gh issue view:*)
  - Bash(gh pr view:*)
  - Bash(gh pr diff:*)
  - Bash(gh pr checks:*)
  - Bash(gh pr list:*)
metadata:
  author: cmj@cmj.tw
  version: "2.1.0"
  shortcut: "open pr, resolve pr, pr-flow"
---

# PR Flow Skill

Gates a pull request on the issue it serves. Three phases: find and verify the originating
issue (or get permission to create one), align the diff with the issue body before the PR is
opened or updated, then work each reviewer comment in turn — test first when behaviour
changes, challenged when it leaves issue scope. GitHub only, through `gh`. Every write to the
forge is a checkpoint: the pre-authorised tools above are read-only, so `gh issue create`,
`gh pr create`, `gh pr edit` and `gh pr comment` each pass through the permission prompt, and
the skill never runs `gh pr merge`.

## Shortcut

This skill is triggered when the user's prompt contains `open pr`, `resolve pr`, or `pr-flow`.

## Phase 1: Issue Gate

Establish which issue this PR serves before reading a line of the diff.

1. Look for a ref, in this order, and stop at the first hit:
   - the user's prompt (`#123`, an issue URL)
   - the branch name — `git branch --show-current` — treated as a **hint**, never as a ref
   - an existing PR — `gh pr view --json number,title,body,closingIssuesReferences`; take
     `closingIssuesReferences` first and parse the body only when it is empty
2. Verify every candidate with `gh issue view <n> --json number,title,body,state,url`. A
   number that does not resolve, or resolves to an issue about something else, is not a ref.
   A branch called `fix-123` proves nothing until `gh issue view 123` describes this work.
3. No verified ref → **checkpoint**. Draft a title and body from the diff
   (`git diff <base>...HEAD --stat`, `git log <base>..HEAD --oneline`, where `<base>` is
   the base branch — `main` unless the repo says otherwise), show both, and ask whether to
   create the issue. Run `gh issue create` only after an explicit yes.
4. The user declines → the ref is `—`. Say so in one line, write "Issue: —" in the PR body
   later, and continue. A missing issue is a fact to record, not a reason to stall.
5. Never invent a ref. No plausible number from a branch name, a commit message, or the diff
   is ever written as `#n` — the rules `agent-ross:agent-ross` follows for commit footers
   apply to the PR body too.

Report the outcome as one line: `Issue: #123 — <title>` or `Issue: —`.

## Phase 2: Alignment

Compare what the branch does with what the issue asked for. Skip when the ref is `—` and
the user has nothing else to compare against; say so and go straight to opening the PR.

1. Read the diff and the issue body from Phase 1. Before a PR exists: `git diff <base>...HEAD`
   with `<base>` the base branch (`main` unless the repo says otherwise). After one exists:
   `gh pr diff <n>`, and take the base from `gh pr view <n> --json baseRefName` rather than
   assuming it.
2. Build two lists:
   - **Missing** — things the issue asks for that the diff does not deliver
   - **Over-engineered** — things the diff delivers that the issue does not ask for: extra
     options, abstractions with one caller, speculative generality, unrelated cleanups
3. When `tenth-man:tenth-man` is installed, invoke it on the diff-versus-issue comparison
   and fold its findings into the second list. Not installed → apply the same test directly:
   for each addition, name the sentence in the issue that requires it, or list it.
4. Present both lists to the user one item at a time and settle each: keep, cut, defer to a
   new issue, or amend the issue. Both lists must be settled — empty counts — before the
   next step.
5. **Checkpoint.** Draft the PR title and body — what changed, why, `Closes #123` or
   `Issue: —` — show the draft, and only after approval run `gh pr create` (no PR yet) or
   `gh pr edit <n>` (PR exists). Reflect any cuts from step 4 in the code before opening.

## Phase 3: Reviewer Loop

Work reviewer feedback item by item, never as one batch.

1. Collect the open items from three sources, then list them numbered and take them in order:
   - top-level reviews and conversation comments — `gh pr view <n> --json reviews,comments`
   - inline review threads (the line-anchored requested changes, which `gh pr view` does
     not return) — `gh api repos/{owner}/{repo}/pulls/<n>/comments`, a GET. `gh api` is
     deliberately **not** pre-authorised, so this read passes through the permission prompt
     exactly as the writes do; the skill never runs `gh api` with `-X`/`--method` or
     `-f`/`-F` fields — reads only
   - failing checks — `gh pr checks <n>`, each failure an item of its own
2. For each item, before anything else, **re-check issue scope** against the issue body from
   Phase 1. This check runs per item, not once per round — a review that is in scope on its
   first three comments can leave it on the fourth. Classify the item:
   - **In scope** — the issue asks for it or it corrects a defect in delivering it
   - **Out of scope** — it asks for work the issue does not cover
   - **Added abstraction** — it asks for a layer, option or generalisation the issue does not
     need to be delivered
3. In-scope item → comply. Decide whether it **changes behaviour**:
   - Changes behaviour (a different output, a new code path, a fixed defect): test first.
     When `agent-hale:agent-hale` is installed, dispatch with the explicit instruction
     "write the failing test before the fix, then make it pass". Not installed → do the same
     directly: failing test, minimal fix, green, no regressions.
   - Does not change behaviour (rename, comment, formatting, docs): make the change and state
     in one line why there is no test — "rename only, covered by the existing suite" — rather
     than leaving the absence unexplained.
   - When `agent-ellis:agent-ellis` is installed, have it verify the fix against the item's
     wording before replying. Not installed → run the affected tests and quote the result.
4. Out-of-scope or added-abstraction item → challenge, in this order:
   - **User first.** Show the item, the sentence in the issue it exceeds (or the absence of
     one), and the options: decline with a reason, do it here anyway, or split it to a new
     issue. Settle it with the user before any word goes to the reviewer.
   - **Reviewer second — checkpoint.** Draft the reply: what the issue covers, why this item
     falls outside it, and what is proposed instead. Show the draft. Post it with
     `gh pr comment <n> --body` only after the user approves the exact text; edit and
     re-show on request.
   - Comply when the challenge does not hold. A reviewer asking for a test, a name that
     matches the codebase, or an edge case the issue implies is in scope, not a challenge.
5. Every reply to a reviewer — agreement, question, or pushback — is drafted, shown, and
   posted only after approval. The skill never speaks to a reviewer on its own.
6. After the last item, summarise: items complied with, items declined (with the reply
   posted), tests added, and the `gh pr checks <n>` state. Stop there — merge is the user's.

## Checkpoints

Every point where the skill stops and waits for the user. None may be skipped or assumed.

| #   | Where          | What waits for the user                                                               |
| --- | -------------- | ------------------------------------------------------------------------------------- |
| 1   | Phase 1 step 3 | Creating an issue — `gh issue create` runs only after an explicit yes                 |
| 2   | Phase 2 step 4 | Settling each missing or over-engineered item                                         |
| 3   | Phase 2 step 5 | Opening or editing the PR — `gh pr create` / `gh pr edit` after the draft is approved |
| 4   | Phase 3 step 4 | Declining or narrowing a reviewer item — the user decides before the reviewer hears   |
| 5   | Phase 3 step 5 | Posting any reviewer reply — `gh pr comment` only with the approved text              |
| 6   | After Phase 3  | Merging — the skill never runs `gh pr merge`; the user does                           |

The `allowed-tools` list enforces the mechanical half of this table: nothing that writes to
GitHub is pre-authorised, so each of those commands also passes through the permission prompt.
`gh api` is left out on the same principle even for its one read (Phase 3 step 1) — it is the
one command that could write, so it is never pre-authorised and is used as a GET only.

## Team Coordination

The skill invokes these when installed and does the same work itself when they are not.

- `tenth-man:tenth-man` — Phase 2, the over-engineered list. Not installed: apply the same
  test directly; each addition must trace to a sentence in the issue.
- `agent-hale:agent-hale` — Phase 3, behaviour-changing fixes, dispatched with the explicit
  test-first instruction. Not installed: write the failing test, then the minimal fix, directly.
- `agent-ellis:agent-ellis` — Phase 3, verifying a fix against the reviewer's wording. Not
  installed: run the affected tests and quote the result.

The same rules apply either way: test before fix when behaviour changes, a stated reason when
it does not, and a challenge only when an item exceeds scope or adds unneeded abstraction.
The skill does not invoke `agent-smith:agent-smith`; when the work turns out to need a plan
rather than a PR, say so and hand back to the user.

## Output Style

Everything addressed to the user follows `briefing:briefing`: the result first — the issue
line, the two alignment lists, the numbered reviewer items — then one numbered topic at a
time, with detail only where asked. Reviewer replies are drafted in full, since they leave the
conversation, but are still shown before they are posted.
