---
title: "Operational Readiness Closure Architecture"
version: "1.0.3"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "AD-0028"
parent_ids:
- "REQ-0025"
created: "2026-07-19"
---
# Operational Readiness Closure Architecture

## Context and Stakeholders

This architecture aligns Compose readiness, PostgreSQL logical recovery,
sample-service supply chain, and local delivery under one isolation
principle. The maintainer, operator, security reviewer, and release reviewer
must each independently verify the subject identity, failure boundary,
cleanup, and evidence of every lane.

## System Boundaries

- Execution is limited to repository-local, task-scoped Docker resources and
  synthetic input.
- `examples/sample-web-service/` is the shared artifact for supply-chain and
  delivery.
- The PostgreSQL lane uses only synthetic schema/data and a task-owned
  temporary volume.
- Registry publication, production/shared runtime, live data, credentials,
  remote deployment, and GitHub setting mutation are out of bounds.
- Raw artifacts and logs are transient, and only a redacted summary remains
  in the current Task.

## Components

| Lane | Current implementation | Primary output |
| --- | --- | --- |
| Compose readiness | `scripts/operations/check-compose-core-readiness.sh` and `scripts/lib/ops/compose-core-readiness.sh` | bounded readiness and cleanup verdict |
| PostgreSQL recovery | `scripts/operations/rehearse-postgres-logical-upgrade.sh` | backup/restore and integrity verdict |
| Supply chain | `scripts/security/verify-sample-service-supply-chain.sh` and `scripts/validation/check-supply-chain-policy.py` | digest-bound trust verdict |
| Local delivery | `scripts/operations/rehearse-sample-service-delivery.sh` | canary, promotion, rollback verdict |

Focused tests supply deterministic positive and negative fixtures for these
components. Operations documents provide operator-facing invocation and
recovery guidance without owning the architectural decision.

## Data Flow

Each wrapper follows the `preflight → allocate → execute → verify → summarize → cleanup`
order. The Compose lane's readiness and the
supply-chain lane's verified digest become delivery input. The recovery lane
uses a separate synthetic state and integrity oracle. A failure does not skip
required verification and exits non-zero along with the owned cleanup
result.

## Deployment View

Tracked scripts, policies, schemas, sample artifacts, and fixtures define the
execution contract. Runtime containers, volumes, networks, generated SBOM,
signature working files, and database state are task-scoped transient
resources. Before execution, confirm the exact target and approval boundary,
and never run automatic cleanup or promotion against an unknown identity.

## Quality Attributes

- **Isolation**: protect other workloads with a unique project identity and
  label.
- **Security**: exclude secrets and private keys from durable evidence, and
  fail closed on a digest mismatch.
- **Reproducibility**: use versioned tools/policies/fixtures and explicit
  timeouts.
- **Recoverability**: distinguish configuration rollback from data recovery.
- **Observability**: summarize the subject, transition, result, cleanup, and
  stable failure class without secrets.

## Traceability

- [REQ-0025 Operational Readiness Closure](../../01.requirements/0025-operational-readiness-closure.md)
- [ADR-0028 Local-Isolated Readiness Evidence](../decisions/0028-local-isolated-readiness-evidence.md)
- `examples/sample-web-service/`
- `tests/validation/test_compose_core_readiness.py`
- `tests/validation/test_postgres_logical_upgrade_rehearsal.py`
- `tests/lib/supply_chain/test_supply_chain_policy.py`
- `tests/validation/test_sample_service_delivery_rehearsal.py`

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.
