---
title: "01-Gateway Traefik Usage Guide"
version: "1.0.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0013"
parent_ids:
- "POL-0013"
implementation_services:
  infra/01-gateway/traefik/docker-compose.yml:
  - traefik
created: "2026-05-10"
---

# 01-Gateway Traefik Usage Guide

## Usage

### Implementation Sources

- [infra/01-gateway/traefik/docker-compose.yml](../../../infra/01-gateway/traefik/docker-compose.yml)

### Overview

이 문서는 `Traefik Primary` 모델에서 01-gateway 소유 라우터를 운영하는 방법을 설명한다. Traefik의 lifecycle class는 **HOME**이다. 표준 미들웨어 체인 적용과 검증 흐름을 중심으로 다룬다.

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
- root `core` profile compose validation 실행 가능

Traefik is selected by `core`, `dev`, or `local`; the service name is `traefik`.
It binds host ports 80/443, reads the Docker API through a read-only socket,
mounts repository static/dynamic configuration read-only, and mounts
`${DEFAULT_CERT_DIR}` read-only. A read-only socket prevents file writes but does
not make Docker API access low privilege, so socket access remains a host-control
security boundary. Compose grants `traefik_basicauth_password`,
`traefik_opensearch_basicauth_password` and
`traefik_prometheus_api_htpasswd`; do not print any of these values in
checks or evidence. The tracked configuration has no ACME storage declaration.

### Step-by-step Instructions

1. 미들웨어 파일 확인
   - `infra/01-gateway/traefik/dynamic/middleware.yml`
   - 필수 블록 확인: `req-rate-limit`, `req-retry`, `req-circuit-breaker`, `gateway-standard-chain`
2. 라우터 라벨 확인
   - `infra/01-gateway/traefik/docker-compose.yml`
   - dashboard 라우터에 `dashboard-auth@file,gateway-standard-chain@file` 적용 확인
3. 설정 정적 검증
   - `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`
4. 하드닝 검증
   - `bash scripts/hardening/check-all-hardening.sh 01-gateway`

### Common Pitfalls

- `gateway-standard-chain` 이름 오타로 middleware resolve 실패
- dashboard middleware 순서/구분자(`,`) 오류
- 비게이트웨이 소유 라우터까지 무분별하게 체인 확장 적용

## Common Checks

- `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 01-gateway`
- `docker compose exec traefik traefik healthcheck --ping` only after an approved root stack is running

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0013-traefik.md)을 따른다.

### Configuration Recovery and Upgrade

Git is the authority for static/dynamic configuration. The private certificate
owner is the authority for `${DEFAULT_CERT_DIR}`; certificate private keys must
not be copied into Git or incident evidence. Recovery restores a reviewed config
commit and matching certificate set, validates Compose and hardening, then starts
only `traefik` in an isolated/canary route context before accepting 80/443 traffic.
An image upgrade must validate config syntax, dashboard BasicAuth, representative
routes, metrics, and rollback to the prior image declaration. There is no tracked
ACME state to back up. This recovery was documented but not executed here.

## Traceability

- Declared parent: [01-Gateway Traefik Operations Policy](../policies/0013-traefik.md) (`POL-0013`)
- Governing authority: [Gateway Tier Architecture Description](../../02.architecture/descriptions/0001-gateway-architecture.md) (`AD-0001`)
- Subject peers: [Policy](../policies/0013-traefik.md) (`POL-0013`), [Runbook](../runbooks/0013-traefik.md) (`RUN-0013`)

## Related Documents

- [Official upstream operational documentation](https://doc.traefik.io/traefik/)
- [Traefik Docker API security guidance](https://doc.traefik.io/traefik/providers/docker/)

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations index](../README.md)
- [Operations policy](../policies/0013-traefik.md)
- [Recovery runbook](../runbooks/0013-traefik.md)
