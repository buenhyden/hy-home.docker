---
title: "07-Workflow Optimization Hardening Operations Policy"
version: "1.1.3"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "POL-0054"
parent_ids:
- "AD-0007"
created: "2026-05-10"
---

# 07-Workflow Optimization Hardening Operations Policy

## Overview

이 문서는 `07-workflow` 계층의 최적화/하드닝 운영 정책을 정의한다. gateway 경계 보안, health 기반 의존성, n8n 컨테이너 하드닝, 카탈로그 기반 확장 승인 기준을 통제한다.

## Scope

- `infra/07-workflow/airflow/docker-compose.yml`
- `infra/07-workflow/n8n/{docker-compose.yml,Dockerfile,dev.Dockerfile,docker-entrypoint.sh,docker-entrypoint.dev.sh}`
- `scripts/hardening/check-all-hardening.sh 07-workflow`

- **Systems**: Airflow, Flower, n8n, n8n-worker, n8n-task-runner, workflow Valkey
- **Environments**: 로컬·개발·검증 및 운영 환경에 준하는 환경

## Rules

- **Required**:
  - Airflow 공개 라우터는 `gateway-standard-chain@file`과 native Keycloak SSO를 유지한다. Flower/n8n은 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 유지한다. Airflow double-auth 추가는 표준 복구가 아니다.
  - `dedicated-valkey` profile은 `airflow-valkey`를 기동할 뿐이다. 실제 전환에는 `AIRFLOW_VALKEY_HOST`와 `AIRFLOW_VALKEY_SECRET`의 matching pair가 필요하다.
  - `dedicated-valkey`를 선택하지 않은 경우의 shared `mng-valkey` broker 경계를 문서와 검증 evidence에 명시한다.
  - n8n worker/task-runner healthcheck를 필수로 유지한다.
  - n8n task-runner는 main health, task-runner-worker는 worker health 의존성을 유지한다. 선택 broker/DB readiness를 별도로 확인하고 `dedicated-valkey`와 실제 host/secret 선택을 구분한다.
  - n8n compose 기본 이미지는 custom image([hyhome/n8n image declaration](../../../infra/07-workflow/n8n/docker-compose.yml))를 사용한다.
  - n8n runtime은 non-root이며 entrypoint secret guard를 유지한다.
  - workflow 변경은 `check-all-hardening.sh 07-workflow` 및 CI `infrastructure-hardening`을 통과해야 한다.
  - 문서(PRD~Procedure)는 optimization-hardening 링크를 유지한다.
- **Allowed**:
  - Airflow DAG quality gate/worker autoscale 기준의 단계적 강화
  - n8n workflow Git backup/OpenBao credential 연계의 단계적 강화
  - 미구현 workflow service 문서 제거 및 archive ledger 추적
- **Disallowed**:
  - 무승인 middleware 완화
  - root runtime 복귀
  - 검증 게이트 우회 배포

### Catalog Expansion Approval Gates

- **Airflow 승인 조건**:
  - DAG parse/schedule/delay 기준 품질 게이트 문서화 및 CI 반영
  - worker autoscale 트리거(큐 지연, 실행 대기 수, CPU/memory) 기준 합의
- **n8n 승인 조건**:
  - workflow Git backup 표준 운영 절차 수립
  - credential store OpenBao 연계 모델 및 롤백 절차 문서화

### Static gate boundary

`check_07_workflow`는 파일과 일부 인증 문자열을 확인하고 Airflow double proxy-auth를 거부한다. Runner 호환성, 선택 Dockerfile/guard, 모든 probe, DB/broker readiness와 로그인 성공까지 증명하지 않는다. 필수 통제에는 추가 소스 검토와 승인된 런타임 근거가 필요하다. 문자열 검사 통과로 n8n 버전·timeout·guard 결함을 닫지 않는다.

## Exceptions

- 장애 대응 시 일시적 접근제어 완화는 허용될 수 있다.
- 단, 변경 승인 기록과 동일 릴리스 내 원상 복구/재검증이 필수다.

### Verification

점검 명령은 [가이드의 Common Checks](../guides/0054-workflow-optimization-hardening.md#common-checks)를 따른다. 정적 검사와 hardening 검사 결과를 변경 증거로 남긴다.

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Review Cadence

- 월 1회 정기 검토
- Airflow/n8n 버전 변경 또는 인증/보안 이슈 발생 시 수시 검토

### Traceability

- Declared parent: [Workflow Tier (07-workflow) Architecture Description](../../02.architecture/descriptions/0007-workflow-architecture.md) (`AD-0007`)
- Subject peers: [Guide](../guides/0054-workflow-optimization-hardening.md) (`GDE-0054`), [Runbook](../runbooks/0054-workflow-optimization-hardening.md) (`RUN-0054`)

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0054-workflow-optimization-hardening.md)
- [Recovery runbook](../runbooks/0054-workflow-optimization-hardening.md)
