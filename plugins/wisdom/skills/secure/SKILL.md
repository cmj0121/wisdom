---
name: secure
description: Reviews source code for security vulnerabilities and maps each finding to a CWE. Use when security is the question — the whole project, or the scope given.
license: MIT
metadata:
  shortcut: "sec review"
---

# Secure

Find security flaws in source and report each with its CWE. Read-only: report, never fix.

## Scope

The caller's scope (a diff, a directory, a file), else the whole project. For a diff, also
read the code the diff calls into — a flaw is often at the boundary it crosses. Skip vendored
code, lockfiles and generated files; dependencies are `wisdom:audit`'s job.

## Steps

1. **Map the attack surface:** entry points (routes, handlers, CLI args, message consumers,
   file and env input), trust boundaries, and where secrets and user data flow.
2. **Trace untrusted input** from each entry point to where it is used, and check each class
   below along the way.
3. **Confirm** every candidate by reading the code path; drop what an existing guard already
   handles. A finding you cannot trace end to end is `Low` with "unconfirmed" in its text.

## Classes

| Class                          | CWE          |
| ------------------------------ | ------------ |
| SQL / command / code injection | 89 / 78 / 94 |
| Cross-site scripting           | 79           |
| Path traversal                 | 22           |
| SSRF                           | 918          |
| Missing or broken authz        | 862 / 863    |
| Broken authentication          | 287          |
| Hardcoded secret               | 798          |
| Weak or misused crypto         | 327 / 330    |
| Unsafe deserialization         | 502          |
| Sensitive data in logs         | 532          |
| Missing input validation       | 20           |

Other flaws get their nearest CWE.

## Output

| Sev | CWE | Location | Finding | Fix |
| --- | --- | -------- | ------- | --- |

Severity: `Critical` exploitable remotely without auth · `High` exploitable with some access
· `Medium` needs an unlikely precondition · `Low` hardening. Most severe first, then one line:

```text
SECURITY: CLEAN|FINDINGS — <n> critical, <n> high, <n> medium, <n> low
```
