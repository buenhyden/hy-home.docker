---
status: completed
artifact_id: plan:2026-07-11-security-supply-chain-remediation
artifact_type: plan
parent_ids:
  - prd:025-operational-readiness-closure
  - ard:0028-operational-readiness-closure
  - adr:0028-local-isolated-readiness-evidence
  - spec:126-security-supply-chain-remediation
---

# Security Supply-Chain Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` (recommended) or
> `superpowers:executing-plans` to implement this plan task-by-task. Sequence
> steps become Task evidence only after execution.

**Goal:** Produce digest-bound, locally verifiable supply-chain evidence for
two task-local `examples/sample-web-service` variants and a deterministic
fixture-only CI policy gate.

**Architecture:** A versioned policy registry pins tool container manifests and
artifact rules. One wrapper builds/exports the sample image, derives a declared
portable subject tuple, deterministically converts the validated OCI artifact
into a Docker-load archive, invokes pinned Syft/Grype/Cosign images, emits
SLSA/in-toto provenance, and writes a concise verdict pair consumed by Spec
127. A Python checker owns network-independent CI decisions; live Scorecard
remains read-only advisory.

**Tech Stack:** Docker/OCI archive; CycloneDX JSON; SLSA provenance v1;
Cosign blob signing; Syft v1.48.0; Grype v0.116.0; Cosign v3.0.6; OpenSSF
Scorecard v5.5.0; Bash; Python `unittest`; GitHub Actions fixture-only gate.

## Global Constraints

- Invoke tools only through the pinned multi-platform image-manifest digests
  listed in Context and Inputs; do not install global binaries.
- Bind the local subject to the OCI manifest digest, image config digest, OCI
  archive SHA-256, deterministic Docker-load archive SHA-256, deterministic
  local reference, and observed runtime image ID/kind. Do not invent a registry
  `RepoDigest` for an unpushed image.
- Build `baseline` and `candidate` variants from the same tracked sample-service
  source and distinguish them only with the OCI label
  `org.hyhome.delivery.rehearsal.role`. Produce and verify a separate verdict
for each digest so Spec 127 can prove previous-runtime-ID rollback.
- Keep private keys under `/tmp` for one wrapper lifetime and delete them on
  exit; never retain them under `_workspace` or tracked paths.
- Local workflow-file changes may run the fixture-only policy checker, but no
  remote GitHub mutation, live workflow dispatch, publication, or registry push
  is authorized.

## Overview

This prospective plan turns Spec 126 into an executable local sequence for
`examples/sample-web-service` supply-chain evidence: digest-bound SBOM,
vulnerability verdict, provenance statement, local blob signing/verification,
and reviewed OpenSSF Scorecard advisory signals. Observed execution and
lifecycle evidence belongs only in the
[domain Task](../tasks/2026-07-19-security-supply-chain-remediation.md).

The implementation is local and advisory-first. It does not publish artifacts,
push images, create releases, use keyless OIDC signing, modify GitHub settings,
claim a SLSA level, or turn Scorecard into a deterministic CI blocker.

## Context and Inputs

Inputs:

- [PRD 025](../../01.requirements/prd-025-operational-readiness-closure.md)
- [Architecture Description 0028](../../02.architecture/descriptions/ad-0028-operational-readiness-closure.md)
- [ADR 0028](../../02.architecture/decisions/adr-0028-local-isolated-readiness-evidence.md)
- [Spec 126](../../98.archive/03.specs/126-security-supply-chain-remediation/spec.md)
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

Verified tool-image pins as of 2026-07-19 KST:

| Tool | Image pin |
| --- | --- |
| Syft | `anchore/syft:v1.48.0@sha256:b4f1df79f97b817682d8b5ff941eb6bfe74f6172553a5e312c75bbc2eabc405c` |
| Grype | `anchore/grype:v0.116.0@sha256:fd4ab4d1042b522c896e73bdf09ab8bf384fa417df99d6dd0d6e1008c7e7c821` |
| Cosign | `gcr.io/projectsigstore/cosign:v3.0.6@sha256:de9c65609e6bde17e6b48de485ee788407c9502fa08b8f4459f595b21f56cd00` |
| Scorecard | `ghcr.io/ossf/scorecard:v5.5.0@sha256:3f24714e9366917adb7a05635382c97dfecb14b21eaef3dfa2ea48c8e23e0795` |

The sample build materials are also pinned in the Dockerfile:

