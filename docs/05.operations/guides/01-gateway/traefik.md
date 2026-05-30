---
status: active
---
<!-- Target: docs/05.operations/guides/01-gateway/traefik.md -->

# 01-Gateway Traefik Usage Guide

## Overview (KR)

이 문서는 `Traefik Primary` 모델에서 01-gateway 소유 라우터를 운영하는 방법을 설명한다. 표준 미들웨어 체인 적용과 검증 흐름을 중심으로 다룬다.

## Usage

### Usage Type

`system-guide | how-to`

### Target Audience

- Infra/DevOps Engineers
- Operators
- Contributors

### Purpose

- Traefik dashboard 라우터 하드닝 정책을 일관되게 적용한다.
- `gateway-standard-chain` 구성요소와 적용 범위를 이해한다.

### Prerequisites

- Docker/Docker Compose 사용 가능
- `infra/01-gateway/traefik` 구성 파일 접근 가능
- `scripts/hardening/check-all-hardening.sh 01-gateway` 실행 가능

### Step-by-step Instructions

1. 미들웨어 파일 확인
   - `infra/01-gateway/traefik/dynamic/middleware.yml`
   - 필수 블록 확인: `req-rate-limit`, `req-retry`, `req-circuit-breaker`, `gateway-standard-chain`
2. 라우터 라벨 확인
   - `infra/01-gateway/traefik/docker-compose.yml`
   - dashboard 라우터에 `dashboard-auth@file,gateway-standard-chain@file` 적용 확인
3. 설정 정적 검증
   - `docker compose -f infra/01-gateway/traefik/docker-compose.yml config`
4. 하드닝 검증
   - `bash scripts/hardening/check-all-hardening.sh 01-gateway`

### Common Pitfalls

- `gateway-standard-chain` 이름 오타로 middleware resolve 실패
- dashboard middleware 순서/구분자(`,`) 오류
- 비게이트웨이 소유 라우터까지 무분별하게 체인 확장 적용

## Common Checks

- `docker compose -f infra/01-gateway/traefik/docker-compose.yml config`
- `bash scripts/hardening/check-all-hardening.sh 01-gateway`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/01-gateway/traefik.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/01-gateway/traefik.md)
- [Recovery runbook](../../runbooks/01-gateway/traefik.md)
