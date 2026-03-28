# 01-Gateway Nginx Operations Policy

## Overview (KR)

이 문서는 `01-gateway`의 Nginx 운영 정책을 정의한다. Nginx는 특수 경로(`/oauth2/`, `/keycloak/`, `/minio/`, `/minio-console/`) 프록시 역할을 수행하며, `Balanced` 하드닝 기준을 준수한다.

## Policy Scope

- `infra/01-gateway/nginx/docker-compose.yml`
- `infra/01-gateway/nginx/config/nginx.conf`
- Nginx healthcheck/readonly/tmpfs 운영 표준

## Applies To

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
- **Allowed**:
  - 서비스 특성(대용량 업로드/다운로드)에 따른 location 단위 timeout override
- **Disallowed**:
  - `/ping`, `/oauth2/`, `/keycloak/`, `/minio/`, `/minio-console/` 기본 흐름 훼손
  - readonly 환경에서 영구 쓰기 경로 의존 설정

## Exceptions

- 장애 대응 중 임시 timeout 완화 가능. 단, 원복 계획과 변경 로그를 남겨야 한다.

## Verification

- `bash scripts/check-gateway-hardening.sh`
- `docker compose -f infra/01-gateway/nginx/docker-compose.yml config`
- `docker compose -f infra/01-gateway/nginx/docker-compose.yml exec nginx nginx -t`

## Review Cadence

- 월 1회 정기 점검
- nginx.conf 변경 시 수시 점검

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: N/A
- **Eval / Guardrail Threshold**: gateway-hardening 스크립트 실패 0건
- **Log / Trace Retention**: nginx access/error 로그는 observability 정책 준수
- **Safety Incident Thresholds**: `/ping` 실패, 반복 5xx 증가, 인증 루프 발생 시 런북 절차 수행

## Related Documents

- **Plan**: [../../05.plans/2026-03-28-01-gateway-optimization-hardening-plan.md](../../05.plans/2026-03-28-01-gateway-optimization-hardening-plan.md)
- **Task**: [../../06.tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md)
- **Runbook**: [../../09.runbooks/01-gateway/nginx.md](../../09.runbooks/01-gateway/nginx.md)
- **Guide**: [../../07.guides/01-gateway/nginx.md](../../07.guides/01-gateway/nginx.md)
