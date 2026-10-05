---
title: "Local-Isolated Readiness Evidence"
version: "1.0.2"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0028"
parent_ids:
- "AD-0028"
created: "2026-07-19"
---
# ADR-0028: Local-Isolated Readiness Evidence

## Context

Compose rendering and static validation do not prove observed readiness,
representative recovery, artifact trust, or promotion/rollback. The repository
implements the current scripts and sample service that perform these four
lanes, and their execution must not encroach on other workloads or remote state.

## Decision

### Decision

### Decision Drivers

- Observe real behavior without changing production, shared runtime, registry,
  or credentials.
- Keep state and Docker resources within a task-owned boundary.
- Bind supply-chain and delivery judgments to an immutable image digest.
- Do not let network-dependent observation destabilize blocking CI.

### Decision

Adopt local-isolated contract-first rehearsal.

- Compose readiness: `check-compose-core-readiness.sh` and the common library
  validate the exact service set, timeout, health, and owned teardown.
- PostgreSQL recovery: `rehearse-postgres-logical-upgrade.sh` validates
  synthetic logical backup/restore, representative upgrade, and the integrity
  oracle.
- Supply chain: `verify-sample-service-supply-chain.sh` and
  `check-supply-chain-policy.py` combine SBOM, policy, provenance, signature,
  and negative fixtures on the sample-service digest.
- Delivery: `rehearse-sample-service-delivery.sh` validates canary, promotion,
  injected failure, and previous-digest rollback of the verified digest.
- Network-dependent remote observation is advisory; deterministic local policy
  and fixtures own the blocking judgment.

## Alternatives

### Alternatives

### Options Considered

### Static-only validation

Safe and fast, but does not prove runtime, recovery, tamper, or rollback
behavior.

### Local-isolated contract-first rehearsal

Independently validates the four lanes using synthetic input and a unique
project identity. Production realism is limited, but blast radius and
reproducibility are clear.

### Remote-first validation

Can validate real registry and control plane, but requires credential and
external state changes that exceed the current approval scope.

## Consequences

- Real-behavior evidence can be reproduced with a small local blast radius.
- Cannot claim production topology, full Compose profile, live data recovery,
  or remote release control completion.
- Raw output and ephemeral key material cannot become tracked evidence, and the
  current Task retains only a secret-scrubbed summary.

## Related Documents

### Traceability

- [REQ-0025 Operational Readiness Closure](../../01.requirements/0025-operational-readiness-closure.md)
- [AD-0028 Operational Readiness Closure](../descriptions/0028-operational-readiness-closure.md)
- `examples/sample-web-service/`
- `tests/validation/test_compose_core_readiness.py`
- `tests/validation/test_postgres_logical_upgrade_rehearsal.py`
- `tests/lib/supply_chain/test_supply_chain_policy.py`
- `tests/validation/test_sample_service_delivery_rehearsal.py`
