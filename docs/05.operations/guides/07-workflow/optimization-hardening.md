---
status: active
---
<!-- Target: docs/05.operations/guides/07-workflow/optimization-hardening.md -->

# 07-Workflow Optimization Hardening Usage Guide

## Usage

### Overview

이 문서는 `07-workflow` 계층의 최적화/하드닝 변경을 운영자와 개발자가 재현 가능하게 적용하기 위한 가이드다. compose 보안 경계, health 기반 startup 계약, n8n 이미지 하드닝, 검증 절차를 제공한다.

### Usage Type

`system-guide | how-to`

### Target Audience

- SRE / Platform Operator
- DevOps Engineer
- Workflow Maintainer

### Purpose

- Airflow/n8n 관리 경로를 gateway+SSO 정책에 정렬한다.
- startup 안정성을 높이고 장애 전파를 줄인다.
- workflow 하드닝 회귀를 script/CI로 조기 차단한다.
- 카탈로그 확장 항목의 운영 기준(Airflow/n8n)을 문서화한다.

### Prerequisites

- Docker / Docker Compose 실행 환경
- `infra/07-workflow` 수정 권한
- Traefik middleware(`gateway-standard-chain`, `sso-errors`, `sso-auth`) 준비

### Step-by-step Instructions

1. 정적 구성 점검
   - `HYHOME_COMPOSE_PROFILES=workflow bash scripts/validation/validate-docker-compose.sh`
   - `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`
   - service-local compose 파일은 root network/secrets context 없이 단독 `config` 대상으로 쓰지 않는다.
2. Gateway/SSO 경계 정렬
   - Airflow, Flower, n8n 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용한다.
3. Health 기반 의존성 강화
   - service-local Airflow compose가 `airflow-valkey` `service_healthy`를 사용하도록 확인한다.
   - root-included dev compose가 `mng-valkey` broker dependency를 사용한다는 경계를 문서화한다.
   - n8n worker/task-runner healthcheck와 task-runner dependency gating을 확인한다.
4. n8n 이미지 하드닝 확인
   - compose가 custom image(`hyhome/n8n:2.29.5-local`)를 사용하도록 확인한다.
   - Dockerfile non-root runtime(`USER node`)와 entrypoint secret guard를 확인한다.
5. 기준선 검증 실행
   - `bash scripts/hardening/check-all-hardening.sh 07-workflow`
   - `bash scripts/validation/check-template-security-baseline.sh`
   - `bash scripts/validation/check-doc-traceability.sh`
6. 카탈로그 확장 운영 기준 반영
   - Airflow DAG quality gate와 worker autoscale 기준을 정책 문서에 반영한다.
   - n8n workflow Git backup/Vault credential 기준을 정책 문서에 반영한다.
   - 미구현 workflow service 문서는 active operations chain에서 제거한다.

### Common Pitfalls

- 일부 라우터에만 SSO 체인을 적용하는 실수
- worker/task-runner healthcheck 없이 startup 불안정을 방치하는 실수
- n8n custom image를 compose에서 사용하지 않아 hardening drift가 생기는 실수
- 카탈로그 확장 항목을 문서만 기록하고 task로 분해하지 않는 실수

## Common Checks

- `HYHOME_COMPOSE_PROFILES=workflow bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 07-workflow`
- `bash scripts/validation/check-template-security-baseline.sh`
- `bash scripts/validation/check-doc-traceability.sh`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/07-workflow/optimization-hardening.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/07-workflow/optimization-hardening.md)
- [Recovery runbook](../../runbooks/07-workflow/optimization-hardening.md)
