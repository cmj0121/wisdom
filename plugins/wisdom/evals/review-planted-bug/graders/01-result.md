---
type: regex
pattern: 'VERDICT: FAIL[^\n]*\W*$'
match: contains
weight: 1
---

The message ends in a VERDICT: FAIL line.
