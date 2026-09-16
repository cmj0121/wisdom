---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"briefing'
min: 0
max: 0
---

Relabelled by #25 and #24 after this case fired 0x on three runs. A dozen more to come does make
this a standing instruction rather than a request to redo the last answer — but briefing holds no
state to set. Its `allowed-tools` is `Read` alone, with no config file and no session hook, so
leading with the result for the rest of the afternoon is something the session can just do, and a
standing instruction it can honour unaided is not a skill invocation.
