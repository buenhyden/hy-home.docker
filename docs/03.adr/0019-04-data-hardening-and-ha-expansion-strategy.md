# ADR-0019: 04-Data Hardening and HA Expansion Strategy

## Overview (KR)

이 문서는 `04-data` 계층에 대해 즉시 적용 가능한 구성 하드닝을 우선 반영하고, 카탈로그 기반 확장 항목은 정책/절차 중심의 단계적 도입으로 관리하는 결정을 기록한다.

## Context

04-data는 다수의 엔진으로 구성되어 있어 단일 일괄 변경 시 장애 반경이 커질 수 있다. 현재 확인된 고위험 항목은 `supabase` healthcheck 공백, `valkey-cluster-exporter` 시크릿 경로 불일치, `seaweedfs` compose expose 오타, `ksql` tier 라벨 불일치다. 즉시 회귀 방지를 위해 자동 검증 게이트가 필요하다.

## Decision

- 즉시 하드닝 항목을 우선 구현한다.
  - `supabase` 핵심 서비스 healthcheck 계약 추가
  - `valkey-cluster-exporter` 시크릿 경로를 `service_valkey_password`로 정규화
  - `seaweedfs` malformed expose 토큰 제거
  - `ksql` tier 라벨 `data` 정규화
  - `scripts/check-data-hardening.sh` + CI `data-hardening` 게이트 추가
- 카탈로그 확장 항목(HA, lifecycle, backup/recovery drill)은 정책/런북에서 승인 가능한 전환 절차로 관리한다.
- 기존 `template-stateful-*`, `template-infra-*` 상속 모델은 유지한다.

## Explicit Non-goals

- 이번 변경에서 각 엔진의 대규모 HA 토폴로지 재구성
- 비즈니스 쿼리 최적화/스키마 리팩터링
- 클라우드 관리형 서비스 전환

## Consequences

- **Positive**:
  - 04-data 구성 회귀를 CI에서 조기 차단할 수 있다.
  - compose 계약 불일치로 인한 장애 가능성을 즉시 낮춘다.
  - 카탈로그 확장 과제를 운영 정책과 연결해 추진 우선순위를 명확히 한다.
- **Trade-offs**:
  - healthcheck는 우선 liveness 기준으로 시작하며 readiness 고도화는 후속 단계가 필요하다.
  - 엔진별 심화 성능/HA 개선은 단계적으로 이행해야 한다.

## Alternatives

### 즉시 모든 04-data 서비스를 HA 기준으로 동시 확장

- Good:
  - 빠른 기능적 확장/가용성 향상 가능
- Bad:
  - 변경 반경이 크고 회귀 원인 분리가 어렵다.

### 문서만 갱신하고 compose/CI 변경 보류

- Good:
  - 단기 변경 리스크가 낮다.
- Bad:
  - 실제 운영 회귀를 차단하지 못한다.

## Agent-related Example Decisions (If Applicable)

- Tool gating: `check-data-hardening.sh`를 PR/Push 게이트로 강제
- Guardrail strategy: 시크릿 경로 정합성, malformed compose 토큰 금지

## Related Documents

- **PRD**: [../01.prd/2026-03-28-04-data-optimization-hardening.md](../01.prd/2026-03-28-04-data-optimization-hardening.md)
- **ARD**: [../02.ard/0019-data-optimization-hardening-architecture.md](../02.ard/0019-data-optimization-hardening-architecture.md)
- **Spec**: [../04.specs/04-data/spec.md](../04.specs/04-data/spec.md)
- **Plan**: [../05.plans/2026-03-28-04-data-optimization-hardening-plan.md](../05.plans/2026-03-28-04-data-optimization-hardening-plan.md)
- **Tasks**: [../06.tasks/2026-03-28-04-data-optimization-hardening-tasks.md](../06.tasks/2026-03-28-04-data-optimization-hardening-tasks.md)
- **Related ADR**: [./0004-postgresql-ha-patroni.md](./0004-postgresql-ha-patroni.md)
