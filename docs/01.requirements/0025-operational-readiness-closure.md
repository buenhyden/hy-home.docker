---
title: "Operational Readiness Closure Requirements"
version: "1.3.0"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-13"
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

- **REQ-0025-FR-0001**: The core readiness rehearsal starts the approved core
  set under a unique Compose project and verifies readiness, timeout and
  cleanup boundaries.
- **REQ-0025-FR-0002**: The rehearsal's inputs are synthetic, and its Compose
  project, networks and volumes carry task-owned identities.
- **REQ-0025-FR-0004**: SBOM, vulnerability, provenance and signature
  verification for the sample web service produce digest-bound positive
  verdicts and reject tampering and identity mismatch.
- **REQ-0025-FR-0005**: The supply-chain checks run with the tool version and
  container image the repository declares, with no host-global install of those
  tools.
- **REQ-0025-FR-0006**: Network-dependent security observations are reported as
  advisory, and the CI verdict comes from local policy and fixtures only.
- **REQ-0025-FR-0007**: The delivery rehearsal deploys only a verified digest
  as canary and promotes it only after the health gate passes.
- **REQ-0025-FR-0008**: An injected failure after canary or promotion rolls
  back to the previous verified digest, and post-rollback health is confirmed.
- **REQ-0025-FR-0009**: The current Task records command, scope, result,
  cleanup and review for each run, and its lifecycle state matches those
  results.
- **REQ-0025-FR-0010**: Task evidence contains no raw runtime logs; durable
  evidence holds only a secret-scrubbed summary and the immutable subject
  identity.
- **REQ-0025-NFR-0011**: Every cleanup targets only task-owned identities.
- **REQ-0025-NFR-0012**: Tracked evidence contains no secret value.
- **REQ-0025-NFR-0013**: Repeated offline runs of a blocking gate give
  identical verdicts.
- **REQ-0025-NFR-0014**: Target ambiguity, digest or integrity mismatch, and
  cleanup failure each yield a failure exit.
- **REQ-0025-NFR-0015**: Every link from this Requirement through AD-0028,
  ADR-0028, the implementation scripts, the Operations procedure and the
  current Task results resolves.
- **REQ-0025-NFR-0016**: Task evidence names only the scope actually verified,
  and claims no production readiness, full-profile coverage, live recovery or
  remote release completion beyond it.

### Verification Method

Each condition is judged by running the focused tests and the registered full profile, and the evidence names only the scope actually verified. No current Spec Package cites REQ-0025; a Spec that implements it records the evidence in its Task. The evidence is the command, scope, result, cleanup and review, recorded in that Task. The owner named in the frontmatter, @buenhyden, judges each condition from that evidence. The same owner accepts the requirement once every condition is judged met.

## Traceability

### Source and Constraints

This package records the owner's requirements for operational readiness closure; no upstream
document governs it.

### Downstream Links

- **Architecture Description**: [AD-0028 Operational Readiness Closure](../02.architecture/descriptions/0028-operational-readiness-closure.md)
- **Implementation**: `scripts/operations/check-compose-core-readiness.sh`,
  `scripts/security/verify-sample-service-supply-chain.sh`,
  `scripts/validation/check-supply-chain-policy.py`,
  `scripts/operations/rehearse-sample-service-delivery.sh`
- **Sample artifact**: `examples/sample-web-service/`
- **Operations**: [Release management runbook](../05.operations/runbooks/10-platform-and-backup/0009-release-management.md)
- **Decision**: [ADR-0028 Local-Isolated Readiness Evidence](../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
- **Retired**: REQ-0025-FR-0003 required a synthetic PostgreSQL 17 to 18
  logical backup, restore, upgrade, and integrity rehearsal, implemented by
  `rehearse-postgres-logical-upgrade.sh` and runbook RUN-0032. Both were
  deleted on 2026-11-10: every HOME PostgreSQL service already runs major 18
  and no later major image exists to rehearse against.
