# /shortcut

List all available shortcuts registered across user-level, project-level, and plugin-bundled
skill and command files.

## Instructions

1. Scan the following directories for `.md` files:

   - `~/.claude/skills/` and `~/.claude/commands/` (user-level)
   - `.claude/skills/` and `.claude/commands/` (project-level)
   - `plugins/*/skills/` and `plugins/*/commands/` (plugin-bundled)

2. In each file, look for a `## Shortcut` section containing lines like:

   > prompt contains \`{word}\`

   Extract the backtick-quoted `{word}` as the magic word.

3. Present the results as a markdown table:

   | Magic Word | Skill / Command | Source | Description |
   | ---------- | --------------- | ------ | ----------- |

   - **Magic Word**: the extracted keyword
   - **Skill / Command**: the skill or command name (from frontmatter `name` or filename)
   - **Source**: `user`, `project`, or `plugin`
   - **Description**: from the frontmatter `description` field

4. If no shortcuts are found, respond with: "No shortcuts registered."

5. Emit a `__DISPATCH_RESULT__` block summarizing whether a match was found, which magic word
   and skill were involved, the source level, and the status (DISPATCHED, NO_MATCH, or ERROR).
   For direct `shortcut:shortcut` invocation (listing mode), emit with `matched: false` and
   `status: NO_MATCH`.
