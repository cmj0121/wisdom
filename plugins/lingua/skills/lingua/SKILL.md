---
name: lingua
description: Answers in the user's chosen language whatever language they write in, and can restate their question in correct terminology first. Use when the user asks to reply in a particular language, or when a project has a stored language preference to load or update.
license: MIT
model: haiku
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
metadata:
  author: cmj@cmj.tw
  version: "2.1.0"
  shortcut: "lingua, respond in, reply in"
---

# Lingua — Response Language

Answer the user in their chosen language, regardless of the language they write in, and
optionally restate their question in clear, correct terminology first. Preferences are
remembered per project.

## Shortcut

This skill is triggered when the user's prompt contains `lingua`, `respond in`, or
`reply in`.

## Config File

Per-project rules live in the project's persistence memory:

```text
~/.claude/projects/<project-path>/memory/lingua.md
```

`<project-path>` is the current working directory with `/` replaced by `-` (the same
convention used for `LESSONS.md`). The file is per-user-per-project and is never committed.

Schema — YAML frontmatter plus freeform notes:

```yaml
---
respond_in: zh-TW # response language (BCP-47 tag or plain name); required
discuss_in: auto # language the user writes in; auto = detect each turn
refine_question: false # restate the user's question cleanly before answering
keep_terms_in: en # keep technical terms / code identifiers in this language
glossary: [] # optional normalizations, e.g. "K8s → Kubernetes"
---
Freeform per-project language notes.
```

## How It Works

### Phase 1: Load

Read the config file for the current project.

- **Exists** → adopt its rules for the rest of the session; go to Phase 3.
- **Missing** → go to Phase 2 (onboard).

Never invent a language. If no rule exists, ask — do not guess from the user's input language.

### Phase 2: Onboard (first run in a project)

Before continuing the conversation, ask the user with `AskUserQuestion`:

1. **Response language** — which language should replies be written in? (e.g. `zh-TW`,
   `English`, `日本語`). Offer a few common choices plus their input language.
2. **Refine questions** — should each question be restated cleanly with correct terminology
   before answering? (on / off). There is no global default; this choice is made per project.
3. **Technical terms** — keep code identifiers and technical terms in their original
   language (recommended), or translate them too?

Write the answers to the config file via `Write`, creating the `memory/` path if needed.
Confirm what was saved in one line, then proceed in the chosen language.

### Phase 3: Apply

For the rest of the session:

- **Respond in `respond_in`.** Translate your entire reply into that language, whatever
  language the user writes in.
- **Keep terms in `keep_terms_in`.** Code, identifiers, commands, filenames, and technical
  terms stay verbatim — do not translate or transliterate them. Apply `glossary`
  normalizations when a listed term appears.
- **If `refine_question: true`**, open the reply with a one-line restatement of what the
  user is asking, cleaned up and using correct terminology, so both sides confirm intent.
  Keep it short; then answer. Skip the restatement for trivial or already-precise prompts.

### Phase 4: Re-memory (update on request)

When the user asks to change any rule mid-session — "respond in Japanese now", "stop
refining", "keep terms in Chinese too" — update the config file with `Edit` (or `Write` if
it must be recreated), confirm the change in one line, and apply it immediately. This also
covers `lingua off`: suspend applying rules for the rest of the session without deleting the
file (a later `lingua` re-enables it).

### Phase 5: Status (direct invocation)

When called directly as `lingua` with no change requested, print the active rules and where
they come from:

| Setting          | Value    | Source           |
| ---------------- | -------- | ---------------- |
| Respond in       | …        | memory/lingua.md |
| Discuss in       | …        | …                |
| Refine questions | on / off | …                |
| Keep terms in    | …        | …                |

If no config exists, say so and offer to onboard.

## Automatic Loading (SessionStart hook)

Once a preference is saved, it applies automatically at the start of every session — no magic
word needed. The plugin's `SessionStart` hook (`hooks/lingua-session-start.py`) reads
`memory/lingua.md` for the current project and injects its rules as session context. When no
preference is configured, the hook is a silent no-op.

Because hooks load when a session starts, a newly saved preference takes effect on the **next**
session; within the current session, Phases 3–4 already apply it live.

## Notes

- Lingua governs **output language only**. It never changes what the user asked for, only how
  the answer is phrased.
- Other skills and agents inherit the preference when they read the same config file — see the
  Smith integration in `agent-smith`.
