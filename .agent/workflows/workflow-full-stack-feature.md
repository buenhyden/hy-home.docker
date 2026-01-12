---
description: Comprehensive workflow for implementing a full-stack feature
---

# Full-Stack Feature Workflow

Orchestrates the lifecycle of a new feature from design to deployment.

1. **Design & Specification**
    - Call `/workflow-api-design` to define the contract.
    - Create `ISSUE_TEMPLATE/feature-spec.yml` ticket.

2. **Backend Implementation**
    - Call `/workflow-feature-component` for backend structure.
    - Implement Service/Controller layers (Ref: `200-Backend`).
    - Implement Database migrations (Ref: `300-Data_AI`).
    - Call `/workflow-testing` for Unit/Integration tests.

3. **Frontend Implementation**
    - Call `/workflow-feature-component` for frontend structure.
    - Implement Components/Pages (Ref: `100-Frontend`).
    - Integrate with Backend API.
    - Call `/workflow-testing` for Component/E2E tests.

4. **Review & Refine**
    - Call `/workflow-pr-review` guideline.
    - Call `/workflow-refactoring` if code quality issues found.
    - Call `/workflow-performance-optimization` to check impact.

5. **Documentation**
    - Call `/workflow-docs-update` to update API docs and User guides.

6. **Merge & Deploy**
    - Trigger CI/CD pipeline.
    - Call `/workflow-release`.
