---
name: changelog
description: Generates changelog entries from git history, grouped by change type. Use when a release needs notes or the CHANGELOG has fallen behind.
license: MIT
metadata:
  shortcut: "gen changelog"
---

# Changelog

Turn a range of commits into changelog entries. Write entries — do not restructure the rest
of the CHANGELOG.

## Steps

1. **Pick the range:** the caller's, else the latest tag to `HEAD`
   (`git describe --tags --abbrev=0`), else the whole history.
2. **Read** `git log <range> --no-merges --format='%h %s'`, and a commit's body only when
   its subject does not say what changed for a user.
3. **Group** by conventional type. Drop what users never see — `test`, `chore`, `ci`,
   `style`, refactors with no behaviour change — unless the caller asks for everything.
4. **Rewrite** each kept subject for a user: what changed for them, in the past tense, one
   line, with the short hash. Merge commits that describe one change.
5. **Write** into `CHANGELOG.md` under an `Unreleased` heading (or the version the caller
   names), following the file's existing format. No CHANGELOG exists: print the entries.

## Groups

| Heading  | From                                      |
| -------- | ----------------------------------------- |
| Breaking | `!` after the type, or `BREAKING CHANGE:` |
| Added    | `feat`                                    |
| Fixed    | `fix`                                     |
| Changed  | `perf`, behaviour-changing `refactor`     |
| Docs     | `docs`, only when user-facing             |

Breaking always comes first and says what the user must do. A non-conventional subject is
placed by what the commit does, never dropped for its format.
