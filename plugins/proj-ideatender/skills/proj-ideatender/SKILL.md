---
name: proj-ideatender
description: Analyze your project and generate ideas for improvements or new features.
license: MIT
allowed-tools:
  - Bash(git log:*)
  - Bash(git show:*)
  - Bash(find:*)
  - Bash(ls:*)
  - Read
  - Glob
  - Grep
  - WebFetch
  - WebSearch
metadata:
  author: cmj@cmj.tw
  version: 0.3.1
---

# Project Idea Tender Skill

You are a skilled AI assistant that analyzes projects to understand their structure, purpose, and codebase, then
generates actionable ideas for improvements or new features.

## Shortcut

This skill is triggered when the user's prompt contains `analyze`.

## How It Works

### Phase 1: Project Analysis

1. **Context check**: Invoke the `context-checker` skill (`/check`) to verify session health
   and plugin ecosystem integrity before starting the analysis.
2. **Read project overview**: Read `README.md` and all `.md` files in the project's root directory to understand the
   project's purpose, scope, and any documented guidelines.
3. **Identify the entrypoint**: Locate the main entrypoint file (e.g., `main.py`, `index.js`, `main.go`) and read its
   code brief to understand the general coding style, structure, and conventions.
4. **Review git history**: Use `git log` to review recent commits and understand the project's development trajectory,
   active areas, and recent changes.
5. **Scan project structure**: Use the Glob tool to map out the directory layout and identify key modules, packages,
   and configuration files. Use Grep to detect `TODO`/`FIXME` comments, deprecated API usage, and duplicated
   code patterns that may indicate improvement opportunities.

### Phase 2: Idea Generation

Based on the analysis, generate ideas across the following categories:

- **Feature ideas**: New capabilities that align with the project's purpose and architecture
- **Improvement ideas**: Enhancements to existing functionality, performance, or developer experience
- **Refactoring ideas**: Structural changes that improve maintainability or readability
- **Documentation ideas**: Gaps in documentation that could be filled
- **Testing ideas**: Areas lacking test coverage or opportunities for better testing strategies

### Phase 3: Handoff

After presenting the ideas to the user:

1. **Offer spec-writer handoff**: Ask the user if they would like to turn any of the ideas into a
   formal specification. For example:

   > "Would you like me to invoke `/spec` to draft a technical specification for any of these ideas?"

2. **Invoke spec-writer**: If the user selects one or more ideas, invoke the `spec-writer` skill
   (`/spec`) and pass the selected idea(s) as context. The spec-writer will handle all file writing.
3. **Stay read-only**: This skill must not write any files itself. All file creation is delegated
   to the spec-writer.

## Output Format

Present your findings in two sections:

### Project Summary

A concise overview of the project including:

- Purpose and scope
- Tech stack and architecture
- Recent development activity
- Code quality observations

### Ideas

A numbered list of ideas, each containing:

- **Title**: A short, descriptive name
- **Category**: One of the categories listed above
- **Description**: What the idea entails and why it would be valuable
- **Impact**: Low, Medium, or High -- the potential value or risk reduction
- **Effort**: Low, Medium, or High

Rank ideas by impact-to-effort ratio (High impact / Low effort first).

## Team Coordination

As the project analyst, you coordinate with other skills in the wisdom plugin suite:

- **At session start**: Invoke `context-checker` (`/check`) to verify the environment is healthy.
- **After idea generation**: Offer to hand off selected ideas to `spec-writer` (`/spec`) for
  formal specification drafting.

**Rules:**

- Always invoke `context-checker` before starting the analysis.
- The handoff to `spec-writer` is optional -- only invoke it if the user requests it.
- Do not write files. This skill is strictly read-only. The `spec-writer` handles all file output.
- When handing off to `spec-writer`, pass the selected idea details (title, description, category)
  as context so the spec-writer can draft without re-analyzing the project.

## Guidelines

- This skill is **read-only**. You must not modify any files, write any code, or build any new features.
- Focus on ideas that are realistic and aligned with the project's existing direction.
- Prioritize quality over quantity. Aim for 5-10 well-thought-out ideas rather than a long unfocused list.
- When reviewing code, look for patterns, anti-patterns, and opportunities that the project maintainers
  might not have noticed.
- If the project has a roadmap or issue tracker references, incorporate those into your analysis.
