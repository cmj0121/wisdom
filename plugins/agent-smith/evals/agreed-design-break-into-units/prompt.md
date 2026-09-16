---
name: agreed-design-break-into-units
tags: [trigger]
runs: 3
max_turns: 8
timeout_seconds: 300
---

The design write-up is in `docs/design/notifications.md` and nobody has anything left to
raise on it. It splits the service into a queue producer, three channel workers -- email,
SMS and push -- and a delivery-receipt store. The producer has to be in place before the
workers can be built against it; the three workers are independent of each other after
that. We agreed the design -- now break it into units and run the iterations.
