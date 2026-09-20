---
title: "01-Gateway Nginx Usage Guide"
version: "1.0.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "GDE-0011"
parent_ids:
- "POL-0011"
implementation_services:
  infra/01-gateway/nginx/docker-compose.yml:
  - nginx
created: "2026-05-10"
---

# 01-Gateway Nginx Usage Guide

## Usage

### Implementation Sources

- [infra/01-gateway/nginx/docker-compose.yml](../../../../../infra/01-gateway/nginx/docker-compose.yml)

### Overview

이 문서는 01-gateway의 Nginx 특수 경로 프록시 구성과 하드닝 포인트를 설명한다. Nginx의 lifecycle class는 **OPTIONAL** alternative gateway다. readonly/tmpfs 운영, timeout/failover, 정적 캐시 정책의 의도를 중심으로 다룬다.

### Usage Type

`system-guide | how-to`

### Target Audience

- Infra/DevOps Engineers
- Operators
- Contributors

### Purpose

- Nginx를 `template-infra-readonly-low` 기반으로 안정적으로 운영한다.
- `/oauth2/`, `/keycloak/`, `/minio/`, `/minio-console/` 경로 흐름을 유지하면서 하드닝 변경을 적용한다.

### Prerequisites

- Docker/Docker Compose 사용 가능
- `infra/01-gateway/nginx` 구성 파일 접근 가능
- `scripts/hardening/check-all-hardening.sh 01-gateway` 실행 가능
- Nginx runtime 검증 시 명시적 root network/dependency context 승인 필요

Nginx is selected only by `nginx`, publishes host ports 80/443, depends on a
healthy `minio`, and mounts its config and `${DEFAULT_CERT_DIR}` read-only. It is
an alternative listener to Traefik: because both claim the same host ports, do
not select `nginx` with `core`, `dev`, or `local` on one host.

### Step-by-step Instructions

1. Compose 하드닝 확인
   - `infra/01-gateway/nginx/docker-compose.yml`
   - readonly 템플릿/필수 tmpfs/`/ping` healthcheck 존재 확인
2. Nginx config 하드닝 확인
   - `infra/01-gateway/nginx/config/nginx.conf`
   - `server_tokens off`, timeout 3종, `proxy_next_upstream`, upstream `max_fails/fail_timeout`, 정적 캐시 location 확인
3. 설정 검증
   - 정적 검증: `bash scripts/hardening/check-all-hardening.sh 01-gateway`
   - runtime lint: approved Nginx runtime context에서 `docker compose exec nginx nginx -t`
4. 하드닝 검증
   - `bash scripts/hardening/check-all-hardening.sh 01-gateway`

### Common Pitfalls

- readonly 전환 후 `/var/cache/nginx`/`/var/log/nginx`/`/var/run` tmpfs 누락
- `proxy_pass` trailing slash 처리 실수로 경로 재작성 오류
- timeout 전역값/특정 location override 충돌

## Common Checks

- `bash scripts/hardening/check-all-hardening.sh 01-gateway`
- `docker compose exec nginx nginx -t` only after an approved Nginx runtime context is running

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](runbook.md)을 따른다.

### Configuration Recovery and Upgrade

Restore `nginx.conf` from Git and certificates from their private owner. Validate
the root `nginx` profile with its MinIO dependency, lint the config in the approved
runtime, then verify `/ping` and every special path before restoring 80/443
traffic. Cache/log/PID tmpfs needs no backup. Upgrade only after config lint and a
canary of OAuth2, Keycloak, MinIO API, and MinIO console paths. This recovery is
planned and was not executed during this correction.

## Traceability

- Declared parent: [01-Gateway Nginx Operations Policy](policy.md) (`POL-0011`)
- Governing authority: [Gateway Tier Architecture Description](../../../../02.architecture/descriptions/0001-gateway-architecture.md) (`AD-0001`)
- Subject peers: [Policy](policy.md) (`POL-0011`), [Runbook](runbook.md) (`RUN-0011`)

## Related Documents

- [Official upstream operational documentation](https://nginx.org/en/docs/beginners_guide.html)

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations index](../../../README.md)
- [Operations policy](policy.md)
- [Recovery runbook](runbook.md)
