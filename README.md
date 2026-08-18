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

| Tool            | Description                                      | Available To                        |
| --------------- | ------------------------------------------------ | ----------------------------------- |
| `spec-writer`   | Technical specs with architecture diagrams       | agent-ward, agent-twain             |
| `tenth-man`     | Challenges assumptions and surfaces risks        | agent-smith, agent-ward             |
| `ascii-grapher` | ASCII diagrams for architecture, flows, concepts | agent-ward, agent-twain, agent-page |
| `test-runner`   | Detects test framework and runs test suite       | agent-hale, agent-ellis, agent-page |
| `changelog-gen` | Generates changelog from git history             | agent-ross, agent-twain             |
| `dep-auditor`   | Audits dependencies for vulns and outdated pkgs  | agent-page, agent-ellis             |
| `sec-review`    | Whole-project security scan, mapped to CWE IDs   | agent-ellis, agent-page             |

### Utilities

Standalone plugins, not part of the scrum chain. Each works on its own.

| Tool        | Description                                                      |
| ----------- | ---------------------------------------------------------------- |
| `shortcut`  | Auto-dispatches a skill when your prompt contains its magic word |
| `compactor` | Re-renders the previous result as a dense, scannable table       |
| `lingua`    | Replies in the language you choose, remembered per project       |

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

Each skill declares a `model` in its `SKILL.md` frontmatter so the right task runs on the
right-sized model. The rule: pin a model only when it matters — the strongest model where
reasoning quality is high-stakes and errors are hard to reverse, a cheaper model for
mechanical, high-frequency work — and otherwise inherit the session default.

- **Strongest (`fable`)** — upstream, high-stakes, hard-to-reverse reasoning:
  `agent-smith`, `agent-ward`, `tenth-man`, `sec-review`
- **Default (inherit)** — already strong on the session model; often dispatched in parallel:
  `agent-hale`, `agent-ellis`, `agent-twain`, `agent-page`, `agent-ross`, `spec-writer`
- **Economical (`haiku`)** — mechanical, deterministic, high-frequency:
  `changelog-gen`, `ascii-grapher`, `test-runner`, `dep-auditor`, `compactor`, `shortcut`, `lingua`

`model` accepts `fable` / `opus` / `sonnet` / `haiku`, a full model ID, or `inherit` (follow
the session default). Changes take effect on the next session — skill frontmatter is read at
session start.

## DDD (Dream-Driven Development)

This project follows the DDD (Dream-Driven Development) methodology, which means the project
is driven by what I envision.

All features are based on my needs and my dreams.
