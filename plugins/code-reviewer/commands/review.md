# /review

Perform a code review on the current branch and provide feedback on code quality.

## Instructions

1. Run `git status` to check the current branch and working tree state. Run `git log --oneline -10`
   to understand the recent commit history.

2. Run `git diff` to identify the changed files and their modifications. If the branch has diverged
   from `main`, use `git diff main...HEAD` to see all changes introduced by the branch.

3. Read the project's `README.md` and `CONTRIBUTING.md` (if they exist) to understand the project's
   conventions and coding standards.

4. Use Glob to find the relevant source files and Read to examine the code. Focus on the files that
   have been changed or added.

5. Review the code against best practices, design patterns, and coding standards. Check for:

   - **Clarity**: Is the code easy to read and understand?
   - **Naming**: Are variables, functions, and classes named clearly and consistently?
   - **Error handling**: Are errors and edge cases handled properly?
   - **Performance**: Are there any obvious performance issues?
   - **Security**: Are there any potential security vulnerabilities?
   - **Tests**: Is there adequate test coverage for the changes?

6. Present the review as a structured report with findings categorized by severity:

   - **Critical**: Issues that must be fixed (bugs, security vulnerabilities, data loss risks)
   - **Warning**: Issues that should be addressed (poor error handling, performance concerns)
   - **Suggestion**: Improvements that would enhance code quality (readability, naming, style)

   Include specific file paths and line references for each finding.
