# Wisdom

> Help your Claude Code more efficiently and effectively, like me

This project is the collection of Claude Code plugins I use, and you can use it the way I do.

## Installation

Add the wisdom marketplace to your Claude Code and install the plugin.

```bash
/plugin marketplace add cmj0121/wisdom
```

## AI Scrum Team

Wisdom organizes AI agents into a scrum team that collaborates to deliver software. Each agent
has a clear role, responsibility boundary, and reporting chain.

### Core Roles

| Role                 | Agent         | Responsibility                                           |
| -------------------- | ------------- | -------------------------------------------------------- |
| **Project Leader**   | `agent-smith` | Plan, dispatch, coordinate sprints, manage git lifecycle |
| **Architect**        | `agent-ward`  | System design, API design, tech stack decisions          |
| **Developer**        | `agent-hale`  | Implement code, write tests                              |
| **QA**               | `agent-ellis` | Code review, test execution, acceptance verification     |
| **Technical Writer** | `agent-twain` | User docs, API docs, migration guides                    |
| **SRE**              | `agent-page`  | Observability, reliability, performance review           |

### Optional Role

| Role                | Agent        | Responsibility                                     |
| ------------------- | ------------ | -------------------------------------------------- |
| **Release Manager** | `agent-ross` | CI/CD, Docker build, cloud deploy, release tagging |

### Support Tools

| Tool            | Description                                      | Available To                         |
| --------------- | ------------------------------------------------ | ------------------------------------ |
| `spec-writer`   | Technical specs with architecture diagrams       | agent-ward, agent-twain              |
| `tenth-man`     | Challenges assumptions and surfaces risks        | agent-smith, agent-ward              |
| `ascii-grapher` | ASCII diagrams for architecture, flows, concepts | agent-ward, agent-twain, agent-page  |
| `test-runner`   | Detects test framework and runs test suite       | agent-hale, agent-ellis, agent-page  |
| `changelog-gen` | Generates changelog from git history             | agent-ross, agent-twain              |
| `dep-auditor`   | Audits dependencies for vulns and outdated pkgs  | agent-ellis                          |
| `sec-review`    | Security scan mapped to CWE IDs                  | agent-ellis (diff), agent-ross (all) |

### Utilities

Standalone plugins, not part of the scrum chain. Each works on its own.

| Tool        | Description                                                               |
| ----------- | ------------------------------------------------------------------------- |
| `shortcut`  | Auto-dispatches a skill when your prompt contains its magic word          |
| `compactor` | Re-renders the previous result as a dense, scannable table                |
| `lingua`    | Replies in the language you choose, remembered per project                |
| `briefing`  | Compact output and one-topic-at-a-time discussion for smith and tenth-man |

### Workflow

```text
  ┌──────┐   idea   ┌─────────┐  challenge  ┌───────────┐
  │ user │─────────>│  smith  │<───────────>│ tenth-man │
  └──────┘          └────┬────┘   verdict   └───────────┘
                         │
                         │  PLAN.md — Context · Units of Work · Decisions · Iteration Log
                         │
     ┌───────────────────┼────────────────────┬─────────────────────┐
     │ design            │ dispatch           │ docs · ops          │ release (optional)
     ▼                   ▼                    ▼                     ▼
┌─────────┐      ┌───────────────┐      ┌───────────┐          ┌─────────┐
│  ward   │─────>│    hale ×N    │      │   twain   │          │  ross   │
│         │      │   worktrees   │      │   page    │          │         │
└────┬────┘      └───────┬───────┘      └───────────┘          └─────────┘
     ▲                   │
     │                   ▼
     │           ┌───────────────┐
     │           │     ellis     │
     │           └───────┬───────┘
     │  redesign         │  fix → re-dispatch hale
     └───────────────────┘
```

Smith plans first, writing `PLAN.md` as the run's shared memory, then dispatches
**independent units to parallel hale instances**, each in an isolated git worktree. Ellis
reviews each unit as it lands. After QA passes, smith merges the worktrees back
sequentially, then runs docs and ops in parallel before the release step.

### Verdict Routing

No agent talks to another directly. Every finding returns to smith, which decides where it
goes next — this is what keeps a review from turning into a side conversation between two
agents that smith cannot see.

```text
  ┌───────┐  __REVIEW_VERDICT__   ┌───────┐   implementation-level   ┌──────┐
  │ ellis │──────────────────────>│ smith │─────────────────────────>│ hale │
  └───────┘    FAIL · WARN        └───┬───┘                          └──────┘
                                      │      design-level            ┌──────┐
                                      └─────────────────────────────>│ ward │
                                                                     └──────┘
```

