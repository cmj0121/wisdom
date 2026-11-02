---
name: history
description: Reshapes a branch's unpushed commits into bump, docs, feats with folded fixes, and one test commit. Use on a finished feature branch before merging.
license: MIT
---

# History

Rewrite the current branch, and only it, into linear history. Input: base ref, default `main`.

## Target order

0. The version bump, if any: a version check may reject an earlier commit touching the package.
1. `docs` commits, when any exist.
2. One commit per purpose: each `feat`, `refactor`, `perf`, `build`, `chore`, minus test files.
3. `fix` commits folded into the commit that introduced what they fix. One that cannot fold
   stays as its own `fix` commit, directly after the feat group.
4. At most one `test` commit, last. Merge commits disappear.

## Preflight

Check in order; stop with the line shown. Never push. Commit or stash nothing for the user.

1. Base ref missing, or HEAD detached: `ABORTED`.
2. `git status --porcelain --untracked-files=no` shows anything: `ABORTED`.
3. `git rev-list --count <base>..HEAD` is 0, or differs from the same count with `--not --remotes`
   (a commit is already on a remote; never force-push): `UNCHANGED`.

Then record `start=$(git rev-parse HEAD)` and `mb=$(git merge-base <base> HEAD)`.

## Classify

List `git rev-list --reverse --topo-order --no-merges "$mb..$start"`, with each commit's
paths from `git diff-tree --no-commit-id --name-only -r --no-renames <sha>`. Files, whole:

- **Test-only:** a file holding nothing but tests or their fixtures.
- **Doc-only:** a file written for readers. Markdown the product ships or loads (a skill body,
  a prompt, a template) is code.
- **Code:** everything else. Inline tests and mixed files stay here; they do not block shaping.

Commits, by their code paths and subject:

- **Bump:** only moves a version.
- **Fix:** a `fix` subject. It folds into commit X when every code path it touches was last
  changed, among earlier non-fix commits, by that one X. Otherwise it stays on its own.
- **Purpose:** any other commit with code paths left, under its own message.

## Rebuild

Run this section in a temporary worktree, so the checkout and branch do not move. Take each
file from a commit instead of replaying its patch, so a reorder cannot conflict. Cwd, variables
and functions reset between Bash calls: re-establish `wt`, `start`, `mb`, `take` and the `cd` in each:

```bash
wt=$(mktemp -d); git worktree add -q --detach "$wt" "$mb"; cd "$wt"
take() { rev=$1; shift; for p in "$@"; do
  if git cat-file -e "$rev:$p" 2>/dev/null; then git checkout -q "$rev" -- "$p"
  else git rm -qf --ignore-unmatch -- "$p"; fi; done; }
```

Build in order, skipping empty commits; `git commit -C <sha>` keeps the author and date.

**Footers:** a commit that disappears (folded, skipped, or all its paths moved) hands its
`Refs:`/`Closes:` lines to the commit now holding its paths; a merge or an empty commit hands
them to the last commit built. `-C` cannot add lines, so a commit receiving any uses:

```bash
msg=$(mktemp); git log -1 --format=%B <sha> | git interpret-trailers --trailer "Refs: #1" >"$msg"
git commit -F "$msg" --author="$(git log -1 --format='%an <%ae>' <sha>)" \
  --date="$(git log -1 --format=%aI <sha>)"
```

1. **Bump:** `take <sha> <its paths>`, then commit.
2. **Docs:** per `docs` commit, `take <sha> <its doc-only paths>`, then commit. Before the last,
   also `take "$start" <all doc-only paths not moved>`; with no `docs` commit, those form a new `docs:`.
3. **Purposes**, in original order: `take <sha> <its code paths>`, then
   `take <fix> <its code paths>` for each fix folding into it, in order, then commit.
4. **Fixes left**, in order: `take <fix> <its code paths no later purpose or folded fix changes>`, then commit.
5. **Tests:** `take "$start" <all test-only paths>`, then commit: `-C` when one `test` commit
   holds them all, otherwise a new `test:` message.

Hooks run on every commit. Never `--no-verify`. A hook failure on a docs commit may be a check
tying a doc to code (a README row naming a skill the same branch adds): move the rejected file
whole into the last feat that needs it, `take HEAD <file>` now and `take "$start" <file>` in
that feat, its footers with it, and retry once. Any other hook failure, a failed retry, a conflict
or failed step aborts: in the checkout, `git worktree remove --force "$wt"`; report `ABORTED`, branch unmoved.

## Verify

1. With `new=$(git -C "$wt" rev-parse HEAD)`, `git diff --quiet "$start" "$new"` must pass, or
   abort. This empty diff proves reviews and the suite hold: do not re-run them or test commits.
2. `git log --format=%B <range> | grep -E '^(Refs|Closes)[: ]' | sort -u` must match for
   `$mb..$start` and `$mb..$new`; otherwise abort.
3. If `git log --format=%T "$mb..$new"` equals the same list for `$mb..$start`, the branch was
   already shaped: `git worktree remove --force "$wt"` and report `UNCHANGED`.
4. In the checkout, HEAD must still be `$start`; otherwise abort. Then `git reset --soft "$new"`
   there (same tree, so index and files do not change), then `git worktree remove --force "$wt"`.

## Result

Print `git log --oneline "$mb..HEAD"` or what stopped the run, then end in exactly one line:

```text
HISTORY: SHAPED <n> commits | UNCHANGED <reason> | ABORTED <reason>
```
