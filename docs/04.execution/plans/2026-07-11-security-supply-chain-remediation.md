---
status: active
artifact_id: plan:2026-07-11-security-supply-chain-remediation
artifact_type: plan
parent_ids:
  - prd:025-operational-readiness-closure
  - ard:0028-operational-readiness-closure
  - adr:0028-local-isolated-readiness-evidence
  - spec:126-security-supply-chain-remediation
---

# Security Supply-Chain Remediation Implementation Plan

## Overview

This active plan turns Spec 126 into an executable local sequence for
`examples/sample-web-service` supply-chain evidence: digest-bound SBOM,
vulnerability verdict, provenance statement, local blob signing/verification,
and reviewed OpenSSF Scorecard advisory signals. It is prospective; actual tool
versions, image digests, command output, review findings, and commits belong in
the future sibling Task.

The implementation is local and advisory-first. It does not publish artifacts,
push images, create releases, use keyless OIDC signing, modify GitHub settings,
claim a SLSA level, or turn Scorecard into a deterministic CI blocker.

## Context and Inputs

Inputs:

- [PRD 025](../../01.requirements/025-operational-readiness-closure.md)
- [ARD 0028](../../02.architecture/requirements/0028-operational-readiness-closure.md)
- [ADR 0028](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
- [Spec 126](../../03.specs/126-security-supply-chain-remediation/spec.md)
- [examples/sample-web-service](../../../examples/sample-web-service/README.md)
- existing security audit:
  [security-framework-maturity.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md)

Official behavior anchors:

- Syft is the Anchore SBOM generator and supports standard SBOM formats,
  including CycloneDX.
- Grype needs network access for initial image/database downloads; after the
  vulnerability DB and image are present, scans can run offline until the DB is
  updated, and Grype does not send scan data to external services.
- Sigstore Cosign supports `sign-blob` / verification for files and blobs.
  Keyless blob signing uses an OIDC identity and ephemeral signing key; bundle
  retention is required for later verification. This plan uses local ephemeral
  test keys unless a later Task separately approves keyless/OIDC.
- SLSA provenance uses the in-toto attestation predicate type
  `https://slsa.dev/provenance/v1`; producing a local statement does not by
  itself claim a SLSA conformance level.
- OpenSSF Scorecard Action has workflow and permission restrictions and is
  advisory for this plan. Deterministic blocking decisions belong to local
  policy fixtures.

## Goals and Non-goals

Goals:

- Prove `SSC-001` with a versioned vulnerability policy, scan result summary,
  exception format, and deterministic pass/fail fixtures.
- Prove `SSC-002` with a CycloneDX JSON SBOM bound to the exact sample image
  digest.
- Prove `SSC-003` with a local provenance statement whose subject digest,
  source revision, builder class, and materials are verifiable.
- Prove `SSC-004` with local signing and verification success plus tampered and
  wrong-subject rejection.
- Prove `SSC-005` with read-only Scorecard observation and reviewed limitations,
  while local fixtures own CI-style decisions.

Non-goals:

- No registry push, remote attestation store, GitHub settings, Release, or
  deployment.
- No keyless/OIDC identity, transparency-log trust, or signed-release claim.
- No raw vulnerability report, private key, token, OIDC token, or secret value
  in tracked docs.
- No SLSA level or broad security maturity claim.

## Work Breakdown

| Unit | Purpose | Planned owned files | Requirements | RED/GREEN evidence | Commit boundary |
| --- | --- | --- | --- | --- | --- |
| `T-SSC-001` | Define tool registry, policy schema, evidence schema, and deterministic fixtures. | `scripts/validation/supply-chain-readiness.*`, `scripts/validation/fixtures/supply-chain/**`, `docs/90.references/data/security/**` if a stable policy reference is needed, Task evidence file. | `SSC-001`–`SSC-005` | RED: digestless artifact, unpinned tool, missing negative fixture, raw finding leakage. GREEN: dry-run resolves tool/image identities, artifact digest, policy, transient paths, redaction. | `feat(security): add local supply-chain verification` |
| `T-SSC-002` | Build/sample artifact identity and generate digest-bound SBOM/scan verdict. | Sample-service harness/tests; no publication. | `SSC-001`, `SSC-002` | RED: SBOM subject mismatches digest or vulnerability policy ignores threshold/exception expiry. GREEN: SBOM and scan verdict bind to same digest and fixture decisions are deterministic. | Same SSC commit unless split by review. |
| `T-SSC-003` | Produce and verify local provenance and signature bundles. | Provenance/signature fixture tests and wrappers. | `SSC-003`, `SSC-004` | RED: tampered/wrong-subject/wrong-identity accepted. GREEN: correct artifact verifies; negative fixtures reject. | Same SSC commit unless split by review. |
| `T-SSC-004` | Add read-only Scorecard observation adapter and local policy fixture gate. | Scorecard wrapper/tests and Task evidence. | `SSC-005` | RED: remote Scorecard result treated as deterministic CI gate. GREEN: read-only result is advisory; local fixture controls decision. | Same SSC commit unless split by review. |
| `T-SSC-005` | Independent security/spec reviews and SDLC closure. | Task evidence and lifecycle updates only after evidence. | `VAL-SSC-001`–`004` | Spec review C0/I0/M0 and quality/security review C0/I0/M0. | `docs(evidence): record supply-chain closure` if separate evidence-only commit is needed. |

## Sequence

1. Create the active Task with exact local tool images/tags/digests, artifact
   subject, transient paths, redaction, private-key lifetime, read-only remote
   observation boundary, and rollback.
2. Implement dry-run/preflight. It must fail when tool identity, artifact
   digest, policy, output path, or redaction boundary is missing.
3. Add deterministic fixtures for clean, threshold-failing, exception-expired,
   tampered SBOM/provenance, wrong-subject signature, and advisory Scorecard
   result cases.
4. Build or resolve the sample-service image digest locally. Do not publish it.
5. Generate CycloneDX JSON SBOM and vulnerability verdict; store only concise
   summaries and checksums in tracked evidence.
6. Produce local SLSA/in-toto-style provenance and local blob signature bundle;
   verify correct and negative cases.
7. Optionally run read-only Scorecard observation only if the Task approves
   network/remote read-only scope. Record it as advisory with timestamp and
   limitations.
8. Run independent specification review, then quality/security review. Fix and
   re-review findings before lifecycle closure.

## Verification Plan

| Gate | Command / method | Expected pass evidence |
| --- | --- | --- |
| Metadata and lifecycle | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref <safe-base>` | Changed Stage 04 docs remain valid. |
| Traceability | `bash scripts/validation/check-doc-traceability.sh` and `bash scripts/validation/check-doc-implementation-alignment.sh` | `SSC-001`–`SSC-005` map to implemented files and Task evidence. |
| Repository contract | `bash scripts/validation/check-repo-contracts.sh` | No new contract breakage. |
| Fixture/unit tests | Future focused test command owned by `T-SSC-001` | Positive/negative policy, SBOM, provenance, signature, and Scorecard fixtures pass. |
| Tool rehearsal | Future Task-approved containerized Syft/Grype/Cosign command envelope | SBOM, scan verdict, provenance, signature, and verifier evidence bind to one digest. |
| Scorecard observation | Future approved read-only command or explicit skip | Advisory result or skip reason; no deterministic CI decision from remote score. |
| Review | Independent spec and quality/security review | C0/I0/M0 or all findings resolved and re-reviewed. |

## Risks and Rollback

| Risk | Impact | Mitigation / rollback |
| --- | --- | --- |
| Digest/SBOM/provenance mismatch | Critical | Key all records by immutable digest and reject mismatches. |
| Raw vulnerability or key leakage | Critical | Store raw outputs only in ignored/transient paths; tracked docs get summaries/checksums. |
| Network freshness makes CI flaky | High | Deterministic fixtures own blocking decisions; live DB/Scorecard evidence is advisory/freshness-stamped. |
| Keyless/OIDC claim without trust evidence | Critical | Use local ephemeral test keys unless a later Task approves OIDC and identity verification. |
| Scorecard overclaim | High | Treat findings as reviewed advisory signals, not maturity or release gates. |

Rollback is by reverting the logical commit, deleting transient task-owned
artifacts, and disabling only newly added advisory/blocking consumers. No
published artifact or remote setting exists in this plan.

## Approval Gates

- Human approval exists for this active Plan conversion.
- The future Task must approve exact tool image tags/digests, artifact subject,
  private-key lifetime, transient paths, redaction, and optional read-only
  Scorecard observation before execution.
- Registry push, artifact publication, keyless/OIDC signing, GitHub settings,
  Releases, deployments, and credential changes remain unapproved.

## Completion Criteria

- [ ] Active Task maps `SSC-001`–`SSC-005` to exact files, commands, rollback,
      redaction, and reviews.
- [ ] Tool/image identities and policy fixtures are pinned and reproducible.
- [ ] SBOM and vulnerability verdict bind to the same sample image digest.
- [ ] Provenance and signature verification pass success and negative cases.
- [ ] Scorecard observation is either read-only advisory with limitations or
      explicitly skipped with rationale.
- [ ] Independent specification and quality/security reviews pass.
- [ ] Spec 126 lifecycle reflects only local supply-chain evidence; remote,
      publication, OIDC, and SLSA-level exclusions remain explicit.

## Related Documents

- **PRD**: [Operational readiness closure](../../01.requirements/025-operational-readiness-closure.md)
- **ARD**: [Operational readiness closure architecture](../../02.architecture/requirements/0028-operational-readiness-closure.md)
- **ADR**: [ADR-0028 local-isolated readiness evidence](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
- **Spec**: [Spec 126](../../03.specs/126-security-supply-chain-remediation/spec.md)
- **Deployment consumer**: [Spec 127](../../03.specs/127-deployment-release-engineering-remediation/spec.md)
- **Syft**: <https://github.com/anchore/syft>
- **Grype getting started / offline behavior**: <https://oss.anchore.com/docs/guides/vulnerability/getting-started/>
- **Cosign blob signing**: <https://docs.sigstore.dev/cosign/signing/signing_with_blobs/>
- **SLSA provenance**: <https://slsa.dev/spec/v1.2/provenance>
- **OpenSSF Scorecard Action**: <https://github.com/ossf/scorecard-action>
