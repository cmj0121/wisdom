# Wisdom

> Help your Claude Code work more efficiently and effectively, like me

[繁體中文](README.zh-TW.md)

Wisdom is the set of Claude Code skills I use every day, packaged as one plugin so you can use
them the way I do.

## Installation

```bash
/plugin marketplace add cmj0121/wisdom
/plugin install wisdom@wisdom
```

## Concept

v3 is a rewrite from scratch around three rules.

1. **One skill, one purpose.** Each skill does one thing and is named after it. A skill that
   needs a second job calls the skill that owns it instead of growing one.
2. **Shortcuts where they help.** Every skill runs with `/wisdom:<name>`. A skill used often
   enough to type in passing also declares a magic word — say `smith` and a prompt hook
   starts the lead skill. Words are unique across the plugin.
3. **Fewer tokens.** A description is loaded in every session, so it stays one short
   sentence. A body is loaded each time its skill runs, so it stays short too; anything only
   some runs need lives in `references/` and is read only then. No personas, no role-play
   framing, no repeated project discovery: the plan file carries the context forward.

## Skills

`smith` is the entry point. Tell it what you want built and it plans the work, then calls the
other skills in turn. Every skill also works on its own.

### Lead

| Skill   | Purpose                                                         | Magic word |
| ------- | --------------------------------------------------------------- | ---------- |
| `smith` | Drive a piece of work from idea to merge using the skills below | `smith`    |

### Build

| Skill    | Purpose                                                                    | Magic word    |
| -------- | -------------------------------------------------------------------------- | ------------- |
| `plan`   | Turn an idea into `PLAN.md` and `PLAN_DETAILS.md`: units, decisions, setup | `plan it`     |
| `design` | Decide an architecture, API or tech choice, with trade-offs                | `design it`   |
| `spec`   | Write a technical specification for an agreed design                       | `write spec`  |
| `code`   | Implement one unit of work with its tests                                  | `code it`     |
| `test`   | Run the project's test suite and report the result                         | `run tests`   |
| `review` | Review a diff for correctness and quality                                  | `review it`   |
| `docs`   | Write or update user-facing documentation                                  | `document it` |

### Ship

| Skill       | Purpose                                                 | Magic word      |
| ----------- | ------------------------------------------------------- | --------------- |
| `commit`    | Write a commit message for the staged change and commit | `commit it`     |
| `changelog` | Generate changelog entries from git history             | `gen changelog` |
| `release`   | Bump the version and tag a release — only when asked    | `release it`    |
| `resolve`   | Work a pull request's review comments, test first       | `resolve pr`    |

### Check

| Skill       | Purpose                                                    | Magic word   |
| ----------- | ---------------------------------------------------------- | ------------ |
| `secure`    | Review source for security issues, mapped to CWE           | `sec review` |
| `audit`     | Audit dependencies for known vulnerabilities and staleness | `audit deps` |
| `ops`       | Review operational readiness before a release              | `ops review` |
| `challenge` | Argue against a plan and name its blind spots              | `tenth man`  |
| `lsp`       | Say whether the repo needs a language server, and which    | `need lsp`   |

### Output

| Skill      | Purpose                                                | Magic word       |
| ---------- | ------------------------------------------------------ | ---------------- |
| `diagram`  | Draw an ASCII diagram of a decided structure           | `draw a diagram` |
| `assets`   | Build media assets one confirmed change per round      | `build assets`   |
| `compact`  | Re-render the previous answer as a dense table         | `compact it`     |
| `brief`    | Keep answers short and discuss one topic at a time     | `brief me`       |
| `afk`      | Work to the end and ping you when done or needed       | `afk mode`       |
| `lingua`   | Answer in your chosen language, remembered per project | `reply in`       |
| `shortcut` | List every magic word, or dispatch one the hook missed | —                |

`afk` rings the terminal (bell + OSC 9) when the agent stops; `afk off` ends it. It does not
change the permission mode: a permission request still stops the agent, and is the
needs-you ping. Terminal.app shows no OSC 9, so there the message arrives through
Notification Center, listed under Script Editor — allow its notifications. Under tmux only
the bell gets through unless passthrough is on. Claude Code's own notification channel, if
you set one, pings as well.

## How smith runs

A boxed step runs in its own subagent; a `smith ─` step is Smith itself; `★` waits for you.

