---
type: regex
pattern: '\b(missing|no|without|did not return)\b[^\n]*HISTORY'
flags: i
match: contains
weight: 1
---

It tells the user the HISTORY line is missing.
