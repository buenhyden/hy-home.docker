---
title: "Common Optimizations Template Exceptions Policy"
version: "1.2.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0001"
parent_ids: []
created: "2026-06-04"
---


# Common Optimizations Template Exceptions Policy

## Overview

이 문서는 `infra/common-optimizations.yml` 적용 시 허용되는 예외 목록과 승인 기준을 정의한다.
예외는 임시 편의가 아니라 운영/보안 상의 명시적 승인 항목으로 관리하며, 모든 검증 스크립트와 운영 문서는 동일 레지스트리를 참조해야 한다.

## Policy Scope

- `common-optimizations.yml` 템플릿 계열(`template-*`)의 제어항목 예외 관리
- Quick Win 기준선(`PLN-QW-001~005`) 검증 시 허용되는 서비스 단위 예외 관리

- **Systems**: Git-tracked `infra/**/{compose,docker-compose}*.{yml,yaml}` (root 통합 Compose 해석 기준)
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

### AI Agent Policy

- **Model / Prompt Change Process**: [agentic governance](../../../.agents/governance/agentic.md)가 소유한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: [task checklists](../../../.agents/governance/task-checklists.md)를 따른다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Exceptions

- 템플릿/서비스 예외의 상세 항목은 [infra/common-optimizations.exceptions.json](../../../infra/common-optimizations.exceptions.json) 를 기준으로 한다.
현재 예외는 JSON registry의 template/job/dev/security 항목까지 적용되는 대상을
확인한다. `mng-pg-init`, OpenBao와 Agent 등 후속 예외를 아래 과거 목록만으로
누락시키지 않는다. 예외의 owner·risk·review·종료 조건을 확인하며, 원본에 없는
예외를 문서로 새로 승인하지 않는다.

> Historical evidence (not current authority; source: Git history):
> Source: `c26bc8026254dffd7d51fc45b4081a1f80f855f2`, POL-0001 Exceptions.
>
> - 2026-03-28 기준 승인된 서비스 예외:
>   - `healthcheck`: `pg-cluster-init`, `valkey-cluster-init`
>   - `secrets`: `etcd-1`, `etcd-2`, `etcd-3`

## Verification

- `bash scripts/validation/check-quickwin-baseline.sh`
- `bash scripts/validation/check-template-security-baseline.sh`
- `python3 scripts/validation/check-document-links.py --mode traceability`
- `bash scripts/validation/validate-docker-compose.sh`

검증기는 선택 범위를 각각 기록한다. 두 baseline script는 기본 `core`의
선언을 검사하며 모든 OPTIONAL/LAB의 compliance나 runtime health를 증명하지
않는다. template source 검사와 resolved service 검사도 구분한다. 공개 입력·임시
파일 경계는 [RUN-0086](../runbooks/0086-dependency-version-management.md#static-configuration-validation)을
따른다. 구현이 통제를 충족하지 못하면 예외를 임의 추가하지 않고 별도 remediation으로 남긴다.

## Review Cadence

책임 소유자는 @buenhyden이다. registry의 role 표기는 책임 설명이며 별도 팀이나
새 승인을 만들지 않는다.

- 월 1회 정기 검토
- 신규 예외 추가/삭제 시 즉시 검토

## Traceability

- 같은 번호 `0001`의 Guide/Runbook은 없다.

## Related Documents

- Compose/Dockerfile이 runtime pin을 소유한다. [파생 projection](../../../infra/tech-stack.versions.json)은 Compose-image drift를 검사한다.

- [Operations index](../README.md)
