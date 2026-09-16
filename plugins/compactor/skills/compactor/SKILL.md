---
name: compactor
description: Re-renders the previous result as a dense, scannable table, dropping prose framing but keeping every data point. Use when an answer was longer than it needed to be.
license: MIT
model: haiku
allowed-tools:
  - Read
  - Glob
  - Grep
metadata:
  author: cmj@cmj.tw
  version: "2.1.0"
  shortcut: "compact it"
---

# Compactor

Re-renders the previous result as a compact, table-like view — dense and scannable.

## Shortcut

This skill is triggered when the user's prompt contains `compact it`.

## How It Works

Each phase assumes a source to work from. When Phase 1 finds none — no prior result, or a
reference that resolves to nothing — say so and stop. Compacting nothing produces an empty
table, and an empty table reads as a finding rather than as the absence of one.

### Phase 1: Identify the Source

Default to the most recent substantive assistant message/result. If the user
references something specific, use that instead.

### Phase 2: Choose a Compact Shape

Pick the densest readable form:

| Source shape             | Compact form                 |
| ------------------------ | ---------------------------- |
| Repeating records/fields | Markdown table               |
| Flat attribute set       | key→value two-column table   |
| No table fits            | tight columnar/bulleted list |

### Phase 3: Compact

Drop filler words, prose framing, and redundant labels. Keep every distinct
data point. Align columns. Truncate over-long cells with `…`, but never drop a
column carrying unique info.

### Phase 4: Output

Print the compact view inline. Read-only — never modify files.

### Example

Before:

```txt
The build finished successfully in 12.4 seconds. It produced 3 artifacts:
the main bundle which is 240 KB, the vendor bundle which is 880 KB, and the
runtime which is 4 KB.
```

After:

```markdown
| Artifact | Size   |
| -------- | ------ |
| main     | 240 KB |
| vendor   | 880 KB |
| runtime  | 4 KB   |

Build: OK · 12.4s · 3 artifacts
```

## Constraints

Read-only: reformat only. Never invent or drop data, and never write files.

## Team Coordination

Directly invocable; returns the compacted view to the caller.
