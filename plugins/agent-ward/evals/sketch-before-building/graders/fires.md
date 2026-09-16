---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"agent-ward'
min: 1
---

A greenfield component with its boundaries and datastore still open is a design question.
The baseline gave it to ascii-grapher twice and spec-writer once.

Deliberately ungraded: neither of those can be asserted silent, because agent-ward's own
body invokes both -- spec-writer for formal specs and ascii-grapher for diagrams. A
grader on either would fail a correctly routed run.
