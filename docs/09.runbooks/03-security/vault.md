# 03-Security Vault Runbook

: Vault Secret Management Recovery & Maintenance

## Overview (KR)

이 런북은 Vault seal/unseal, raft 상태 점검, audit 활성/검증, Vault Agent 렌더 실패 복구, 안전 롤백 절차를 즉시 실행 가능 형태로 제공한다.

## Purpose

- Vault 장애/오작동 상황에서 복구 시간을 줄인다.
- 하드닝 계약 위반을 빠르게 진단하고 원복한다.

## Canonical References

- [Spec](../../04.specs/03-security/spec.md)
- [Operations Policy](../../08.operations/03-security/vault.md)
- [Plan](../../05.plans/2026-03-28-03-security-optimization-hardening-plan.md)
- [Tasks](../../06.tasks/2026-03-28-03-security-optimization-hardening-tasks.md)

## When to Use

- Vault가 `Sealed: true` 상태일 때
- raft peer 상태가 비정상일 때
- audit device가 비활성화되었을 때
- Vault Agent healthcheck 또는 템플릿 렌더가 실패할 때

## Procedure or Checklist

### Checklist

- [ ] `docker exec vault vault status` 확인
- [ ] `docker inspect --format '{{json .State.Health}}' vault` 확인
- [ ] `docker inspect --format '{{json .State.Health}}' vault-agent` 확인
- [ ] 최근 변경 파일/커밋 식별

### Procedure

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
   - `docker exec vault-agent ls -la /vault/out`로 출력 파일 재검증
5. 재검증
   - `bash scripts/check-security-hardening.sh`
   - `bash scripts/check-template-security-baseline.sh`

## Verification Steps

- [ ] `bash scripts/check-security-hardening.sh` 통과
- [ ] `docker exec vault vault status`에서 `Sealed: false` 확인
- [ ] `docker inspect`에서 `vault`, `vault-agent` health가 정상
- [ ] `/vault/out` 하위 템플릿 파일 생성 확인

## Observability and Evidence Sources

- **Signals**: container health, Vault status, audit list, agent render logs
- **Evidence to Capture**:
  - `docker logs vault --tail=200`
  - `docker logs vault-agent --tail=200`
  - `vault status`, `vault operator raft list-peers`, `vault audit list` 출력

## Safe Rollback or Recovery Procedure

- [ ] 롤백 대상 파일
  - `infra/03-security/vault/docker-compose.yml`
  - `infra/03-security/vault/config/templates/*.ctmpl`
  - `scripts/check-security-hardening.sh`
  - `.github/workflows/ci-quality.yml`
  - `scripts/check-auth-hardening.sh`
- [ ] compose 재반영
  - `docker compose -f infra/03-security/vault/docker-compose.yml up -d vault vault-agent`
- [ ] 하드닝/추적성 검증 재실행

## Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: CI `security-hardening` 임시 비활성은 승인 후만 수행
- **Eval Re-run**: `check-security-hardening`, `check-auth-hardening`, `check-doc-traceability`
- **Trace Capture**: CI job logs + container logs

## Related Operational Documents

- **Guide**: [../../07.guides/03-security/vault.md](../../07.guides/03-security/vault.md)
- **Operation**: [../../08.operations/03-security/vault.md](../../08.operations/03-security/vault.md)
