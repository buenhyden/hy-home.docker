---
status: active
---

<!-- Target: docs/05.operations/policies/common-optimizations-template-exceptions.md -->

# Common Optimizations Template Exceptions Policy

## Overview (KR)

이 문서는 `infra/common-optimizations.yml` 적용 시 허용되는 예외 목록과 승인 기준을 정의한다.
예외는 임시 편의가 아니라 운영/보안 상의 명시적 승인 항목으로 관리하며, 모든 검증 스크립트와 운영 문서는 동일 레지스트리를 참조해야 한다.

## Policy Scope

- `common-optimizations.yml` 템플릿 계열(`template-*`)의 제어항목 예외 관리
- Quick Win 기준선(`PLN-QW-001~005`) 검증 시 허용되는 서비스 단위 예외 관리

## Policy Scope

- **Systems**: `infra/**/docker-compose*.yml` (root 통합 compose 해석 기준)
- **Agents**: Infra/DevOps/Operations 역할 에이전트
- **Environments**: Local, Dev, Stage, Production-like

## Controls

- **Required**:
  - 예외 목록 SSoT는 [infra/common-optimizations.exceptions.json](../../../infra/common-optimizations.exceptions.json) 단일 파일로 유지
  - `scripts/validation/check-quickwin-baseline.sh`는 해당 레지스트리를 직접 읽어 검증
  - 신규 예외 추가 시 `reason`, `owner_role`, `review_cadence`와 함께 갱신
- **Allowed**:
  - one-shot init job의 `healthcheck` 생략
  - auth-disabled bootstrap 모드 서비스의 `secrets` 생략
  - DB 템플릿의 capability 관련 제한적 예외(`cap_drop`)
- **Disallowed**:
  - 레지스트리 미등록 상태의 임의 예외 적용
  - 문서와 레지스트리 간 불일치 상태로 배포 진행

## Exceptions

- 템플릿/서비스 예외의 상세 항목은 [infra/common-optimizations.exceptions.json](../../../infra/common-optimizations.exceptions.json) 를 기준으로 한다.
- 2026-03-28 기준 승인된 서비스 예외:
  - `healthcheck`: `pg-cluster-init`, `valkey-cluster-init`
  - `secrets`: `etcd-1`, `etcd-2`, `etcd-3`

## Verification

- `bash scripts/validation/check-quickwin-baseline.sh`
- `bash scripts/validation/check-template-security-baseline.sh`
- `bash scripts/validation/check-doc-traceability.sh`
- `bash scripts/validation/validate-docker-compose.sh`

## Review Cadence

- 월 1회 정기 검토
- 신규 예외 추가/삭제 시 즉시 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Related Documents

- [Operations index](../README.md)
- [Operations template](../../99.templates/operation.template.md)
