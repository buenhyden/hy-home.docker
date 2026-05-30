---
layer: agentic
---

# Documentation Workflow

This workflow dictates how documentation is generated and maintained by Gemini within the Antigravity IDE.

## 1. Objective

Ensure that all markdown documentation and plans strictly adhere to the Template Contracts defined in `docs/99.templates/`.

## 2. Pipeline Steps

1. **Review Requirement**: Analyze user prompt and identify the correct stage-gate template (e.g., `prd.template.md`, `task.template.md`).
2. **Determine Reasoning Effort (Model)**:
   - If generating architectural concepts or planning from scratch, use `gemini-3.1-pro`.
   - If only formatting, organizing, or summarizing existing context, use `gemini-3.5-flash`.
3. **Execute Draft**: Use the chosen template to draft the document in `_workspace/`.
4. **Validation**: Check against the template's placeholder constraints and ensure all links are target-relative.
5. **Finalize**: Move to the designated stage folder under `docs/`.
