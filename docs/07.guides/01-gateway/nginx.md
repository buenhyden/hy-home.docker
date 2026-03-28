# 01-Gateway Nginx Guide

## Overview (KR)

이 문서는 01-gateway의 Nginx 특수 경로 프록시 구성과 하드닝 포인트를 설명한다. readonly/tmpfs 운영, timeout/failover, 정적 캐시 정책의 의도를 중심으로 다룬다.

## Guide Type

`system-guide | how-to`

## Target Audience

- Infra/DevOps Engineers
- Operators
- Contributors

## Purpose

- Nginx를 `template-infra-readonly-low` 기반으로 안정적으로 운영한다.
- `/oauth2/`, `/keycloak/`, `/minio/`, `/minio-console/` 경로 흐름을 유지하면서 하드닝 변경을 적용한다.

## Prerequisites

- Docker/Docker Compose 사용 가능
- `infra/01-gateway/nginx` 구성 파일 접근 가능
- `scripts/check-gateway-hardening.sh` 실행 가능

## Step-by-step Instructions

1. Compose 하드닝 확인
   - `infra/01-gateway/nginx/docker-compose.yml`
   - readonly 템플릿/필수 tmpfs/`/ping` healthcheck 존재 확인
2. Nginx config 하드닝 확인
   - `infra/01-gateway/nginx/config/nginx.conf`
   - `server_tokens off`, timeout 3종, `proxy_next_upstream`, upstream `max_fails/fail_timeout`, 정적 캐시 location 확인
3. 설정 검증
   - `docker compose -f infra/01-gateway/nginx/docker-compose.yml exec nginx nginx -t`
4. 하드닝 검증
   - `bash scripts/check-gateway-hardening.sh`

## Common Pitfalls

- readonly 전환 후 `/var/cache/nginx`/`/var/log/nginx`/`/var/run` tmpfs 누락
- `proxy_pass` trailing slash 처리 실수로 경로 재작성 오류
- timeout 전역값/특정 location override 충돌

## Related Documents

- **Spec**: [../../04.specs/01-gateway/spec.md](../../04.specs/01-gateway/spec.md)
- **Operation**: [../../08.operations/01-gateway/nginx.md](../../08.operations/01-gateway/nginx.md)
- **Runbook**: [../../09.runbooks/01-gateway/nginx.md](../../09.runbooks/01-gateway/nginx.md)
- **Plan**: [../../05.plans/2026-03-28-01-gateway-optimization-hardening-plan.md](../../05.plans/2026-03-28-01-gateway-optimization-hardening-plan.md)
