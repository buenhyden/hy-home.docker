---
status: active
---
<!-- Target: docs/05.operations/runbooks/02-auth/oauth2-proxy.md -->

# 02-Auth OAuth2 Proxy Runbook

## Overview (KR)

이 런북은 OAuth2 Proxy 인증 루프, OIDC 장애, readonly/tmpfs 관련 오류, 설정 검증 실패 상황에 대한 복구 절차를 정의한다.

## 02-Auth OAuth2 Proxy Procedure

> Scope: OAuth2 Proxy ForwardAuth Recovery

### Purpose

- 인증 경로 장애를 신속히 복구한다.
- degraded-mode 수행/종료를 통제한다.
- config lint 실패 시 안전하게 롤백한다.

### Canonical References

- [Operations Policy](../../policies/02-auth/oauth2-proxy.md)
- [Plan](../../../04.execution/plans/2026-03-28-02-auth-optimization-hardening-plan.md)
- [Tasks](../../../04.execution/tasks/2026-03-28-02-auth-optimization-hardening-tasks.md)

## When to Use

- 로그인 루프(무한 redirect)
- OIDC issuer 접근 실패
- `/ping` healthcheck 실패
- readonly/tmpfs 관련 쓰기 오류
- compose/config 변경 후 런타임 부팅 실패

## Procedure

### Checklist

- [ ] `docker compose -f infra/02-auth/oauth2-proxy/docker-compose.yml config` 성공
- [ ] `bash scripts/hardening/check-all-hardening.sh 02-auth` 실행
- [ ] `docker logs oauth2-proxy --tail=200` 오류 패턴 확인

### Steps

1. 기본 진단
   - `/ping` 확인: `docker exec oauth2-proxy wget -qO- http://127.0.0.1:4180/ping`
   - OIDC issuer 확인: `https://keycloak.${DEFAULT_URL}/realms/hy-home.realm`
2. 로그인 루프 대응
   - `OAUTH2_PROXY_COOKIE_DOMAINS`, `OAUTH2_PROXY_WHITELIST_DOMAINS`, `redirect_url` 정합성 확인
   - `cookie_secure=true` 환경에서 HTTPS 진입 여부 확인
3. readonly/tmpfs 장애 복구
   - 쓰기 대상 경로가 `/tmp`, `/run` 내인지 점검
   - 엔트리포인트/인증서 마운트 경로 권한 확인
4. degraded-mode 절차(승인 필요)
   - OIDC 장기 장애 시 운영 승인 후 제한적 degraded-mode 적용
   - 적용 시간/범위/종료 조건을 티켓에 기록
   - Keycloak 정상화 즉시 기본 fail-closed로 복귀
5. config lint 실패 롤백
   - 직전 정상 커밋으로 compose/config 복원
   - 재기동 후 `/ping` 및 인증 플로우 재검증

### Verification Steps

- [ ] `bash scripts/hardening/check-all-hardening.sh 02-auth` 통과
- [ ] `docker exec oauth2-proxy wget -qO- http://127.0.0.1:4180/ping` 성공
- [ ] 인증 콜백(`/oauth2/callback`) 정상 동작

### Observability and Evidence Sources

- **Signals**: `/ping`, oauth2-proxy 로그, Keycloak 연결 오류율
- **Evidence to Capture**:
  - `docker logs oauth2-proxy --tail=200`
  - `docker logs keycloak --tail=200`
  - check-all-hardening.sh 02-auth 출력

### Safe Rollback or Recovery Procedure

- [ ] 아래 파일을 직전 정상 커밋으로 복원
  - `infra/02-auth/oauth2-proxy/docker-compose.yml`
  - `infra/02-auth/oauth2-proxy/docker-entrypoint.sh`
  - `infra/02-auth/oauth2-proxy/Dockerfile`
  - `infra/02-auth/oauth2-proxy/config/oauth2-proxy.cfg`
- [ ] `docker compose -f infra/02-auth/oauth2-proxy/docker-compose.yml up -d oauth2-proxy`
- [ ] `/ping` + 로그인 시나리오 재검증

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: N/A
- **Eval Re-run**: `bash scripts/hardening/check-all-hardening.sh 02-auth`
- **Trace Capture**: oauth2-proxy/keycloak 로그 + CI job 로그

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
- [Usage guide](../../guides/02-auth/oauth2-proxy.md)
- [Operations policy](../../policies/02-auth/oauth2-proxy.md)
