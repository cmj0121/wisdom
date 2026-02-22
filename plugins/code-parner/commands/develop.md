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

6. After implementation, review the changes with `git diff` and write tests if applicable.

7. Commit the changes following the project's commit template or conventional commit format.
   Always confirm the commit message with the user before executing `git commit`.
