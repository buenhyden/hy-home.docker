---
title: Local-Isolated Readiness Evidence
type: sdlc/architecture-decision
layer: architecture
status: active
owner: "@buenhyden"
artifact_id: ADR-0028
parent_ids:
  - AD-0028
created: 2026-07-19
updated: 2026-09-01
---
# ADR-0028: Local-Isolated Readiness Evidence

## Context

Compose rendering과 정적 검증은 observed readiness, representative recovery,
artifact trust, promotion/rollback을 증명하지 않는다. 저장소에는 이 네 lane을
수행하는 현재 스크립트와 sample service가 구현되어 있으며, 그 실행은 다른
workload와 원격 상태를 침범하지 않아야 한다.

## Decision Drivers

- 실제 동작을 관찰하되 production, shared runtime, registry, credential을
  변경하지 않는다.
- state와 Docker resource를 task-owned 경계 안에 둔다.
- supply-chain과 delivery 판정을 immutable image digest에 결합한다.
- network-dependent 관찰이 blocking CI를 불안정하게 만들지 않는다.

## Options Considered

### Static-only validation

안전하고 빠르지만 runtime, recovery, tamper, rollback 동작을 증명하지 못한다.

### Local-isolated contract-first rehearsal

Synthetic input과 고유 project identity를 사용해 네 lane을 독립적으로
검증한다. Production realism은 제한되지만 blast radius와 재현성이 명확하다.

### Remote-first validation

실제 registry와 control plane을 검증할 수 있지만 credential과 외부 상태
변경이 필요해 현재 승인 범위를 넘는다.

## Decision

Local-isolated contract-first rehearsal을 채택한다.

- Compose readiness는 `run-compose-core-readiness.sh`와 공통 library가 exact
  service set, timeout, health, owned teardown을 검증한다.
- PostgreSQL recovery는 `rehearse-postgres-logical-upgrade.sh`가 synthetic
  logical backup/restore, representative upgrade, integrity oracle을 검증한다.
- Supply chain은 `verify-sample-service-supply-chain.sh`와
  `check-supply-chain-policy.py`가 sample-service digest에 SBOM, policy,
  provenance, signature 및 negative fixtures를 결합한다.
- Delivery는 `rehearse-sample-service-delivery.sh`가 verified digest의 canary,
  promotion, injected failure, previous-digest rollback을 검증한다.
- Network-dependent remote observation은 advisory이며 deterministic local
  policy와 fixture가 blocking 판정을 소유한다.

## Consequences

- 실제 동작 evidence를 작은 로컬 blast radius로 재현할 수 있다.
- Production topology, 전체 Compose profile, live data recovery, remote
  release control 완료를 주장할 수 없다.
- Raw output과 ephemeral key material은 tracked evidence가 될 수 없고,
  current Task에는 비밀이 제거된 요약만 남는다.

## Traceability

- [REQ-0025 Operational Readiness Closure](../../01.requirements/0025-operational-readiness-closure.md)
- [AD-0028 Operational Readiness Closure](../descriptions/0028-operational-readiness-closure.md)
- `examples/sample-web-service/`
- `tests/validation/test_compose_core_readiness.py`
- `tests/validation/test_postgres_logical_upgrade_rehearsal.py`
- `tests/validation/test_supply_chain_policy.py`
- `tests/validation/test_sample_service_delivery_rehearsal.py`