| Material | Image pin |
| --- | --- |
| Build stage | `alpine:3.21@sha256:48b0309ca019d89d40f670aa1bc06e426dc0931948452e8491e3d65087abc07d` |
| Runtime stage | `nginxinc/nginx-unprivileged:1.31.3-alpine3.24-slim@sha256:90d82b3358df5758b3c57d20f2565082ce6f744906e7dc09afd0096c1b8eb2b5` |

## Goals and Non-goals

Goals:

- Prove `SSC-001` with a versioned vulnerability policy, scan result summary,
  exception format, and deterministic pass/fail fixtures.
- Prove `SSC-002` with a CycloneDX JSON SBOM bound to the exact sample image
  identity and a portable, deterministic local image handoff.
- Prove `SSC-003` with a local provenance statement whose subject digest,
  source revision, builder class, and materials are verifiable.
- Prove `SSC-004` with local signing and verification success plus tampered and
  wrong-subject rejection.
- Prove `SSC-005` with read-only Scorecard observation and reviewed limitations,
  while local fixtures own CI-style decisions.

Non-goals:

- No registry push, remote attestation store, remote GitHub mutation/dispatch,
  Release, or deployment. A tracked fixture-only CI gate is in scope and must
  remain network-independent.
- No keyless/OIDC identity, transparency-log trust, or signed-release claim.
- No raw vulnerability report, private key, token, OIDC token, or secret value
  in tracked docs.
- No SLSA level or broad security maturity claim.

## Work Breakdown

| Unit | Purpose | Planned owned files | Requirements | RED/GREEN evidence | Commit boundary |
| --- | --- | --- | --- | --- | --- |
| `T-SSC-001` | Define tool registry, policy, exceptions, evidence schema, checker, and fixtures. | `infra/supply-chain.tool-images.json`; `infra/supply-chain.sample-service-policy.json`; `infra/supply-chain.vulnerability-exceptions.json`; `scripts/validation/check-supply-chain-policy.py`; the exact fixture manifest below; `tests/validation/test_supply_chain_policy.py`; `docs/04.execution/tasks/2026-07-19-security-supply-chain-remediation.md`. | `SSC-001`–`SSC-005` | RED: digestless artifact, unpinned tool, expired/unowned exception, subject mismatch, raw finding leakage, or Scorecard blocking by score. GREEN: the fixture-only checker accepts/rejects each case deterministically. | `feat(security): add local supply-chain verification` |
| `T-SSC-002` | Build/export baseline and candidate variants, derive portable OCI/Docker identities, and generate digest-bound SBOM/scan verdicts. | `scripts/security/verify-sample-service-supply-chain.sh`; `scripts/validation/check-supply-chain-policy.py`; `examples/sample-web-service/Dockerfile`; `examples/sample-web-service/service.md`; ignored task runtime directory. | `SSC-001`, `SSC-002` | RED: an OCI descriptor/layer/DiffID is invalid, the Docker-load archive is nondeterministic, either SBOM subject differs from its declared tuple, the role identities are equal, or scan policy is bypassed. GREEN: each CycloneDX SBOM and Grype verdict binds to its distinct full tuple and loaded local image. | Same SSC commit. |
| `T-SSC-003` | Produce and verify provenance and local signature bundle. | The wrapper, policy checker, provenance/signature fixtures, and tests. | `SSC-003`, `SSC-004` | RED: tampered/wrong-subject material is accepted. GREEN: correct OCI archive verifies and negative fixtures reject. | Same SSC commit. |
| `T-SSC-004` | Wire fixture-only CI/repo gates, generated summary freshness, and optional Scorecard advisory. | `.github/workflows/ci-quality.yml`; `scripts/validation/run-local-qa-gates.sh`; `scripts/validation/check-repo-contracts.sh`; `scripts/security/generate-supply-chain-sample-service-summary.sh`; `docs/90.references/data/security/supply-chain-sample-service.md`. | `SSC-005` | RED: network/live score controls CI or generated summary is stale. GREEN: fixture-only checks block deterministically; summary freshness passes; live Scorecard is advisory or explicitly skipped. | Same SSC commit. |
| `T-SSC-005` | Complete independent specification and security/quality reviews. | Domain Task and lifecycle/index updates only when supported. | `VAL-SSC-001`–`004` | All findings are remediated and independently re-reviewed before closure. | Evidence-only closure unit after approval. |

Exact deterministic fixture manifest:

