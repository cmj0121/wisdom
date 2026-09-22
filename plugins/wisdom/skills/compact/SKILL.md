---
name: compact
description: Re-renders the previous answer as a dense, scannable table, dropping prose but keeping every data point. Use when an answer ran longer than it needed to.
license: MIT
metadata:
  shortcut: "compact it"
---

# Compact

Re-render one earlier result in its densest readable form. Reformat only: never add, drop
or reinterpret a data point, and never write files.

## Steps

1. **Source:** the most recent substantive answer, unless the user points at another. None
   exists: say so and stop — an empty table reads as a finding.
2. **Shape** — the first that fits:
   - repeating records → a table, one row per record
   - a flat set of attributes → a two-column key / value table
   - neither → a tight list, one fact per line
3. **Compress:** drop framing, filler and repeated labels; keep every number, name, status
   and caveat. Shorten a long cell with `…`, but never drop a column that holds unique data.
4. **Print** the result inline, then one summary line if the source had a conclusion.

## Example

Before: "The build finished in 12.4 seconds and produced three artifacts: the main bundle at
240 KB, the vendor bundle at 880 KB, and the runtime at 4 KB."

After:

| Artifact | Size   |
| -------- | ------ |
| main     | 240 KB |
| vendor   | 880 KB |
| runtime  | 4 KB   |

Build: OK · 12.4 s · 3 artifacts
