---
title: "04-Data Hardening Gate and Staged Expansion"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-24"
layer: "architecture"
artifact_id: "ADR-0040"
parent_ids:
- "AD-0019"
supersedes:
- "ADR-0019"
created: "2026-09-24"
---

# ADR-0040: 04-Data Hardening Gate and Staged Expansion

## Context

ADR-0019는 `04-data` 계층의 즉시 하드닝 항목을 먼저 반영하고, HA·lifecycle·
backup/recovery 확장은 정책과 절차로 단계적으로 도입하기로 결정했다. 즉시 항목
가운데 `ksql` tier label 정규화는 ksqlDB가 SPEC-0180 S19에서 제거되어(ADR-0039)
더 이상 대상이 없다. 나머지 결정은 그대로 유효하므로, 이 ADR은 현재 서비스 기준으로
같은 결정을 다시 적는다.

04-data는 여러 엔진으로 이루어져 한 번에 바꾸면 장애 반경이 크다. 그래서 회귀를
막는 자동 검증 gate가 필요하다.

## Decision

- 즉시 하드닝 항목은 Compose 계약으로 구현하고 gate로 지킨다.
  - `supabase` 핵심 서비스 healthcheck 계약
  - `valkey-cluster-exporter` 시크릿 경로를 `service_valkey_password`로 정규화
  - `seaweedfs` malformed expose token 금지
  - `scripts/hardening/check-all-hardening.sh 04-data`와 CI `infrastructure-hardening`
    gate
- 새 04-data 서비스(예: SPEC-0180의 lakehouse 엔진)는 같은 gate에 자기 검사를
  더한다.
- HA, lifecycle, backup/recovery drill 같은 확장은 정책과 runbook의 승인된 전환
  절차로 관리한다.
- `template-stateful-*`, `template-infra-*` 상속 모델을 유지한다.

## Consequences

- **Positive**:
  - 04-data 구성 회귀를 CI에서 일찍 막는다.
  - 확장 과제가 운영 정책과 연결되어 우선순위가 분명하다.
- **Trade-offs**:
  - healthcheck는 liveness부터 시작하며 readiness 고도화는 후속 단계다.
  - 엔진별 성능·HA 개선은 단계적으로 해야 한다.

### Explicit Non-goals

- 각 엔진의 대규모 HA topology 재구성
- 비즈니스 query 최적화와 schema refactoring
- 클라우드 관리형 서비스 전환

## Options Considered

### 모든 04-data 서비스를 동시에 HA 기준으로 확장

- **Good**: 가용성을 빠르게 높일 수 있다.
- **Bad**: 변경 반경이 크고 회귀 원인을 가르기 어렵다.

### 문서만 갱신하고 Compose와 CI 변경을 보류

- **Good**: 단기 변경 위험이 낮다.
- **Bad**: 실제 운영 회귀를 막지 못한다.

## Traceability

근거는 `check-all-hardening.sh`의 04-data 검사, CI `infrastructure-hardening`
gate와 현재 저장소 구성이다. 기록되지 않은 런타임 상태는 주장하지 않는다.

## Related Documents

- **Superseded ADR**: `ADR-0019` (`docs/98.archive/superseded/`에 보존)
- **Architecture Description**: [0019-data-optimization-hardening-architecture.md](../descriptions/0019-data-optimization-hardening-architecture.md)
- **Requirements**: [0004-data.md](../../01.requirements/0004-data.md)
- **Related ADR**: [ADR-0004](0004-postgresql-ha-patroni.md), [ADR-0039](0039-analytics-engines-after-lakehouse-convergence.md)
