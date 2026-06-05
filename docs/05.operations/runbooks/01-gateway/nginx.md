---
status: active
---
<!-- Target: docs/05.operations/runbooks/01-gateway/nginx.md -->

# 01-Gateway Nginx Runbook

## Overview

이 런북은 Nginx readonly/tmpfs 전환 이후 발생 가능한 장애, `nginx -t` 실패, `/ping` 헬스체크 실패 상황의 복구 절차를 정의한다.

## 01-Gateway Nginx Procedure

> Scope: Nginx Special-path Proxy Recovery

### Purpose

- readonly/tmpfs 운영 안정성 확보
- config lint 실패 시 안전 롤백
- 특수 경로 프록시(`/oauth2/`, `/keycloak/`, `/minio/`, `/minio-console/`) 정상성 회복

### Canonical References

- [Operations Policy](../../policies/01-gateway/nginx.md)
- [Plan](../../../04.execution/plans/2026-03-28-01-gateway-optimization-hardening-plan.md)
- [Tasks](../../../04.execution/tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md)

## When to Use

- `nginx -t` 실패
- `/ping` healthcheck 반복 실패
- readonly 전환 후 캐시/로그/PID 쓰기 오류
- 백엔드 장애 전환(failover) 동작 이상

## Procedure

### Checklist

- [ ] `bash scripts/hardening/check-all-hardening.sh 01-gateway` 실행
- [ ] Nginx runtime 조치가 필요하면 명시적 root network/dependency context와 승인 범위를 확인
- [ ] standalone service-local compose rendering을 readiness evidence로 사용하지 않는다

### Steps

1. 설정 검증
   - `bash scripts/hardening/check-all-hardening.sh 01-gateway`
   - approved Nginx runtime context가 실행 중이면 `docker compose exec nginx nginx -t`
2. readonly/tmpfs 장애 복구
   - compose에 아래 tmpfs 3개가 있는지 확인:
     - `/var/cache/nginx`
     - `/var/log/nginx`
     - `/var/run`
   - 누락 시 compose 수정 후 하드닝 검증을 재실행한다. runtime restart는 승인된 Nginx context에서만 수행한다.
3. config lint 실패 대응
   - 실패 로그에서 오류 지점 수정
   - approved runtime context에서 `nginx -t` 재통과 확인 후 reload 또는 재기동을 수행한다.
4. 특수 경로 정상성 확인
   - `/ping` 200 응답
   - `/oauth2/`, `/keycloak/`, `/minio/`, `/minio-console/` 경로 응답 확인
5. failover 정책 확인
   - `proxy_next_upstream` 정책/업스트림 `max_fails`, `fail_timeout` 존재 확인

### Verification Steps

- [ ] approved runtime context에서 `docker compose exec nginx nginx -t` 통과
- [ ] `/ping` 200
- [ ] 인증 플로우 정상 동작 (`/oauth2/`)
- [ ] 하드닝 검증 스크립트 통과

### Observability and Evidence Sources

- **Signals**: nginx healthcheck, 4xx/5xx 비율, upstream error 로그
- **Evidence to Capture**:
  - `docker compose logs --tail=200 nginx` from the approved running Nginx context
  - `nginx -t` 결과

### Safe Rollback or Recovery Procedure

- [ ] 직전 정상 커밋으로 아래 파일 복원
  - `infra/01-gateway/nginx/docker-compose.yml`
  - `infra/01-gateway/nginx/config/nginx.conf`
- [ ] runtime restart가 승인되면 approved Nginx context에서 Nginx 단위로만 수행
- [ ] `nginx -t` 및 `/ping` 재검증

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: N/A
- **Eval Re-run**: `bash scripts/hardening/check-all-hardening.sh 01-gateway`
- **Trace Capture**: nginx logs + CI job logs

## Evidence

- Capture command output, timestamps, and operator or agent actions for any execution of this runbook.
- Record failed checks, observed symptoms, and the final recovery or escalation state in the related task or incident evidence.

## Rollback or Recovery

- Use only recovery or rollback steps already documented in this runbook, including any `Safe Rollback or Recovery Procedure` subsection above.
- N/A for additional verified recovery steps: this file does not validate a broader service-specific rollback beyond the documented procedure.
- If the observed failure does not match the documented steps, stop changes, preserve evidence, and escalate under `## Escalation`.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/01-gateway/nginx.md)
- [Operations policy](../../policies/01-gateway/nginx.md)
