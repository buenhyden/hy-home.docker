---
title: "Local-Isolated Readiness Evidence"
version: "1.1.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-11-10"
layer: "architecture"
artifact_id: "ADR-0028"
parent_ids:
- "AD-0028"
created: "2026-07-19"
---
# ADR-0028: Local-Isolated Readiness Evidence

## Context

Compose rendering and static validation do not prove observed readiness,
artifact trust, or promotion/rollback. The repository
implements the current scripts and sample service that perform these three
lanes, and their execution must not encroach on other workloads or remote state.

## Decision Drivers

- Observe real behavior without changing production, shared runtime, registry,
  or credentials.
- Keep state and Docker resources within a task-owned boundary.
- Bind supply-chain and delivery judgments to an immutable image digest.
- Do not let network-dependent observation destabilize blocking CI.

## Options

### Static-only validation

Safe and fast, but does not prove runtime, recovery, tamper, or rollback
behavior.

### Local-isolated contract-first rehearsal

Independently validates the three lanes using synthetic input and a unique
project identity. Production realism is limited, but blast radius and
reproducibility are clear.

### Remote-first validation

Can validate real registry and control plane, but requires credential and
external state changes that exceed the current approval scope.

## Decision

Adopt local-isolated contract-first rehearsal.

- Compose readiness: `check-compose-core-readiness.sh` and the common library
  validate the exact service set, timeout, health, and owned teardown.
- Supply chain: `verify-sample-service-supply-chain.sh` and
  `check-supply-chain-policy.py` combine SBOM, policy, provenance, signature,
  and negative fixtures on the sample-service digest.
- Delivery: `rehearse-sample-service-delivery.sh` validates canary, promotion,
  injected failure, and previous-digest rollback of the verified digest.
- Network-dependent remote observation is advisory; deterministic local policy
  and fixtures own the blocking judgment.

## Consequences

- Real-behavior evidence can be reproduced with a small local blast radius.
- Cannot claim production topology, full Compose profile, live data recovery,
  or remote release control completion.
- Raw output and ephemeral key material cannot become tracked evidence, and the
  current Task retains only a secret-scrubbed summary.

### Follow-up

On 2026-11-10 the owner directed retirement of the PostgreSQL recovery lane,
amended here in place. That lane ran `rehearse-postgres-logical-upgrade.sh`, a
synthetic PostgreSQL 17 to 18 logical backup, restore, upgrade, and integrity
oracle rehearsal with runbook RUN-0032. Every HOME PostgreSQL service already
runs major 18 and no later major image exists, so the pinned 17 to 18 harness
had nothing left to rehearse and could not follow image updates. The harness,
its fixture, test, and runbook were deleted and REQ-0025-FR-0003 retired.

## Related Documents

### Traceability

- [REQ-0025 Operational Readiness Closure](../../01.requirements/0025-operational-readiness-closure.md)
- [AD-0028 Operational Readiness Closure](../descriptions/0028-operational-readiness-closure.md)
- `examples/sample-web-service/`
- `tests/validation/test_compose_core_readiness.py`
- `tests/lib/supply_chain/test_supply_chain_policy.py`
- `tests/validation/test_sample_service_delivery_rehearsal.py`