Page reports the same way with `__OPS_VERDICT__` (READY · CONCERN · BLOCK), and smith
dispatches hale for fixes when it blocks.

## Model Tiers

A skill declares a `model` in its `SKILL.md` frontmatter only to run mechanical work on a
cheaper model. Nothing here pins upward: reasoning-heavy skills inherit whatever model the
session already runs on, so the user's own choice — not the marketplace — decides how much
model a plan or a review gets.

- **Default (inherit)** — everything not listed below, including the reasoning-heavy skills:
  `agent-smith`, `agent-ward`, `agent-hale`, `agent-ellis`, `agent-twain`, `agent-page`,
  `agent-ross`, `spec-writer`, `tenth-man`, `sec-review`
- **Economical (`haiku`)** — mechanical, deterministic, high-frequency:
  `changelog-gen`, `ascii-grapher`, `test-runner`, `dep-auditor`, `compactor`, `shortcut`, `lingua`

`model` accepts `fable` / `opus` / `sonnet` / `haiku`, a full model ID, or `inherit`; omitting
the field means the same as `inherit`. Changes take effect on the next session — skill
frontmatter is read at session start.

A pin applies for the rest of the turn, not just while the skill runs, so a skill an agent
invokes mid-task would move the session that invoked it. The four an agent can reach —
`ascii-grapher`, `test-runner`, `changelog-gen`, `dep-auditor` — therefore also set
`context: fork`, which aims the pin at a forked subagent instead, and `background: false`, so
their caller still gets the result in the same turn. `compactor`, `shortcut` and `lingua` pin
bare: you invoke those yourself, so the only turn they move is their own.

## Development

