# Agent Ward Plugin

> Architect agent — designs systems and APIs and decides the tech stack. Use before implementation
> starts on anything non-trivial, when the user asks how something should be structured, weighs one
> library or protocol against another, or needs a design reviewed for consistency.

Named after Ward Cunningham — inventor of the wiki, pioneer of design patterns and agile.

Agent Ward is the architect of the development team. Ward owns system design, API design,
and tech stack decisions. Ward is consulted before coding begins and reviews architectural
consistency after implementation.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install agent-ward
```

## Role in the Team

| Agent             | Role           | Ward's Relationship                        |
| ----------------- | -------------- | ------------------------------------------ |
| **agent-smith**   | Project Leader | Assigns design tasks, forwards escalations |
| **agent-hale**    | Developer      | Implements Ward's designs                  |
| **agent-ellis**   | QA             | Escalates design-level issues via Smith    |
| **spec-writer**   | Support Tool   | Produces formal specs on Ward's behalf     |
| **ascii-grapher** | Support Tool   | Produces architecture diagrams for Ward    |
| **tenth-man**     | Support Tool   | Challenges Ward's designs before handoff   |

## How It Works

1. **Understand** — Reads plan, codebase, and constraints
2. **Design** — Produces architecture, API contracts, data models, tech decisions
3. **Challenge** — Invokes tenth-man to stress-test the design
4. **Handoff** — Reports design to Smith (or user if called directly)

## Usage

### Magic Words

- `design it` → Ward produces a design for the requested feature
- `architect this` → Direct invocation
- `ward` → Direct invocation

## License

MIT
