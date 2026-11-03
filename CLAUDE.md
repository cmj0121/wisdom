# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

Wisdom is a Claude Code plugin marketplace shipping one plugin, `wisdom`: single-purpose
skills written as Markdown (`SKILL.md`) with YAML frontmatter; a skill may ship a script for
deterministic work. `smith` is the entry point and coordinates the rest. `README.md` is the
roster and the design; keep `README.zh-TW.md` in step with it.

## Layout

```text
.claude-plugin/marketplace.json     # registers the wisdom plugin
plugins/wisdom/
├── .claude-plugin/plugin.json
├── evals/<case>/                   # what `make eval` runs
├── hooks/                          # hooks.json and the scripts it runs
└── skills/<name>/
    ├── SKILL.md
    ├── references/                 # optional, read only when the body says so
    └── scripts/                    # optional, run only when the body says so
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
- **Machine-readable result:** a skill another skill routes on ends in one fixed line, in a
  code fence (`VERDICT:`, `RESULT:`, `SECURITY:`, `AUDIT:`, `OPS:`, `HISTORY:`, `CODE:`,
  `COMMIT:`, `DOCS:`; a hook reads `AFK:` the same way), always emitted, so its absence means
  the skill did not run. A `smith` route, written `<skill>: <TOKEN>`, must name a token that
  skill's line states; `validate` fails otherwise.
- **README:** add the skill to the `## Skills` tables of both READMEs, magic words included.

## Checks

`make test` runs six checks and reports all of them; run it before handing work back.

pre-commit runs `test`, `check-version-sync`, `validate --per-commit` and `check-skill-spec`
on every commit, `test-hooks` when `plugins/wisdom/hooks/`, a `SKILL.md` or the script itself
changes, and `validate-fixtures` when `scripts/` changes. `--per-commit` skips only the README
table comparison, so a row can land before its skill. `test-history` is not a hook.

CI runs on a push to `main` and on every pull request: `make test`, `validate-fixtures`, and
every pre-commit hook over all files.

| Script                       | Fails when                                                                        |
| ---------------------------- | --------------------------------------------------------------------------------- |
| `scripts/test`               | a required file is missing, a manifest name disagrees, a hook path dangles        |
| `scripts/check-version-sync` | versions disagree, the release lags the tag, or a plugin changed unbumped         |
| `scripts/validate`           | a magic word repeats, a README table drifts, a reference or smith route dangles   |
| `scripts/check-skill-spec`   | frontmatter breaks the Agent Skills standard or the budgets                       |
| `scripts/test-hooks`         | a prompt or SessionStart hook prints the wrong context, fails or writes to stderr |
| `scripts/test-history`       | `reshape.py` gives the wrong result, or an `ABORTED` run changes the checkout     |

Run `bash scripts/validate-fixtures` after editing `validate` or `check-skill-spec`: it
breaks a temp copy one way at a time and asserts each check notices. `make doctor` reports a
local `~/.claude/skills` copy that shadows a shipped skill.

`make eval` runs `plugins/wisdom/evals/` with real, billed model runs, capped at $5 a run; CI
does not run it. A low score or the cap makes `make` exit 2: a result to read, not a broken run.

Green checks do not prove the prose is right; a stale sentence still needs reading.

## Versions and releases

- One version, in two places that must agree: the plugin's entry in `marketplace.json` and
  `plugins/wisdom/.claude-plugin/plugin.json`. The top-level `version` in `marketplace.json`
  must not lag the latest `v*` tag.
- Bump the plugin whenever anything under `plugins/wisdom/` changes, a description
  included: an installed copy is re-fetched only when the version moves. A change outside
  it (README, scripts) bumps the top-level version alone.
- Never tag or release without the user asking.
