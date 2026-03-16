---
layer: agentic
---

# Documentation Refactor Implementation Plan
n**Overview (KR):** 기존 기술 문서의 구조적 정렬 및 메타데이터 동기화를 위한 리팩토링 단계입니다.

> **Technical Specification**: `[../specs/refactor-docs-spec.md]`

## Milestone 1: Core Metadata and Hubs (DONE)

- [x] Add `layer` metadata to README and core files.
- [x] Create entrypoint hubs for `operations/incidents` and `operations/postmortems`.

## Milestone 2: Agentic Logic (DONE)

- [x] Refactor `gateway.md` for lazy loading categories.
- [x] Update `core-governance.md` with flat taxonomy paths.
- [x] Create centralized `instructions.md`.

## Milestone 3: Project Documentation (DONE)

- [x] Create PRD for the refactor project.
- [x] Create ARD for the refactor project.
- [x] Create ADR for the refactor project.
- [x] Create Technical Spec.
- [x] Finalize project log/plan.

## Milestone 4: Operations and Runbooks (DONE)

- [x] Create `docs/runbooks/documentation-maintenance.md`.
- [x] Create example incident report.
- [x] Create example postmortem report.

## Milestone 5: Verification (DONE)

- [x] Validate 100% metadata coverage.
- [x] Run link integrity checks.
- [x] Final Walkthrough.

## References

- [../prd/README.md]
- [../specs/README.md]
