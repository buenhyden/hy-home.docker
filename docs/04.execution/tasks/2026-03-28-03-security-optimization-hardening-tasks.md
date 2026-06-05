---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-03-28-03-security-optimization-hardening-tasks.md -->

# Task: 03-Security (Vault) Optimization Hardening

## Overview

이 문서는 `03-security` 최적화/하드닝 구현 태스크를 추적한다. Vault 구성 하드닝, 검증 자동화, 문서 동기화, auth 검증 회귀 복구를 작업 단위로 관리한다.

## Inputs

- **Parent Spec**: [../../03.specs/03-security/spec.md](../../03.specs/03-security/spec.md)
- **Parent Plan**: [../plans/2026-03-28-03-security-optimization-hardening-plan.md](../plans/2026-03-28-03-security-optimization-hardening-plan.md)

## Working Rules

- placeholder 시크릿 경로(`secret/data/example`)는 허용하지 않는다.
- 하드닝/추적성 스크립트를 증빙으로 남긴다.
- auto-unseal/원격 audit는 이번 단계에서 문서화만 수행한다.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-SEC-001 | Vault compose에 `vault-agent` healthcheck, `/vault/out` 볼륨, cap 조정 반영 | impl | 03-security/spec.md / Contracts | PLN-SEC-001 | root security profile validation | Infra | Done |
| T-SEC-002 | Vault Agent 템플릿 경로/키 정규화 및 placeholder 제거 | impl | 03-security/spec.md / Contracts | PLN-SEC-002 | `bash scripts/hardening/check-all-hardening.sh 03-security` | Infra | Done |
| T-SEC-003 | `scripts/hardening/check-all-hardening.sh 03-security` 추가 | ops | 03-security/spec.md / Governance | PLN-SEC-003 | 스크립트 pass/fail 확인 | DevOps | Done |
| T-SEC-004 | CI `infrastructure-hardening` job 추가 | ops | 03-security/spec.md / Governance | PLN-SEC-004 | workflow 정적 검토 | DevOps | Done |
| T-SEC-005 | scripts README 인덱스 갱신 | doc | 03-security/spec.md / Related Docs | PLN-SEC-005 | README 항목 확인 | Docs | Done |
| T-SEC-006 | root profile 기반 security validation 경계 반영 | ops | 03-security/spec.md / Governance | PLN-SEC-006 | `HYHOME_COMPOSE_PROFILES=security bash scripts/validation/validate-docker-compose.sh` | DevOps | Done |
| T-SEC-007 | PRD/ARD/ADR/Plan/Task 생성 및 Spec/Guide/Ops/Runbook 갱신 | doc | 03-security/spec.md / Related Docs | PLN-SEC-007 | 문서 링크/인덱스 확인 | Docs | Done |
| T-SEC-008 | README 인덱스(Stage 01~05 + 03-security 하위) 반영 | doc | 03-security/spec.md / Related Docs | PLN-SEC-007 | README 반영 확인 | Docs | Done |
| T-SEC-009 | 정적 검증 커맨드 실행 및 결과 기록 | test | 03-security/spec.md / Verification | PLN-SEC-001~007 | 5개 검증 커맨드 실행 | Infra | Done |
| T-SEC-010 | runtime 검증(가능 환경) 수행 및 증빙 기록 | test | 03-security/spec.md / Verification | PLN-SEC-001~007 | Live `vault/vault-agent` health/runtime 점검은 approved runtime session에서 수행 | Infra | Deferred |

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
- [x] T-SEC-010 (Deferred runtime evidence recorded)

## Verification Summary

- **Test Commands**:
  - `HYHOME_COMPOSE_PROFILES=security bash scripts/validation/validate-docker-compose.sh`
  - `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`
  - `bash scripts/hardening/check-all-hardening.sh 03-security`
  - `bash scripts/validation/check-template-security-baseline.sh`
  - `bash scripts/validation/check-doc-traceability.sh`
- **Eval Commands**: N/A
- **Logs / Evidence Location**: 로컬 실행 출력 + CI quality gates(`infrastructure-hardening`, `template-security-baseline`, `docs-traceability`)
- **Deferred Runtime Evidence**: T-SEC-010 requires an approved live Vault runtime session; static implementation and hardening gates are complete.

## Related Documents

- **PRD**: [../01.requirements/2026-03-28-03-security-optimization-hardening.md](../../01.requirements/2026-03-28-03-security-optimization-hardening.md)
- **ARD**: [../02.architecture/requirements/0018-security-optimization-hardening-architecture.md](../../02.architecture/requirements/0018-security-optimization-hardening-architecture.md)
- **ADR**: [../02.architecture/decisions/0018-vault-hardening-and-ha-expansion-strategy.md](../../02.architecture/decisions/0018-vault-hardening-and-ha-expansion-strategy.md)
- **Plan**: [../plans/2026-03-28-03-security-optimization-hardening-plan.md](../plans/2026-03-28-03-security-optimization-hardening-plan.md)
- **Guide**: [../../05.operations/guides/03-security/vault.md](../../05.operations/guides/03-security/vault.md)
- **Policy**: [../../05.operations/policies/03-security/vault.md](../../05.operations/policies/03-security/vault.md)
- **Runbook**: [../../05.operations/runbooks/03-security/vault.md](../../05.operations/runbooks/03-security/vault.md)
