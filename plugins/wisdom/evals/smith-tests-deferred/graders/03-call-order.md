---
type: regex
pattern: 'UNIT: U1\b.*UNIT: U2\b.*UNIT: tests\b'
flags: s
match: contains
target: trace
weight: 1
---

The code subagents were launched in the order U1, U2, tests.
