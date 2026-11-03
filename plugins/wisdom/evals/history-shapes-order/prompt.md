---
tags: [history]
max_turns: 15
timeout_seconds: 600
allowed_tools: [Skill, Bash, Read]
---

Run the wisdom:history skill on this branch, base main. Then print the output of
`git log --reverse --format=%s main..HEAD` in your final message, and end it with the
skill's result line.
