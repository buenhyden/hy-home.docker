---
status: active
---
<!-- Target: docs/05.operations/guides/05-messaging/optimization-hardening.md -->

# 05-Messaging Optimization Hardening Usage Guide

## Usage

### Overview

이 문서는 `05-messaging` 계층의 최적화/하드닝 항목을 운영자/개발자가 재현 가능하게 적용하기 위한 가이드다. Kafka/RabbitMQ 관리 경로의 게이트웨이 제어, 이미지 태그 고정, 개발 구성 정합성, CI 검증 절차를 제공한다.

### Usage Type

`system-guide | how-to`

### Target Audience

- Messaging Operator
- DevOps Engineer
- Platform Developer

### Purpose

- 메시징 관리 경로를 게이트웨이 표준 정책으로 정렬한다.
- 예측 불가능한 이미지/구성 회귀를 사전에 차단한다.
- 카탈로그 기반 확장(DLQ/재처리/quorum queue) 준비 상태를 확보한다.

### Prerequisites

- Docker / Docker Compose 실행 환경
- `infra/05-messaging` 및 `scripts/` 수정 권한
- Traefik 미들웨어(`gateway-standard-chain`, `sso-*`) 구성 존재

### Step-by-step Instructions

1. 구성 변경 전 정적 상태 점검
   - `HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh`
   - `HYHOME_COMPOSE_PROFILES='messaging dev' bash scripts/validation/validate-docker-compose.sh`
   - `docker compose --env-file .env.example --profile messaging config --services`
2. Kafka 하드닝 적용
   - `kafbat-ui` 이미지를 고정 태그로 유지한다.
   - `schema-registry`, `kafka-connect`, `kafka-rest`, `kafka-ui` 라우터에 `gateway-standard-chain@file`를 적용한다.
   - `kafka-ui`는 `sso-errors@file,sso-auth@file`를 체인에 포함한다.
3. Kafka dev 정합성 적용
   - 볼륨 마운트 경로를 compose 파일 디렉터리 기준 상대 경로로 유지한다.
   - dev 라우터에도 동일 체인/SSO 정책을 적용한다.
4. RabbitMQ 하드닝 적용
   - `rabbitmq` 관리 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용한다.
   - `messaging-option` 프로필을 유지해 선택적 활성화 모델을 보존한다.
5. 검증 자동화 및 CI 반영
   - `bash scripts/hardening/check-all-hardening.sh 05-messaging`
   - CI workflow에 `infrastructure-hardening` job 반영 여부 확인
6. 문서 추적성 동기화
   - PRD~Guide/Policy/Runbook optimization-hardening 문서 링크를 점검한다.

### Common Pitfalls

- UI 라우터에 SSO를 누락해 관리 경로가 과노출되는 실수
- 부동 태그(`:main`)를 재도입해 예측 불가능한 런타임 회귀를 유발하는 실수
- dev compose 경로를 repo-root 기준으로 작성해 파일 마운트 실패를 유발하는 실수
- 하드닝 스크립트와 문서 링크를 함께 갱신하지 않는 실수
- service-local compose가 root `infra_net` 및 secret context 없이 standalone으로 렌더링된다고 가정하는 실수

## Common Checks

- `HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_COMPOSE_PROFILES='messaging dev' bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 05-messaging`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/05-messaging/optimization-hardening.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/05-messaging/optimization-hardening.md)
- [Recovery runbook](../../runbooks/05-messaging/optimization-hardening.md)
