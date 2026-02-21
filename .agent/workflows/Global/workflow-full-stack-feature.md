---
description: Comprehensive workflow for implementing a full-stack feature
---

# Full-Stack Feature Workflow

Orchestrates the lifecycle of a new feature from design to deployment, utilizing the standard 3-phase Spec-Driven Development approach.

This is a thin-index workflow. To execute the end-to-end SDLC, run the following workflows in sequence:

1. **Phase 1: Pre-Development (Planning & Design)**
   - Call `/workflow-agent-pre-development`
   - *Outputs*: PRD (`docs/prd/`), ADRs (`docs/adr/`), and final implementation Spec (`specs/`).
   - *Gate*: Must receive human approval on the Spec before proceeding.

2. **Phase 2: During-Development (Implementation & Testing)**
   - Call `/workflow-agent-during-development`
   - *Inputs*: The approved Spec from `specs/`.
   - *Execution*: Coder Agents implement business logic and required test layers (Unit/Integration) in the designated root directories (`server/`, `web/`, or `app/`).

3. **Phase 3: Post-Development (Code Review & Operations)**
   - Call `/workflow-agent-post-development`
   - *Execution*: Reviewer Agent verifies spec compliance and security. DevOps Agent creates or updates deployment runbooks in `runbooks/`.

*Note: For specific platform structuring (e.g., separating Web and Server), see [0900-Backend](../../.agent/rules/0900-Backend/0900-backend-standard.md) and [1000-Frontend](../../.agent/rules/1000-Frontend/1003-frontend-project-standard.md) Workspace Separation rules.*
