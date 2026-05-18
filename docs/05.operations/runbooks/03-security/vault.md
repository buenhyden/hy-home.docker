---
status: active
---

# 03-Security Vault Runbook

## 03-Security Vault Procedure

> Scope: Vault Secret Management Recovery & Maintenance

### Overview (KR)

이 런북은 Vault seal/unseal, raft 상태 점검, audit 활성/검증, Vault Agent 렌더 실패 복구, 안전 롤백 절차를 즉시 실행 가능 형태로 제공한다.

### Purpose

- Vault 장애/오작동 상황에서 복구 시간을 줄인다.
- 하드닝 계약 위반을 빠르게 진단하고 원복한다.

### Canonical References

- [Spec](../../../03.specs/03-security/spec.md)
- [Operations Policy](../../policies/03-security/vault.md)
- [Plan](../../../04.execution/plans/2026-03-28-03-security-optimization-hardening-plan.md)
- [Tasks](../../../04.execution/tasks/2026-03-28-03-security-optimization-hardening-tasks.md)

### When to Use

- Vault가 `Sealed: true` 상태일 때
- raft peer 상태가 비정상일 때
- audit device가 비활성화되었을 때
- Vault Agent healthcheck 또는 템플릿 렌더가 실패할 때

### Procedure or Checklist

#### Checklist

- [ ] `docker exec vault vault status` 확인
- [ ] `docker inspect --format '{{json .State.Health}}' vault` 확인
- [ ] `docker inspect --format '{{json .State.Health}}' vault-agent` 확인
- [ ] 최근 변경 파일/커밋 식별

#### Procedure

1. Seal/Unseal 복구
   - 상태 확인: `docker exec vault vault status`
   - 필요한 경우 unseal 키 3회 입력
2. Raft 상태 점검
   - `docker exec vault vault operator raft list-peers`
   - 비정상 peer 식별 후 정책에 따라 조치
3. Audit 활성/검증
   - `docker exec vault vault audit list`
   - 로컬 audit 활성 확인, 원격 audit는 정책 승인 상태 확인
4. Vault Agent 렌더 실패 복구
   - `docker logs vault-agent --tail=200`
   - `/vault/agent/role_id`, `/vault/agent/secret_id`, `/vault/agent/token` 확인
   - 인증 정보(`role_id`/`secret_id`) 부재/오류 시 위 AppRole bootstrap 절차를 재실행한다. 생성값은 파일로 직접 저장하고 문서/PR/로그에 노출하지 않는다.
   - `docker exec vault-agent ls -la /vault/out`로 출력 파일 재검증
5. 재검증
   - `bash scripts/hardening/check-all-hardening.sh 03-security`
   - `bash scripts/validation/check-template-security-baseline.sh`

### Verification Steps

- [ ] `bash scripts/hardening/check-all-hardening.sh 03-security` 통과
- [ ] `docker exec vault vault status`에서 `Sealed: false` 확인
- [ ] `docker inspect`에서 `vault`, `vault-agent` health가 정상
- [ ] `/vault/out` 하위 템플릿 파일 생성 확인

### Observability and Evidence Sources

- **Signals**: container health, Vault status, audit list, agent render logs
- **Evidence to Capture**:
  - `docker logs vault --tail=200`
  - `docker logs vault-agent --tail=200`
  - `vault status`, `vault operator raft list-peers`, `vault audit list` 출력

### Safe Rollback or Recovery Procedure

- [ ] 롤백 대상 파일
  - `infra/03-security/vault/docker-compose.yml`
  - `infra/03-security/vault/config/templates/*.ctmpl`
  - `scripts/hardening/check-all-hardening.sh 03-security`
  - `.github/workflows/ci-quality.yml`
  - `scripts/hardening/check-all-hardening.sh 02-auth`
- [ ] compose 재반영
  - `docker compose -f infra/03-security/vault/docker-compose.yml up -d vault vault-agent`
- [ ] 하드닝/추적성 검증 재실행

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: CI `security-hardening` 임시 비활성은 승인 후만 수행
- **Eval Re-run**: `check-security-hardening`, `check-auth-hardening`, `check-doc-traceability`
- **Trace Capture**: CI job logs + container logs

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/03-security/vault.md)
- [Operations policy](../../policies/03-security/vault.md)
- [Operations template](../../../99.templates/operation.template.md)
