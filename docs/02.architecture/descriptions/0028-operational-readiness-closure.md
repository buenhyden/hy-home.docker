---
title: "Operational Readiness Closure Architecture"
version: "1.0.0"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
layer: "architecture"
artifact_id: "AD-0028"
parent_ids:
- "REQ-0025"
created: "2026-07-19"
---
# Operational Readiness Closure Architecture

## Context and Stakeholders

이 아키텍처는 Compose readiness, PostgreSQL logical recovery, sample-service
supply chain, local delivery를 하나의 격리 원칙으로 정렬한다. Maintainer,
operator, security reviewer, release reviewer는 각 lane의 subject identity,
failure boundary, cleanup, evidence를 독립적으로 검증해야 한다.

## System Boundaries

- 실행은 repository-local, task-scoped Docker resource와 synthetic input으로
  제한한다.
- `examples/sample-web-service/`가 supply-chain과 delivery의 공통 artifact다.
- PostgreSQL lane은 synthetic schema/data와 task-owned temporary volume만
  사용한다.
- Registry publication, production/shared runtime, live data, credential,
  remote deployment와 GitHub setting mutation은 경계 밖이다.
- Raw artifact와 log는 transient이며 current Task에는 redacted summary만
  남는다.

## Components

| Lane | Current implementation | Primary output |
| --- | --- | --- |
| Compose readiness | `scripts/validation/run-compose-core-readiness.sh` and `compose-core-readiness.lib.sh` | bounded readiness and cleanup verdict |
| PostgreSQL recovery | `scripts/lib/ops/rehearse-postgres-logical-upgrade.sh` | backup/restore and integrity verdict |
| Supply chain | `scripts/security/verify-sample-service-supply-chain.sh` and `scripts/validation/check-supply-chain-policy.py` | digest-bound trust verdict |
| Local delivery | `scripts/operations/rehearse-sample-service-delivery.sh` | canary, promotion, rollback verdict |

Focused tests supply deterministic positive and negative fixtures for these
components. Operations documents provide operator-facing invocation and
recovery guidance without owning the architectural decision.

## Data Flow

각 wrapper는 `preflight → allocate → execute → verify → summarize → cleanup`
순서를 따른다. Compose lane의 readiness와 supply-chain lane의 verified digest가
delivery input이 된다. Recovery lane은 별도 synthetic state와 integrity oracle을
사용한다. Failure는 required verification을 건너뛰지 않으며 owned cleanup
결과와 함께 non-zero로 종료한다.

## Deployment View

Tracked scripts, policies, schemas, sample artifact와 fixtures가 실행 계약을
정의한다. Runtime container, volume, network, generated SBOM, signature working
file, database state는 task-scoped transient resource다. 실행 전 exact target과
승인 경계를 확인하며 unknown identity에는 자동 cleanup 또는 promotion을
수행하지 않는다.

## Quality Attributes

- **Isolation**: unique project identity와 label로 다른 workload를 보호한다.
- **Security**: secret와 private key를 durable evidence에서 배제하고 digest
  mismatch를 fail closed한다.
- **Reproducibility**: versioned tool/policy/fixture와 explicit timeout을
  사용한다.
- **Recoverability**: configuration rollback과 data recovery를 구분한다.
- **Observability**: subject, transition, result, cleanup, stable failure class를
  비밀 없이 요약한다.

## Traceability

- [REQ-0025 Operational Readiness Closure](../../01.requirements/0025-operational-readiness-closure.md)
- [ADR-0028 Local-Isolated Readiness Evidence](../decisions/0028-local-isolated-readiness-evidence.md)
- `examples/sample-web-service/`
- `tests/validation/test_compose_core_readiness.py`
- `tests/validation/test_postgres_logical_upgrade_rehearsal.py`
- `tests/validation/test_supply_chain_policy.py`
- `tests/validation/test_sample_service_delivery_rehearsal.py`
