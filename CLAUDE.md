# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

Wisdom is a Claude Code plugin marketplace shipping one plugin, `wisdom`: single-purpose
skills written as Markdown (`SKILL.md`) with YAML frontmatter, not as code. `smith` is the
entry point and coordinates the rest. `README.md` is the roster and the design; keep
`README.zh-TW.md` in step with it.

## Layout

```text
.claude-plugin/marketplace.json     # registers the wisdom plugin
plugins/wisdom/
├── .claude-plugin/plugin.json
├── hooks/                          # lingua's SessionStart hook
└── skills/<name>/
    ├── SKILL.md
    └── references/                 # optional, read only when the body says so
scripts/                            # the checks
```

## Writing a skill

- **One purpose.** A skill that needs a second job calls the skill that owns it, as
  `wisdom:<name>`. Name it after its purpose, a verb or a noun, never a persona.
- **Frontmatter:** `name` (matches the directory), `description`, `license`, optional
  `allowed-tools` (a YAML list — a grant like `Bash(gh pr view:*)` contains a space, which a
  space-separated string cannot hold), and `metadata.shortcut` for magic words
  (comma-separated, unique across the plugin; omit when no word is needed). Nothing else:
  no per-skill version, no `model` pin.
- **Description:** third person, what it does and when to use it, ≤ 160 characters — it is
  loaded in every session.
- **Body:** ≤ 100 lines (`smith` ≤ 150) — it is read in full each run. Only what some runs
  need goes to `references/`, linked where the condition is stated.
- **Machine-readable result:** a skill another skill routes on ends in one fixed line
  (`VERDICT:`, `RESULT:`, `SECURITY:`, `AUDIT:`, `OPS:`), always emitted, so its absence
  means the skill did not run.
- **README:** add the skill to the `## Skills` tables of both READMEs, magic words included.

## Checks

`make test` runs four checks and reports all of them; run it before handing work back.
pre-commit runs the same four on every commit, plus `scripts/validate-fixtures` when
`scripts/` changes; CI runs all five on every push.

| Script                       | Fails when                                                                |
| ---------------------------- | ------------------------------------------------------------------------- |
| `scripts/test`               | a required file is missing or a manifest name disagrees                   |
| `scripts/check-version-sync` | versions disagree, the release lags the tag, or a plugin changed unbumped |
| `scripts/validate`           | a magic word repeats, a README table drifts, a reference dangles          |
| `scripts/check-skill-spec`   | frontmatter breaks the Agent Skills standard or the budgets               |

Run `bash scripts/validate-fixtures` after editing `validate` or `check-skill-spec`: it
breaks a temp copy one way at a time and asserts each check notices. `make doctor` reports a
local `~/.claude/skills` copy that shadows a shipped skill.

Green checks do not prove the prose is right; a stale sentence still needs reading.

## Versions and releases

- One version, in two places that must agree: the plugin's entry in `marketplace.json` and
  `plugins/wisdom/.claude-plugin/plugin.json`. The top-level `version` in `marketplace.json`
  must not lag the latest `v*` tag.
- Bump the plugin whenever anything under `plugins/wisdom/` changes, a description
  included: an installed copy is re-fetched only when the version moves. A change outside
  it (README, scripts) bumps the top-level version alone. At most one plugin bump between
  two tags.
- Never tag or release without the user asking.
