---
name: agreed-design-run-it
tags: [trigger]
runs: 3
max_turns: 8
timeout_seconds: 300
---

Ward's write-up is in `docs/design/notifications.md`. It splits the notification service
into a queue producer, three channel workers -- email, SMS and push -- and a
delivery-receipt store, and it says the three workers can be built in parallel. Four
people need to be kept in step on it. We agreed the design, now run the implementation.