```text
① Plan & Design

  smith ─ wisdom:plan ──> PLAN.md + PLAN_DETAILS.md
                │
                ▼
      ┌───────────────────┐
      │ wisdom:challenge  │
      └───────────────────┘
                │
                ├──PAUSE──> smith revises, challenge once more
                ├──RECONSIDER──> ask user
                │ GO
                ▼
  ★ Checkpoint 1 · user approves plan
                │
                ▼
  smith ─ wisdom:design / wisdom:spec ──> design units marked done
                │
                ▼
             ② Build

② Build · repeated per batch

  ┌──────────────────────┐ ┌──────────────────────┐
  │ wisdom:code · U1     │ │ wisdom:code · U2     │   parallel, one worktree each
  └──────────────────────┘ └──────────────────────┘
             │                        │
             ▼                        ▼
  ┌──────────────────────┐ ┌──────────────────────┐
  │ wisdom:review · U1   │ │ wisdom:review · U2   │   parallel
  └──────────────────────┘ └──────────────────────┘
             └───────────┬────────────┘
                         ▼
  smith ─ routes VERDICT lines ──design wrong──> smith ─ wisdom:design
                         │
                         ├──FAIL──> same code agent fixes ──> review again
                         │ PASS
                         ▼
  ┌──────────────────────────────────────────────┐
  │ same code agent · wisdom:commit in worktree  │   resumed via SendMessage
  └──────────────────────────────────────────────┘
                         │
                         ▼
  smith ─ merges each branch into feat/<slug>
                         │
                         ▼
  ┌──────────────────────────────────────────────┐
  │ wisdom:test · full suite on feat/<slug>      │   once per batch
  └──────────────────────────────────────────────┘
                         │
                         ├──FAIL──> new wisdom:code agent ──> review, commit, test
                         │ PASS
                         ▼
  smith ─ Baseline = PASS at <sha> ──> next batch, or ③

③ Check & Merge

  ┌─────────────┐ ┌───────────────┐ ┌──────────────┐ ┌────────────┐
  │ wisdom:docs │ │ wisdom:secure │ │ wisdom:audit │ │ wisdom:ops │   only those needed
  └─────────────┘ └───────────────┘ └──────────────┘ └────────────┘
         └────────────────┴────────┬───────┴───────────────┘
                                   │
                                   ├──FAIL──> new wisdom:code agent ──> review, commit
                                   ▼
               ★ Checkpoint 2 · user approves merge
                                   │
                                   ▼
  smith ─ git merge --no-ff into main · rm PLAN.md PLAN_DETAILS.md
```

- `plan` writes two files once, and every later skill reads them instead of rediscovering
  the project: `PLAN.md`, the short view `smith` reads — units, decisions, verdicts — and
  `PLAN_DETAILS.md`, what a subagent needs to start cold — setup, baseline, each unit's
  files and acceptance, each decision's interface.
- Every step on a unit runs in a subagent; `smith` reads result lines, never diffs.
- Independent units run in parallel, each `code` in its own git worktree, running only its
  own tests; the full suite runs once per merged batch.
- `review` returns a one-line verdict; `smith` routes a failure back to the same `code`
  subagent (or to `design` when the design is at fault), which commits once it passes.
- `smith` stops for you twice: to approve the plan, and to approve the merge. It never tags
  or releases unless you ask.

## Token budget

| Part              | Loaded                   | Budget                         |
| ----------------- | ------------------------ | ------------------------------ |
| `description`     | every session            | one sentence, ≤ 160 characters |
| `SKILL.md` body   | each time it runs        | ≤ 100 lines (`smith` ≤ 150)    |
| `references/*.md` | only when a run needs it | no limit, one topic per file   |

## Development

Skills are Markdown with YAML frontmatter following the
[Agent Skills standard](https://agentskills.io/specification); there is no build step.

```text
plugins/wisdom/
├── .claude-plugin/plugin.json
├── hooks/               # hooks.json and the scripts it runs
└── skills/<name>/
    ├── SKILL.md
    └── references/      # optional
```

Run `make test` before a commit — it checks the layout, the version sync, frontmatter against
the standard, and that magic words are unique.

## DDD (Dream-Driven Development)

This project follows DDD (Dream-Driven Development): it is driven by what I envision. Every
feature comes from my own needs and my own dreams.
