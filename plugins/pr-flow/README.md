# PR Flow Plugin

> Walks a pull request from its issue to merge-ready — verifies the originating issue exists, checks
> the diff against the issue body for missing and over-engineered parts, and works each reviewer
> comment test-first within issue scope. Use when the user asks to open a PR, resolve review
> comments, or check a PR against its issue; merging stays with the user.

A utility skill for the pull-request lifecycle. It gates a PR on the issue it serves, aligns
the diff with what that issue asked for, and works reviewer comments one at a time —
test-first when behaviour changes, and kept within issue scope. Merging stays with you.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install pr-flow
```

## How It Works

1. **Issue gate** — find and verify the originating issue; none found → propose one and
   create it only after an explicit yes, or record `Issue: —` if you decline
2. **Alignment** — compare the diff with the issue body and settle two lists with you,
   missing parts and over-engineered parts, before the PR is opened or edited
3. **Reviewer loop** — take each reviewer item in turn: re-check issue scope, write the test
   before the fix when behaviour changes, and challenge out-of-scope items with you first,
   then the reviewer

Every write to GitHub — creating an issue, opening or editing the PR, posting a reviewer
comment — is a checkpoint that waits for your approval. The skill never merges.

## Usage

### Magic Words

- `open pr` → Walk the current branch through the issue gate and alignment, then open the PR
- `resolve pr` → Work the open reviewer comments on the PR, one item at a time
- `pr-flow` → Run the full flow from issue gate to merge-ready

Note that the words open pr also occur in ordinary prose — a sentence about the open PR
list, for instance — so a stray trigger is possible; the skill reports the issue line first,
which makes an unintended start easy to spot and stop.

## When To Use Which

Use `pr-flow` when the work ships as a GitHub pull request with reviewers to answer. Use
`agent-smith` when the work is planned and merged locally without a PR — the two do not
overlap, and `pr-flow` hands back to you when a task turns out to need a plan rather than a PR.

When `tenth-man`, `agent-hale` and `agent-ellis` are installed, `pr-flow` invokes them for
the over-engineering check, test-first fixes and fix verification. When they are not, it
does the same steps itself.

## Requirements

GitHub only. The `gh` CLI must be installed and authenticated (`gh auth status`) for the
repository the PR belongs to.

## License

MIT
