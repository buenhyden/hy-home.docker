---
title: "Operational Readiness Closure Architecture"
version: "1.1.1"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "architecture"
artifact_id: "AD-0028"
parent_ids:
- "REQ-0025"
created: "2026-07-19"
---

# Operational Readiness Closure Architecture

## Overview

### Purpose and Readers

This architecture aligns Compose readiness, sample-service supply chain, and local delivery under one isolation
principle. The maintainer, operator, security reviewer, and release reviewer
must each independently verify the subject identity, failure boundary,
cleanup, and evidence of every lane.

### System Boundary

- Execution is limited to repository-local, task-scoped Docker resources and
  synthetic input.
- `examples/sample-web-service/` is the shared artifact for supply-chain and
  delivery.
- Registry publication, production/shared runtime, live data, credentials,
  remote deployment, and GitHub setting mutation are out of bounds.
- Raw artifacts and logs are transient, and only a redacted summary remains
  in the current Task.

## Context and Constraints

### Context

The maintainer, operator, security reviewer and release reviewer verify each lane. The lanes act on repository-local, task-scoped Docker resources and synthetic input, with `examples/sample-web-service/` as the shared artifact for supply chain and delivery.

### Constraints

Execution is limited to repository-local, task-scoped Docker resources and synthetic input. Registry publication, production or shared runtime, live data, credentials, remote deployment and GitHub setting mutation are out of bounds, and secrets and private keys stay out of durable evidence.

## Current Structure

### Building Blocks

| Lane | Current implementation | Primary output |
| --- | --- | --- |
| Compose readiness | `scripts/operations/check-compose-core-readiness.sh` and `scripts/lib/ops/compose-core-readiness.sh` | bounded readiness and cleanup verdict |
| Supply chain | `scripts/security/verify-sample-service-supply-chain.sh` and `scripts/validation/check-supply-chain-policy.py` | digest-bound trust verdict |
| Local delivery | `scripts/operations/rehearse-sample-service-delivery.sh` | canary, promotion, rollback verdict |

Focused tests supply deterministic positive and negative fixtures for these
components. Operations documents provide operator-facing invocation and
recovery guidance without owning the architectural decision.

### Runtime and Deployment

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

## Interfaces

### Contracts

- Each wrapper follows the `preflight → allocate → execute → verify → summarize → cleanup` order.
- The Compose lane's readiness and the supply-chain lane's verified digest become delivery input.
- Each lane's primary output is listed in the Building Blocks table.

### Failure Boundaries

A failure does not skip required verification and exits non-zero along with the owned cleanup result. A digest mismatch fails closed, and automatic cleanup and promotion act only on an identity the lane allocated itself. Configuration rollback is distinct from data recovery.

## Decisions

### Decision Links

- [ADR-0028 Local-Isolated Readiness Evidence](../decisions/0028-local-isolated-readiness-evidence.md)

### Quality and Risks

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

## Traceability

### Requirement Mapping

- [REQ-0025 Operational Readiness Closure](../../01.requirements/0025-operational-readiness-closure.md)

### Currentness and Lineage

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