- `tests/fixtures/supply-chain/sample-service-sbom.valid.cdx.json`
- `tests/fixtures/supply-chain/sample-service-sbom.subject-mismatch.cdx.json`
- `tests/fixtures/supply-chain/grype.clean.json`
- `tests/fixtures/supply-chain/grype.high-without-exception.json`
- `tests/fixtures/supply-chain/grype.high-with-valid-exception.json`
- `tests/fixtures/supply-chain/grype.expired-exception.json`
- `tests/fixtures/supply-chain/grype.valid-exception-then-critical.json`
- `tests/fixtures/supply-chain/provenance.valid.intoto.json`
- `tests/fixtures/supply-chain/provenance.subject-mismatch.intoto.json`
- `tests/fixtures/supply-chain/cosign.verify.valid.json`
- `tests/fixtures/supply-chain/cosign.verify.tampered.json`
- `tests/fixtures/supply-chain/cosign.verify.wrong-subject.json`
- `tests/fixtures/supply-chain/scorecard.advisory.json`

### Implementation contract

The wrapper accepts only `--fixture-only`, `--preflight`, `--advisory`, and
`--scorecard-advisory`. Exit classes are `0=pass/accepted`, `2=usage`,
`10=policy/preflight`, `20=build/export`, `30=SBOM`, `40=vulnerability verdict`,
`50=provenance`, `60=signature verification`, and `70=Scorecard observation`.

Required wrapper symbols and order:

```bash
load_tool_registry
validate_policy_and_exceptions
prepare_transient_directory
build_role_image baseline
build_role_image candidate
export_oci_archive baseline
export_oci_archive candidate
derive_subject_tuple baseline
derive_subject_tuple candidate
generate_cyclonedx_and_grype_verdict baseline
generate_cyclonedx_and_grype_verdict candidate
load_role_image_object baseline
load_role_image_object candidate
generate_slsa_provenance baseline
generate_slsa_provenance candidate
sign_and_verify_archive baseline
sign_and_verify_archive candidate
write_verification_verdict baseline
write_verification_verdict candidate
delete_ephemeral_private_key
```

Both builds consume the same deterministic `.dockerignore`-aware source-tree
tar snapshot and the Dockerfile material pins above. The wrapper records and
revalidates snapshot identity metadata before and immediately after build.
The wrapper passes one of the two exact build labels
`org.hyhome.delivery.rehearsal.role=baseline` or
`org.hyhome.delivery.rehearsal.role=candidate`, rejects equal image/config or
archive digests. For every pinned material/tool image, the wrapper independently
requires the configured repository manifest digest in `.RepoDigests` and the
configured image configuration digest in `.Id`.

The checker validates one bounded, uncompressed OCI layout with secure
USTAR/PAX handling, exact descriptor sizes and SHA-256 values, supported gzip
layers, and config `rootfs.diff_ids`. It emits one deterministic uncompressed
Docker-load archive from the same config and layer blobs with fixed metadata
and one role/config-derived `local_image_ref`; it neither rebuilds nor pulls the
subject. The wrapper loads that archive, verifies the role label, and records
the observed `.Id` as `runtime_image_id` with `runtime_identity_kind` equal to
`config-digest` or `docker-target-digest`.

`infra/supply-chain.tool-images.json` uses schema v2 and contains
`schema_version`, `policy_id`,
`effective_date`, `owner_role`, and four `tools` rows. Every row contains
`name`, `image`, `digest`, `repo_digest`, `config_id`, `expected_version`,
`command_contract`, and `network_mode`; manifest and configuration identities
remain independently verifiable.

`infra/supply-chain.sample-service-policy.json` contains:

```json
{
  "schema_version": 1,
  "policy_id": "sample-service-local-v1",
  "subject": {
    "service": "examples/sample-web-service",
    "roles": ["baseline", "candidate"]
  },
  "sbom": {"format": "cyclonedx-json"},
  "vulnerability": {
    "blocking_severities": ["critical"],
    "review_severities": ["high"],
    "exception_registry": "infra/supply-chain.vulnerability-exceptions.json"
  },
  "provenance": {"predicate_type": "https://slsa.dev/provenance/v1"},
  "signature": {"mode": "cosign-sign-blob", "key_lifetime": "process"},
  "scorecard": {"mode": "read-only-advisory"},
  "ci_enforcement": "fixture-policy-only"
}
```

Each exception row contains `id`, `subject_digest`, `package`,
`vulnerability_id`, `severity`, `owner_role`, `reason`, `expires_on`,
`compensating_control`, and `approval_reference`. Empty, expired,
wrong-subject, or unapproved rows fail closed.

Each verification verdict has exactly this interface:

