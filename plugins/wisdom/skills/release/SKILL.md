---
name: release
description: Bumps the version, tags and publishes a release once the user has asked for one. Use only when a finished change is to be shipped as a version.
license: MIT
metadata:
  shortcut: "release it"
---

# Release

Cut a version. Every step that leaves the machine — push, tag, publish — needs the user's
explicit yes in this conversation; a release is never inferred from finished work.

## Steps

1. **Gate.** On the release branch (usually `main`), clean worktree, tests green (the `test`
   skill). Any failure: stop and report — diagnosing it is not this skill's job.
2. **Version.** Read the current one from the tag list and the version files the project
   keeps (`package.json`, `pyproject.toml`, `Cargo.toml`, `plugin.json`, …). Propose the
   next by semver from the commits since the last tag: breaking → major, `feat` → minor,
   otherwise patch. Ask the user to confirm the number.
3. **Bump** every version location to the same number, and update the CHANGELOG with
   `wisdom:changelog` if the project keeps one. Commit as `chore(release): v<version>`.
4. **Confirm, then tag.** Show the commit, the tag name and the remote; wait for a yes.
   Then `git tag -a v<version> -m "v<version>"` and push the branch and the tag.
5. **Publish** only what the project already publishes (`gh release create`, a registry, an
   image), with the changelog entries as notes. A deploy the project has no pipeline for is
   out of scope — say so.
6. **Report** the version, tag, and every place it was published.

## Rules

- Never move or delete an existing tag, never force-push, never skip hooks.
- Push to the remote the user names; with several remotes and no name, ask.
- A failed step stops the release where it is. Report what was done and what was not.
