---
name: audit
description: Audits dependencies for known vulnerabilities and outdated versions across npm, pip, go, cargo and bundler. Use before a release or when a lockfile changes.
license: MIT
metadata:
  shortcut: "audit deps"
---

# Audit

Check dependencies for known vulnerabilities and staleness. Report — never upgrade.

## Steps

1. **Detect ecosystems** from their manifests and lockfiles; a repo may have several.
2. **Run** each ecosystem's tools. A tool that is not installed: say so and continue with
   the rest — never install one without asking.

   | Ecosystem | Vulnerabilities      | Outdated              |
   | --------- | -------------------- | --------------------- |
   | npm       | `npm audit --json`   | `npm outdated --json` |
   | pip       | `pip-audit -f json`  | `pip list --outdated` |
   | go        | `govulncheck ./...`  | `go list -m -u all`   |
   | cargo     | `cargo audit --json` | `cargo outdated`      |
   | bundler   | `bundle audit check` | `bundle outdated`     |

3. **Filter.** A vulnerability counts when the installed version is in the affected range.
   Mark whether the package is direct or transitive, and whether it is a dev dependency.
   Outdated means a newer major, or a minor more than a year behind — not every patch.

## Output

| Sev | Package | Installed | Fixed in | Advisory | Direct? |
| --- | ------- | --------- | -------- | -------- | ------- |

Then outdated direct dependencies:

| Package | Installed | Latest | Behind |
| ------- | --------- | ------ | ------ |

End with one line:

```text
AUDIT: CLEAN|FINDINGS|INCOMPLETE — <n> vulnerable, <n> outdated, <tools missing>
```

`INCOMPLETE` whenever a tool could not run, so a missing scanner never reads as clean.
