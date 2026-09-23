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
   enough to type in passing also declares a magic word — say `smith` and the dispatcher
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

| Skill    | Purpose                                                     | Magic word    |
| -------- | ----------------------------------------------------------- | ------------- |
| `plan`   | Turn an idea into `PLAN.md`: goal, units of work, decisions | `plan it`     |
| `design` | Decide an architecture, API or tech choice, with trade-offs | `design it`   |
| `spec`   | Write a technical specification for an agreed design        | `write spec`  |
| `code`   | Implement one unit of work with its tests                   | `code it`     |
| `test`   | Run the project's test suite and report the result          | `run tests`   |
| `review` | Review a diff for correctness and quality                   | `review it`   |
| `docs`   | Write or update user-facing documentation                   | `document it` |

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

| Skill      | Purpose                                                   | Magic word       |
| ---------- | --------------------------------------------------------- | ---------------- |
| `diagram`  | Draw an ASCII diagram of a decided structure              | `draw a diagram` |
| `compact`  | Re-render the previous answer as a dense table            | `compact it`     |
| `brief`    | Keep answers short and discuss one topic at a time        | `brief me`       |
| `lingua`   | Answer in your chosen language, remembered per project    | `reply in`       |
| `shortcut` | Dispatch the skill whose magic word appears in the prompt | —                |

## How smith runs

```text
  idea ──> smith ──> plan ──> (design) ──> code ×N ──> review ──> docs ──> commit
             │         │                     ▲           │
             │         └── challenge         └── fix ────┘
             │
             └── release · only when you ask
```

- `plan` writes `PLAN.md` once — context, units, decisions — and every later skill reads it
  instead of rediscovering the project.
- Independent units run in parallel, each `code` in its own git worktree.
- `review` returns a one-line verdict; `smith` routes a failure back to `code` (or to
  `design` when the design is at fault).
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
└── skills/<name>/
    ├── SKILL.md
    └── references/      # optional
```

Run `make test` before a commit — it checks the layout, the version sync, frontmatter against
the standard, and that magic words are unique.

## DDD (Dream-Driven Development)

This project follows DDD (Dream-Driven Development): it is driven by what I envision. Every
feature comes from my own needs and my own dreams.
