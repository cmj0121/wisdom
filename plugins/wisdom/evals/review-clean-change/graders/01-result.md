---
type: regex
pattern: 'VERDICT: PASS[^\n]*\W*$'
match: contains
weight: 1
---

The message ends in a VERDICT: PASS line.
