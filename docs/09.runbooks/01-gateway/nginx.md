# 01-Gateway Nginx Runbook

: Nginx Special-path Proxy Recovery

## Overview (KR)

이 런북은 Nginx readonly/tmpfs 전환 이후 발생 가능한 장애, `nginx -t` 실패, `/ping` 헬스체크 실패 상황의 복구 절차를 정의한다.

## Purpose

- readonly/tmpfs 운영 안정성 확보
- config lint 실패 시 안전 롤백
- 특수 경로 프록시(`/oauth2/`, `/keycloak/`, `/minio/`, `/minio-console/`) 정상성 회복

## Canonical References

- [Operations Policy](../../08.operations/01-gateway/nginx.md)
- [Plan](../../05.plans/2026-03-28-01-gateway-optimization-hardening-plan.md)
- [Tasks](../../06.tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md)

## When to Use

- `nginx -t` 실패
- `/ping` healthcheck 반복 실패
- readonly 전환 후 캐시/로그/PID 쓰기 오류
- 백엔드 장애 전환(failover) 동작 이상

## Procedure or Checklist

### Checklist

- [ ] `docker compose -f infra/01-gateway/nginx/docker-compose.yml config` 성공
- [ ] `bash scripts/check-gateway-hardening.sh` 실행
- [ ] `docker compose -f infra/01-gateway/nginx/docker-compose.yml ps` 상태 확인

### Procedure

1. 설정 검증
   - `bash scripts/check-gateway-hardening.sh`
   - `docker compose -f infra/01-gateway/nginx/docker-compose.yml exec nginx nginx -t`
2. readonly/tmpfs 장애 복구
   - compose에 아래 tmpfs 3개가 있는지 확인:
     - `/var/cache/nginx`
     - `/var/log/nginx`
     - `/var/run`
   - 누락 시 compose 수정 후 재기동:
     - `docker compose -f infra/01-gateway/nginx/docker-compose.yml up -d nginx`
3. config lint 실패 대응
   - 실패 로그에서 오류 지점 수정
   - `nginx -t` 재통과 확인 후 `nginx -s reload` 또는 재기동
4. 특수 경로 정상성 확인
   - `/ping` 200 응답
   - `/oauth2/`, `/keycloak/`, `/minio/`, `/minio-console/` 경로 응답 확인
5. failover 정책 확인
   - `proxy_next_upstream` 정책/업스트림 `max_fails`, `fail_timeout` 존재 확인

## Verification Steps

- [ ] `docker compose -f infra/01-gateway/nginx/docker-compose.yml exec nginx nginx -t` 통과
- [ ] `/ping` 200
- [ ] 인증 플로우 정상 동작 (`/oauth2/`)
- [ ] 하드닝 검증 스크립트 통과

## Observability and Evidence Sources

- **Signals**: nginx healthcheck, 4xx/5xx 비율, upstream error 로그
- **Evidence to Capture**:
  - `docker compose -f infra/01-gateway/nginx/docker-compose.yml logs --tail=200 nginx`
  - `nginx -t` 결과

## Safe Rollback or Recovery Procedure

- [ ] 직전 정상 커밋으로 아래 파일 복원
  - `infra/01-gateway/nginx/docker-compose.yml`
  - `infra/01-gateway/nginx/config/nginx.conf`
- [ ] `docker compose -f infra/01-gateway/nginx/docker-compose.yml up -d nginx`
- [ ] `nginx -t` 및 `/ping` 재검증

## Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: N/A
- **Eval Re-run**: `bash scripts/check-gateway-hardening.sh`
- **Trace Capture**: nginx logs + CI job logs

## Related Operational Documents

- **Guide**: [../../07.guides/01-gateway/nginx.md](../../07.guides/01-gateway/nginx.md)
- **Traefik Runbook**: [./traefik.md](./traefik.md)
