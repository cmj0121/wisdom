---
name: sketch-before-building
tags: [trigger]
runs: 3
max_turns: 8
timeout_seconds: 300
---

We are pulling billing out of the monolith into something standalone. It has to take
webhook events from Stripe, reconcile them against our own invoice records, and expose a
read surface the dashboard can poll. Nothing exists yet -- no repository, no schema, no
decision on whether it owns its own datastore. Sketch the architecture before we write
anything.
