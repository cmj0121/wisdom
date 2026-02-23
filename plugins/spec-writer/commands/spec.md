# /spec

Write technical specifications for the current software project.

## Instructions

1. If the user has not provided specific requirements, invoke `/analyze` (proj-ideatender) to
   gather project context and understand improvement opportunities. Skip this step if invoked
   as a handoff from `/analyze` or if the user provides explicit requirements.

2. Check whether a `README.md` file exists in the project root. If it is missing, inform the user
   and ask them to create one before proceeding.

3. Read the existing `README.md` to understand the project's purpose, top features, and examples.

4. Scan the project structure using Glob to identify existing documentation files, source code
   layout, and any `docs/` directory content.

5. Ask the user what kind of specification they need. Common options include:

   - **CONCEPTS.md**: Core concepts, architecture, and design principles
   - **Technical spec**: Implementation details and requirements inside `docs/`
   - **Full specification suite**: Both of the above

6. Draft the specification documents following these rules:

   - Keep each file under 5000 words or 800 lines
   - Use clear headings, bullet points, and code blocks for readability
   - Include reference links between related documents
   - Be precise about requirements, constraints, and expected behavior

7. Invoke `/review` (code-reviewer) to validate the quality of the drafted specifications.

8. If the reviewer reports Critical or Warning findings, fix the issues in the draft and
   re-invoke `/review` until no Critical issues remain. Present Suggestions to the user
   and apply the ones they approve.

9. Present the final draft to the user and ask for confirmation before writing the files.

10. Once confirmed, write the specification files to the appropriate locations.
