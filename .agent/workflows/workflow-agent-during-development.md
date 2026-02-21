---
description: AI Backend/Frontend Coder Agent logic for the During-Development phase.
---

# Workflow: Agent During-Development

This workflow defines the execution loop for the **Backend Coder Agent** and **Frontend Coder Agent**.

## 1. Specification Ingestion

**CRITICAL RULE**: Do not write a single line of executable code without an approved spec in `specs/`.

1. Locate the assigned spec in the `specs/` directory.
2. Read the spec and the project's `ARCHITECTURE.md`.
3. If the spec demands a technology forbidden by `ARCHITECTURE.md`, or if an acceptance criteria is impossible, **STOP** and ask the human to update the spec.

## 2. Code Generation & TDD

1. Write the code precisely as dictated by the spec. Do not hallucinate extra features.
2. **QA Testing Mandate**: You must write Unit and Integration tests. If the original PRD defines E2E (End-to-End) or Performance testing (e.g., K6) criteria, you MUST also implement those test suites.
3. Tests must cover the explicit **Given-When-Then** acceptance criteria from the PRD/Spec.
4. Do not omit negative test paths (error handling).

## 3. Self-Correction & Verification

1. Run the local compilation, linters, and type checkers.
2. If errors occur, read the logs and recursively fix your code until the build passes cleanly.
3. Verify test coverage meets the project standard (generally > 80%).
4. **Documentation Sync**: Before finishing, you MUST update any impacted API specifications (e.g., OpenAPI/Swagger) and technical documentation in `docs/` and `specs/` to reflect the final implemented code.

## 4. End State

Notify the human that code implementation and local tests are complete. Request the human to review locally before they trigger the PR and the Reviewer Agent.
