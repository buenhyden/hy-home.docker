---
title: "Operational Readiness Closure Requirements"
version: "1.0.2"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "requirements"
artifact_id: "REQ-0025"
parent_ids: []
created: "2026-07-19"
---
# Operational Readiness Closure Requirements

## Problem and Goals

Static documents and Compose rendering alone cannot prove startup/readiness,
data recovery, artifact trust, or promotion/rollback behavior. This
requirement reproduces the four behaviors in a locally isolated environment
using sample artifacts and synthetic state owned by the repository, and
records the actually verified scope without overstatement.

## Stakeholders and User Needs

- The maintainer must distinguish implemented readiness behavior from
  unapproved remote operations.
- The operator needs a guarantee that the rehearsal does not change another
  Docker project or real data.
- The security reviewer must confirm that supply-chain verdicts are bound to
  the same image digest.
- The release reviewer must reproduce that a failed canary is not promoted
  and is rolled back to the previous digest.

## Functional Requirements

- **REQ-0025-FR-0001**: The approved `core` service set must start under a
  unique Compose project and provide bounded readiness and teardown results.
- **REQ-0025-FR-0002**: The runtime rehearsal must use synthetic
  configuration and task-owned network/volume/project identity.
- **REQ-0025-FR-0003**: The PostgreSQL rehearsal must perform logical backup,
  restore, a representative major-version upgrade, and integrity comparison
  of synthetic state.
- **REQ-0025-FR-0004**: SBOM, vulnerability verdict, provenance, and
  signature verification for `examples/sample-web-service` must be bound to
  the same image digest and reject tampering and identity mismatch.
- **REQ-0025-FR-0005**: Supply-chain tools must use the version and container
  image identity declared by the repository and must not require a
  host-global install.
- **REQ-0025-FR-0006**: Network-dependent security observations must be
  marked advisory, and deterministic local policy and fixtures must own the
  CI verdict.
- **REQ-0025-FR-0007**: The delivery rehearsal must deploy only a verified
  digest as canary and promote to the local stable target only after it
  passes the health gate.
- **REQ-0025-FR-0008**: On failure after canary or promotion, roll back to
  the previous verified digest and confirm post-rollback health.
- **REQ-0025-FR-0009**: Execution results must be recorded in the active
  Spec Package's current Task with command, scope, result, cleanup, and
  review, and must match the lifecycle state.
- **REQ-0025-FR-0010**: Raw runtime output must stay only in ignored or
  process-local temporary storage; durable evidence must contain only a
  secret-scrubbed summary and immutable subject identity.

## Non-functional Requirements

- **REQ-0025-NFR-0011 — Isolation**: Every resource must be identified by a
  task-owned identity, and cleanup must apply only to that resource.
- **REQ-0025-NFR-0012 — Security**: Secrets, private keys, tokens, raw auth
  logs, and production data must not be stored in tracked evidence.
- **REQ-0025-NFR-0013 — Determinism**: A blocking gate must reproduce the
  same pass/fail result without network access, using versioned inputs and
  fixtures.
- **REQ-0025-NFR-0014 — Fail closed**: Target ambiguity, digest or integrity
  mismatch, and cleanup failure must not be treated as success or skip.
- **REQ-0025-NFR-0015 — Traceability**: Traceability must be maintained
  between this Requirement, AD-0028, ADR-0028, the implementation scripts,
  the Operations procedure, and current Task results.
- **REQ-0025-NFR-0016 — Honest scope**: Local rehearsal success must not be
  overstated as production readiness, full-profile coverage, live recovery,
  or remote release completion.

## Constraints

- Scope is limited to local isolated Compose readiness, synthetic PostgreSQL
  logical recovery, sample-service supply chain, and local
  promotion/rollback.
- Production/shared runtime, real data, registry publication, OIDC signing,
  and remote GitHub configuration and deployment are out of scope.
- Automatic cleanup is allowed only for precisely identified task-owned
  resources.

## Acceptance Criteria

- `check-compose-core-readiness.sh` verifies readiness, timeout, and cleanup
  boundaries.
- `rehearse-postgres-logical-upgrade.sh` verifies backup/restore and the
  integrity oracle of synthetic state.
- `verify-sample-service-supply-chain.sh` and `check-supply-chain-policy.py`
  verify digest-bound positive/negative verdicts.
- `rehearse-sample-service-delivery.sh` verifies canary, promotion, injected
  failure, and rollback.
- Related focused tests and the registered full profile pass, and Task
  evidence contains no secrets or raw runtime logs.

## Traceability

- **Architecture Description**: [AD-0028 Operational Readiness Closure](../02.architecture/descriptions/0028-operational-readiness-closure.md)
- **Decision**: [ADR-0028 Local-Isolated Readiness Evidence](../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
- **Implementation**: `scripts/operations/check-compose-core-readiness.sh`,
  `scripts/operations/rehearse-postgres-logical-upgrade.sh`,
  `scripts/security/verify-sample-service-supply-chain.sh`,
  `scripts/validation/check-supply-chain-policy.py`,
  `scripts/operations/rehearse-sample-service-delivery.sh`
- **Sample artifact**: `examples/sample-web-service/`
