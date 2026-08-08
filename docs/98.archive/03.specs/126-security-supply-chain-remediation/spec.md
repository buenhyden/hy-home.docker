---
status: archived
artifact_id: spec:126-security-supply-chain-remediation
artifact_type: archive
parent_ids:
  - prd:025-operational-readiness-closure
  - ard:0028-operational-readiness-closure
  - adr:0028-local-isolated-readiness-evidence
  - spec:123-agentic-engineering-audit-remediation
archived_from: docs/03.specs/126-security-supply-chain-remediation/spec.md
archived_on: 2026-08-08
archive_reason: Terminal Stage 03 specification relocated into the content archive after its work completed; the record is retained as evidence, not active guidance.
archive_disposition: evidence-preserve
archived_commit: b342a5aea5ffb60b7a0dcde0b567339008e8e0fc
archived_blob: df8959c6ac2d9298417d334286abb99db971c492
preservation_class: git-history
---

# Security Supply-Chain Remediation Technical Specification (Spec)

## Overview

This completed specification records the local-isolated contract used for
digest-bound container scanning, SBOM, provenance, local signing/verification,
and reviewed OpenSSF Scorecard signals for `examples/sample-web-service`. It
owns six canonical audit gaps. PRD 025, ARD 0028, and ADR 0028 approve the
design; the linked Plan and Task own the exact tool identities, policies,
commands, generated-artifact boundaries, and observed local evidence. Broader
or remote execution requires a new approved Task.

## Archive Metadata

This specification's work reached a terminal state (`completed` or `superseded`); the record is preserved under the `evidence-preserve` disposition rather than kept as an active Stage 03 guidance surface. Provenance resolves through Git history (`preservation_class: git-history`): `archived_commit` identifies the last commit that touched this document at its original path, and `archived_blob` identifies the exact content preserved at that commit.

## Strategic Boundaries & Non-goals

- Own supply-chain artifact identity and evidence from source/dependency/image
  inputs through verifier acceptance.
- Own vulnerability scope, thresholds, exceptions, remediation ownership, and
  reviewed advisory Scorecard signals.
- Supply verification outputs to Spec 127; do not own deployment promotion.
- Do not claim SLSA level, broad SCA coverage, signed releases, or artifact
  trust from version declarations, Dependabot, one npm audit, or workflow lint.
- Do not claim remote registry trust, keyless identity, transparency-log
  integration, publication, signed release, or a SLSA conformance level from
  the bounded local implementation.

## Boundaries and Inputs

- **PRD**: [PRD 025](../../../01.requirements/025-operational-readiness-closure.md)
  defines the sample artifact, local trust outcome, and remote non-goals.
- **ARD**: [ARD 0028](../../../02.architecture/requirements/0028-operational-readiness-closure.md)
  defines the digest-bound producer/consumer and transient-evidence boundaries.
