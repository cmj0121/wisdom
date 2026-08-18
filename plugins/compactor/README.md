# Compactor Plugin

> Re-render the previous result into a compact, table-like view.

A shared support tool that takes the previous result and re-renders it as a
dense, scannable, table-like view — stripping prose and filler.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install compactor
```

## How It Works

1. **Identify** — Takes the most recent substantive result, or whatever you point it at
2. **Choose a shape** — Markdown table for repeating records, key→value table for a flat
   attribute set, a tight columnar list when no table fits
3. **Compact** — Drops prose framing and redundant labels, keeps every distinct data point
4. **Output** — Prints the compact view inline

Read-only by design: it reformats what is already there and never invents, drops, or
writes data.

## Usage

### Magic Words

- `compact it` → Compact the previous result

## License

MIT
