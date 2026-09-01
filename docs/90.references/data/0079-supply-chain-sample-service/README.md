---
title: "Reference: Sample-service Local Supply-chain Verification"
type: references/data
layer: reference
status: active
owner: "@buenhyden"
artifact_id: DATA-0079
parent_ids: []
created: 2026-07-19
updated: 2026-08-23
observed_at: 2026-08-23
generated_by: scripts/security/generate-supply-chain-sample-service-summary.sh
---

# Reference: Sample-service Local Supply-chain Verification

## Purpose

This generated reference records the tracked, local-only supply-chain
fixture contract for `examples/sample-web-service`. It is evidence routing,
not a publication, release, registry, remote attestation, OIDC, or SLSA
conformance claim.

### Verification Intent

The deterministic policy gate verifies pinned repository manifests,
observed target descriptors, independently hashed config bodies, distinct
baseline/candidate subject fixtures, redacted Grype policy handling, SBOM and
provenance binding, signature-negative fixtures, and Scorecard advisory-only
semantics without network access.

## Consumers

This reference is a generated Stage 90 index to completed Spec 126 and its
completed local Stage 04 Task. The checker and wrapper own executable policy
behavior; this document does not replace security policy, CI configuration,
or Task evidence and does not extend the completed local boundary.

## Limitations

### In Scope

- Fixture-only validation for the local sample-service policy.
- Digest-bound portable local subject tuples and redacted verification verdict schema.
- Local ephemeral Cosign key lifetime and advisory-only Scorecard boundary.

### Out of Scope

- Registry pushes, artifact publication, remote attestations, workflow dispatch,
  GitHub mutation, OIDC, transparency-log trust, releases, and deployment.
- Raw scan reports, SBOM/provenance bodies, signature bundles, private keys,
  credentials, tokens, and Scorecard response payloads.

## Schema

- **Policy ID**: `sample-service-local-v1`.
- **Subject**: `examples/sample-web-service` with roles `baseline, candidate`.
- **SBOM format**: `cyclonedx-json`.
- **Provenance predicate**: `https://slsa.dev/provenance/v1`.
- **Signature mode**: `cosign-sign-blob` with `process` key lifetime.
- **CI enforcement**: `fixture-policy-only`.

### Definitions / Facts

- **Fixture-only** means deterministic local JSON validation with no network
  access, image build, signature key, or consumer verdict creation.
- **Advisory rehearsal** means an optional local execution that may report
  unavailable prerequisites without claiming a passing runtime result.
- **Accepted verdict** means a redacted, digest-bound local consumer record;
  it is not a published artifact, remote attestation, or release approval.

## Inventory

| Tool | Repository manifest | Target descriptor | Config digest | Command contract | Network mode |
| --- | --- | --- | --- | --- | --- |
| `syft` | `anchore/syft@sha256:b4f1df79f97b817682d8b5ff941eb6bfe74f6172553a5e312c75bbc2eabc405c` | `sha256:b4f1df79f97b817682d8b5ff941eb6bfe74f6172553a5e312c75bbc2eabc405c` | `sha256:3567af297260e786440f30d149c2846302fd1df0823ee769d8b167d068f7d181` | `oci-archive-to-cyclonedx-json` | `none` |
| `grype` | `anchore/grype@sha256:fd4ab4d1042b522c896e73bdf09ab8bf384fa417df99d6dd0d6e1008c7e7c821` | `sha256:fd4ab4d1042b522c896e73bdf09ab8bf384fa417df99d6dd0d6e1008c7e7c821` | `sha256:4d4127e08c9eaafe6fa1eb2fcc05c83b2608562541949ffb33ef32eb4b1b25c0` | `sbom-to-redacted-json-verdict` | `advisory-network-optional` |
| `cosign` | `gcr.io/projectsigstore/cosign@sha256:de9c65609e6bde17e6b48de485ee788407c9502fa08b8f4459f595b21f56cd00` | `sha256:de9c65609e6bde17e6b48de485ee788407c9502fa08b8f4459f595b21f56cd00` | `sha256:4221e0d9d429afa26a9f1b8bc8f0ba2c9af470f7b495d845c31ac982a5d1182b` | `local-sign-blob-and-verify-blob` | `none` |
| `scorecard` | `ghcr.io/ossf/scorecard@sha256:3f24714e9366917adb7a05635382c97dfecb14b21eaef3dfa2ea48c8e23e0795` | `sha256:3f24714e9366917adb7a05635382c97dfecb14b21eaef3dfa2ea48c8e23e0795` | `sha256:6b05eb0cfef8a6df4f78dae40cbbe8b18da1ec881c4c70a14796201a122a3491` | `read-only-advisory-repository-observation` | `read-only-advisory` |

## Provenance

- The Task consumer contract is exactly three ignored local handoff files:
  `_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.baseline.json`
  `verification-verdict.candidate.json`, and `verification-verdict.pair.json`.
- Each schema-v2 verdict binds source revision and build context to the full
  portable identity tuple: OCI manifest digest, image config digest, OCI
  archive SHA-256, deterministic Docker-load archive SHA-256, deterministic
  local image reference, observed runtime image ID, and runtime identity kind.
  It also carries policy ID, role, accepted verdict, a null exception ID,
  verification time, and redaction status.
- The schema-v3 pair manifest uses generation
  `hyhome-verification-verdict-pair-v3`; it binds the exact bytes of both
  verdicts and repeats the full per-role identity tuple. Partial, legacy,
  mixed-generation, or substituted handoffs fail closed.
- The OCI-to-Docker handoff is a deterministic, uncompressed Docker load
  archive derived from the validated OCI config and layers. Consumers use
  only the bound local reference, require `pull_policy: never`, `--pull never`,
  and `--no-build`, and compare both the local object's `.Id` and the running
  container `.Image` with the recorded runtime image ID.
- Fixture-only checks do not create consumer verdicts. Advisory execution must
  produce distinct accepted subjects without a vulnerability exception or
  report a truthful prerequisite block, exception-review rejection, or policy
  rejection.

### Advisory Boundary

Scorecard is a read-only advisory observation. Its score cannot be a fixture
policy or CI blocking decision. This generator does not assert that any live
tool image, vulnerability database, Scorecard endpoint, or remote workflow
was available or run.

### Sources

- [tool registry](../../../../infra/supply-chain.tool-images.json)
- [sample-service policy](../../../../infra/supply-chain.sample-service-policy.json)
- [exception registry](../../../../infra/supply-chain.vulnerability-exceptions.json)
- [fixture checker](../../../../scripts/validation/check-supply-chain-policy.py)
- [local wrapper](../../../../scripts/security/verify-sample-service-supply-chain.sh)

## Refresh

- **Owner**: Security Auditor / CI-CD Engineer.
- **Refresh**: run `bash scripts/security/generate-supply-chain-sample-service-summary.sh`
  after changing the fixture contract, policy, tool registry, or wrapper.
- **Freshness**: run `bash scripts/security/generate-supply-chain-sample-service-summary.sh --check`.

## Traceability

- [Archive migration lookup](../../../98.archive/migrations/0003-workspace-governance-simplification.md)
- [security data index](./README.md)