- **ADR**: [ADR 0028](../../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
  selects pinned Syft, Grype, and Cosign containers plus advisory read-only
  Scorecard observation and deterministic local policy fixtures.
- **Audit lineage**: [Spec 123](../123-agentic-engineering-audit-remediation/spec.md)
  remains the canonical audit lineage.

Architecture-changing build, identity, registry, artifact, workflow, or
verification changes remain blocked until the approved Plan and active Task
identify the exact protected surfaces and rollback.

## Canonical Gap Ownership

| Audit gap | Disposition | Requirement owner | Reason |
| --- | --- | --- | --- |
| `QAF-10` | Owned | `SSC-001` | Expand the scoped npm vulnerability gate into an explicitly governed multi-ecosystem/image contract. |
| `SEC-01`–`SEC-05` | Not routed: already implemented controls | Existing security/governance/workflow owners | Disclosure, approvals, pinned permissions, gitleaks, and Dependabot remain prerequisite controls. |
| `SEC-06` | Not routed: already implemented but narrow | Existing Storybook security/QA owner | The one high-severity npm gate is current evidence consumed by `SSC-001`, not a second requirement. |
| `SEC-07` | Owned | `SSC-001` | Broader dependency and container-image scanning. |
| `SEC-08` | Owned | `SSC-002` | Artifact-associated SBOM generation and retention. |
| `SEC-09` | Owned | `SSC-003` | Build provenance/attestation production. |
| `SEC-10` | Owned | `SSC-004` | Artifact signing and consumer verification; Spec 127 consumes the result. |
| `SEC-11` | Owned | `SSC-005` | Reviewed advisory Scorecard execution. |
| `SEC-12` | Not routed: governance/change-specific | Stage 00 security governance plus affected future spec/task | Threat-model attachment is broader than supply-chain runtime ownership. |
| `SEC-13` | Not routed: operations drill | Security and Operations/SRE owners | Vulnerability/incident tabletop evidence belongs to a future operations task. |
| `SEC-14` | Not routed: remote revalidation | GitHub governance owner | Requires separately approved timestamped remote read-only verification. |

Owned gap count: **6 audit IDs** mapped to five requirements because `QAF-10`
and `SEC-07` are two canonical audit views of the same broader scanning
contract. Both IDs are owned only here.

## Contracts

### Supply-Chain Evidence Contract

| Requirement | Target behavior | Required evidence |
| --- | --- | --- |
| `SSC-001` | Scan approved dependency ecosystems and container images with owned severity, freshness, exception, remediation, and release-impact rules. | Scope/tool/version, target/digest, policy version, redacted finding counts/classes, threshold result, exception owner/expiry, remediation disposition, and negative fixture. |
| `SSC-002` | Generate a deterministic SBOM for each approved artifact-producing flow and associate it with the exact artifact identity/digest. | Format/version, generator/version, subject digest, materials/dependencies, retention/publication location class, consumer check, and reproducibility result. |
| `SSC-003` | Produce provenance/attestation that binds builder identity, source/materials, build parameters, and subject digest. | Builder/workflow identity, source revision, materials, subject digest, attestation format, retention, and verifier acceptance/rejection. |
| `SSC-004` | Sign approved artifacts and verify signature/attestation identity and subject digest before consumption; fail closed on mismatch. | Test artifact/digest, signer identity class, signature/attestation reference, trusted policy, success and tampered/wrong-identity failures, exception/rollback result. |
| `SSC-005` | Run OpenSSF Scorecard only as a scoped advisory security-health signal with reviewed limitations and findings. | Pinned tool/action, repository identity, permissions, result date, reviewed findings/false positives, disposition owners, and explicit non-maturity disclaimer. |

### Configuration Contract

- Future active work names exact ecosystems, images, artifacts, build flows,
  tool/action versions, policies, thresholds, identities, permissions,
  retention, publication, consumers, and enforcement mode.
- Advisory rollout precedes blocking rollout; false-positive/exception review
  and failure fixtures are required before any release gate.
- Version declaration provenance remains distinct from build provenance.

### Data / Interface Contract

Every artifact-facing record uses immutable subject digests and provenance/SBOM
association. Tracked evidence contains concise results and identifiers only,
never raw vulnerability reports, token-bearing URLs, credentials, private keys,
OIDC tokens, secret values, or unrestricted artifact contents.

The local delivery handoff is versioned and fail-closed:

- each role has one schema-v2 verification verdict binding source revision and
  build context to `oci_manifest_digest`, `image_config_digest`,
  `oci_archive_sha256`, `docker_archive_sha256`, `local_image_ref`,
  `runtime_image_id`, and `runtime_identity_kind`, plus the policy result,
  null exception, timestamp, and redaction status;
- one schema-v3 `verification-verdict.pair.json` with generation
  `hyhome-verification-verdict-pair-v3` binds the exact verdict bytes and the
  full identity tuple for both roles; and
- legacy, partial, stale, mixed-generation, equal-subject, or substituted
  handoffs are rejected before a consumer reaches runtime.

### Governance Contract

- A future Stage 04 task must name exact local/CI/runtime/remote surfaces,
  approvals, validation, rollback, secret/identity boundary, and redaction.
- Signing identity, OIDC trust, registry permissions, publication, and remote
  workflow changes need separate exact approvals.
- Tool output is evidence, not an automatic maturity or safety claim.

## Current Evidence

This Spec defines the supply-chain contract; it does not own observed execution
evidence or lifecycle conclusions. Observed evidence and current status are
owned by the exact [domain Task](../../../04.execution/tasks/2026-07-19-security-supply-chain-remediation.md)
and [Program Task](../../../04.execution/tasks/2026-07-19-operational-readiness-closure-program.md).

## Core Design

- **Component Boundary**: Local sample-service image build plus digest-bound
  SBOM, scan policy verdict, provenance statement, blob signature, verification,
  portable Docker-load handoff, and positive/negative fixtures.
- **Key Dependencies and Consumers**: The tracked
  `examples/sample-web-service` source and local fixture build produce the test
  artifact identity. Spec 127 consumes the verification verdict; Specs 124/125
  may consume image verdicts without owning this requirement.
- **Tech Stack**: Digest-pinned Syft, Grype, and Cosign containers; CycloneDX
  JSON SBOM; SLSA/in-toto-style provenance statement; local ephemeral signing
  key; deterministic OCI-to-Docker archive conversion; read-only OpenSSF
  Scorecard; versioned local policy fixtures.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Key all records by immutable subject digest,
  source revision, policy version, producer/verifier identity class, and
  disposition. Store artifact evidence in an approved protected location and
  retain only concise references in tracked docs.
- **Migration / Transition Plan**: Inventory -> approved architecture/ADRs ->
  local fixture/advisory mode -> reviewed CI advisory -> exception/false-positive
  review -> separately approved blocking/promotion integration.

## Interfaces and Data

### Core Interfaces

| Interface | Producer | Consumer | Contract |
| --- | --- | --- | --- |
| Artifact identity | Spec 126 local sample-service fixture build | SBOM/provenance/signing | OCI manifest and image-config digests plus source/build identity and OCI archive hash. |
| Portable image handoff | Spec 126 verifier | Spec 127 local runtime gate | Deterministic Docker-load archive hash, deterministic local reference, observed runtime image ID/kind, and the originating OCI identity. |
| Verification verdict pair | Spec 126 verifier | Spec 127 promotion gate | Verdict schema v2 plus pair schema/generation v3, exact verdict-byte hashes, full per-role identity tuples, policy result, and no-exception/redaction status. |
| Image/artifact verdict | Future scanner/verifier | Specs 124/125 | Exact digest, policy, freshness, and redacted result. |
| Exception record | Human security owner | Build/release consumer | Scope, reason, owner, approval, expiry, compensating control, disposition. |

## API Contract (If Applicable)

Not applicable. Any future vendor/registry API contract must be specified after
tool selection and remote approval.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Future implementation by `security-auditor` plus
  `ci-cd-engineer`; independent review by artifact owners and `qa-engineer`.
- **Inputs**: Approved predecessors/task, exact artifact/tool/policy/identity
  scope, test fixtures, redaction, exception, rollback.
- **Outputs**: Deterministic redacted evidence and verifier verdicts.
- **Success Definition**: Every scoped artifact has policy-bound evidence and
  failure cases; no unapproved identity, secret, registry, workflow, or remote
  change occurs.

## Tools & Tool Contract (If Applicable)

- **Tool List**: Syft for SBOM, Grype for SBOM/image vulnerability evaluation,
  Cosign `sign-blob`/`verify-blob` for local subject binding, a bounded standard-
  library OCI-to-Docker archive converter for portable local loading, and
  Scorecard for read-only advisory observation. Exact releases and image
  digests belong in the Plan after current official-release verification.
- **Permission Boundary**: Local build and task-owned artifact execution only;
  Scorecard may query the exact repository read-only. Registry, workflow,
  identity, publication, and remote mutation remain prohibited.
- **Failure Handling**: Fail closed for identity/digest/policy mismatch after a
  blocking mode is separately approved; advisory mode records disposition.

## Prompt / Policy Contract (If Applicable)

Future instructions must name exact artifact/digest, policy, tool/action pin,
identity/secret scope, permissions, output/redaction, exception, and rollback.
No agent may infer command approval from this specification or audit lineage.

## Memory & Context Strategy (If Applicable)

Persist identifiers, digests, policy versions, counts/classes, and decisions.
Do not store raw findings, artifact bodies, tokens, credentials, private keys,
or secret-bearing logs in tracked evidence or memory.

## Guardrails (If Applicable)

- **Input Guardrails**: Validate immutable artifact identity, tool pin, policy,
  permissions, identity/secret scope, and target repository/registry.
- **Output Guardrails**: Redact raw findings and token-bearing locations; keep
  digest-bound concise summaries.
- **Blocked Conditions**: Missing artifact boundary, predecessor/ADR, identity,
  verifier, failure fixture, exception policy, retention, or rollback.
- **Escalation Rule**: Stop and require new human/security/secret/remote approval
  whenever trust root, identity, registry, permissions, or enforcement changes.

## Approval Gates

| Gate | Remaining approval required before execution | Evidence required |
| --- | --- | --- |
| Architecture | Approved PRD/ARD/ADRs for artifacts, trust, identity, retention, verification, and exceptions | Canonical IDs/paths and approval state. |
| Human | Security/artifact owners approve scope, thresholds, blocking mode, exceptions, retention, and residual risk | Approval reference and named remediation owner. |
| Runtime | Any scanner/build/sign/verify execution names exact targets, commands, resources, failure handling, and cleanup | Future Stage 04 task and fixture evidence. |
| Secret | Signing/OIDC/registry secret or identity use names exact IDs/claims/paths and permitted metadata; no values | Identity/secret threat boundary, redaction, rotation/revocation, and reviewer. |
| Remote | GitHub, registry, attestation store, Scorecard, or publication/query/mutation is separately approved | Repository/registry identity, permissions, command/action class, before/after evidence, rollback. |

## Edge Cases & Error Handling

- Scanner ecosystems overlap or disagree: preserve tool/policy-specific results
  and require human disposition; do not average away a failure.
- SBOM subject digest differs from artifact: reject association.
- OCI descriptor, layer digest/DiffID, archive bounds, local reference, loaded
  image ID, or role label differs from the pair: reject the handoff.
- Provenance is produced but not verified: mark unverified, never trusted.
- Signature verifies cryptographically but identity/policy is wrong: reject.
- Scorecard produces a score: treat checks as advisory findings, not maturity.

## Failure Modes and Guardrails

- **Failure Mode**: Target/digest/identity/policy mismatch, tool failure,
  unhandled finding, expired exception, or evidence publication failure.
- **Fallback**: Stop promotion/consumption only where blocking behavior was
  explicitly approved; otherwise retain advisory evidence and escalate.
- **Human Escalation**: Security/artifact/release owners decide remediation,
  time-bounded exception, rollback, or abandonment.

## Migration, Rollback, and Recovery

- Start with deterministic local fixtures and advisory outputs; add remote/CI
  surfaces only after reviewed evidence.
- Preserve the current scoped npm gate until a replacement demonstrates equal
  or stronger coverage and approved exception semantics.
- Roll back workflow/tool changes by reviewed commit while retaining evidence;
  revoke/rotate identity material through an approved secret procedure.
- A failed verifier blocks only the separately approved consumer boundary; it
  does not authorize deleting artifacts or state.

## Verification

Documentation-phase checks:

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 4937ae999825391963149cb285c686808dbb394b
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

No tool command is authorized until the Plan and active Task pin exact images,
targets, policies, exception schema, transient paths, redaction, cleanup, and
the read-only repository identity. Registry and mutation commands remain out of
scope.

## Success Criteria & Verification Plan

- **VAL-SSC-001**: Six owned audit IDs map exactly once to `SSC-001`–`SSC-005`.
- **VAL-SSC-002**: Artifact evidence is digest-bound and producer/consumer
  verification includes success and failure cases.
- **VAL-SSC-003**: Advisory and blocking modes, exceptions, identities,
  retention, and rollback remain explicit and independently approved.
- **VAL-SSC-004**: Architecture, human, runtime, secret, and remote gates are
  resolved before implementation.

## Archive Ledger

| Original Path | Archived Path |
| -------------- | -------------- |
| `docs/03.specs/126-security-supply-chain-remediation/spec.md` | `docs/98.archive/03.specs/126-security-supply-chain-remediation/spec.md` |

The repository-wide archive mapping is recorded in
[../../README.md](../../README.md).

## Related Documents

- **README**: [README.md](./README.md)
- **PRD**: [Operational readiness closure](../../../01.requirements/025-operational-readiness-closure.md)
- **ARD**: [Operational readiness closure architecture](../../../02.architecture/requirements/0028-operational-readiness-closure.md)
- **ADR**: [ADR-0028 local-isolated readiness evidence](../../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
- **Plan**: [Security supply-chain draft plan](../../../04.execution/plans/2026-07-11-security-supply-chain-remediation.md)
- **Task**: [Supply-chain Task](../../../04.execution/tasks/2026-07-19-security-supply-chain-remediation.md)
- **Umbrella lineage**: [Spec 123](../123-agentic-engineering-audit-remediation/spec.md)
- **Security audit**: [Security framework maturity](../../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md)
- **Quality audit**: [SDLC quality and formatting](../../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-quality-formatting-implementation.md)
- **Security research**: [Security governance](../../../90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md)
- **Deployment consumer**: [Spec 127](../127-deployment-release-engineering-remediation/spec.md)
- **Runtime consumers**: [Spec 124](../124-compose-runtime-readiness-remediation/spec.md), [Spec 125](../125-infrastructure-operations-readiness-remediation/spec.md)
