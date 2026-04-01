# Wisdom

> Help your Claude Code more efficiently and effectively, like me

This project is the Claude Code Plug-in for me and you can use it like me.

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

### System Tool

| Tool       | Description                                     |
| ---------- | ----------------------------------------------- |
| `shortcut` | Auto-dispatch skills when you type a magic word |

### Workflow

```text
             plan       design     code (parallel)    review        docs
 ┌──────┐  ┌───────┐  ┌───────┐  ┌──────┐ ┌──────┐  ┌──────┐     ┌───────┐
 │ User │─>│ smith │─>│ ward  │─>│hale-1│ │hale-2│─>│ellis │──┬─>│ twain │
 └──────┘  └───┬───┘  └───────┘  └──────┘ └──────┘  └──┬───┘  │  └───────┘
               │                   ▲  ▲       ▲         │      │
               │                   │  └───────┼── fix ──┘      │   ops
               │                   │  worktree│                │  ┌───────┐
               │                   └──────────┘                └─>│ page  │
               │                                                  └───┬───┘
               │                                              deploy  │
               │           ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘
               │           ┌──────────────────┐
               │           │  ross (optional) │
               │           └──────────────────┘
               │
               │        ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐
               └ ─ ─ ─    tenth-man  spec-writer
                        │ ascii-grapher  test-runner      │
                          changelog-gen  dep-auditor
                        └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘
```

Smith dispatches **independent units to parallel hale instances**, each in an isolated
git worktree. After QA passes, smith merges all worktrees back sequentially.

### Dependency Graph

```text
agent-smith (Project Leader)
    ├──▶ agent-ward (Architect)
    ├──▶ agent-hale (Developer)
    ├──▶ agent-ellis (QA) ──findings──▶ agent-hale (fix) or agent-ward (redesign)
    ├──▶ agent-twain (Technical Writer)
    ├──▶ agent-page (SRE)
    └──▶ agent-ross (Release Manager, optional)

Support tools (invoked by roles as needed):
    spec-writer    ──▶ agent-ward, agent-twain
    tenth-man      ──▶ agent-smith, agent-ward
    ascii-grapher  ──▶ agent-ward, agent-twain, agent-page
    test-runner    ──▶ agent-hale, agent-ellis, agent-page
    changelog-gen  ──▶ agent-ross, agent-twain
    dep-auditor    ──▶ agent-page, agent-ellis

System: shortcut (auto-dispatch)
```

## DDD (Dream-Driven Development)

This project follows the DDD (Dream-Driven Development) methodology, which means the project
is driven by what I envision.

All features are based on my needs and my dreams.
