<!-- Target: docs/05.plans/2026-03-26-04-data-standardization.md -->

# Data Tier Documentation Standardization (04-data) Implementation Plan

## Overview (KR)

이 문서는 `04-data` 티어의 다중 모델 영속성 계층에 대한 문서 체계를 표준화하는 실행 계획서다. 작업 분해, 검증, 롤아웃, 위험 관리, 완료 기준을 정의한다.

## Context

`04-data` 티어의 인프라 구성은 이미 완료되었으나, 프로젝트 전체의 거버넌스 및 문서 표준에 부합하도록 역설계(Reverse Engineering)를 통한 문서 동기화가 필요하다.

## Goals & In-Scope

- **Goals**: `04-data` 티어의 PRD, ARD, ADR, Spec 문서를 표준 템플릿으로 갱신.
- **In Scope**: `docs/01`~`06` 레이어의 데이터 티어 관련 문서 작성 및 인덱스 업데이트.

## Non-Goals & Out-of-Scope

- **Non-goals**: 실제 인프라 구성(Compose 파일 등)의 변경.
- **Out of Scope**: 데이터베이스 내 데이터 마이그레이션 또는 스키마 변경.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | PRD 갱신 | `docs/01.prd/2026-03-26-04-data.md` | REQ-PRD-FUN-04 | 템플릿 준수 확인 |
| PLN-002 | ARD 갱신 | `docs/02.ard/0004-data-architecture.md` | - | 다이어그램 포함 여부 |
| PLN-003 | ADR 갱신 | `docs/03.adr/0004-postgresql-ha-patroni.md` | - | 의사결정 맥락 기술 |
| PLN-004 | Spec 갱신 | `docs/04.specs/04-data/spec.md` | VAL-SPC-001 | 기술 명세 구체성 |
| PLN-005 | Tasks 생성 | `docs/06.tasks/04-data-tasks.md` | - | 작업 추적성 확보 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | 모든 문서의 `Overview (KR)` 존재 확인 | `grep -r "Overview (KR)" docs/` | 전 문서 포함 |
| VAL-PLN-002 | Traceability | 문서 간 상호 참조 링크 유효성 검사 | `find docs -name "*.md" -exec grep -l "\\[.*\\](.*\\.md)" {} +` | 깨진 링크 없음 |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| 문서와 실제 인프라 설정 불일치 | Medium | `infra/04-data`의 실제 파일을 재검증하여 작성 |
| 링크 참조 오류 | Low | 상대 경로 규칙 준수 및 교차 검증 |

## Completion Criteria

- [ ] `01.prd`, `02.ard`, `03.adr`, `04.specs` 문서 갱신 완료
- [ ] 각 레이어 README 인덱스 업데이트 완료
- [ ] 모든 검증 단계 통과

## Related Documents

- **PRD**: `[../01.prd/2026-03-26-04-data.md]`
- **ARD**: `[../02.ard/0004-data-architecture.md]`
- **Spec**: `[../04.specs/04-data/spec.md]`
- **ADR**: `[../03.adr/0004-postgresql-ha-patroni.md]`
