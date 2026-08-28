# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Wisdom is a Claude Code plugin marketplace — a collection of AI-agent skill plugins that extend Claude
Code's capabilities. Plugins are defined primarily through Markdown-based skill definitions (SKILL.md)
with YAML frontmatter, not traditional source code.

All plugins follow the PoLP (Principle of Least Power) principle, which means they are designed
to be as simple and declarative as possible, relying on Claude's natural language understanding rather
than complex code logic. This makes them more maintainable and easier to extend by the community.

## Architecture

### Plugin Structure

Every plugin lives under `plugins/<name>/` and must contain:

```text
plugins/<name>/
├── .claude-plugin/plugin.json   # Metadata: name, version, license, author
├── skills/<name>/SKILL.md       # AI agent instructions with YAML frontmatter
├── README.md
└── LICENSE
```

### Skill Definitions (SKILL.md)

Frontmatter follows the [Agent Skills standard](https://agentskills.io/specification), and
this repo treats its fields as two layers. `scripts/check-skill-spec` enforces the split, and
its `CLAUDE_CODE_EXTENSIONS` map is where the second layer is declared.

**The standard's six** — portable to any client, including claude.ai uploads and the Skills
API, both of which reject an unknown key with a hard error rather than ignoring it:

- `name`: 1–64 chars, lowercase alphanumerics and single hyphens, no leading, trailing or
  doubled hyphen, no `anthropic` or `claude`, and it must equal the skill's directory name
- `description`: what the skill does **and when to use it**, third person, no XML tags. The
  standard's ceiling is 1024 characters; this repo's is 400 and its skills sit near 250,
  because the same string is catalogue copy in `/plugin`, in `.claude-plugin/marketplace.json`
  and in both READMEs
- `license`
- `allowed-tools`: a **YAML list** — the one place this repo knowingly departs from the
  standard, which types the field as a space-separated string. 70 of its grants contain a
  space (`Bash(git status:*)`), which a space-separated string cannot express, and the only
  space-free spelling (`Bash(git:*)`) widens the grant from one subcommand to all of git. Of
  the two remaining spellings, a list is rejected loudly on its type by a spec-strict reader,
  while a comma-separated string gets split on spaces into `Bash(git` and `status:*),` —
  patterns that match nothing, silently dropping a permission. The standard marks this field
  Experimental, so it is the one to depart from
- `metadata`: string keys to string values only — hence `version: "2.0.0"`, quoted
- `compatibility`: unused here; most skills do not need it

**Claude Code extensions this repo has adopted** — each costs portability, so each needs a
reason recorded next to it:

- `model`: `fable` / `opus` / `sonnet` / `haiku`, a full model ID, or `inherit`; omitting the
  field means the same as `inherit`. Pin downward only. Read at session start, so changes take
  effect next session.
- `context: fork` and `background: false`: a `model` pin applies for the **rest of the turn**,
  not just while the skill runs, so a skill an agent invokes mid-task would move the session
  that invoked it. Any pinned skill an agent can reach sets both — `fork` aims the pin at a
  subagent, `background: false` keeps the result inline for the caller.

Adding a third extension means adding it to `CLAUDE_CODE_EXTENSIONS` with the same kind of
reason. Anything outside both layers fails the check.

The body contains phase-by-phase instructions that guide the AI agent through a workflow, and
must stay under 500 lines — the check warns at 250. 350 never fired: the longest body here,
`agent-smith`, sat at 346, four lines under the line meant to flag it. The warning asks for a
judgement rather than a split — move what a run merely consults (rosters, schemas, worked
examples) into `references/`, and shorten what it executes instead of moving that too, because
a procedure in `references/` is read anyway, one fetch later.

### Skill Discovery (Three Tiers)

1. User-level: `~/.claude/skills/`, `~/.claude/commands/`
2. Project-level: `.claude/skills/`, `.claude/commands/`
3. Plugin-bundled: `plugins/*/skills/`

## Checks

Run `make test` before handing work back: it runs `scripts/test` (structure),
`scripts/check-version-sync` (versions), `scripts/validate` (semantics) and
`scripts/check-skill-spec` (the Agent Skills standard), and reports all four rather than
stopping at the first failure. Those same four run on every commit, ungated — pre-commit's
candidate list excludes deletions, so a path-gated hook sees nothing on a deletion-only commit
and is skipped. After editing `scripts/validate` or `scripts/check-skill-spec`, also run
`scripts/validate-fixtures` — the negative-fixture self-test for both, and the one hook still
gated (on `^scripts/`), which the commit path runs but `make test` does not. CI
(`.github/workflows/checks.yml`) runs those five plus the full pre-commit suite on every push
and pull request.

`scripts/check-install-drift` is the sixth and is in none of those paths. It reports a skill
this repo ships that the local `~/.claude/skills` also serves — a stale copy there outranks
the installed plugin and gives the model two routers to choose between, so every trigger eval
here measures a description the session may never have loaded. It asserts on the machine, not
the repo, so it runs from `make doctor` by hand: in CI there is no `$HOME/.claude` and it
would pass for the wrong reason. Run it when a skill behaves like an older version of itself.

What that means for edits here:

- A plugin version bump touches three files at once: `.claude-plugin/marketplace.json`, the
  plugin's `plugin.json`, and the skill's `metadata.version`. Never change one alone.
- A release also bumps the **top-level** `version` in `.claude-plugin/marketplace.json`, which
  must not lag the latest `v*` git tag. That is a fourth location and a separate check.
- A plugin's `description` must read identically in `.claude-plugin/marketplace.json`, its
  `plugin.json` and its `SKILL.md` frontmatter.
- A skill that hands another skill a machine-readable block declares that block's marker in
  `metadata.verdict`. The check runs both ways — a shown block must be declared, a declared
  marker must be shown as a block carrying at least one `Field: value` line, and a marker a
  skill routes on must be one some skill in the marketplace emits. Five exist:
  `__REVIEW_VERDICT__`, `__OPS_VERDICT__`, `__TEST_RESULT__`, `__AUDIT_RESULT__` and
  `__SEC_REVIEW_RESULT__`. A marker inside a fenced block is read as emitted; the same token in
  prose backticks is read as routed on.
- Every skill declares its magic words in `metadata.shortcut`, a comma-separated string;
  `shortcut` itself is the sole exception. Magic words must be unique across all plugins. Its
  `## Shortcut` section must spell each declared word out in backticks for human readers, but
  that section is documentation — an extra backtick span there is ordinary prose.
- A plugin README must document exactly the magic words its skill declares — no extras, none
  missing — and keep its H1, `## Installation` and `## License` sections.
- Under a plugin README's Magic Words heading — and only there — EVERY backtick span is read
  as a magic word, because that check runs both ways: no declared word may go undocumented and
  no documented word may be invented. Write anything else under that heading without
  backticks. Such a section ends only at a heading of the same or higher level, so its
  subsections are still inside it, and a fenced block there is stripped before it is read.
- A plugin registered in `.claude-plugin/marketplace.json` must also be named in the
  top-level `README.md` prose; a mention only inside a code fence does not count.
- Write a `<plugin>:<skill>` reference only when both halves exist in this repo.
- `model:` must be a known tier, `inherit`, or a full `claude-*` ID. Omitting the field and
  writing `inherit` do the same thing.
- Frontmatter may carry only the standard's six fields plus the Claude Code extensions listed
  in `CLAUDE_CODE_EXTENSIONS` (`scripts/check-skill-spec`). A new one needs a recorded reason.
- Every plugin carries `evals/trigger-queries.json`: 20 labelled prompts, half of
  them near-misses, split train/validation. Rewriting a `description` means re-running them,
  tuning on train and judging on validation. `scripts/validate` fails a plugin with no such
  file, one that labels every query the same way, one that never splits off a validation half,
  and one whose positive queries carry another plugin's magic word — a negative that does is
  the near-miss, a positive that does is two skills racing. No runner is committed — `claude
plugin eval` is the intended one and is still in early access, so the file states the intent
  that a runner will check, not a passing test.

Passing checks only prove nothing mechanically checkable is broken. Prose accuracy — a stale
table row, a wrong command name — is not covered and still needs review.
