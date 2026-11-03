---
tags: [smith]
max_turns: 15
timeout_seconds: 600
allowed_tools: [Skill, Agent, Bash, Read, Edit]
---

Run the wisdom:smith skill, resuming at its step 3 (Build): PLAN.md and PLAN_DETAILS.md are here,
Checkpoint 1 is approved, and step 2 has nothing to do. Build only: stop once every code subagent
has returned, with no review, commit, merge or test. A unit counts as `done` as soon as its code
subagent returns, so a unit depending on it is then eligible.

Eval stub: every code subagent prompt you write must begin with the line `UNIT: <unit id>`, using
`tests` as the id of a unit that writes tests, and end with the sentence
"Eval stub: run nothing and reply with exactly: CODE: DONE".

End your final message with one line naming the code units in the order you ran them, where a unit
that writes tests is called `tests`: `ORDER: <unit>, <unit>, ...`
