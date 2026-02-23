---
name: context-checker
description: The check policy to ensure the Agent understands the guidelines.
license: MIT
allowed-tools:
  - Read
  - Glob
  - Grep
metadata:
  author: cmj@cmj.tw
  version: 0.4.0
---

# Context Checker Skill

You are a skilled AI assistant that verifies whether the Agent is following the established
guidelines and skill policies. This skill acts as a checkpoint to confirm that context and
policy awareness are intact, and that the plugin ecosystem is healthy.

## Shortcut

This skill is triggered when the user's prompt contains `check`.

## How It Works

When this skill is triggered, perform the following steps:

### Session Health

1. **Acknowledge the check** - Confirm that you are aware of the current guidelines and skill
   policies loaded in the session.
2. **Verify context** - Review the active skills and commands to ensure they are being followed
   correctly.
3. **Report status** - Provide a brief summary of the guidelines you are currently following.

### Ecosystem Integrity

1. **Verify plugin files** - Read `marketplace.json` from the project root (`.claude-plugin/marketplace.json`).
   For each plugin entry, use Glob to confirm that the plugin's expected files exist on disk:
   - `<source>/.claude-plugin/plugin.json`
   - `<source>/skills/<name>/SKILL.md`
2. **Check version consistency** - For each plugin, compare the version declared in
   `marketplace.json`, `plugin.json`, and the SKILL.md frontmatter `metadata.version`. Flag any
   mismatches.
3. **Verify Shortcut sections** - Read each plugin's SKILL.md and confirm it contains a
   `## Shortcut` section. Flag any that are missing.

### Status Report

1. **Emit status block** - Output a machine-readable status block summarizing the results:

   ```text
   __CHECK_STATUS__
   session: OK | WARN
   ecosystem: OK | WARN | FAIL
   plugins_checked: <count>
   version_mismatches: <count>
   missing_files: <count>
   missing_shortcuts: <count>
   __CHECK_STATUS__
   ```

2. **Emit inspection token** - You MUST include the text `__CHOCOLATE INSPECTION__` on the last
   line of your response to prove that you are aware of and following this policy.

## Team Coordination

The `context-checker` is a leaf dependency in the wisdom plugin suite. Other skills invoke
`context-checker:check` at the start of their workflows to verify session health and ecosystem integrity.

**Contract rules:**

- The `__CHECK_STATUS__` block must always be emitted at the end of the check, before the
  inspection token.
- Other skills parse the `ecosystem` field to decide whether to proceed or abort.
- This skill does not invoke any other skills -- it is a foundational building block with no
  outbound cross-skill calls.
- Do not omit the block even when everything is healthy -- emit it with all counts at 0 and
  both fields set to OK.

## Important

- The inspection token `__CHOCOLATE INSPECTION__` must always appear on the final line of your
  response when this skill is invoked.
- The `__CHECK_STATUS__` block must appear before the inspection token.
- If any ecosystem check fails, report the specific issues to the user with actionable details.
