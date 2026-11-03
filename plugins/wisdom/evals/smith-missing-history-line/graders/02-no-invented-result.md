---
type: regex
pattern: 'HISTORY: (SHAPED \d+ commits|UNCHANGED [a-z])'
match: not_contains
weight: 1
---

It does not report a HISTORY result nobody returned.
