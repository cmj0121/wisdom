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

| Tool            | Description                                                |
| --------------- | ---------------------------------------------------------- |
| `spec-writer`   | Writes technical specs with architecture diagrams          |
| `tenth-man`     | Devil's advocate — challenges assumptions, surfaces risks  |
| `ascii-grapher` | Draws ASCII diagrams for architecture, flows, and concepts |
| `git-committer` | Generates clear, conventional commit messages              |
| `shortcut`      | Auto-dispatch skills when you type a magic word            |

### Workflow

```text
                            ┌──────┐
                            │ User │
                            └──┬───┘
                               │
                               ▼
                 ┌──────────────────────────┐
                 │     PROJECT LEADER       │
                 │     (agent-smith)        │
                 │     plan, dispatch,      │
                 │     coordinate           │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐       ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐
                 │     ARCHITECT            │         Support Tools
                 │     (agent-ward)         │       │                   │
                 │     system design,       │         spec-writer
                 │     tech decisions       │       │ tenth-man         │
                 └────────────┬─────────────┘         ascii-grapher
                              │                     │ git-committer     │
                              ▼                       shortcut
                 ┌──────────────────────────┐       │                   │
                 │     DEVELOPER            │       └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘
                 │     (agent-hale)         │
                 │     implement code       │
                 │     + tests              │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │     QA                   │
                 │     (agent-ellis)        │
                 │     code review, test,   │
                 │     acceptance           │
                 └─────┬──────────────┬─────┘
                       │              │
            ┌──────────┘              └──────────┐
            ▼                                    ▼
┌────────────────────────┐         ┌──────────────────────────┐
│   TECHNICAL WRITER     │         │     SRE                  │
│   (agent-twain)        │         │     (agent-page)         │
│   user docs, API docs, │         │     observability,       │
│   migration guides     │         │     reliability,         │
└────────────────────────┘         │     performance review   │
                                   └────────────┬─────────────┘
                                                │
                                                ▼
                                   ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ────┐
                                     RELEASE MANAGER (optional)
                                   │ (agent-ross)              │
                                     CI/CD, Docker,
                                   │ cloud deploy, tagging     │
                                   └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ──── ─┘
                                                │
                                                ▼
                                        ┌──────────────┐
                                        │   Release    │
                                        └──────────────┘
```

### Dependency Graph

```text
agent-smith (Project Leader)
    ├──▶ agent-ward (Architect)
    ├──▶ agent-hale (Developer)
    ├──▶ agent-ellis (QA) ──findings──▶ agent-hale (fix) or agent-ward (redesign)
    ├──▶ agent-twain (Technical Writer)
    ├──▶ agent-page (SRE)
    └──▶ agent-ross (Release Manager, optional)

Support tools (invoked by any role as needed):
    spec-writer, tenth-man, ascii-grapher, git-committer, shortcut
```

## DDD (Dream-Driven Development)

This project follows the DDD (Dream-Driven Development) methodology, which means the project
is driven by what I envision.

All features are based on my needs and my dreams.
