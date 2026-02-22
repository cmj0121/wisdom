# /spec

Write technical specifications for the current software project.

## Instructions

1. Check whether a `README.md` file exists in the project root. If it is missing, inform the user
   and ask them to create one before proceeding.

2. Read the existing `README.md` to understand the project's purpose, top features, and examples.

3. Scan the project structure using Glob to identify existing documentation files, source code
   layout, and any `docs/` directory content.

4. Ask the user what kind of specification they need. Common options include:

   - **CONCEPTS.md**: Core concepts, architecture, and design principles
   - **Technical spec**: Implementation details and requirements inside `docs/`
   - **Full specification suite**: Both of the above

5. Draft the specification documents following these rules:

   - Keep each file under 5000 words or 800 lines
   - Use clear headings, bullet points, and code blocks for readability
   - Include reference links between related documents
   - Be precise about requirements, constraints, and expected behavior

6. Present the draft to the user and ask for confirmation before writing the files.

7. Once confirmed, write the specification files to the appropriate locations.
