# /develop

Start a pair programming session to develop a feature or fix a bug collaboratively.

## Instructions

1. Read the project's README.md and any relevant documentation to understand the codebase,
   architecture, and coding standards.

2. Ask the user what they want to develop or fix. Gather enough context to understand the
   scope of the task.

3. Propose a high-level design and approach. Present a brief implementation plan as a
   markdown table:

   | Step | Description | Status |
   | ---- | ----------- | ------ |

   Wait for the user to confirm before proceeding.

4. Create a new branch for the work:

   ```text
   git checkout -b <type>/<short-description>
   ```

   Use an appropriate branch type: `feat`, `fix`, `refactor`, `docs`, `test`, or `chore`.

5. Implement the code step by step, following the plan. At each step:

   - Explain what you are about to do
   - Write clean, modular code with proper naming conventions
   - Confirm with the user before moving to the next step
   - Invoke `code-reviewer:review` (code-reviewer) to check the step's code quality
   - **Refine**: Fix any Critical or Warning issues reported by the reviewer. Re-invoke
     `code-reviewer:review` until no Critical issues remain. Present Suggestions to the user and apply
     the ones they approve.
   - Proceed to the next step only after the review cycle is clean

6. After all steps are implemented, review the changes with `git diff` and write tests if
   applicable. Invoke `code-reviewer:review` one final time on the complete changeset to catch cross-step
   issues.

7. Invoke `git-committer:commit` (git-committer) to craft and execute the commit. The git-committer will
   handle staging, review (which it skips since code-partner already reviewed), message
   drafting, and user confirmation.

8. Emit a `__SESSION_RESULT__` block summarizing the session: steps planned vs completed,
   review cycles, final verdict, commit hash, whether tests passed, and the overall status
   (COMPLETE, PARTIAL, or ABORTED).
