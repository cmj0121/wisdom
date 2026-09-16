# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project Overview

Wisdom is a Claude Code plugin marketplace: AI-agent skill plugins defined as Markdown skill
definitions (`SKILL.md`) with YAML frontmatter, not as source code.

Plugins follow PoLP (Principle of Least Power) — as declarative as they can be, relying on
Claude's language understanding rather than code logic, so the community can extend them.

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

Frontmatter follows the [Agent Skills standard](https://agentskills.io/specification) in two
layers, and `scripts/check-skill-spec` enforces the split. Anything outside both layers fails.

**The standard's six** — `name`, `description`, `license`, `allowed-tools`, `metadata`,
`compatibility` — are portable to any client, including claude.ai uploads and the Skills API,
which reject an unknown key outright rather than ignoring it. Three carry rules worth stating:

- `description`: what the skill does **and when to use it**, third person. The repo ceiling is
  320 characters and its skills average 173, because the same string is catalogue copy in four
  places: `/plugin`, `marketplace.json`, the plugin `README.md` blockquote and the skill's own
  frontmatter. All four are compared; the blockquote is line-wrapped, so an edit by exact
  string match reaches three of them and leaves the fourth stale.
- `allowed-tools`: a **YAML list**, the one place this repo knowingly departs from the
  standard's space-separated string. 70 grants contain a space (`Bash(git status:*)`), and the
  space-free spelling `Bash(git:*)` widens the grant from one subcommand to all of git. Of the
  two remaining spellings, a comma-separated string is split on spaces into patterns that
  match nothing — a permission dropped in silence — while a list at worst reaches a consumer
  that cannot use it as given. The field is still typed as a space-separated string and still
  marked Experimental, so it is the one to leave. Note the claim this rests on has narrowed:
  as of September 2026 tools are normalising a list into a string rather than rejecting it
  loudly, which is the quiet handling the list was chosen to avoid. `CLAUDE_CODE_EXTENSIONS`
  in `scripts/check-skill-spec` records what would make this decision worth revisiting.
- `metadata`: string keys to string values only — hence `version: "2.0.0"`, quoted.

**Claude Code extensions adopted here** — each costs portability, so each records its reason
in `CLAUDE_CODE_EXTENSIONS`; a third one needs the same:

- `model`: a tier, a full `claude-*` ID, or `inherit` (the same as omitting it). Pin downward
  only. Read at session start, so a change takes effect next session.
- `context: fork` and `background: false`: a `model` pin applies for the **rest of the turn**,
  so a pinned skill invoked mid-task would move the session that invoked it. Any pinned skill
  an agent can reach sets both — `fork` aims the pin at a subagent, `background: false` keeps
  the result inline for the caller.

The body is phase-by-phase instructions, under 500 lines, with a warning at 300 that asks for
a judgement rather than a split. **Form decides what moves, not topic.** A list or table
carries items a run looks up one at a time — a roster, a field table, a rubric — and each row
stands alone, so it survives the move into `references/` intact. Prose carries what joins
them: the condition, the tie-break, the reason. `If both trigger types appear, prefer
Autonomous mode.` is a relation, not an item; as two bullets it becomes two assertions with
nothing between them, and the case neither covers gets improvised. So prose stays in the body
and is shortened in place — which bounds what a split can reach: of `agent-smith`'s 292 lines,
84 are table, list and heading, so moving every movable line still leaves 208, and most of
those 84 are unconditional and would only cost a fetch. A target under that is a rewrite of
the phase text, and is worth planning as one.

Whether a procedure moves is a second, orthogonal question: unconditional or conditional. A
procedure every run needs is read anyway, one fetch later, so moving it costs a round trip and
buys nothing. A procedure only some runs need is what `references/` is for — put it there and
name the file where the condition is stated, because nothing in `references/` is read unless
the body says to read it. `agent-smith`'s Phase 2.5 is the example: it now runs only when the
plan touches a user-visible surface, so on most dispatches its detail is cost with no reader.

### Skill Discovery (Three Tiers)

1. User-level: `~/.claude/skills/`, `~/.claude/commands/`
2. Project-level: `.claude/skills/`, `.claude/commands/`
3. Plugin-bundled: `plugins/*/skills/`

## Checks

`make test` runs four and reports all four rather than stopping at the first failure:
`scripts/test` (structure), `scripts/check-version-sync` (versions), `scripts/validate`
(semantics), `scripts/check-skill-spec` (the standard). Run it before handing work back. Those
same four run on every commit, ungated — pre-commit's candidate list excludes deletions, so a
path-gated hook sees nothing on a deletion-only commit and is skipped.

Two more sit outside `make test`:

- `scripts/validate-fixtures`, the negative-fixture self-test for `validate` and
  `check-skill-spec`. Run it after editing either. It is the one hook still path-gated (on
  `^scripts/`), so the commit path runs it and `make test` does not.
- `scripts/check-install-drift`, run by hand from `make doctor`. It reports a skill this repo
  ships that the local `~/.claude/skills` also serves — a stale copy there outranks the
  installed plugin, so every trigger eval here measures a description the session may never
  have loaded. It asserts on the machine, not the repo; in CI there is no `$HOME/.claude`, so
  it would pass for the wrong reason. Run it when a skill behaves like an older version of
  itself.

CI (`.github/workflows/checks.yml`) runs all five plus the full pre-commit suite on every push
and pull request.

What that means for edits here:

- A version bump touches three files at once: `marketplace.json`, the plugin's `plugin.json`,
  and the skill's `metadata.version`. Never one alone. A release also bumps the **top-level**
  `version` in `marketplace.json`, which must not lag the latest `v*` tag — a fourth location
  and a separate check.
- A bump tracks what the plugin **does** — its `SKILL.md` body. A change confined to the
  `description`, or to the README blockquote, `plugin.json` and marketplace entry that mirror
  it, is catalogue copy: the router matches on it, but nothing the plugin does afterwards is
  different, so it moves the **top-level** `version` alone. Frontmatter that declares a
  contract the skill already honoured — `metadata.verdict` is the case at hand — is not a
  behaviour change either. And a plugin moves at most once per release window: between one
  `v*` tag and the next, a plugin already bumped is not bumped again, or the number stops
  naming a released state and starts counting pull requests.
- A plugin's `description` must read identically in `marketplace.json`, its `plugin.json` and
  its `SKILL.md` frontmatter.
- A skill that hands another a machine-readable block declares that marker in
  `metadata.verdict`. The check runs both ways: a shown block must be declared, a declared
  marker must appear as a block carrying at least one `Field: value` line, and a marker routed
  on must be one some skill here emits. Five exist — `__REVIEW_VERDICT__`, `__OPS_VERDICT__`,
  `__TEST_RESULT__`, `__AUDIT_RESULT__`, `__SEC_REVIEW_RESULT__`. Inside a fence reads as
  emitted; the same token in prose backticks reads as routed on.
- Every skill declares its magic words in `metadata.shortcut`, a comma-separated string
  (`shortcut` itself is the sole exception), and they must be unique across all plugins. The
  `## Shortcut` section spells each declared word out in backticks for human readers; that
  section is documentation, so an extra backtick span there is ordinary prose.
- A plugin README documents exactly the magic words its skill declares — no extras, none
  missing — and keeps its H1, `## Installation` and `## License` sections. Under its Magic
  Words heading, and only there, EVERY backtick span is read as a magic word, so write
  anything else there without backticks. That section ends only at a heading of the same or
  higher level, so its subsections are still inside it; a fence there is stripped first.
- A plugin registered in `marketplace.json` must also be named in the top-level `README.md`
  prose; a mention only inside a code fence does not count.
- Write a `<plugin>:<skill>` reference only when both halves exist in this repo.
- Every plugin carries `evals/trigger-queries.json`: 20 labelled prompts, half of them
  near-misses, split train/validation. Rewriting a `description` means re-running them — tune
  on train, judge on validation. `scripts/validate` fails a plugin with no such file, one that
  labels every query the same way, one that never splits off a validation half, and one whose
  positive queries carry another plugin's magic word: a negative that does is the near-miss, a
  positive that does is two skills racing. All 380 of these stay the cheap record — they cost
  nothing, run offline, and a rewrite can be judged against them with no runner at all: hand
  the frontmatter to a model, ask it for prompts that should and should not fire, and compare
  those against the labels already in the file. What they are not is executable, so on their
  own they state an intent rather than a passing test.
- `make eval` is the executable half, and it deliberately covers 13 of those 380. The runner
  is `claude plugin eval`, which is generally available — no opt-in flag, whatever an older
  paragraph here may have said — but each case is a full Claude child session on the
  operator's own credential, so it wants a network and real money where the four checks want
  neither. That is why it sits outside `make test` for `check-install-drift`'s reason, and why
  CI cannot run it: `.github/workflows/checks.yml` carries `permissions: contents: read` and
  no secrets, and putting a credential in a public repo to automate a check a human can run by
  hand is a bad trade. The 13 are the misses from a 3-sample blind-router baseline over the
  whole corpus, which scored 367/380 — the boundaries that actually move, rather than a
  sample. Converting the other 367 would buy repetition at a measured $0.142 a run: the 13 at
  `runs: 3` come to about $5.50, where all 380 would be roughly $54 at one run each and $324
  at the two-arm default with three.
- A case is `evals/<name>/prompt.md` plus a `graders/` directory, where a grader of
  `type: tool_used`, `tool: Skill`, `input_match: '"skill"\s*:\s*"<name>'` and `min: 1` asserts
  the skill fired and `min: 0` with `max: 0` asserts it did not. Leave the closing quote off
  that pattern — it is the spelling measured to match, it still covers a namespaced
  `plugin:skill` value, and no skill name here is a prefix of another, so it cannot over-match.
  Pass `--ablation none`, because under the default the CLI stops scoring a `tool_used: Skill`
  grader and demotes it to a with-only indicator. Two things decide whether a case measures
  anything. **A bare query does not fire a skill**: `what are we not seeing here` is a labelled
  `tenth-man` positive and it produced `Skill called 0x` with the plugin loaded, while the same
  words wrapped in a turn with something to act on — a team that agreed a monorepo move inside
  ten minutes, and what are we not seeing — fired first try. So a case is the labelled query
  rewritten as a real turn, keeping its intent and vocabulary but never its skill's own
  description wording, and a 1:1 migration of the bare queries would measure something else and
  mostly fail. **And a skill its owner invokes cannot be graded silent**: `agent-ward` calls
  `ascii-grapher` and `spec-writer` itself, so asserting either stayed quiet fails the runs that
  routed correctly. Rule out the second skill only where it is not downstream of the first;
  where it is, say so in the surviving grader's prose, which the report prints.

Passing checks only prove nothing mechanically checkable is broken. Prose accuracy — a stale
table row, a wrong command name — is not covered and still needs review.
