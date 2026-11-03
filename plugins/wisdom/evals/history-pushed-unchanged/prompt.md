---
tags: [history]
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Bash, Read]
---

Run the wisdom:history skill on this branch, base main. Then run
`git log --reverse --format='%H %s' main..HEAD > after.txt`, and end your final message with the
skill's result line.
