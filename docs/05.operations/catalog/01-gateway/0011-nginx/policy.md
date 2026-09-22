---
title: "01-Gateway Nginx Operations Policy"
version: "1.1.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-22"
layer: "operations"
artifact_id: "POL-0011"
parent_ids:
- "AD-0001"
created: "2026-05-17"
---


# 01-Gateway Nginx Operations Policy

## Overview

이 문서는 `01-gateway`의 Nginx 운영 정책을 정의한다. Nginx는 특수 경로(`/oauth2/`, `/keycloak/`, `/cdn/`) 프록시 역할을 수행하며, `Balanced` 하드닝 기준을 준수한다.

## Policy Scope

- `infra/01-gateway/nginx/docker-compose.yml`
- `infra/01-gateway/nginx/config/nginx.conf`
- Nginx healthcheck/readonly/tmpfs 운영 표준 and the `nginx` profile runtime boundary
- **Systems**: Nginx gateway proxy
- **Agents**: Infra/DevOps/Ops agents
- **Environments**: Local, Dev, Stage, Production-like

## Controls

- **Required**:
  - Nginx 서비스는 `template-infra-readonly-low`를 사용해야 한다.
  - 필수 `tmpfs`: `/var/cache/nginx`, `/var/log/nginx`, `/var/run`
  - healthcheck는 `/ping` 경로를 사용해야 한다.
  - `server_tokens off;`를 유지해야 한다.
  - `proxy_connect_timeout`, `proxy_send_timeout`, `proxy_read_timeout`을 명시해야 한다.
  - 업스트림 서버는 `max_fails`, `fail_timeout` 정책을 명시해야 한다.
  - `proxy_next_upstream` 정책을 명시해야 한다.
  - 정적 자산 확장자 기반 캐시 정책(`expires`, `Cache-Control`)을 유지해야 한다.
  - `nginx`를 host ports 80/443을 점유하는 Traefik profile과 함께 선택하지 않는다.
  - Git config와 private certificate backup authority를 구분한다. tmpfs는 복구
    대상이 아니며 private key를 repository/evidence에 복사하지 않는다.
- **Allowed**:
  - 서비스 특성(대용량 업로드/다운로드)에 따른 location 단위 timeout override
- **Disallowed**:
  - `/ping`, `/oauth2/`, `/keycloak/`, `/cdn/` 기본 흐름 훼손
  - readonly 환경에서 영구 쓰기 경로 의존 설정

### AI Agent Policy

- **Model / Prompt Change Process**: N/A
- **Eval / Guardrail Threshold**: check-all-hardening.sh 01-gateway 실패 0건
- **Log / Trace Retention**: nginx access/error 로그는 observability 정책 준수
- **Safety Incident Thresholds**: `/ping` 실패, 반복 5xx 증가, 인증 루프 발생 시 런북 절차 수행

## Exceptions

- 장애 대응 중 임시 timeout 완화 가능. 단, 원복 계획과 변경 로그를 남겨야 한다.

## Verification

- `bash scripts/hardening/check-all-hardening.sh 01-gateway`
- Nginx runtime lint such as `docker compose exec nginx nginx -t` is valid only after an approved Nginx context with root `infra_net` and backend dependencies is running.
- Standalone `infra/01-gateway/nginx/docker-compose.yml` compose rendering is not readiness evidence.

### Recovery and Upgrade Controls

Rollback restores a reviewed config commit and matching private certificate set,
then validates all special paths with the real SeaweedFS/auth dependencies.
Image upgrades require `nginx -t`, representative route acceptance, and a prior
image declaration that can be restored with the same config.

## Review Cadence

- 월 1회 정기 점검
- nginx.conf 변경 시 수시 점검

## Traceability

- Declared parent: [Gateway Tier Architecture Description](../../../../02.architecture/descriptions/0001-gateway-architecture.md) (`AD-0001`)
- Subject peers: [Guide](guide.md) (`GDE-0011`), [Runbook](runbook.md) (`RUN-0011`)

## Related Documents

- [Official upstream operational documentation](https://nginx.org/en/docs/beginners_guide.html)

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations index](../../../README.md)
- [Usage guide](guide.md)
- [Recovery runbook](runbook.md)
