---
name: history
description: Reshapes a branch's unpushed commits into bump, docs, feats with folded fixes, and one test commit. Use on a finished feature branch before merging.
license: MIT
---

# History

Rewrite the current branch, and only it, into linear history. Input: base ref, default `main`.
What each file and commit is for takes judgement, so you classify; everything mechanical
(preflight, rebuild, verify, the reset, the result line) is
[`scripts/reshape.py`](scripts/reshape.py), so it cannot drift between runs.

The target order: bump, `docs`, one commit per purpose with its fixes folded in, fixes that
cannot fold, at most one `test` commit last. Merge commits disappear.

## Classify

```bash
start=$(git rev-parse HEAD); mb=$(git merge-base <base> HEAD)
git rev-list --reverse --topo-order --no-merges "$mb..$start"
git diff-tree --no-commit-id --name-only -r --no-renames <sha>   # for each sha
```

Files, whole:

- **Test-only:** a file holding nothing but tests or their fixtures.
- **Doc-only:** a file written for readers. Markdown the product ships or loads (a skill body,
  a prompt, a template) is code.
- **Code:** everything else. Inline tests and mixed files stay here; they do not block shaping.

Commits, by their code paths and subject:

- **`bump`:** only moves a version.
- **`fix`:** a `fix` subject. It folds into commit X when every code path it touches was last
  changed, among earlier non-fix commits, by that one X, and X is a `purpose`. Otherwise
  `fold_into` is null.
- **`docs`** or **`test`:** a commit of that type with no code paths.
- **`purpose`:** any other commit, under its own message.

## Run

Write the manifest to a `mktemp` file, every non-merge commit once, paths from the repo root:

```json
{
  "base": "main",
  "start": "<sha>",
  "docs": ["every doc-only path the branch touches"],
  "tests": ["every test-only path the branch touches"],
  "commits": [
    {
      "sha": "<full sha>",
      "kind": "bump|docs|purpose|fix|test",
      "fold_into": null
    }
  ]
}
```

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/reshape.py" "$manifest"
```

If a command above fails (no base ref, detached HEAD), still write what you have and run the
script: it decides. Do not rebuild or verify by hand, and do not re-run reviews or the suite
after `SHAPED`: the script proved the tree identical.

On `ABORTED` stop and report; never push, stash, commit for the user or use `--no-verify`.

## Result

Relay the script's output. Its last line is the result, exactly one of:

```text
HISTORY: SHAPED <n> commits | UNCHANGED <reason> | ABORTED <reason>
```