Plugins are markdown and JSON, so there is no build step — what keeps the marketplace
coherent is four checks, each owning one failure domain. The last of them measures the repo
against the [Agent Skills standard](https://agentskills.io/specification).

| Check                        | Domain            | Fails when                                                       |
| ---------------------------- | ----------------- | ---------------------------------------------------------------- |
| `scripts/test`               | structural        | a required file is missing, or a manifest name/version disagrees |
| `scripts/check-version-sync` | version integrity | a plugin's three versions disagree, or the release lags its tag  |
| `scripts/validate`           | semantic          | a reference, model, magic word, description, section or roster   |
| `scripts/check-skill-spec`   | standard          | a `SKILL.md` breaks the Agent Skills standard                    |

They stay four scripts rather than one because they fail for different reasons — a missing
file is a packaging mistake, a version drift is a release mistake, an unresolved skill
reference is an authoring mistake, an unknown frontmatter field is a portability mistake —
and because each is worth running on its own while you fix that one class of problem.

A fifth script, `scripts/validate-fixtures`, is the self-test for the last two: it mutates a
throwaway copy of the repo to break each check in turn and asserts the check catches it. It
stays out of `make test` — a suite of checks and the proof those checks can still fail are
different jobs.

```text
                             ┌─ scripts/test                structural
   make test ──────────┐     │
                       │     ├─ scripts/check-version-sync  version integrity
   git commit ──┬──────┼────>┤
   (pre-commit) │      │     ├─ scripts/validate            semantic
   CI ──────────┤      └     │
                │            └─ scripts/check-skill-spec    Agent Skills standard
                │
                └──────────────> scripts/validate-fixtures  self-test
                                 (pre-commit: only when scripts/ changes; CI: always)
```

`make test` runs the first four and reports all four; it does not stop at the first failure.
It never runs `scripts/validate-fixtures`. Committing runs all five: the same four
unconditionally, plus the fixtures self-test whenever a file under `scripts/` changes. CI runs
all five unconditionally. So a green `make test` says nothing about whether the checks' own
tests still hold.

Four of the five are deliberately ungated, and the reason is worth knowing before you add a
`files:` pattern of your own. pre-commit builds its candidate file list with
`--diff-filter=ACMRTUXB`, which excludes deletions, so a commit that only _deletes_ a file
presents zero candidates — and a gated hook with nothing to match is skipped, however exactly
its pattern would have fitted the deleted path. Deleting `plugins/<name>/LICENSE`, the
top-level `README.md`, or a check script is precisely what the structural, version and
semantic and standard checks exist to catch, so all four run on every commit regardless of
what you touched.

### Trigger evals

A skill only helps if it activates, and the `description` is the only thing Claude has at the
moment it decides. The seven utility skills — `test-runner`, `dep-auditor`, `sec-review`,
`changelog-gen`, `ascii-grapher`, `spec-writer`, `compactor` — each carry
`evals/trigger-queries.json`: 20 labelled prompts, ten that should activate the skill and ten
near-misses that share its vocabulary but need something else. Split 60/40 into train and
validation, so a reworded description is tuned on one half and judged on the other rather than
fitted to the phrasings used to tune it.

The scrum agents have no such file. They are dispatched by `agent-smith` rather than triggered
by a prompt, and by design each is the next one's nearest near-miss.

No runner is committed: `claude plugin eval` is the intended one and is in early access, so
its case format is not yet public.

Only `scripts/validate-fixtures` stays gated, on `^scripts/`: it costs a few seconds and says
nothing new unless a check changes. That gate has the same blind spot — deleting
`scripts/validate` presents no `scripts/` file either — which is why `scripts/test` asserts
that all five check scripts exist and are executable, and why CI runs the fixtures every time.

### What the semantic validator enforces

When you add or edit a plugin, this is the check to know about. It enforces:

- **Shortcut section** — every skill declares its magic words in a `## Shortcut` section, in
  backticks, on a line reading ``prompt contains `word` ``. `shortcut` itself, the
  dispatcher, is the only exception.
- **Unique magic words** — no two plugins may claim the same word, and the plugin README's
  magic-word list must name exactly what its skill declares, no more and no fewer.
- **README sections** — every plugin README needs an H1 title, `## Installation` and
  `## License`.
- **Plugin roster** — every plugin registered in `.claude-plugin/marketplace.json` must be
  named in the prose of this top-level README. Prose only: a name that appears solely inside
  a fenced code block does not count, because a name in a diagram is not a roster entry.
- **Resolvable references** — a `<plugin>:<skill>` reference in a skill body must point at a
  plugin and skill that exist here, or at a known external plugin.
- **Known model tiers** — `model:` must be `fable`, `opus`, `sonnet`, `haiku` or a full
  `claude-*` model ID; omit the field to inherit the session default.
- **Agreeing descriptions** — a plugin's one-sentence `description` must read identically in
  `.claude-plugin/marketplace.json`, its `plugin.json` and its `SKILL.md` frontmatter. It is
  the one piece of prose a plugin repeats verbatim, so the one that can be compared at all.
- **Balanced code fences** — an unterminated fence hides everything after it from the checks.

### Backticks are reserved

Two places in this repo are read as declarations rather than as prose:

- the `## Shortcut` section of any `SKILL.md`
- the Magic Words heading of any plugin `README.md`

Inside those two sections, **every backtick span is taken as a magic word** — not only the
ones in the `prompt contains` line. Put a filename, a tool name or a skill reference in
backticks there and you have declared it as a trigger word; the validator then reports it as
an undocumented magic word, or as a collision with whichever other plugin also mentioned it.
This is not hypothetical: `plugins/lingua/README.md` had to unwrap two ordinary prose
backticks under its Magic Words heading for exactly this reason.

So in those two sections, write anything that is not a trigger word without backticks.
Backticks are normal everywhere else in the same file, but the sections reach further than
they look: one ends only at a heading of the _same or higher_ level, so a `### Additional
Triggers` nested under `## Shortcut` is still inside it.

A code fence is not a way out of the rule. Nothing in a `## Shortcut` section needs one, and a
fence there used to swallow a declaration without a word, so the validator now rejects any
backtick span — and any `prompt contains` line — inside a fence in that section, whether or
not it was meant as a trigger.

The over-collection is deliberate. Collecting too few words would hide a real collision
behind a green tick; collecting too many fails loudly and takes one edit to fix.

### Versions and self-tests

`scripts/check-version-sync` reads four version locations, in two independent checks with two
different failure modes.

Three of them must be identical, per plugin: its entry in `.claude-plugin/marketplace.json`,
its own `plugin.json`, and its skill's `metadata.version`. Bump them together or the sync
check fails.

The fourth is the **top-level** `version` in `.claude-plugin/marketplace.json` — the
marketplace's own release number, not any plugin's. It is compared against the latest `v*` git
tag: equal means released, ahead means a release is being prepared, behind is an error. A
plugin bump that leaves it alone is the usual way to hit this one, so cutting a release means
bumping this field too.

`scripts/validate-fixtures` is outside `make test`, but the commit path runs it whenever
anything under `scripts/` changes. Run it by hand while you edit `scripts/validate`, rather
than finding out at commit time that a check can no longer be made to fail.

### What the checks cannot tell you

Green checks mean nothing _mechanically_ checkable is broken. They cannot tell you the prose
is right: a stale table row, a wrong slash command name or an inaccurate description passes
every one of them. That stays a matter of reading it.

## DDD (Dream-Driven Development)

This project follows the DDD (Dream-Driven Development) methodology, which means the project
is driven by what I envision.

All features are based on my needs and my dreams.
