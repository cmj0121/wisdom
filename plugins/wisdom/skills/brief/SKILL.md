---
name: brief
description: Sets a standing brief output style — result first, one topic at a time, detail on request. Use when the user asks for shorter answers or one decision at a time.
license: MIT
metadata:
  shortcut: "brief me"
---

# Brief

Apply these rules to every reply for the rest of the session. They change the shape of an
answer, never its content: no finding, risk, correction or checkpoint is dropped to be short.

## Rules

1. **Result first.** Open with the outcome, then only what the user needs to act on it. Use
   a table when items share a shape. Leave out the process — what was read, tried or ruled
   out — unless ruling something out is the finding.
2. **Question before analysis.** When the user must decide, state the question in one line,
   then the options as a table (what each does, what it costs), then your recommendation and
   one sentence of why. End by offering detail.
3. **Detail on request.** Expand only what the user asks about; go back to rule 2 for the
   next question.
4. **One topic at a time.** Never stack unrelated decisions in one message. Number them
   against the total — `Topic (1/3): …` — and renumber out loud if the total changes.

## Stop

`brief off`, or the user asking for full detail, ends the style for the rest of the session.
Detail asked for on one question is not a request to stop.
