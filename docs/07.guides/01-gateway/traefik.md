# 01-Gateway Traefik Guide

## Overview (KR)

이 문서는 `Traefik Primary` 모델에서 01-gateway 소유 라우터를 운영하는 방법을 설명한다. 표준 미들웨어 체인 적용과 검증 흐름을 중심으로 다룬다.

## Guide Type

`system-guide | how-to`

## Target Audience

- Infra/DevOps Engineers
- Operators
- Contributors

## Purpose

- Traefik dashboard 라우터 하드닝 정책을 일관되게 적용한다.
- `gateway-standard-chain` 구성요소와 적용 범위를 이해한다.

## Prerequisites

- Docker/Docker Compose 사용 가능
- `infra/01-gateway/traefik` 구성 파일 접근 가능
- `scripts/check-gateway-hardening.sh` 실행 가능

## Step-by-step Instructions

1. 미들웨어 파일 확인
   - `infra/01-gateway/traefik/dynamic/middleware.yml`
   - 필수 블록 확인: `req-rate-limit`, `req-retry`, `req-circuit-breaker`, `gateway-standard-chain`
2. 라우터 라벨 확인
   - `infra/01-gateway/traefik/docker-compose.yml`
   - dashboard 라우터에 `dashboard-auth@file,gateway-standard-chain@file` 적용 확인
3. 설정 정적 검증
   - `docker compose -f infra/01-gateway/traefik/docker-compose.yml config`
4. 하드닝 검증
   - `bash scripts/check-gateway-hardening.sh`

## Common Pitfalls

- `gateway-standard-chain` 이름 오타로 middleware resolve 실패
- dashboard middleware 순서/구분자(`,`) 오류
- 비게이트웨이 소유 라우터까지 무분별하게 체인 확장 적용

## Related Documents

- **Spec**: [../../04.specs/01-gateway/spec.md](../../04.specs/01-gateway/spec.md)
- **Operation**: [../../08.operations/01-gateway/traefik.md](../../08.operations/01-gateway/traefik.md)
- **Runbook**: [../../09.runbooks/01-gateway/traefik.md](../../09.runbooks/01-gateway/traefik.md)
- **Plan**: [../../05.plans/2026-03-28-01-gateway-optimization-hardening-plan.md](../../05.plans/2026-03-28-01-gateway-optimization-hardening-plan.md)
