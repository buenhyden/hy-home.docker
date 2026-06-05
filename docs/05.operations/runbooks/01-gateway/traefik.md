---
status: active
---
<!-- Target: docs/05.operations/runbooks/01-gateway/traefik.md -->

# 01-Gateway Traefik Runbook

## Overview

이 런북은 Traefik 미들웨어 회귀, dashboard 접근 장애, 라우팅 이상 상황에서 복구 절차를 정의한다.

## 01-Gateway Traefik Procedure

> Scope: Traefik Primary Gateway Recovery

### Purpose

- `gateway-standard-chain` 회귀 시 신속 복구
- Dashboard 인증/접근 장애 진단
- Traefik 서비스 정상성 복원

### Canonical References

- [Operations Policy](../../policies/01-gateway/traefik.md)
- [Plan](../../../04.execution/plans/2026-03-28-01-gateway-optimization-hardening-plan.md)
- [Tasks](../../../04.execution/tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md)

## When to Use

- dashboard 접근 실패(401 loop, 429 burst, 5xx)
- 미들웨어 체인 누락/오타/잘못된 순서
- Traefik healthcheck 실패

## Procedure

### Checklist

- [ ] `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh` 성공
- [ ] `bash scripts/hardening/check-all-hardening.sh 01-gateway` 실패 원인 확인
- [ ] runtime 조치가 필요하면 root stack 실행 상태와 승인 범위를 확인

### Steps

1. 설정 검증
   - `bash scripts/hardening/check-all-hardening.sh 01-gateway`
   - `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`
2. middleware 회귀 대응
   - `infra/01-gateway/traefik/dynamic/middleware.yml`에서 아래 4개 블록 존재 확인:
     - `req-rate-limit`
     - `req-retry`
     - `req-circuit-breaker`
     - `gateway-standard-chain`
3. dashboard 라우터 체인 확인
   - `infra/01-gateway/traefik/docker-compose.yml`의 dashboard middleware 라벨이
     `dashboard-auth@file,gateway-standard-chain@file`인지 확인
4. runtime 상태 확인
   - approved root stack이 실행 중이면 `docker compose ps traefik`으로 상태를 확인한다.
   - runtime restart/reload가 필요하면 영향 범위와 승인자를 기록하고 root compose context에서만 수행한다.
5. 사후 확인
   - approved root stack이 실행 중이면 `docker compose exec traefik traefik healthcheck --ping`을 실행한다.

### Verification Steps

- [ ] `bash scripts/hardening/check-all-hardening.sh 01-gateway` 통과
- [ ] dashboard 접근 시 BasicAuth 요구 및 인증 성공
- [ ] 기존 라우팅 규칙 회귀 없음

### Observability and Evidence Sources

- **Signals**: Traefik healthcheck, gateway access/error logs
- **Evidence to Capture**:
  - `docker compose logs --tail=200 traefik` from the approved running root stack
  - 검증 스크립트 출력

### Safe Rollback or Recovery Procedure

- [ ] 직전 정상 커밋으로 `infra/01-gateway/traefik/*` 복원
- [ ] runtime restart/reload가 승인되면 root compose context에서 Traefik 단위로만 수행
- [ ] 롤백 후 `check-all-hardening.sh 01-gateway` 재실행

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: N/A
- **Eval Re-run**: `bash scripts/hardening/check-all-hardening.sh 01-gateway`
- **Trace Capture**: Traefik logs + CI job logs

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
- [Usage guide](../../guides/01-gateway/traefik.md)
- [Operations policy](../../policies/01-gateway/traefik.md)
