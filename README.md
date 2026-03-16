# Wisdom

> Help your Claude Code more efficiently and effectively, like me

This project is the Claude Code Plug-in for me and you can use it like me.

## Installation

Add the wisdom marketplace to your Claude Code and install the plugin.

```bash
/plugin marketplace add cmj0121/wisdom
```

### Plugins

The wisdom plugin is the all-in-one plugin for me, for those the developer who want to code like me.
This plugin includes all the features that I use in my coding routine, and it is designed to help you
code more efficiently and effectively, just like me.

| Feature         | Description                                                                |
| --------------- | -------------------------------------------------------------------------- |
| shortcut        | AI agent can be triggered automatically when you type a specific shortcut. |
| agent-smith     | Team leader agent: dispatches jobs to specialized agents.                  |
| proj-ideatender | Project owner: analyzes project context, produces brief plans.             |
| spec-writer     | Spec writer: writes technical specs with architecture diagrams.            |
| agent-hale      | Programmer agent: writes code based on plan and spec.                      |
| agent-ellis     | Code reviewer agent: reviews code, reports findings.                       |
| git-committer   | The git committer to help you commit your code.                            |
| ascii-grapher   | Draw ASCII diagrams for architecture, flows, and concepts.                 |

#### Dependency Graph

```text
agent-smith (Leader)
    ├──▶ proj-ideatender (Project Owner)
    ├──▶ spec-writer ─────┬──▶ proj-ideatender
    │                     └──▶ ascii-grapher
    ├──▶ agent-hale (Programmer)
    ├──▶ agent-ellis (Code Reviewer) ──reports──▶ agent-hale or proj-ideatender
    └──▶ git-committer ──▶ agent-ellis

shortcut, ascii-grapher    (no team dependencies)
```

## DDD (Dream-Driven Development)

This project follows the DDD (Dream-Driven Development) methodology, which means the project
is driven by what I envision.

All features are based on my needs and my dreams.
