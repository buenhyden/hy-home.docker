---
status: active
generated_by: scripts/security/generate-supply-chain-sample-service-summary.sh
---

# Reference: Sample-service Local Supply-chain Verification

## Overview

This generated reference records the tracked, local-only supply-chain
fixture contract for `examples/sample-web-service`. It is evidence routing,
not a publication, release, registry, remote attestation, OIDC, or SLSA
conformance claim.

## Purpose

The deterministic policy gate verifies pinned tool identities, distinct
baseline/candidate subject fixtures, redacted Grype policy handling, SBOM and
provenance binding, signature-negative fixtures, and Scorecard advisory-only
semantics without network access.

## Repository Role

This reference is a generated Stage 90 index to the active Spec 126 and
Stage 04 Task. The checker and wrapper own executable policy behavior; this
document does not replace security policy, CI configuration, or Task evidence.

## Scope

### In Scope

- Fixture-only validation for the local sample-service policy.
- Digest-bound local subject tuples and redacted verification verdict schema.
- Local ephemeral Cosign key lifetime and advisory-only Scorecard boundary.

### Out of Scope

- Registry pushes, artifact publication, remote attestations, workflow dispatch,
  GitHub mutation, OIDC, transparency-log trust, releases, and deployment.
- Raw scan reports, SBOM/provenance bodies, signature bundles, private keys,
  credentials, tokens, and Scorecard response payloads.

## Policy Contract

- **Policy ID**: `sample-service-local-v1`.
- **Subject**: `examples/sample-web-service` with roles `baseline, candidate`.
- **SBOM format**: `cyclonedx-json`.
- **Provenance predicate**: `https://slsa.dev/provenance/v1`.
- **Signature mode**: `cosign-sign-blob` with `process` key lifetime.
- **CI enforcement**: `fixture-policy-only`.

## Definitions / Facts

- **Fixture-only** means deterministic local JSON validation with no network
  access, image build, signature key, or consumer verdict creation.
- **Advisory rehearsal** means an optional local execution that may report
  unavailable prerequisites without claiming a passing runtime result.
- **Accepted verdict** means a redacted, digest-bound local consumer record;
  it is not a published artifact, remote attestation, or release approval.

## Pinned Tool Images

| Tool | Repository manifest | Config ID | Command contract | Network mode |
| --- | --- | --- | --- | --- |
| `syft` | `anchore/syft@sha256:b4f1df79f97b817682d8b5ff941eb6bfe74f6172553a5e312c75bbc2eabc405c` | `sha256:b4f1df79f97b817682d8b5ff941eb6bfe74f6172553a5e312c75bbc2eabc405c` | `oci-archive-to-cyclonedx-json` | `none` |
| `grype` | `anchore/grype@sha256:fd4ab4d1042b522c896e73bdf09ab8bf384fa417df99d6dd0d6e1008c7e7c821` | `sha256:fd4ab4d1042b522c896e73bdf09ab8bf384fa417df99d6dd0d6e1008c7e7c821` | `sbom-to-redacted-json-verdict` | `advisory-network-optional` |
| `cosign` | `gcr.io/projectsigstore/cosign@sha256:de9c65609e6bde17e6b48de485ee788407c9502fa08b8f4459f595b21f56cd00` | `sha256:de9c65609e6bde17e6b48de485ee788407c9502fa08b8f4459f595b21f56cd00` | `local-sign-blob-and-verify-blob` | `none` |
| `scorecard` | `ghcr.io/ossf/scorecard@sha256:3f24714e9366917adb7a05635382c97dfecb14b21eaef3dfa2ea48c8e23e0795` | `sha256:3f24714e9366917adb7a05635382c97dfecb14b21eaef3dfa2ea48c8e23e0795` | `read-only-advisory-repository-observation` | `read-only-advisory` |

## Evidence Boundary

- The Task consumer contract is exactly two ignored local verdicts at
  `_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.baseline.json`
  and `verification-verdict.candidate.json`.
- Each published consumer verdict carries only source revision, image config
  digest, OCI archive SHA-256, policy ID, role, verdict, a null exception ID,
  verification time, and redaction status.
- Fixture-only checks do not create consumer verdicts. Advisory execution must
  produce distinct accepted subjects without a vulnerability exception or
  report a truthful prerequisite block, exception-review rejection, or policy
  rejection.

## Advisory Boundary

Scorecard is a read-only advisory observation. Its score cannot be a fixture
policy or CI blocking decision. This generator does not assert that any live
tool image, vulnerability database, Scorecard endpoint, or remote workflow
was available or run.

## Sources

- [tool registry](../../../../infra/supply-chain.tool-images.json)
- [sample-service policy](../../../../infra/supply-chain.sample-service-policy.json)
- [exception registry](../../../../infra/supply-chain.vulnerability-exceptions.json)
- [fixture checker](../../../../scripts/validation/check-supply-chain-policy.py)
- [local wrapper](../../../../scripts/security/verify-sample-service-supply-chain.sh)

## Maintenance

- **Owner**: Security Auditor / CI-CD Engineer.
- **Refresh**: run `bash scripts/security/generate-supply-chain-sample-service-summary.sh`
  after changing the fixture contract, policy, tool registry, or wrapper.
- **Freshness**: run `bash scripts/security/generate-supply-chain-sample-service-summary.sh --check`.

## Related Documents

- [Supply-chain Task](../../../04.execution/tasks/2026-07-19-security-supply-chain-remediation.md)
- [Supply-chain Plan](../../../04.execution/plans/2026-07-11-security-supply-chain-remediation.md)
- [Spec 126](../../../03.specs/126-security-supply-chain-remediation/spec.md)
- [security data index](./README.md)
