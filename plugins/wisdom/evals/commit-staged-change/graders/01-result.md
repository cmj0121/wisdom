---
type: regex
pattern: 'COMMIT: [0-9a-f]{7,40}\W*$'
match: contains
weight: 1
---

The message ends in COMMIT: and a hash.
