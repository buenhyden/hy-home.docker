---
description: Initialize workspace rules and structural pillars
---

# Project Initialization Workflow

1. **Directory Pruning (Usage Analysis)**: Ask the user about the project's primary purpose. If it is a backend-only project, suggest deleting the `web/` and `app/` directories. If it's frontend-only, suggest deleting `server/` and `app/`. Optimize the repository structure before proceeding.
2. Verify that the collaboration agreements are formally documented:
   - Expected path: `docs/manuals/collaboration-guide.md`
   - If missing or incomplete, halt and ask the user to fill out the 11 items in the **Development Process & Collaboration Checklist** using `templates/guides/collaboration-guide-template.md`.
3. Verify that the QA & Security agreements are formally documented:
   - Expected path: `docs/manuals/qa-security-guide.md`
   - If missing or incomplete, halt and ask the user to fill out the 11 items in the **QA & Security Checklist** using `templates/guides/qa-security-guide-template.md`.
4. Verify that the Operations & Deployment agreements are formally documented:
   - Expected path: `docs/manuals/operations-guide.md`
   - If missing or incomplete, halt and ask the user to fill out the 11 items in the **Operations & Deployment Checklist** using `templates/guides/operations-guide-template.md`.
5. Identify the active implementation plan (e.g., `specs/auth/plan.md`).
6. Confirm the feature PRD exists and is approved:
   - Expected path: `docs/prd/<feature>-prd.md`
7. Confirm the feature spec exists and references the PRD:
   - Expected path: `specs/<feature>/spec.md`
   - The spec MUST include a `PRD Reference` line and traceability IDs.
8. Complete QA prerequisites in the spec before coding:
   - Fill `templates/engineering/spec-template.md` Section 0: **Quality / Testing / Security Checklist (Fill Before Implementation)**
   - Fill `templates/engineering/spec-template.md` Section 7: **Verification Plan (Unit/Integration/E2E/Load + coverage targets)**
   - If E2E or Load testing is not applicable, write `N/A (reason: ...)` in the Verification Plan.
9. If you make a significant architectural decision, create an ADR and link it from the spec:
   - Use `templates/architecture/adr-template.md` to track the decision.
10. If you introduce or change a reusable implementation pattern, create/update an ARD and link it from the spec:

- `docs/ard/*.md` (living reference, kept current with code)

1. Verify that the plan contains a "Technical Context" section.
2. Install project dependencies based on the designated tech stack (e.g. `npm install`, `poetry install`, `cargo build`).

3. Verify that the relevant rule files have been copied to `.agent/rules/`.
4. Execute any project scaffolding commands identified in the setup output (e.g., `npm install`).
5. Confirm 100% adherence to the project's [Onboarding Guide](../../../README.md).
