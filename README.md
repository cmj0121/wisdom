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
| code-reviewer   | The code reviewer to help you review your code.                            |
| proj-ideatender | The project idea tender to help you generate project ideas.                |
| git-committer   | The git committer to help you commit your code.                            |
| spec-writer     | The spec writer to help you write the spec for your code.                  |
| code-partner    | The code partner to help you code together with the AI agent.              |
| agent-smith     | Fully autonomous development agent: idea in, code out.                     |

#### Dependency Graph

```text
agent-smith ─────┐
                 ├──▶ git-committer ──▶ code-reviewer
code-partner ────┤
                 ├──▶ code-reviewer
                 └──▶ proj-ideatender

spec-writer ─────┬──▶ code-reviewer
                 └──▶ proj-ideatender

shortcut, code-reviewer, proj-ideatender    (no dependencies)
```

## DDD (Dream-Driven Development)

This project follows the DDD (Dream-Driven Development) methodology, which means the project
is driven by what I envision.

All features are based on my needs and my dreams.
