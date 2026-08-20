# Security Reviewer Plugin

> Reviews the whole project source for security issues and maps each finding to a CWE. Use when the
> user wants a security review of the codebase rather than of a diff, since diff-only reviewers
> inspect the current branch and nothing older.

A shared support tool that reads the **whole project** source and surfaces potential
security issues, mapping each to a related CWE ID. Unlike the built-in diff-only
`/security-review` (which only inspects the current branch diff), this reviewer scans
the entire codebase and attaches CWE classifications to every finding.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install sec-review
```

## How It Works

1. **Scope** — Enumerates source with `git ls-files`, skipping vendored and generated code,
   then identifies the languages and entry points in use
2. **Review** — Reads and greps for common weakness classes, mapping each to its CWE
3. **Triage** — Rates findings by severity and discards what the codebase makes unreachable
4. **Report** — Lists each finding with its location, CWE ID, and a concrete fix

Covered weakness classes include injection (SQL, command, template), XSS, hardcoded
secrets, broken authentication and access control, insecure deserialization, path
traversal, SSRF, weak cryptography, and missing input validation.

Read-only: it reports, and never edits the project.

## Usage

### Magic Words

- `sec-review` → Direct invocation
- `security review` → Whole-project security review

## License

MIT
