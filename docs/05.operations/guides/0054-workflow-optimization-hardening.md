---
title: "07-Workflow Optimization Hardening Usage Guide"
version: "1.1.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0054"
parent_ids:
- "POL-0054"
created: "2026-05-17"
---

# 07-Workflow Optimization Hardening Usage Guide

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

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
   - Airflow는 `gateway-standard-chain@file`과 native Keycloak SSO를 사용한다. Flower/n8n은 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 사용한다. 변경·복구는 RUN-0054로 넘긴다.
3. Health 기반 의존성 강화
   - `dedicated-valkey` profile은 `airflow-valkey`를 기동한다. 실제 사용은 `AIRFLOW_VALKEY_HOST=airflow-valkey`와 matching secret selector를 함께 설정했는지 확인한다.
   - 선택하지 않은 경우 shared `mng-valkey` broker dependency를 사용한다는 경계를 문서화한다.
   - n8n worker/task-runner healthcheck와 task-runner dependency gating을 확인한다.
4. n8n 이미지 하드닝 확인
   - compose가 custom image([hyhome/n8n image declaration](../../../infra/07-workflow/n8n/docker-compose.yml))를 사용하도록 확인한다.
   - Compose가 선택한 dev.Dockerfile(`USER node`) 또는 Dockerfile(`USER 1000`)와 각각의 entrypoint guard를 확인한다. Guard의 고정 secret과 선택 broker secret은 다를 수 있다; [n8n Guide](0053-n8n.md#build-readiness-and-runner-boundary)를 따른다.
5. 기준선 검증 실행
   - `bash scripts/hardening/check-all-hardening.sh 07-workflow`
   - `bash scripts/validation/check-template-security-baseline.sh`
   - `python3 scripts/validation/check-document-links.py --mode traceability`
6. 카탈로그 확장 운영 기준 반영
   - Airflow DAG quality gate와 worker autoscale 기준을 정책 문서에 반영한다.
   - n8n workflow Git backup/OpenBao credential 기준을 정책 문서에 반영한다.
   - 미구현 workflow service 문서는 active operations chain에서 제거한다.

### Common Pitfalls

- 일부 라우터에만 SSO 체인을 적용하는 실수
- worker/task-runner healthcheck 없이 startup 불안정을 방치하는 실수
- n8n custom image를 compose에서 사용하지 않아 hardening drift가 생기는 실수
- 카탈로그 확장 항목을 문서만 기록하고 task로 분해하지 않는 실수

### Static gate boundary

`check_07_workflow`는 파일과 일부 인증 문자열을 확인하고 Airflow double proxy-auth를 거부한다. Runner 호환성, 선택 Dockerfile/guard, 모든 probe, DB/broker readiness와 로그인 성공까지 증명하지 않는다. 필수 통제에는 추가 소스 검토와 승인된 런타임 근거가 필요하다. 문자열 검사 통과로 n8n 버전·timeout·guard 결함을 닫지 않는다.

### Common Checks

- `HYHOME_COMPOSE_PROFILES=workflow bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 07-workflow`
- `bash scripts/validation/check-template-security-baseline.sh`
- `python3 scripts/validation/check-document-links.py --mode traceability`

### Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0054-workflow-optimization-hardening.md)을 따른다.

### Traceability

- Declared parent: [07-Workflow Optimization Hardening Operations Policy](../policies/0054-workflow-optimization-hardening.md) (`POL-0054`)
- Governing authority: [Workflow Tier (07-workflow) Architecture Description](../../02.architecture/descriptions/0007-workflow-architecture.md) (`AD-0007`)
- Subject peers: [Policy](../policies/0054-workflow-optimization-hardening.md) (`POL-0054`), [Runbook](../runbooks/0054-workflow-optimization-hardening.md) (`RUN-0054`)

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Operations policy](../policies/0054-workflow-optimization-hardening.md)
- [Recovery runbook](../runbooks/0054-workflow-optimization-hardening.md)
