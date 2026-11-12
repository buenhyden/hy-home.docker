---
title: "Operational Readiness Closure Requirements"
version: "1.2.1"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-12"
layer: "requirements"
artifact_id: "REQ-0025"
created: "2026-07-19"
---

# Operational Readiness Closure Requirements

## Overview

### Problem and Outcome

Static documents and Compose rendering alone cannot prove startup/readiness,
artifact trust, or promotion/rollback behavior. This
requirement reproduces the three behaviors in a locally isolated environment
using sample artifacts and synthetic state owned by the repository, and
records the actually verified scope without overstatement.

### Stakeholders

- The maintainer must distinguish implemented readiness behavior from
  unapproved remote operations.
- The operator needs a guarantee that the rehearsal does not change another
  Docker project or real data.
- The security reviewer must confirm that supply-chain verdicts are bound to
  the same image digest.
- The release reviewer must reproduce that a failed canary is not promoted
  and is rolled back to the previous digest.

The owner, @buenhyden, writes, reviews and accepts this package.

## Scope

### In Scope

- Scope is limited to local isolated Compose readiness, sample-service supply
  chain, and local promotion/rollback.

### Constraints and Exclusions

- Production/shared runtime, real data, registry publication, OIDC signing,
  and remote GitHub configuration and deployment are out of scope.
- Automatic cleanup is allowed only for precisely identified task-owned
  resources.

## Requirements

### Functional Requirements

- **REQ-0025-FR-0001**: The approved core service set must start under a
  unique Compose project and provide bounded readiness and teardown results.
- **REQ-0025-FR-0002**: The runtime rehearsal must use synthetic
  configuration and task-owned network/volume/project identity.
- **REQ-0025-FR-0004**: SBOM, vulnerability verdict, provenance, and
  signature verification for the repository sample web service must be bound to
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

### Quality Requirements

- **REQ-0025-NFR-0011 — Isolation**: Every resource must be identified by a
  task-owned identity, and cleanup must apply only to that resource; measure: every cleanup targets only task-owned identities.
- **REQ-0025-NFR-0012 — Security**: Secrets, private keys, tokens, raw auth
  logs, and production data must not be stored in tracked evidence; measure: tracked evidence contains no secret value.
- **REQ-0025-NFR-0013 — Determinism**: A blocking gate must reproduce the
  same pass/fail result without network access, using versioned inputs and
  fixtures; measure: repeated offline runs give identical verdicts.
- **REQ-0025-NFR-0014 — Fail closed**: Target ambiguity, digest or integrity
  mismatch, and cleanup failure must not be treated as success or skip; measure: each listed condition yields a failure exit.
- **REQ-0025-NFR-0015 — Traceability**: Traceability must be maintained
  between this Requirement, AD-0028, ADR-0028, the implementation scripts,
  the Operations procedure, and current Task results; measure: every link in the chain resolves.
- **REQ-0025-NFR-0016 — Honest scope**: Local rehearsal success must not be
  overstated as production readiness, full-profile coverage, live recovery,
  or remote release completion; measure: Task evidence names the verified scope only.

## Acceptance Criteria

### Acceptance Conditions

- The core readiness rehearsal verifies readiness, timeout, and cleanup
  boundaries.
- The supply-chain verification and policy check produce digest-bound
  positive and negative verdicts.
- The delivery rehearsal verifies canary, promotion, injected failure, and
  rollback.
- Related focused tests and the registered full profile pass, and Task
  evidence contains no secrets or raw runtime logs.

### Verification Method

Each condition is judged by running the focused tests and the registered full profile, and the evidence names only the scope actually verified. No current Spec Package cites REQ-0025; a Spec that implements it records the evidence in its Task. The evidence is the command, scope, result, cleanup and review, recorded in that Task. The owner named in the frontmatter, @buenhyden, judges each condition from that evidence. The same owner accepts the requirement once every condition is judged met.

## Traceability

### Source and Constraints

- **Retired**: REQ-0025-FR-0003 required a synthetic PostgreSQL 17 to 18
  logical backup, restore, upgrade, and integrity rehearsal, implemented by
  `rehearse-postgres-logical-upgrade.sh` and runbook RUN-0032. Both were
  deleted on 2026-11-10: every HOME PostgreSQL service already runs major 18
  and no later major image exists to rehearse against.

### Downstream Links

- **Architecture Description**: [AD-0028 Operational Readiness Closure](../02.architecture/descriptions/0028-operational-readiness-closure.md)
- **Implementation**: `scripts/operations/check-compose-core-readiness.sh`,
  `scripts/security/verify-sample-service-supply-chain.sh`,
  `scripts/validation/check-supply-chain-policy.py`,
  `scripts/operations/rehearse-sample-service-delivery.sh`
- **Sample artifact**: `examples/sample-web-service/`
- **Operations**: [Release management runbook](../05.operations/runbooks/10-platform-and-backup/0009-release-management.md)
- **Decision**: [ADR-0028 Local-Isolated Readiness Evidence](../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