```json
{
  "schema_version": 2,
  "producer_spec": "spec:126-security-supply-chain-remediation",
  "role": "candidate",
  "source_revision": "0123456789abcdef0123456789abcdef01234567",
  "build_context_sha256": "sha256:9999999999999999999999999999999999999999999999999999999999999999",
  "oci_manifest_digest": "sha256:8888888888888888888888888888888888888888888888888888888888888888",
  "image_config_digest": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "oci_archive_sha256": "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "docker_archive_sha256": "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
  "local_image_ref": "hyhome.local/sample-web-service:candidate-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "runtime_image_id": "sha256:dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
  "runtime_identity_kind": "docker-target-digest",
  "policy_id": "sample-service-local-v1",
  "verdict": "accepted",
  "exception_id": null,
  "verified_at": "2026-07-19T00:00:00Z",
  "redaction_status": "passed"
}
```

The two accepted verdicts are committed only with
`verification-verdict.pair.json`, which uses schema v3 and generation
`hyhome-verification-verdict-pair-v3`. It binds their exact byte hashes to the
same 40-hex `source_revision` and `build_context_sha256` and repeats the seven-
field portable identity tuple for each role; partial, legacy, substituted, or
mixed generations are never published.

The Python checker exports `load_json`, `validate_tool_registry`,
`validate_policy`, `validate_exceptions`, `evaluate_grype_fixture`,
`validate_sbom_subject`, `validate_provenance_subject`,
`validate_signature_fixture`, `validate_scorecard_advisory`, and
`inspect_oci_archive_config_digest`, plus the bounded OCI-to-Docker conversion
and atomic pair-publication interfaces. Tests use one
method per fixture plus `test_tool_manifest_pins_are_exact`,
`test_roles_have_distinct_subjects`, and
`test_live_score_cannot_be_a_blocking_decision`.

## Sequence

- [ ] Create the active Task with the four exact image pins above, artifact
      subject, transient paths, redaction, private-key lifetime, read-only
      observation boundary, and rollback.
- [ ] Write failing tests in `tests/validation/test_supply_chain_policy.py` for
      missing pins, threshold failure, exception expiry/ownership/digest, SBOM
      and provenance subject mismatch, signature tamper/wrong subject, and
      Scorecard advisory-only semantics.
- [ ] Run `python3 -m unittest tests.validation.test_supply_chain_policy -v` and
      confirm failure before the checker and policy files exist.
- [ ] Implement the three policy files and
      `scripts/validation/check-supply-chain-policy.py`; rerun the focused tests
      until all fixture-only positive and negative cases pass.
- [ ] Implement
      `bash scripts/security/verify-sample-service-supply-chain.sh --preflight`;
      fail when tool identity, artifact subject, policy, output path, or
      redaction boundary is missing.
- [ ] Run
      `bash scripts/security/verify-sample-service-supply-chain.sh --fixture-only`.
- [ ] Attempt
      `bash scripts/security/verify-sample-service-supply-chain.sh --advisory`
      to build/export labelled baseline and candidate variants locally, create
      CycloneDX and Grype results for each, produce SLSA/in-toto provenance,
      sign each OCI archive, and verify success plus tampered/wrong-subject
      rejection. Require two distinct subject tuples and write
      `verification-verdict.baseline.json` plus
      `verification-verdict.candidate.json` plus the exact pair manifest. Do
      not publish any partial generation. Require exact loaded role labels and
      distinct runtime IDs before publication.
- [ ] Run
      `bash scripts/security/verify-sample-service-supply-chain.sh --scorecard-advisory`
      only when the Task confirms network/read-only scope; otherwise record an
      explicit advisory skip.
- [ ] Wire `python3 scripts/validation/check-supply-chain-policy.py --check`
      into local/repository contracts and a network-independent CI job; do not
      dispatch it remotely.
- [ ] Record only concise subject, tool-pin, policy, verdict, checksum, and
      limitation fields in tracked evidence.
- [ ] Run fresh independent specification review, then quality/security review
      for the immutable-input controls; record all observed review evidence
      only in the domain Task.

## Verification Plan

`$COMPARISON_BASE_REF` denotes the explicit reviewed comparison ref recorded by
the [Program Task](../tasks/2026-07-19-operational-readiness-closure-program.md);
this Plan does not own a concrete base identity.

