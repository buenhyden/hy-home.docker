---
title: "Local-Isolated Readiness Evidence"
version: "2.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "architecture"
artifact_id: "ADR-0028"
parent_ids:
- "AD-0028"
created: "2026-07-19"
---

# ADR-0028: Local-Isolated Readiness Evidence

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the architecture-decision payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Context

##### Problem and Drivers

Compose rendering and static validation do not prove observed readiness,
artifact trust, or promotion/rollback. The repository
implements the current scripts and sample service that perform these three
lanes, and their execution must not encroach on other workloads or remote state.

- Observe real behavior without changing production, shared runtime, registry,
  or credentials.
- Keep state and Docker resources within a task-owned boundary.
- Bind supply-chain and delivery judgments to an immutable image digest.
- Do not let network-dependent observation destabilize blocking CI.

###### Sources
<!-- core-payload-level:4 -->

- [REQ-0025 Operational Readiness Closure](../../01.requirements/0025-operational-readiness-closure.md)
- [AD-0028 Operational Readiness Closure](../01.descriptions/0028-operational-readiness-closure.md)
- `examples/sample-web-service/`
- `tests/validation/test_compose_core_readiness.py`
- `tests/lib/supply_chain/test_supply_chain_policy.py`
- `tests/validation/test_sample_service_delivery_rehearsal.py`

##### Decision Scope

The decision covers the three lanes of compose readiness, supply chain, and delivery, run as local-isolated rehearsal. It does not claim production topology, full Compose profile, live data recovery, or remote release control completion.

#### Options

##### Considered Options

###### Static-only validation
<!-- core-payload-level:4 -->

Safe and fast, but does not prove runtime, recovery, tamper, or rollback
behavior.

###### Local-isolated contract-first rehearsal
<!-- core-payload-level:4 -->

Independently validates the three lanes using synthetic input and a unique
project identity. Production realism is limited, but blast radius and
reproducibility are clear.

###### Remote-first validation
<!-- core-payload-level:4 -->

Can validate real registry and control plane, but requires credential and
external state changes that exceed the current approval scope.

##### Trade-offs

| Option | Benefit | Cost and Risk | Reason |
| --- | --- | --- | --- |
| Static-only validation | Safe and fast. | Does not prove runtime, recovery, tamper, or rollback behavior. | Not chosen because it does not prove runtime, recovery, tamper, or rollback behavior. |
| Local-isolated contract-first rehearsal | Independently validates the three lanes using synthetic input and a unique project identity, with a clear blast radius and reproducibility. | Production realism is limited; it cannot claim production topology, full Compose profile, live data recovery, or remote release control completion. | Chosen because it accepts limited production realism for a clear blast radius and reproducibility. |
| Remote-first validation | Can validate the real registry and control plane. | Requires credential and external state changes that exceed the current approval scope. | Not chosen because it requires credential and external state changes that exceed the current approval scope. |

Static-only validation was not chosen because it does not prove runtime, recovery, tamper, or rollback behavior. Remote-first validation was not chosen because it requires credential and external state changes that exceed the current approval scope. The chosen rehearsal accepts limited production realism for a clear blast radius and reproducibility.

#### Decision

##### Chosen Option

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

##### Authority and Effect

Decided by the owner, @buenhyden; status `accepted`. No separate approval record is linked. Effective from 2026-07-19. On 2026-11-10 the owner directed the amendment recorded under Follow-up.

#### Consequences

##### Impacts

- Real-behavior evidence can be reproduced with a small local blast radius.
- Cannot claim production topology, full Compose profile, live data recovery,
  or remote release control completion.
- Raw output and ephemeral key material cannot become tracked evidence, and the
  current Task retains only a secret-scrubbed summary.

##### Follow-up

On 2026-11-17 the owner, @buenhyden, directed an in-place amendment of this
record: its sections moved line for line to the core decision form, and the
options table under Trade-offs was derived from the options it records. The
decision text is unchanged.

On 2026-11-10 the owner directed retirement of the PostgreSQL recovery lane,
amended here in place. That lane ran `rehearse-postgres-logical-upgrade.sh`, a
synthetic PostgreSQL 17 to 18 logical backup, restore, upgrade, and integrity
oracle rehearsal with runbook RUN-0032. Every HOME PostgreSQL service already
runs major 18 and no later major image exists, so the pinned 17 to 18 harness
had nothing left to rehearse and could not follow image updates. The harness,
its fixture, test, and runbook were deleted and REQ-0025-FR-0003 retired.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
