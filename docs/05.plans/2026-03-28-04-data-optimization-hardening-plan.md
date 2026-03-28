# 04-Data Optimization Hardening Implementation Plan

## Overview (KR)

이 문서는 `infra/04-data` 최적화/하드닝 실행 계획서다. 즉시 회귀 위험이 큰 구성 정합성 항목을 우선 반영하고, 카탈로그 확장 항목은 운영 정책/런북 기반으로 단계적 이행 계획을 정의한다.

## Context

- 기준 카탈로그: [12-infra-service-optimization-catalog.md](../08.operations/12-infra-service-optimization-catalog.md)
- 상위 우선순위 계획: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md)
- 즉시 하드닝 대상: `supabase`, `valkey-cluster`, `seaweedfs`, `ksql`

## Goals & In-Scope

- **Goals**:
  - 04-data compose 구성 정합성(healthcheck/시크릿/라벨/토큰)을 고정한다.
  - 04-data 전용 CI 하드닝 게이트를 도입한다.
  - 01~09 문서 체계를 optimization/hardening 문맥으로 동기화한다.
- **In Scope**:
  - `infra/04-data/operational/supabase/docker-compose.yml`
  - `infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml`
  - `infra/04-data/lake-and-object/seaweedfs/docker-compose.yml`
  - `infra/04-data/analytics/ksql/docker-compose.yml`
  - `scripts/check-data-hardening.sh`
  - `.github/workflows/ci-quality.yml`
  - `scripts/README.md`
  - `docs/01~09` + 관련 README 인덱스

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - 카탈로그 확장 항목의 즉시 실구현(전 서비스 동시)
  - 앱 레벨 성능 튜닝/쿼리 리팩터링
- **Out of Scope**:
  - 신규 데이터 엔진 도입
  - 클라우드 매니지드 데이터 플랫폼 전환

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-DATA-001 | `supabase` 핵심 서비스 healthcheck 보강 | `infra/04-data/operational/supabase/docker-compose.yml` | REQ-PRD-DATA-FUN-01 | compose config + 서비스 블록 healthcheck 확인 |
| PLN-DATA-002 | Valkey exporter 시크릿 경로 계약 정합화 | `infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml` | REQ-PRD-DATA-FUN-02 | stale secret path 0건 |
| PLN-DATA-003 | SeaweedFS expose 토큰 오타 제거 | `infra/04-data/lake-and-object/seaweedfs/docker-compose.yml` | REQ-PRD-DATA-FUN-03 | malformed expose 토큰 0건 |
| PLN-DATA-004 | ksql tier 라벨 정규화 | `infra/04-data/analytics/ksql/docker-compose.yml` | REQ-PRD-DATA-FUN-04 | `hy-home.tier: data` 확인 |
| PLN-DATA-005 | 04-data 하드닝 검증 스크립트 추가 | `scripts/check-data-hardening.sh` | REQ-PRD-DATA-FUN-05 | 스크립트 pass/fail 정상 동작 |
| PLN-DATA-006 | CI `data-hardening` job 추가 | `.github/workflows/ci-quality.yml` | REQ-PRD-DATA-FUN-05 | workflow 정적 점검 |
| PLN-DATA-007 | scripts 인덱스 갱신 | `scripts/README.md` | REQ-PRD-DATA-FUN-05 | README 항목/사용 예시 반영 |
| PLN-DATA-008 | PRD~Runbook 문서 생성/갱신 + 상호 링크 정합화 | `docs/01~09/**` | REQ-PRD-DATA-FUN-06 | 링크/인덱스 반영 확인 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-DATA-001 | Structural | Supabase compose 정적 검증 | `docker compose -f infra/04-data/operational/supabase/docker-compose.yml config` | 오류 없음 |
| VAL-DATA-002 | Structural | Valkey compose 정적 검증 | `docker compose -f infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml config` | 오류 없음 |
| VAL-DATA-003 | Structural | SeaweedFS compose 정적 검증 | `docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml config` | 오류 없음 |
| VAL-DATA-004 | Structural | ksql compose 정적 검증 | `docker compose -f infra/04-data/analytics/ksql/docker-compose.yml config` | 오류 없음 |
| VAL-DATA-005 | Compliance | 04-data 하드닝 검증 | `bash scripts/check-data-hardening.sh` | 실패 0건 |
| VAL-DATA-006 | Baseline | 템플릿/보안 기준선 | `bash scripts/check-template-security-baseline.sh` | 실패 0건 |
| VAL-DATA-007 | Traceability | 문서 추적성 | `bash scripts/check-doc-traceability.sh` | 실패 0건 |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| liveness 기반 healthcheck 한계 | Medium | 후속 단계에서 readiness endpoint 기반으로 고도화 |
| 다중 서비스 동시 변경으로 인한 파급 | High | 즉시 하드닝 범위를 정합성 항목으로 제한 |
| 카탈로그 확장 미완료 | Medium | 정책/런북에 승인 조건과 전환 절차를 선반영 |
| 문서 링크 회귀 | Medium | README 인덱스와 상호 링크를 동일 변경 세트에서 갱신 |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: `check-data-hardening`, `check-template-security-baseline`, `check-doc-traceability`
- **Sandbox / Canary Rollout**: 04-data 서비스별 compose config 검증 후 단계 반영
- **Human Approval Gate**: HA 확장/보존 정책/외부 노출 정책 변경 시 운영 승인 필수
- **Rollback Trigger**: healthcheck fail 지속, exporter 인증 실패, compose 파싱 오류
- **Prompt / Model Promotion Criteria**: N/A

## Completion Criteria

- [x] 04-data 즉시 하드닝 항목 반영
- [x] data-hardening 검증/CI 게이트 반영
- [x] 01~09 문서 및 README 인덱스 동기화
- [ ] runtime 검증 증적 확보(환경 가능 시)

## Related Documents

- **PRD**: [../01.prd/2026-03-28-04-data-optimization-hardening.md](../01.prd/2026-03-28-04-data-optimization-hardening.md)
- **ARD**: [../02.ard/0019-data-optimization-hardening-architecture.md](../02.ard/0019-data-optimization-hardening-architecture.md)
- **ADR**: [../03.adr/0019-04-data-hardening-and-ha-expansion-strategy.md](../03.adr/0019-04-data-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../04.specs/04-data/spec.md](../04.specs/04-data/spec.md)
- **Tasks**: [../06.tasks/2026-03-28-04-data-optimization-hardening-tasks.md](../06.tasks/2026-03-28-04-data-optimization-hardening-tasks.md)
- **Guide**: [../07.guides/04-data/optimization-hardening.md](../07.guides/04-data/optimization-hardening.md)
- **Operations**: [../08.operations/04-data/optimization-hardening.md](../08.operations/04-data/optimization-hardening.md)
- **Runbooks**: [../09.runbooks/04-data/optimization-hardening.md](../09.runbooks/04-data/optimization-hardening.md)
