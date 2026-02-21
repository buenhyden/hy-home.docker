---
description: Standard workflow for implementing features or components
---

# Feature/Component Implementation Workflow

Based on `098-core-create-command-specific.md`, `102-frontend-project-structure-specific.md`, and `202-backend-project-structure-specific.md`.

1. **Analysis**
    - Understand requirements.
    - Confirm PRD + Spec gates:
      - PRD is **Approved**: `docs/prd/<feature>-prd.md`
      - Spec exists and references PRD: `specs/<feature>/spec.md`
    - Identify domain/feature area.

2. **Structure Creation**
    - Create directory structure if needed (Feature-first).
    - Frontend: `src/features/<feature>/`
    - Backend: `src/<domain>/`

3. **Scaffolding**
    - Create base files (Controller/Service or Component/Hook).
    - Add types/DTOs.

4. **Implementation**
    - Implement core logic.
    - Follow strict typing rules.

5. **Testing**
    - Add unit tests co-located or in `tests/`.
    - Minimum expectations:
      - **Unit**: required for all new/changed logical branches.
      - **Integration**: required when changing boundaries (API, DB, external services).
      - **E2E**: required for critical user journeys; otherwise document `N/A (reason: ...)` in the Spec Verification Plan.
      - **Load/Performance**: required for high-traffic or latency-sensitive paths; otherwise document `N/A (reason: ...)` in the Spec Verification Plan.
    - Follow test standards (AAA, isolation, determinism) and keep tests traceable to `REQ-*` / `VAL-*` IDs.
    - Use testing workflows as needed:
      - `.agent/workflows/Testing/workflow-testing.md`
      - `.agent/workflows/Testing/workflow-jest-testing.md` (unit/TDD)
      - `.agent/workflows/Testing/workflow-playwright-testing.md` (E2E)
    - Ensure changes map back to PRD/Spec requirement IDs and update the spec if scope changed.
