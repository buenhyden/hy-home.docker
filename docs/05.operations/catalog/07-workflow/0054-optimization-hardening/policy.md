---
title: 07-Workflow Optimization Hardening Operations Policy
version: 1.0.0
type: operation/policy
layer: operations
status: active
owner: "@buenhyden"
artifact_id: POL-0054
parent_ids:
  - AD-0007
created: 2026-05-10
updated: 2026-08-11
---
<!-- Target: docs/05.operations/catalog/07-workflow/0054-optimization-hardening/policy.md -->

# 07-Workflow Optimization Hardening Operations Policy

## Overview

이 문서는 `07-workflow` 계층의 최적화/하드닝 운영 정책을 정의한다. gateway 경계 보안, health 기반 의존성, n8n 컨테이너 하드닝, 카탈로그 기반 확장 승인 기준을 통제한다.

## Policy Scope

- `infra/07-workflow/airflow/docker-compose.yml`
- `infra/07-workflow/n8n/{docker-compose.yml,Dockerfile,docker-entrypoint.sh}`
- `scripts/hardening/check-all-hardening.sh 07-workflow`

- **Systems**: Airflow, Flower, n8n, n8n-worker, n8n-task-runner, workflow Valkey
- **Agents**: Infra/DevOps/Operations agents
- **Environments**: Local, Dev, Stage, Production-like

## Controls

- **Required**:
  - Airflow/Flower/n8n 공개 라우터는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용한다.
  - service-local Airflow compose는 `airflow-valkey` `service_healthy` dependency를 사용한다.
  - root-included dev compose는 shared `mng-valkey` broker 경계를 문서와 검증 evidence에 명시한다.
  - n8n worker/task-runner healthcheck를 필수로 유지한다.
  - service-local n8n task-runner는 `n8n`/`n8n-valkey` health 기반 의존성을 유지하고, root-included dev compose는 `mng-valkey` broker 경계를 명시한다.
  - n8n compose 기본 이미지는 custom image(`hyhome/n8n:2.29.5-local`)를 사용한다.
  - n8n runtime은 non-root이며 entrypoint secret guard를 유지한다.
  - workflow 변경은 `check-all-hardening.sh 07-workflow` 및 CI `infrastructure-hardening`을 통과해야 한다.
  - 문서(PRD~Procedure)는 optimization-hardening 링크를 유지한다.
- **Allowed**:
  - Airflow DAG quality gate/worker autoscale 기준의 단계적 강화
  - n8n workflow Git backup/Vault credential 연계의 단계적 강화
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
  - credential store Vault 연계 모델 및 롤백 절차 문서화


## Exceptions

- 장애 대응 시 일시적 접근제어 완화는 허용될 수 있다.
- 단, 변경 승인 기록과 동일 릴리스 내 원상 복구/재검증이 필수다.

## Verification

- `HYHOME_COMPOSE_PROFILES=workflow bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 07-workflow`
- `bash scripts/validation/check-template-security-baseline.sh`
- `python3 scripts/validation/check-document-links.py --mode traceability`

## Review Cadence

- 월 1회 정기 검토
- Airflow/n8n 버전 변경 또는 인증/보안 이슈 발생 시 수시 검토

## Traceability

- Declared parent: [Workflow Tier (07-workflow) Architecture Description](../../../../02.architecture/descriptions/0007-workflow-architecture.md) (`AD-0007`)
- Subject peers: [Guide](guide.md) (`GDE-0054`), [Runbook](runbook.md) (`RUN-0054`)

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](guide.md)
- [Recovery runbook](runbook.md)
