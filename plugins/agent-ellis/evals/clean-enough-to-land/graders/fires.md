---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"agent-ellis'
min: 1
---

Quality, tests and acceptance asked for together, on finished work and before it merges,
are this skill's whole gate rather than any one of the three on its own.

Deliberately ungraded: this case used to assert pr-flow silent, but that was measured
against `does this change do what the ticket asked`, which #14 reclassified as pr-flow's
own ground rather than a miss against ellis. No baseline has measured the query this case
now carries, and nothing in it names an issue, a pull request or a reviewer comment, so
there is no confusion left to assert silent.
