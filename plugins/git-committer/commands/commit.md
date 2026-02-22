# /commit

Create a git commit with a well-structured message following conventional commit format.

## Instructions

1. Check if a commit template is configured via `git config git.commit.template`. If set,
   read the template file and follow its format.

2. Run `git status` to review the current working tree state. If there are unstaged changes,
   ask the user which files to stage, then run `git add` for the selected files.

3. Run `git diff --staged` to review the changes that will be committed. Understand the full
   scope of the changes.

4. Draft a commit message following the configured template or the conventional commit format:

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

5. Present the draft message to the user and ask for confirmation before executing the commit.

6. Once confirmed, execute `git commit -m "<message>"` with the approved message.
