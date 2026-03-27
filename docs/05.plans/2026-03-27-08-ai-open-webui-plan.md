<!-- Target: docs/05.plans/2026-03-27-08-ai-open-webui-plan.md -->

# Open WebUI Implementation Plan

---

# Open WebUI Plan

## Overview (KR)

이 문서는 Open WebUI의 실행 계획서다. 작업 분해, 검증, 롤아웃, 완료 기준을 정의하여 시스템의 안정적인 구축과 운영을 보장한다.

## Context

Open WebUI is a critical component for the AI tier, providing the primary interface for users and automated RAG workflows. This plan ensures its deployment is standardized and traceable.

## Goals & In-Scope

- **Goals**: 
    - Standardize Open WebUI deployment config.
    - Establish a complete documentation chain.
    - Enable RAG with local Ollama/Qdrant integration.
- **In Scope**:
    - `docs/` hierarchy standardization.
    - `infra/08-ai/open-webui/docker-compose.yml` validation.

## Non-Goals & Out-of-Scope

- **Non-goals**: Optimizing model weights or fine-tuning.
- **Out of Scope**: Infrastructure for external model providers (OpenAI, Anthropic).

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Create PRD, ARD, ADR | `docs/01-03/` | REQ-PRD-FUN-01 | Files created & indexed |
| PLN-002 | Create Technical Spec | `docs/04.specs/` | REQ-PRD-FUN-02 | Contract defined |
| PLN-003 | Create Task List | `docs/06.tasks/` | REQ-PRD-FUN-03 | Maintenance tasks ready |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Verify relative links | `find docs/ -name "*.md" | xargs -n1 grep "\[..\/.*\]"` | All links resolve |
| VAL-PLN-002 | Functional | Check container health | `docker inspect -f '{{.State.Health.Status}}' open-webui` | Status: healthy |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| GPU OOM | High | Limit `qwen3-embedding` concurrency or use CPU fallback |
| SSO Failure | Medium | Maintain internal healthcheck as non-SSO route |

## Completion Criteria

- [x] Scoped documentation completed
- [x] Verification criteria defined
- [x] Indices updated

## Related Documents

- **PRD**: `[../01.prd/2026-03-27-08-ai-open-webui.md]`
- **ARD**: `[../02.ard/0013-open-webui-architecture.md]`
- **Spec**: `[../04.specs/08-ai/open-webui.md]`
- **ADR**: `[../03.adr/0016-open-webui-implementation.md]`
