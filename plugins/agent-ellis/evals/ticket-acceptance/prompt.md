---
name: ticket-acceptance
tags: [trigger]
runs: 3
max_turns: 8
timeout_seconds: 300
---

I've finished the branch for WIS-214. The ticket asked for rate limiting on the public
API -- 100 requests a minute per key, a 429 once that is exceeded, and a `Retry-After`
header on the way out. The code is in `src/middleware/ratelimit.ts` with a test file
beside it. Does this change do what the ticket asked?
