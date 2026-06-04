---
status: completed
---

<!-- Target: docs/04.execution/tasks/2026-06-02-governance-optimization.md -->

# Task: Governance Optimization (I1+I2)

> 거버넌스 고도화 라운드(I1+I2)의 구현·검증 작업 기록이다.

## Overview (KR)

이 문서는 거버넌스 고도화 라운드의 작업 목록과 검증 증거를 추적한다. Parent Plan에서
파생된 I1·I2 작업의 변경 파일과 실행한 계약 검사 결과를 기록한다.

## Inputs

- **Parent Plan**: [Execution plan](../plans/2026-06-02-governance-optimization.md)
- **Parent Spec**: N/A — 거버넌스/문서 최적화로 별도 `docs/03.specs/` 스펙 체인이 없다.

## Working Rules

- 모든 변경은 계약 검사 `failures=0`을 유지해야 한다.
- 문서 전용 작업도 검증 증거(명령·결과)를 남긴다.
- task-owned 경로만 stage한다. 무관한 변경은 건드리지 않는다.

## Task Table

| Task ID | Description                              | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence                       | Owner               | Status |
| ------- | ---------------------------------------- | ---- | --------------------- | ------------------- | ------------------------------------------- | ------------------- | ------ |
| T-001   | 보안 하드닝 내장 서비스 시드 작성        | impl | N/A                   | PLN-001             | `yaml.safe_load` OK, 계약 검사 `failures=0` | workflow-supervisor | Done   |
| T-002   | service scaffold 템플릿 + 4파일 등록     | doc  | N/A                   | PLN-002             | `check-repo-contracts.sh` `failures=0`      | workflow-supervisor | Done   |
| T-003   | 신규 서비스 온보딩 가이드 작성           | doc  | N/A                   | PLN-003             | guide 정규화 통과, `failures=0`             | workflow-supervisor | Done   |
| T-004   | 코드리뷰 요청/수용 루프 명문화           | doc  | N/A                   | PLN-004             | `check-repo-contracts.sh` `failures=0`      | workflow-supervisor | Done   |
| T-005   | 생성물 freshness 계약을 QA 스코프에 주입 | doc  | N/A                   | PLN-005             | `check-repo-contracts.sh` `failures=0`      | workflow-supervisor | Done   |

## Suggested Types

- `impl`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-001 서비스 시드 작성
- [x] T-002 템플릿 + 등록

### Phase 2

- [x] T-003 온보딩 가이드
- [x] T-004 코드리뷰 루프

## Verification Summary

- **Test Commands**: `bash scripts/validation/check-repo-contracts.sh`, `bash scripts/validation/check-doc-traceability.sh`
- **Eval Commands**: N/A — 모델/에이전트 평가 대상 아님.
- **Logs / Evidence Location**: 두 검사 모두 `failures=0`. 시드 compose는 `yaml.safe_load` 통과.

## Related Documents

- **Parent Plan**: [Execution plan](../plans/2026-06-02-governance-optimization.md)
- **Service template**: [Service scaffold template](../../99.templates/service.template.md)
- **Operations**: [New-service onboarding guide](../../05.operations/guides/00-workspace/new-service-onboarding.md)
