---
title: "Operational Readiness Closure Architecture"
version: "1.2.0"
type: "sdlc/architecture-description"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "architecture"
artifact_id: "AD-0028"
parent_ids:
- "REQ-0025"
created: "2026-07-19"
---

# Operational Readiness Closure Architecture

## Context and Boundaries

### System Boundary

- Execution is limited to repository-local, task-scoped Docker resources and
  synthetic input.
- `examples/sample-web-service/` is the shared artifact for supply-chain and
  delivery.
- Registry publication, production/shared runtime, live data, credentials,
  remote deployment, and GitHub setting mutation are out of bounds.
- Raw artifacts and logs are transient, and only a redacted summary remains
  in the current Task.

#### Purpose and Readers

This architecture aligns Compose readiness, sample-service supply chain, and local delivery under one isolation
principle. The maintainer, operator, security reviewer, and release reviewer
must each independently verify the subject identity, failure boundary,
cleanup, and evidence of every lane.

#### Context

The maintainer, operator, security reviewer and release reviewer verify each lane. The lanes act on repository-local, task-scoped Docker resources and synthetic input, with `examples/sample-web-service/` as the shared artifact for supply chain and delivery.

### Constraints

Execution is limited to repository-local, task-scoped Docker resources and synthetic input. Registry publication, production or shared runtime, live data, credentials, remote deployment and GitHub setting mutation are out of bounds, and secrets and private keys stay out of durable evidence.

## Structure

### Building Blocks

| Lane | Current implementation | Primary output |
| --- | --- | --- |
| Compose readiness | `scripts/operations/check-compose-core-readiness.sh` and `scripts/lib/ops/compose-core-readiness.sh` | bounded readiness and cleanup verdict |
| Supply chain | `scripts/security/verify-sample-service-supply-chain.sh` and `scripts/validation/check-supply-chain-policy.py` | digest-bound trust verdict |
| Local delivery | `scripts/operations/rehearse-sample-service-delivery.sh` | canary, promotion, rollback verdict |

Focused tests supply deterministic positive and negative fixtures for these
components. Operations documents provide operator-facing invocation and
recovery guidance without owning the architectural decision.

### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| Compose readiness lane | `scripts/operations/check-compose-core-readiness.sh` and `scripts/lib/ops/compose-core-readiness.sh` | Local delivery lane and the current Task | `tests/validation/test_compose_core_readiness.py` | A failure does not skip required verification and exits non-zero with the owned cleanup result. |
| Supply-chain verified digest | `scripts/security/verify-sample-service-supply-chain.sh` and `scripts/validation/check-supply-chain-policy.py` | Local delivery lane | `tests/lib/supply_chain/test_supply_chain_policy.py` | A digest mismatch fails closed. |
| Local delivery rehearsal | `scripts/operations/rehearse-sample-service-delivery.sh` | The current Task | `tests/validation/test_sample_service_delivery_rehearsal.py` | Automatic cleanup and promotion act only on an identity the lane allocated itself; configuration rollback is distinct from data recovery. |
| Shared sample artifact | `examples/sample-web-service/` | Supply-chain and local delivery lanes | `examples/sample-web-service/` | The description records no failure handling for this interface. |

- Each wrapper follows the `preflight → allocate → execute → verify → summarize → cleanup` order.
- The Compose lane's readiness and the supply-chain lane's verified digest become delivery input.
- Each lane's primary output is listed in the Building Blocks table.

## Runtime Behavior

### Normal Flow

#### Runtime View

Each wrapper follows the `preflight → allocate → execute → verify → summarize → cleanup`
order. The Compose lane's readiness and the
supply-chain lane's verified digest become delivery input. A failure does not skip
required verification and exits non-zero along with the owned cleanup
result.

#### Deployment View

Tracked scripts, policies, schemas, sample artifacts, and fixtures define the
execution contract. Runtime containers, volumes, networks, generated SBOM,
signature working files, and database state are task-scoped transient
resources. Automatic cleanup and promotion act only on an identity the lane
allocated itself.

### Failure and Recovery

A failure does not skip required verification and exits non-zero along with the owned cleanup result. A digest mismatch fails closed, and automatic cleanup and promotion act only on an identity the lane allocated itself. Configuration rollback is distinct from data recovery.

## Quality Scenarios

### Scenarios

#### Quality Attributes

- **Isolation**: protect other workloads with a unique project identity and
  label.
- **Security**: exclude secrets and private keys from durable evidence, and
  fail closed on a digest mismatch.
- **Reproducibility**: use versioned tools/policies/fixtures and explicit
  timeouts.
- **Recoverability**: distinguish configuration rollback from data recovery.
- **Observability**: summarize the subject, transition, result, cleanup, and
  stable failure class without secrets.

#### Risks

- The lanes prove behavior on synthetic input in task-scoped resources only;
  they establish nothing about production data or a shared runtime.

### Trade-offs

- The lanes run only on synthetic input in task-scoped resources, which
  protects other workloads but establishes nothing about production data or a
  shared runtime (System Boundary, Risks).
- Raw artifacts and logs are transient and only a redacted summary remains in
  the current Task, keeping secrets and private keys out of durable evidence
  (System Boundary, Quality Attributes).
- Configuration rollback is kept distinct from data recovery; the PostgreSQL
  recovery lane was removed on 2026-11-10 (Quality Attributes, Evolution).

## Decisions and Adoption

### Decisions

- [ADR-0028 Local-Isolated Readiness Evidence](../decisions/0028-local-isolated-readiness-evidence.md)

### Adoption Boundaries

#### Requirement Mapping

- [REQ-0025 Operational Readiness Closure](../../01.requirements/0025-operational-readiness-closure.md)

#### Currentness and Lineage

- `examples/sample-web-service/`
- `tests/validation/test_compose_core_readiness.py`
- `tests/lib/supply_chain/test_supply_chain_policy.py`
- `tests/validation/test_sample_service_delivery_rehearsal.py`

#### Evolution

- A new lane follows the same wrapper order and isolation boundary.
- The PostgreSQL recovery lane, a synthetic 17 to 18 logical upgrade
  rehearsal, was removed on 2026-11-10 because every HOME PostgreSQL service
  already runs major 18; ADR-0028 Follow-up records the retirement.

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.