| Gate | Command / method | Expected pass evidence |
| --- | --- | --- |
| Metadata and lifecycle | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref "$COMPARISON_BASE_REF"` | Changed Stage 04 docs remain valid. |
| Traceability | `bash scripts/validation/check-doc-traceability.sh` and `bash scripts/validation/check-doc-implementation-alignment.sh` | `SSC-001`–`SSC-005` map to implemented files and Task evidence. |
| Repository contract | `bash scripts/validation/check-repo-contracts.sh` | No new contract breakage. |
| Fixture/unit tests | `python3 -m unittest tests.validation.test_supply_chain_policy -v` and `python3 scripts/validation/check-supply-chain-policy.py --check` | Positive/negative policy, SBOM, provenance, signature, and Scorecard fixtures pass. |
| Tool rehearsal | `bash scripts/security/verify-sample-service-supply-chain.sh --advisory` | Each baseline/candidate SBOM, scan verdict, provenance, signature, deterministic Docker-load archive, loaded role/runtime ID, and verifier evidence binds to its distinct portable subject tuple. |
| Scorecard observation | `bash scripts/security/verify-sample-service-supply-chain.sh --scorecard-advisory` or explicit Task skip | Advisory result or skip reason; no deterministic CI decision from remote score. |
| Review | Independent spec and quality/security review | All findings are resolved and independently re-reviewed. |

## Risks and Rollback

| Risk | Impact | Mitigation / rollback |
| --- | --- | --- |
| Digest/SBOM/provenance mismatch | Critical | Key all records by immutable digest and reject mismatches. |
| OCI-to-Docker or loaded-image identity mismatch | Critical | Validate descriptor/digest/DiffID and archive bounds, derive deterministic local refs, bind both archives and observed runtime IDs in verdict/pair schemas, and reject substitution. |
| Raw vulnerability or key leakage | Critical | Store raw outputs only in ignored/transient paths; tracked docs get summaries/checksums. |
| Network freshness makes CI flaky | High | Deterministic fixtures own blocking decisions; live DB/Scorecard evidence is advisory/freshness-stamped. |
| Keyless/OIDC claim without trust evidence | Critical | Use local ephemeral test keys unless a later Task approves OIDC and identity verification. |
| Scorecard overclaim | High | Treat findings as reviewed advisory signals, not maturity or release gates. |

Rollback is by reverting the logical commit, deleting transient task-owned
artifacts, and disabling only newly added advisory/blocking consumers. No
rollback step may assume or mutate a published artifact or remote setting.

## Approval Gates

- Plan activation requires recorded human approval.
- The future Task must approve exact tool image tags/digests, artifact subject,
  private-key lifetime, transient paths, redaction, and optional read-only
  Scorecard observation before execution.
- Registry push, artifact publication, keyless/OIDC signing, remote GitHub
  mutation/dispatch, Releases, deployments, and credential changes remain
  unapproved. The tracked fixture-only CI configuration is approved local code.

## Completion Criteria

- [ ] Active Task maps `SSC-001`–`SSC-005` to exact files, commands, rollback,
      redaction, and reviews.
- [ ] Tool/image identities and policy fixtures are pinned and reproducible.
- [ ] SBOM and vulnerability verdict bind to the same sample image digest.
- [ ] Provenance and signature verification pass success and negative cases.
- [ ] Scorecard observation is either read-only advisory with limitations or
      explicitly skipped with rationale.
- [ ] Independent specification and quality/security review acceptance remains
      a Task-owned prerequisite to program closure.
- [ ] Spec 126 lifecycle reflects only local supply-chain evidence; remote,
      publication, OIDC, and SLSA-level exclusions remain explicit.

## Related Documents

- **PRD**: [Operational readiness closure](../../01.requirements/prd-025-operational-readiness-closure.md)
- **ARD**: [Operational readiness closure architecture](../../02.architecture/descriptions/ad-0028-operational-readiness-closure.md)
- **ADR**: [ADR-0028 local-isolated readiness evidence](../../02.architecture/decisions/adr-0028-local-isolated-readiness-evidence.md)
- **Spec**: [Spec 126](../../98.archive/03.specs/126-security-supply-chain-remediation/spec.md)
- **Deployment consumer**: [Spec 127](../../98.archive/03.specs/127-deployment-release-engineering-remediation/spec.md)
- **Syft v1.48.0 release**: <https://github.com/anchore/syft/releases/tag/v1.48.0>
- **Grype v0.116.0 release**: <https://github.com/anchore/grype/releases/tag/v0.116.0>
- **Grype getting started / offline behavior**: <https://oss.anchore.com/docs/guides/vulnerability/getting-started/>
- **Cosign v3.0.6 release**: <https://github.com/sigstore/cosign/releases/tag/v3.0.6>
- **Cosign blob signing**: <https://docs.sigstore.dev/cosign/signing/signing_with_blobs/>
- **SLSA provenance**: <https://slsa.dev/spec/v1.2/provenance>
- **OpenSSF Scorecard v5.5.0 release**: <https://github.com/ossf/scorecard/releases/tag/v5.5.0>
- **OpenSSF Scorecard Action**: <https://github.com/ossf/scorecard-action>
