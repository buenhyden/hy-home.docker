---
status: active
---
<!-- Target: docs/05.operations/runbooks/02-auth/keycloak.md -->

# 02-Auth Keycloak Runbook

## Overview (KR)

이 런북은 Keycloak readiness 실패, DB 연결 오류, 시크릿 회전 후 인증 장애 상황의 복구 절차를 정의한다.

## 02-Auth Keycloak Procedure

> Scope: Keycloak Runtime Recovery

### Purpose

- Keycloak 가용성을 빠르게 복구한다.
- 시크릿/설정 회귀 시 안전하게 롤백한다.

### Canonical References

- [Operations Policy](../../policies/02-auth/keycloak.md)
- [Plan](../../../04.execution/plans/2026-03-28-02-auth-optimization-hardening-plan.md)
- [Tasks](../../../04.execution/tasks/2026-03-28-02-auth-optimization-hardening-tasks.md)

## When to Use

- `/health/ready` 실패 지속
- DB 인증 오류 또는 연결 오류
- 관리자/DB 비밀 회전 직후 로그인 실패

## Procedure

### Checklist

- [ ] `docker compose -f infra/02-auth/keycloak/docker-compose.yml config` 성공
- [ ] `bash scripts/hardening/check-all-hardening.sh 02-auth` 결과 확인
- [ ] `docker compose ps`에서 `keycloak`, `mng-pg` 상태 확인

### Steps

1. 설정/로그 확인
   - `docker logs keycloak --tail=200`
   - `docker compose -f infra/02-auth/keycloak/docker-compose.yml config`
2. readiness 실패 대응
   - DB 연결 상태 확인(`mng-pg` 로그/상태)
   - Keycloak 재기동: `docker compose -f infra/02-auth/keycloak/docker-compose.yml up -d keycloak`
3. 시크릿 회전 장애 대응
   - `/run/secrets/keycloak_admin_password`, `/run/secrets/keycloak_db_password` 파일 존재와 mount 상태 확인
   - secret 값은 출력하지 않고 환경 변수/secret 파일 매핑 오타, rotation timestamp, 관련 서비스 재시작 여부 점검
4. 사후 검증
   - readiness 재확인
   - OAuth2 Proxy 연동 로그인 테스트

### Verification Steps

- [ ] `bash scripts/hardening/check-all-hardening.sh 02-auth` 통과
- [ ] `docker exec keycloak sh -c 'exec 3<>/dev/tcp/127.0.0.1/9000; printf \"GET /health/ready HTTP/1.1\\r\\nHost: localhost\\r\\nConnection: close\\r\\n\\r\\n\" >&3; cat <&3'`에서 `\"status\":\"UP\"` 확인

### Observability and Evidence Sources

- **Signals**: readiness 상태, Keycloak 로그의 DB/OIDC 오류
- **Evidence to Capture**:
  - `docker logs keycloak --tail=200`
  - `check-auth-hardening.sh` 실행 결과

### Safe Rollback or Recovery Procedure

- [ ] 직전 정상 커밋으로 `infra/02-auth/keycloak/docker-compose.yml` 복원
- [ ] `docker compose -f infra/02-auth/keycloak/docker-compose.yml up -d keycloak`
- [ ] readiness 및 로그인 플로우 재검증

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: N/A
- **Eval Re-run**: `bash scripts/hardening/check-all-hardening.sh 02-auth`
- **Trace Capture**: Keycloak 로그 + CI job 로그

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
- [Usage guide](../../guides/02-auth/keycloak.md)
- [Operations policy](../../policies/02-auth/keycloak.md)
- [Operations template](../../../99.templates/operation.template.md)
