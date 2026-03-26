<!-- Target: docs/05.plans/2026-03-26-08-ai-standardization.md -->

# 08-ai Documentation Standardization Plan

## Overview (KR)

이 문서는 `08-ai` 계층의 문서 표준화 작업을 위한 실행 계획서다. 프로젝트의 "Thin Root" 아키텍처 및 "Golden 5" 태조노미에 따라 거버넌스 문서군을 생성하고 정렬한다.

## Context

`08-ai` 계층의 인프라 정보가 파편화되어 있어, 프로젝트 전체의 AI 전략 및 에이전트 가시성을 높이기 위해 표준 템플릿 기반의 문서 시스템으로 이관이 필요하다.

## Goals & In-Scope

- **Goals**:
  - `08-ai` 계층 전용 PRD, ARD, ADR, Spec 문서 구축.
  - 각 문서 계층별 README 갱신 및 상호 참조 링크 무결성 확보.
- **In Scope**:
  - `docs/01.prd` ~ `docs/06.tasks` 내 관련 문서 생성.
  - 상위 템플릿 준수 및 린트 오류 수정.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-01 | PRD/ARD 생성 및 README 갱신 | `docs/01.prd/`, `docs/02.ard/` | REQ-01 | 파일 존재 및 링크 정상 |
| PLN-02 | ADR/Spec 생성 및 README 갱신 | `docs/03.adr/`, `docs/04.specs/` | REQ-02 | 파일 존재 및 링크 정상 |
| PLN-03 | Plan/Task 생성 및 README 갱신 | `docs/05.plans/`, `docs/06.tasks/` | REQ-03 | 파일 존재 및 링크 정상 |
| PLN-04 | 전역 린트 이슈 수정 | 생성된 모든 md 파일 | REQ-04 | markdownlint 통과 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-01 | Linkage | 모든 상대 경로 링크 유효성 확인 | `ls -l [path]` | 모든 링크 대상 파일 실제 존재 |
| VAL-PLN-02 | Format | 템플릿 필수 섹션 포함 여부 확인 | `grep "Overview (KR)" [file]` | 모든 파일에 섹션 포함됨 |

## Completion Criteria

- [x] PRD/ARD/ADR/Spec 생성 완료
- [ ] Plan/Task 생성 완료
- [x] 각 계층 README 링크 업데이트 완료
- [ ] 모든 문서 린트 및 링크 검증 완료

## Related Documents

- **PRD**: [2026-03-26-08-ai.md](../01.prd/2026-03-26-08-ai.md)
- **ARD**: [0008-ai-architecture.md](../02.ard/0008-ai-architecture.md)
- **Spec**: [08-ai/spec.md](../04.specs/08-ai/spec.md)
- **ADR**: [0008-ollama-openwebui-local-ai.md](../03.adr/0008-ollama-openwebui-local-ai.md)
