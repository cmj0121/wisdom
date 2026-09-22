---
name: docs
description: Writes or updates user-facing documentation — READMEs, guides, API references — to match the code. Use when a change needs documenting or docs went stale.
license: MIT
metadata:
  shortcut: "document it"
---

# Docs

Make the documentation match the code. Write for the reader who will use the thing, not for
the one who built it.

## Steps

1. **Find the change.** The caller's scope, else `git diff main...HEAD`. List the
   user-visible effects: new or changed commands, flags, APIs, config, behaviour, removals.
2. **Find the docs it affects:** README, `docs/`, API references, examples, help text,
   CHANGELOG pointers. Grep for the old names — stale mentions hide outside the obvious file.
3. **Update in place,** following each file's existing structure, tone and language. When a
   project ships the same doc in more than one language, update every copy.
4. **Verify** each example and command against the code: flags exist, outputs match, paths
   resolve. Run a command when running it is safe and cheap.
5. **Report** the files changed, one line each, and anything you could not verify.

## Writing rules

- Lead with what the reader can do, then how. One idea per paragraph.
- Show a working example before explaining the options.
- Use the code's exact names; never paraphrase an identifier, flag or path.
- Document behaviour, not implementation — internals belong in code and commits.
- Delete what is no longer true rather than marking it deprecated, unless users still need
  a migration path; then write that path.
- A breaking change gets a short migration note: before, after, and the steps between.

Release notes are `wisdom:changelog`'s job; a design record is `wisdom:spec`'s.
