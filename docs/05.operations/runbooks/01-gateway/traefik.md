---
status: active
---

# 01-Gateway Traefik Runbook

## 01-Gateway Traefik Procedure

> Scope: Traefik Primary Gateway Recovery

### Overview (KR)

이 런북은 Traefik 미들웨어 회귀, dashboard 접근 장애, 라우팅 이상 상황에서 복구 절차를 정의한다.

### Purpose

- `gateway-standard-chain` 회귀 시 신속 복구
- Dashboard 인증/접근 장애 진단
- Traefik 서비스 정상성 복원

### Canonical References

- [Operations Policy](../../policies/01-gateway/traefik.md)
- [Plan](../../../04.execution/plans/2026-03-28-01-gateway-optimization-hardening-plan.md)
- [Tasks](../../../04.execution/tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md)

### When to Use

- dashboard 접근 실패(401 loop, 429 burst, 5xx)
- 미들웨어 체인 누락/오타/잘못된 순서
- Traefik healthcheck 실패

### Procedure or Checklist

#### Checklist

- [ ] `docker compose -f infra/01-gateway/traefik/docker-compose.yml config` 성공
- [ ] `docker compose -f infra/01-gateway/traefik/docker-compose.yml ps`에서 상태 정상
- [ ] `bash scripts/hardening/check-all-hardening.sh 01-gateway` 실패 원인 확인

#### Procedure

1. 설정 검증
   - `bash scripts/hardening/check-all-hardening.sh 01-gateway`
   - `docker compose -f infra/01-gateway/traefik/docker-compose.yml config`
2. middleware 회귀 대응
   - `infra/01-gateway/traefik/dynamic/middleware.yml`에서 아래 4개 블록 존재 확인:
     - `req-rate-limit`
     - `req-retry`
     - `req-circuit-breaker`
     - `gateway-standard-chain`
3. dashboard 라우터 체인 확인
   - `infra/01-gateway/traefik/docker-compose.yml`의 dashboard middleware 라벨이
     `dashboard-auth@file,gateway-standard-chain@file`인지 확인
4. 서비스 재기동
   - `docker compose -f infra/01-gateway/traefik/docker-compose.yml up -d traefik`
5. 사후 확인
   - `docker compose -f infra/01-gateway/traefik/docker-compose.yml exec traefik traefik healthcheck --ping`

### Verification Steps

- [ ] `bash scripts/hardening/check-all-hardening.sh 01-gateway` 통과
- [ ] dashboard 접근 시 BasicAuth 요구 및 인증 성공
- [ ] 기존 라우팅 규칙 회귀 없음

### Observability and Evidence Sources

- **Signals**: Traefik healthcheck, gateway access/error logs
- **Evidence to Capture**:
  - `docker compose -f infra/01-gateway/traefik/docker-compose.yml logs --tail=200 traefik`
  - 검증 스크립트 출력

### Safe Rollback or Recovery Procedure

- [ ] 직전 정상 커밋으로 `infra/01-gateway/traefik/*` 복원
- [ ] `docker compose -f infra/01-gateway/traefik/docker-compose.yml up -d traefik`
- [ ] 롤백 후 `check-gateway-hardening.sh` 재실행

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: N/A
- **Eval Re-run**: `bash scripts/hardening/check-all-hardening.sh 01-gateway`
- **Trace Capture**: Traefik logs + CI job logs

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/01-gateway/traefik.md)
- [Operations policy](../../policies/01-gateway/traefik.md)
- [Operations template](../../../99.templates/operation.template.md)
