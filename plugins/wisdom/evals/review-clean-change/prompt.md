---
tags: [review]
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Bash, Read, Grep, Glob]
---

Run the wisdom:review skill on `git diff main...HEAD`. Purpose: `total` returns the sum of all
the prices it is given. Tests, from the caller: `python3 test_cart.py` passed 2/2, so do not run
them again. End your final message with the skill's verdict line.
