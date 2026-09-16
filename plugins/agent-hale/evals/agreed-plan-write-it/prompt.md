---
name: agreed-plan-write-it
tags: [trigger]
runs: 3
max_turns: 8
timeout_seconds: 300
---

This morning's review landed on parsing the config once at startup, caching it in a
module-level singleton, and failing loudly on a missing key instead of quietly
defaulting. Nobody objected and nothing else is open. The plan is agreed -- write it.
