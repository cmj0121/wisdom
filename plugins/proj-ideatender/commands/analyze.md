# /analyze

Analyze the current project and generate ideas for improvements or new features.

## Instructions

1. Invoke `/check` (context-checker) to verify session health and ecosystem integrity.

2. Read `README.md` and all `.md` files in the project's root directory to understand the project's
   purpose, scope, and guidelines.

3. Locate the main entrypoint file (e.g., `main.py`, `index.js`, `main.go`) and read it to understand
   the coding style and project structure.

4. Run `git log --oneline -20` to review recent development activity and understand the project's
   trajectory.

5. Use the Glob tool to scan the directory layout, identifying key modules, packages, and configuration
   files.

6. Synthesize your findings into a **Project Summary** covering:

   - Purpose and scope
   - Tech stack and architecture
   - Recent development activity
   - Code quality observations

7. Generate 5-10 actionable ideas across these categories:

   - **Feature ideas**: New capabilities aligned with the project's purpose
   - **Improvement ideas**: Enhancements to existing functionality or developer experience
   - **Refactoring ideas**: Structural changes for better maintainability
   - **Documentation ideas**: Gaps in documentation worth filling
   - **Testing ideas**: Opportunities for better test coverage or strategies

8. Present each idea with a title, category, description, and effort estimate (Low / Medium / High).

9. After presenting the ideas, ask the user if they would like to invoke `/spec` (spec-writer)
   to draft a formal specification for any of the ideas.

10. If the user selects ideas for specification, invoke `/spec` and pass the selected idea details
    as context.

11. Emit an `__IDEAS_GENERATED__` block summarizing the total number of ideas, per-category
    counts, whether a spec-writer handoff occurred, and the status (COMPLETE or PARTIAL).

12. This command is **read-only**. Do not modify any files or write any code.
