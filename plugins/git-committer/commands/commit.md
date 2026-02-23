# /commit

Create a git commit with a well-structured message following conventional commit format.

## Instructions

1. Invoke `/check` (context-checker) to verify session health and ecosystem integrity.

2. Check if a commit template is configured via `git config git.commit.template`. If set,
   read the template file and follow its format.

3. Run `git status` to review the current working tree state. If there are unstaged changes,
   ask the user which files to stage, then run `git add` for the selected files.

4. Run `git diff --staged` to review the changes that will be committed. Use Grep to scan
   staged files for debug artifacts (`console.log`, `debugger`, `TODO`) that should not be
   committed. Understand the full scope of the changes.

5. **Quality gate**: Invoke `/review` (code-reviewer) to validate the staged changes. If the
   reviewer reports Critical findings, abort the commit. If the reviewer reports Warnings,
   present them to the user. **Skip this step when invoked by `/develop` (code-partner)**,
   which already runs its own review cycle.

6. Draft a commit message following the configured template or the conventional commit format:

   ```txt
   <type>(scope): <Short description>

       <body>

       <footer>

       Committer: <model name>
   ```

   - **type**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, etc.
   - **scope**: the affected area of the codebase
   - **body**: explanation of the change, indented with one tab or four spaces, wrapped at 72 chars
   - **footer**: issue references or breaking changes, indented with one tab or four spaces
   - **Committer**: your model name

7. Present the draft message to the user and ask for confirmation before executing the commit.

8. Once confirmed, execute `git commit -m "<message>"` with the approved message.

9. Emit a `__COMMIT_RESULT__` block summarizing the commit hash, branch, type, scope, status
   (COMMITTED, ABORTED, or ERROR), and whether the review was skipped.
