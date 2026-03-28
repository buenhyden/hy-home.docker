# 05-Messaging Optimization Hardening Guide

## Overview (KR)

이 문서는 `05-messaging` 계층의 최적화/하드닝 항목을 운영자/개발자가 재현 가능하게 적용하기 위한 가이드다. Kafka/RabbitMQ 관리 경로의 게이트웨이 제어, 이미지 태그 고정, 개발 구성 정합성, CI 검증 절차를 제공한다.

## Guide Type

`system-guide | how-to`

## Target Audience

- Messaging Operator
- DevOps Engineer
- Platform Developer

## Purpose

- 메시징 관리 경로를 게이트웨이 표준 정책으로 정렬한다.
- 예측 불가능한 이미지/구성 회귀를 사전에 차단한다.
- 카탈로그 기반 확장(DLQ/재처리/quorum queue) 준비 상태를 확보한다.

## Prerequisites

- Docker / Docker Compose 실행 환경
- `infra/05-messaging` 및 `scripts/` 수정 권한
- Traefik 미들웨어(`gateway-standard-chain`, `sso-*`) 구성 존재

## Step-by-step Instructions

1. 구성 변경 전 정적 상태 점검
   - `docker compose -f infra/05-messaging/kafka/docker-compose.yml config`
   - `docker compose -f infra/05-messaging/kafka/docker-compose.dev.yml config`
   - `docker compose -f infra/05-messaging/rabbitmq/docker-compose.yml config`
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
   - `bash scripts/check-messaging-hardening.sh`
   - CI workflow에 `messaging-hardening` job 반영 여부 확인
6. 문서 추적성 동기화
   - PRD~Runbook optimization-hardening 문서 링크를 점검한다.

## Common Pitfalls

- UI 라우터에 SSO를 누락해 관리 경로가 과노출되는 실수
- 부동 태그(`:main`)를 재도입해 예측 불가능한 런타임 회귀를 유발하는 실수
- dev compose 경로를 repo-root 기준으로 작성해 파일 마운트 실패를 유발하는 실수
- 하드닝 스크립트와 문서 링크를 함께 갱신하지 않는 실수

## Related Documents

- **PRD**: [../../01.prd/2026-03-28-05-messaging-optimization-hardening.md](../../01.prd/2026-03-28-05-messaging-optimization-hardening.md)
- **Spec**: [../../04.specs/05-messaging/spec.md](../../04.specs/05-messaging/spec.md)
- **Plan**: [../../05.plans/2026-03-28-05-messaging-optimization-hardening-plan.md](../../05.plans/2026-03-28-05-messaging-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md)
- **Operation**: [../../08.operations/05-messaging/optimization-hardening.md](../../08.operations/05-messaging/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/05-messaging/optimization-hardening.md](../../09.runbooks/05-messaging/optimization-hardening.md)
- **Catalog**: [../../08.operations/12-infra-service-optimization-catalog.md](../../08.operations/12-infra-service-optimization-catalog.md)
