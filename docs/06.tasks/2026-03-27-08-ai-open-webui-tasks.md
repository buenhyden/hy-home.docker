<!-- Target: docs/06.tasks/2026-03-27-08-ai-open-webui-tasks.md -->

# Task: Open WebUI Documentation & Verification

---

## Overview (KR)

이 문서는 Open WebUI의 구현·검증 작업 목록이다. Spec과 Plan에서 파생된 작업을 추적 가능하게 기록하여 실질적인 운영 준비 상태를 관리한다.

## Inputs

- **Parent Spec**: `[../04.specs/08-ai/open-webui.md]`
- **Parent Plan**: `[../05.plans/2026-03-27-08-ai-open-webui-plan.md]`

## Working Rules

- Every task must define evidence.
- Documentation-only work still needs validation evidence.
- This document remains the execution-tracking source of truth.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Synthesize PRD/ARD/ADR/Spec/Plan | doc | All | Phase 1 | `ls docs/` | Agent | Done |
| T-002 | Verify Relative Links | doc | All | Phase 1 | `grep` validation | Agent | Done |
| T-003 | Check Infrastructure Readme parity | doc | § Contracts | Phase 1 | Manual review | Agent | Done |
| T-004 | Verify container health & connectivity | ops | § Verification | Phase 2 | `docker inspect` | Operator | Todo |
| T-005 | Test RAG Indexing workflow | eval | § Success Criteria | Phase 2 | Indexing evidence | Engineer | Todo |

## Verification Summary

- **Test Commands**:
  - `grep -r "\[..\/.*\]" docs/` (Link verification)
  - `docker exec open-webui curl -f localhost:8080/health`
- **Eval Commands**:
  - [Self-eval] Check documentation completeness against mandatory templates.
