# /check

Verify that the Agent understands and follows the current guidelines and skill policies,
and validate the health of the plugin ecosystem.

## Instructions

### Session Health

1. Review all active skills and commands loaded in the current session. Confirm that you are
   aware of their guidelines and policies.

2. Provide a brief summary of the guidelines you are currently following, including:

   - Active skills and their purposes
   - Any project-specific policies in effect
   - Key behavioral rules you are observing

3. If any guidelines appear to be missing or conflicting, report them to the user.

### Ecosystem Integrity

1. Read `.claude-plugin/marketplace.json` to get the list of registered plugins.

2. For each plugin, verify that the following files exist on disk:

   - `<source>/.claude-plugin/plugin.json`
   - `<source>/skills/<name>/SKILL.md`
   - At least one `<source>/commands/*.md` file

3. For each plugin, compare the version in `marketplace.json`, `plugin.json`, and the SKILL.md
   frontmatter `metadata.version`. Flag any mismatches.

4. Read each plugin's SKILL.md and confirm it contains a `## Shortcut` section. Flag any
   that are missing.

### Status Report

1. Output a `__CHECK_STATUS__` block summarizing session and ecosystem health.

2. You MUST include the text `__CHOCOLATE INSPECTION__` on the last line of your response
   to confirm that you are aware of and following the context-checker policy.
