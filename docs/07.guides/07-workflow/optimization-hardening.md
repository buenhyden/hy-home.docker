# 07-Workflow Optimization Hardening Guide

## Overview (KR)

이 문서는 `07-workflow` 계층의 최적화/하드닝 변경을 운영자와 개발자가 재현 가능하게 적용하기 위한 가이드다. compose 보안 경계, health 기반 startup 계약, n8n 이미지 하드닝, 검증 절차를 제공한다.

## Guide Type

`system-guide | how-to`

## Target Audience

- SRE / Platform Operator
- DevOps Engineer
- Workflow Maintainer

## Purpose

- Airflow/n8n 관리 경로를 gateway+SSO 정책에 정렬한다.
- startup 안정성을 높이고 장애 전파를 줄인다.
- workflow 하드닝 회귀를 script/CI로 조기 차단한다.
- 카탈로그 확장 항목의 운영 기준(Airflow/n8n/airbyte)을 문서화한다.

## Prerequisites

- Docker / Docker Compose 실행 환경
- `infra/07-workflow` 수정 권한
- Traefik middleware(`gateway-standard-chain`, `sso-errors`, `sso-auth`) 준비

## Step-by-step Instructions

1. 정적 구성 점검
   - `docker compose -f infra/07-workflow/airflow/docker-compose.yml config`
   - `docker compose -f infra/07-workflow/n8n/docker-compose.yml config`
2. Gateway/SSO 경계 정렬
   - Airflow, Flower, n8n 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용한다.
3. Health 기반 의존성 강화
   - Airflow 핵심 서비스가 `airflow-valkey` `service_healthy`를 사용하도록 확인한다.
   - n8n worker/task-runner healthcheck와 task-runner dependency gating을 확인한다.
4. n8n 이미지 하드닝 확인
   - compose가 custom image(`hyhome/n8n:2.15.0-local`)를 사용하도록 확인한다.
   - Dockerfile non-root runtime(`USER node`)와 entrypoint secret guard를 확인한다.
5. 기준선 검증 실행
   - `bash scripts/check-workflow-hardening.sh`
   - `bash scripts/check-template-security-baseline.sh`
   - `bash scripts/check-doc-traceability.sh`
6. 카탈로그 확장 운영 기준 반영
   - Airflow DAG quality gate와 worker autoscale 기준을 정책 문서에 반영한다.
   - n8n workflow Git backup/Vault credential 기준을 정책 문서에 반영한다.
   - airbyte infra artifact gap을 backlog로 추적한다.

## Common Pitfalls

- 일부 라우터에만 SSO 체인을 적용하는 실수
- worker/task-runner healthcheck 없이 startup 불안정을 방치하는 실수
- n8n custom image를 compose에서 사용하지 않아 hardening drift가 생기는 실수
- 카탈로그 확장 항목을 문서만 기록하고 task로 분해하지 않는 실수

## Related Documents

- **PRD**: [../../01.prd/2026-03-28-07-workflow-optimization-hardening.md](../../01.prd/2026-03-28-07-workflow-optimization-hardening.md)
- **Spec**: [../../04.specs/07-workflow/spec.md](../../04.specs/07-workflow/spec.md)
- **Plan**: [../../05.plans/2026-03-28-07-workflow-optimization-hardening-plan.md](../../05.plans/2026-03-28-07-workflow-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md)
- **Operation**: [../../08.operations/07-workflow/optimization-hardening.md](../../08.operations/07-workflow/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/07-workflow/optimization-hardening.md](../../09.runbooks/07-workflow/optimization-hardening.md)
- **Catalog**: [../../08.operations/12-infra-service-optimization-catalog.md](../../08.operations/12-infra-service-optimization-catalog.md)
