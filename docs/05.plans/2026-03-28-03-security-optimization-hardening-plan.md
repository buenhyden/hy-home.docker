# 03-Security (Vault) Optimization Hardening Implementation Plan

## Overview (KR)

이 문서는 `infra/03-security/vault` 최적화/하드닝 실행 계획서다. 즉시 적용 가능한 하드닝 구현과 검증 자동화를 우선 적용하고, auto-unseal/원격 audit는 정책/전환 절차로 고정한다.

## Context

- 기준 카탈로그: [12-infra-service-optimization-catalog.md](../08.operations/12-infra-service-optimization-catalog.md)
- 상위 우선순위 계획: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md)
- 적용 전략: Phase 적용(즉시 하드닝 -> 정책/전환 설계 -> 문서 추적성 동기화)

## Goals & In-Scope

- **Goals**:
  - Vault Agent 템플릿/헬스/볼륨 계약을 안정화한다.
  - 03-security 하드닝 검증을 CI 게이트로 강제한다.
  - 01~09 문서 체계를 optimization/hardening 목적에 맞게 동기화한다.
  - auth 하드닝 검증 스크립트 회귀를 복구한다.
- **In Scope**:
  - `infra/03-security/vault/docker-compose.yml`
  - `infra/03-security/vault/config/templates/*.ctmpl`
  - `scripts/check-security-hardening.sh`
  - `.github/workflows/ci-quality.yml`
  - `scripts/check-auth-hardening.sh`, `scripts/README.md`
  - `docs/01~09` 및 README 인덱스

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - 즉시 auto-unseal(KMS/HSM) 구현
  - 즉시 원격 audit sink 구현
- **Out of Scope**:
  - 내부 TLS 모델 변경
  - 타 티어 애플리케이션 설정 변경

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-SEC-001 | `vault-agent` healthcheck + `/vault/out` 볼륨 + cap 정리 | `infra/03-security/vault/docker-compose.yml` | REQ-PRD-FUN-02,03 | compose config + healthcheck contract 확인 |
| PLN-SEC-002 | Vault Agent 템플릿 placeholder 제거 및 경로/키 정규화 | `infra/03-security/vault/config/templates/*.ctmpl` | REQ-PRD-FUN-01 | placeholder 0건, source/destination 무결성 |
| PLN-SEC-003 | 03-security 하드닝 검증 스크립트 추가 | `scripts/check-security-hardening.sh` | REQ-PRD-FUN-04 | 스크립트 pass/fail 동작 검증 |
| PLN-SEC-004 | CI `security-hardening` job 추가 | `.github/workflows/ci-quality.yml` | REQ-PRD-FUN-04 | PR/Push job 실행 |
| PLN-SEC-005 | scripts README 인벤토리 반영 | `scripts/README.md` | REQ-PRD-FUN-04 | README 항목/예시 존재 |
| PLN-SEC-006 | auth hardening 검증 스크립트 최신화 | `scripts/check-auth-hardening.sh` | REQ-PRD-FUN-06 | 최신 02-auth 계약 기준 통과 |
| PLN-SEC-007 | PRD~Runbook 문서 생성/갱신 + README 인덱스 동기화 | `docs/01~09/**` | REQ-PRD-FUN-05 | 상호 링크/인덱스 반영 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-SEC-001 | Structural | Vault compose 정적 검증 | `docker compose -f infra/03-security/vault/docker-compose.yml config` | 오류 없음 |
| VAL-SEC-002 | Compliance | 03-security 하드닝 검증 | `bash scripts/check-security-hardening.sh` | 실패 0건 |
| VAL-SEC-003 | Baseline | 템플릿/보안 기준선 | `bash scripts/check-template-security-baseline.sh` | 실패 0건 |
| VAL-SEC-004 | Traceability | 문서 추적성 검증 | `bash scripts/check-doc-traceability.sh` | 실패 0건 |
| VAL-SEC-005 | Regression | auth 하드닝 회귀 복구 확인 | `bash scripts/check-auth-hardening.sh` | 실패 0건 |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Vault 내부 시크릿 경로/키 미정합 | High | 템플릿 계약 문서화 + runbook 복구 절차 제공 |
| 단일 노드 유지로 인한 가용성 리스크 | Medium | HA 확장(raft 3-node) 전환 절차를 ops/runbook에 명시 |
| CI 게이트 추가로 초기 실패 증가 | Medium | 스크립트 계약을 현재 구성과 동기화 후 적용 |
| 문서 링크 회귀 | Medium | README 인덱스/상호 링크를 동일 변경 세트에서 갱신 |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: `check-security-hardening`, `check-auth-hardening`, `check-doc-traceability` 통과
- **Sandbox / Canary Rollout**: vault compose 검증 후 단계 반영
- **Human Approval Gate**: auto-unseal/원격 audit 전환은 운영 승인 필수
- **Rollback Trigger**: vault-agent health fail 지속, template render 실패 지속
- **Prompt / Model Promotion Criteria**: N/A

## Completion Criteria

- [x] 03-security 구성 하드닝 반영
- [x] security-hardening 검증/CI 게이트 반영
- [x] auth hardening 회귀 수정 반영
- [x] 01~09 문서/README 인덱스 동기화
- [ ] runtime 검증(환경 가능 시) 증적 확보

## Related Documents

- **PRD**: [../01.prd/2026-03-28-03-security-optimization-hardening.md](../01.prd/2026-03-28-03-security-optimization-hardening.md)
- **ARD**: [../02.ard/0018-security-optimization-hardening-architecture.md](../02.ard/0018-security-optimization-hardening-architecture.md)
- **ADR**: [../03.adr/0018-vault-hardening-and-ha-expansion-strategy.md](../03.adr/0018-vault-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../04.specs/03-security/spec.md](../04.specs/03-security/spec.md)
- **Tasks**: [../06.tasks/2026-03-28-03-security-optimization-hardening-tasks.md](../06.tasks/2026-03-28-03-security-optimization-hardening-tasks.md)
- **Guide**: [../07.guides/03-security/vault.md](../07.guides/03-security/vault.md)
- **Operations**: [../08.operations/03-security/vault.md](../08.operations/03-security/vault.md)
- **Runbooks**: [../09.runbooks/03-security/vault.md](../09.runbooks/03-security/vault.md)
