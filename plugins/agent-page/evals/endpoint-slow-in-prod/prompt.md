---
name: endpoint-slow-in-prod
tags: [trigger]
runs: 3
max_turns: 8
timeout_seconds: 300
---

`GET /api/orders/:id` sits at p99 3.4s in production but 40ms on staging against a
database of the same size. It started after last Thursday's deploy. There is nothing in
the error logs, CPU is flat across all four pods, and the only graph that moved is
connection-pool wait time. Why is this endpoint slow in production?
