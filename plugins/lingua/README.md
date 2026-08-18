# Lingua Plugin

> Discuss in any language — always get answers in yours.

The lingua plugin makes Claude Code reply in a language you choose, no matter what language
you type in. Optionally it also restates your question in clear, correct terminology before
answering. Preferences are remembered per project.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install lingua
```

## How It Works

### Magic Words

Registered via the skill's Shortcut section, so the shortcut plugin auto-dispatches them:

| Magic word          | Effect                                        |
| ------------------- | --------------------------------------------- |
| `lingua`            | Configure preferences, or show current status |
| `respond in <lang>` | Set and persist the response language         |
| `reply in <lang>`   | Same as above                                 |

### First Run

The first time lingua runs in a project it asks three questions:

1. **Response language** — e.g. `zh-TW`, `English`, `日本語`.
2. **Refine questions** — restate each question cleanly before answering? (per project).
3. **Technical terms** — keep code and technical terms in their original language?

Your answers are saved and applied automatically on later sessions.

### Persistence

Rules live in the project's persistence memory — the same place `agent-smith` stores
`LESSONS.md`:

```text
~/.claude/projects/<project-path>/memory/lingua.md
```

The file is per-user-per-project and is never committed.

```yaml
---
respond_in: zh-TW
discuss_in: auto
refine_question: false
keep_terms_in: en
glossary: []
---
```

### Automatic Loading

A `SessionStart` hook loads your saved preference at the start of every session, so replies
come back in your language without typing anything. If no preference is configured, the hook
does nothing.

Because hooks load when a session begins, a newly saved preference takes effect on the **next**
session. Restart Claude Code (or start a new session) to pick up changes.

### Updating

Just say it — "respond in Japanese now", "stop refining", "keep terms in Chinese too".
Lingua rewrites the config and applies the change immediately.

Saying "lingua off" once lingua is active suspends the rules for the rest of the session
without deleting the config; a later "lingua" re-enables them.

## Usage

### Set a language

```text
respond in zh-TW
```

### Show current rules

```text
/lingua
```

### With agent-smith

When `agent-smith` runs, it reads the same config and answers in your language, and passes
it down so the whole scrum team reports back in that language too.

## License

MIT
