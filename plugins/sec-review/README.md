# Security Reviewer Plugin

> Whole-project security reviewer mapping findings to CWE.

A shared support tool that reads the **whole project** source and surfaces potential
security issues, mapping each to a related CWE ID. Unlike the built-in diff-only
`/security-review` (which only inspects the current branch diff), this reviewer scans
the entire codebase and attaches CWE classifications to every finding.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install sec-review
```

## Usage

### Magic Words

- `sec-review` → Direct invocation
- `security review` → Whole-project security review

## License

MIT
