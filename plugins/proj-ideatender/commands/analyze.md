# /analyze

Analyze the current project and generate ideas for improvements or new features.

## Instructions

1. Read `README.md` and all `.md` files in the project's root directory to understand the project's
   purpose, scope, and guidelines.

2. Locate the main entrypoint file (e.g., `main.py`, `index.js`, `main.go`) and read it to understand
   the coding style and project structure.

3. Run `git log --oneline -20` to review recent development activity and understand the project's
   trajectory.

4. Use the Glob tool to scan the directory layout, identifying key modules, packages, and configuration
   files.

5. Synthesize your findings into a **Project Summary** covering:

   - Purpose and scope
   - Tech stack and architecture
   - Recent development activity
   - Code quality observations

6. Generate 5-10 actionable ideas across these categories:

   - **Feature ideas**: New capabilities aligned with the project's purpose
   - **Improvement ideas**: Enhancements to existing functionality or developer experience
   - **Refactoring ideas**: Structural changes for better maintainability
   - **Documentation ideas**: Gaps in documentation worth filling
   - **Testing ideas**: Opportunities for better test coverage or strategies

7. Present each idea with a title, category, description, and effort estimate (Low / Medium / High).

8. This command is **read-only**. Do not modify any files or write any code.
