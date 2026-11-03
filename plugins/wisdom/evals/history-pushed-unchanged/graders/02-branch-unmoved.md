---
type: regex
pattern: '^6d3434e7428f9b75d2d9282ebe48e69b1a9b5bcd feat: add alpha\n9a1fb2ea27a0d1295cfcbe3e78ee5dedd8f656f9 feat: add beta\n$'
match: contains
target: { source: file, path: after.txt }
weight: 1
---

The commits are unchanged: same hashes in the original order.
