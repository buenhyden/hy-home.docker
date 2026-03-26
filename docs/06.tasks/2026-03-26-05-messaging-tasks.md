# Task: Messaging Infrastructure Documentation Standardization

## Overview (KR)

이 문서는 메시징 계층(`05-messaging`)의 문서화 및 표준 인프라 가이드라인 적용을 위한 작업 목록이다. Spec과 Plan에서 도출된 작업을 추적한다.

## Inputs

- **Parent Spec**: `[../04.specs/05-messaging/spec.md]`
- **Parent Plan**: `[../05.plans/2026-03-26-05-messaging-standardization.md]`

## Working Rules

- 모든 문서는 templates 디렉터리의 최신 템플릿 형식을 따른다.
- 상대 경로 링크(`../../`)는 상위/하위 폴더 깊이를 정확히 계산하여 삽입한다.
- 불필요한 자리표시자(Placeholder) 텍스트는 모두 제거한다.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | PRD 생성 및 상위 README 업데이트 | doc | Overview | Phase 1 | 파일 존재 확인 | Antigravity | Done |
| T-002 | ARD 생성 및 상위 README 업데이트 | doc | Core Design | Phase 1 | 아키텍처 속성 검증 | Antigravity | Done |
| T-003 | ADR-0005 채택 및 문서 생성 | doc | Core Design | Phase 1 | 결정 배경 타당성 | Antigravity | Done |
| T-004 | Spec 문서 생성 (Technical 명세) | doc | All sections | Phase 2 | 기술 설정 일치 확인 | Antigravity | Done |
| T-005 | Plan 문서 생성 (실행 계획) | doc | All sections | Phase 2 | 마일스톤 적절성 | Antigravity | Done |
| T-006 | README 통합 리팩토링 (Layer & Service) | doc | Governance | Phase 3 | 템플릿 준수도 | Antigravity | Todo |

## Verification Summary

- **Test Commands**: N/A (Documentation project)
- **Links**: `head -n 20 docs/**/*.md` 를 통해 링크 레이아웃 검증 필요.
