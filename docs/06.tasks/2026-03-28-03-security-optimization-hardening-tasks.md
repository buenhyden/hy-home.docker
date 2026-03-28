# Task: 03-Security (Vault) Optimization Hardening

## Overview (KR)

이 문서는 `03-security` 최적화/하드닝 구현 태스크를 추적한다. Vault 구성 하드닝, 검증 자동화, 문서 동기화, auth 검증 회귀 복구를 작업 단위로 관리한다.

## Inputs

- **Parent Spec**: [../04.specs/03-security/spec.md](../04.specs/03-security/spec.md)
- **Parent Plan**: [../05.plans/2026-03-28-03-security-optimization-hardening-plan.md](../05.plans/2026-03-28-03-security-optimization-hardening-plan.md)

## Working Rules

- placeholder 시크릿 경로(`secret/data/example`)는 허용하지 않는다.
- 하드닝/추적성 스크립트를 증빙으로 남긴다.
- auto-unseal/원격 audit는 이번 단계에서 문서화만 수행한다.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-SEC-001 | Vault compose에 `vault-agent` healthcheck, `/vault/out` 볼륨, cap 조정 반영 | impl | 03-security/spec.md / Contracts | PLN-SEC-001 | `docker compose -f infra/03-security/vault/docker-compose.yml config` | Infra | Done |
| T-SEC-002 | Vault Agent 템플릿 경로/키 정규화 및 placeholder 제거 | impl | 03-security/spec.md / Contracts | PLN-SEC-002 | `bash scripts/check-security-hardening.sh` | Infra | Done |
| T-SEC-003 | `scripts/check-security-hardening.sh` 추가 | ops | 03-security/spec.md / Governance | PLN-SEC-003 | 스크립트 pass/fail 확인 | DevOps | Done |
| T-SEC-004 | CI `security-hardening` job 추가 | ops | 03-security/spec.md / Governance | PLN-SEC-004 | workflow 정적 검토 | DevOps | Done |
| T-SEC-005 | scripts README 인덱스 갱신 | doc | 03-security/spec.md / Related Docs | PLN-SEC-005 | README 항목 확인 | Docs | Done |
| T-SEC-006 | `check-auth-hardening.sh` 최신 02-auth 계약 반영 | ops | 03-security/spec.md / Governance | PLN-SEC-006 | `bash scripts/check-auth-hardening.sh` | DevOps | Done |
| T-SEC-007 | PRD/ARD/ADR/Plan/Task 생성 및 Spec/Guide/Ops/Runbook 갱신 | doc | 03-security/spec.md / Related Docs | PLN-SEC-007 | 문서 링크/인덱스 확인 | Docs | Done |
| T-SEC-008 | README 자동 인덱스(01~09 + 03-security 하위) 반영 | doc | 03-security/spec.md / Related Docs | PLN-SEC-007 | README 반영 확인 | Docs | Done |
| T-SEC-009 | 정적 검증 커맨드 실행 및 결과 기록 | test | 03-security/spec.md / Verification | PLN-SEC-001~007 | 5개 검증 커맨드 실행 | Infra | Done |
| T-SEC-010 | runtime 검증(가능 환경) 수행 및 증빙 기록 | test | 03-security/spec.md / Verification | PLN-SEC-001~007 | `vault/vault-agent` health/runtime 점검 | Infra | Planned |

## Suggested Types

- `impl`
- `test`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-SEC-001
- [x] T-SEC-002
- [x] T-SEC-003
- [x] T-SEC-004
- [x] T-SEC-005
- [x] T-SEC-006

### Phase 2

- [x] T-SEC-007
- [x] T-SEC-008
- [x] T-SEC-009
- [ ] T-SEC-010

## Verification Summary

- **Test Commands**:
  - `docker compose -f infra/03-security/vault/docker-compose.yml config`
  - `bash scripts/check-security-hardening.sh`
  - `bash scripts/check-template-security-baseline.sh`
  - `bash scripts/check-doc-traceability.sh`
  - `bash scripts/check-auth-hardening.sh`
- **Eval Commands**: N/A
- **Logs / Evidence Location**: 로컬 실행 출력 + CI quality gates(`security-hardening`, `auth-hardening`, `template-security-baseline`, `docs-traceability`)

## Related Documents

- **PRD**: [../01.prd/2026-03-28-03-security-optimization-hardening.md](../01.prd/2026-03-28-03-security-optimization-hardening.md)
- **ARD**: [../02.ard/0018-security-optimization-hardening-architecture.md](../02.ard/0018-security-optimization-hardening-architecture.md)
- **ADR**: [../03.adr/0018-vault-hardening-and-ha-expansion-strategy.md](../03.adr/0018-vault-hardening-and-ha-expansion-strategy.md)
- **Plan**: [../05.plans/2026-03-28-03-security-optimization-hardening-plan.md](../05.plans/2026-03-28-03-security-optimization-hardening-plan.md)
- **Guide**: [../07.guides/03-security/vault.md](../07.guides/03-security/vault.md)
- **Operation**: [../08.operations/03-security/vault.md](../08.operations/03-security/vault.md)
- **Runbook**: [../09.runbooks/03-security/vault.md](../09.runbooks/03-security/vault.md)
