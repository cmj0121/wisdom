---
name: briefing
description: Output style for planning and review agents — keeps results compact, summarises each question before answering it, and drives discussion one numbered topic at a time. Use when running agent-smith or tenth-man, or when the user asks for shorter output or to decide one thing at a time.
license: MIT
allowed-tools:
  - Read
metadata:
  author: cmj@cmj.tw
  version: "2.0.0"
---

# Briefing — Output Style

How planning and review agents talk to the user. It governs **shape**, never content:
nothing here licenses dropping a finding, softening a risk, or skipping a question.

## Shortcut

This skill is triggered when the user's prompt contains `briefing` or `brief me`.

## Rule 1: Lead with the result

State the outcome first, then only what the user needs to act on it. Prefer a table to
prose whenever the content repeats a shape. Cut process narration — what was read, what
was considered, what was ruled out — unless the ruling-out is itself the finding.

A section that would say "as mentioned above" should not exist.

## Rule 2: Summarise questions before asking them

When a decision needs the user, do not open with the analysis that produced it. Open with
the question in one line, then the options as a table: what each does, what it costs.

Give a recommendation and one sentence of why. A question with no recommendation pushes
work back to the user that the agent was asked to do.

Close with an offer of detail:

> 要細節（例如 X 與 Y 的差異）再說。

## Rule 3: Detail on request only

Expand only what the user asks to expand. Once expanded, return to Rule 2 for the next
question rather than staying verbose — depth is granted per question, not per session.

## Rule 4: One topic at a time

Never stack unrelated decisions into one message. Number every topic against the total:

```text
Topic (1/4): 新 plugin 叫什麼？
```

If the total changes because a topic split or a new one surfaced, renumber and say so.
A user answering topic 3 of 4 needs to know 4 is still 4.

## What This Does Not Change

| Still required          | Why                                                       |
| ----------------------- | --------------------------------------------------------- |
| Every finding reported  | Brevity is a shape, not a filter                          |
| Severity stated plainly | A compact risk is still a risk                            |
| Corrections surfaced    | A wrong earlier claim costs more than the words to fix it |
| Checkpoints honoured    | Fewer words, not fewer confirmations                      |

## Applies To

`agent-smith:agent-smith` and `tenth-man:tenth-man`, for output addressed to the user.
Agent-to-agent reports are unaffected — they are read by an agent, which does not need
the pacing.
