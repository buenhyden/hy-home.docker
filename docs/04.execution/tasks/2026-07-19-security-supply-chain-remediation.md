---
status: active
artifact_id: task:2026-07-19-security-supply-chain-remediation
artifact_type: task
parent_ids:
  - spec:126-security-supply-chain-remediation
  - plan:2026-07-11-security-supply-chain-remediation
---

# Task: Security Supply-Chain Remediation

## Overview

This active Task will record local, digest-bound supply-chain evidence for
`examples/sample-web-service` baseline and candidate variants. At activation,
no image has been built or exported, no SBOM or scan has run, no key has been
created, and no artifact, attestation, workflow, or Scorecard result has been
published or remotely dispatched.

The Task owns two concise consumer verdicts under
`_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/`.
Raw scanner output, private keys, and response payloads are not tracked Task
evidence.

## Inputs

- [Spec 126](../../03.specs/126-security-supply-chain-remediation/spec.md)
- [Security supply-chain Plan](../plans/2026-07-11-security-supply-chain-remediation.md)
- [Program Plan](../plans/2026-07-19-operational-readiness-closure-program.md)
- `examples/sample-web-service` source and pinned Dockerfile materials
- The exact tool-container manifests and policy interfaces in the Plan

## Goals and Non-goals

Goals:

- enforce deterministic tool, subject, vulnerability, exception, provenance,
  signature, and advisory policy fixtures;
- build two distinct local subject tuples from one source revision;
- bind CycloneDX SBOM, Grype verdict, SLSA/in-toto provenance, and Cosign blob
  verification to each tuple;
- expose only two accepted/rejected typed verdicts to the delivery Task;
- keep Scorecard read-only advisory and fixture policy network-independent.

Non-goals:

- registry push, artifact publication, remote attestation storage, GitHub
  mutation/dispatch, GitHub Release, or deployment;
- keyless/OIDC signing, transparency-log trust, signed-release, SLSA-level, or
  broad security-maturity claims;
- raw vulnerability reports, credentials, tokens, private keys, or secret
  values in tracked evidence.

## Scope and Change Boundaries

Allowed authored paths are the exact policy, checker, wrapper, fixture, sample
service, test, generated-summary, local QA, repository-contract, and
`.github/workflows/ci-quality.yml` paths listed in the approved Plan, plus this
Task and directly supported lifecycle/index evidence.

Allowed transient path: only
`_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/`.
Ephemeral signing keys must live under `/tmp` for one wrapper lifetime and be
deleted by the exit trap.

Forbidden paths/actions: global tool installation, mutable or unpinned tool
identity, fabricated `RepoDigest`, equal baseline/candidate subjects, key or raw
finding promotion, remote publication/dispatch, OIDC, credentials, deployment,
and production policy claims.

Compose impact: local Docker build/export and pinned tool containers only; no
workspace Compose service or production runtime change.

Security impact: deterministic local policy enforcement and ephemeral local
blob signing. The tracked fixture-only CI configuration is local code; remote
workflow execution or enforcement is not authorized.

Operations impact: none beyond task-owned local artifacts and cleanup.

Runtime impact: local image builds and pinned tool-container executions only.
The optional Scorecard command is read-only and may run only after network
scope is re-confirmed in this Task.

## Approval Evidence

Approval source:

- The user approved protected-surface and local CI/QA changes within the
  operational-readiness program.
- [ADR 0028](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md),
  [Spec 126](../../03.specs/126-security-supply-chain-remediation/spec.md), and
  the active Plan approve the local fixture/advisory design.

Protected surfaces: the pinned tool registry, sample-service build materials,
policy and exception registries, local fixture CI gate, task-owned Docker
artifacts, `/tmp` signing key, and concise verdicts may change within the Plan.
Registry, GitHub, OIDC, credentials, Releases, deployments, and published
attestations remain protected.

Approval boundary: authorized tool identities are exactly Syft v1.48.0, Grype
v0.116.0, Cosign v3.0.6, and Scorecard v5.5.0 at the manifest digests in the
Plan. Wrapper modes are only `--fixture-only`, `--preflight`, `--advisory`, and
`--scorecard-advisory`. Changed identity, subject, policy, output, network, or
key lifetime requires stop and new approval.

| Tool or material | Exact approved image identity |
| --- | --- |
| Syft | `anchore/syft:v1.48.0@sha256:b4f1df79f97b817682d8b5ff941eb6bfe74f6172553a5e312c75bbc2eabc405c` |
| Grype | `anchore/grype:v0.116.0@sha256:fd4ab4d1042b522c896e73bdf09ab8bf384fa417df99d6dd0d6e1008c7e7c821` |
| Cosign | `gcr.io/projectsigstore/cosign:v3.0.6@sha256:de9c65609e6bde17e6b48de485ee788407c9502fa08b8f4459f595b21f56cd00` |
| Scorecard | `ghcr.io/ossf/scorecard:v5.5.0@sha256:3f24714e9366917adb7a05635382c97dfecb14b21eaef3dfa2ea48c8e23e0795` |
| Build material | `alpine:3.21@sha256:48b0309ca019d89d40f670aa1bc06e426dc0931948452e8491e3d65087abc07d` |
| Runtime material | `nginxinc/nginx-unprivileged:1.27.3-alpine@sha256:9e7238f579a54582263a960d1b0094b4a3ecce641342eda3f8e2ff82b1703d2b` |

Rollback or recovery: delete task-owned transient artifacts and the ephemeral
private key, revert the one logical SSC commit, and regenerate only the
supply-chain summary through its owner. No remote artifact or setting exists to
delete. If subject identity is ambiguous, fail closed and retain no key.

Redaction boundary: tracked evidence may contain tool pins, source revision,
image config digest, OCI archive SHA-256, policy ID, exception ID, concise
verdict, timestamp, cleanup, and review results. Raw scanner findings, SBOM
contents, provenance payloads, signatures, keys, logs, tokens, credentials, and
Scorecard response bodies remain transient.

## Work Breakdown

| Task ID | Description | Parent requirement | Validation / evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| `T-SSC-001` | Tool registry, policies, exceptions, checker, and fixtures | `SSC-001`–`SSC-005` | Deterministic fixture RED/GREEN suite | Fresh implementation agent | Not run |
| `T-SSC-002` | Distinct builds, OCI export, SBOM, and scan verdict | `SSC-001`, `SSC-002` | Two subject tuples and verdicts | Fresh implementation agent | Not run |
| `T-SSC-003` | Provenance and local signature verification | `SSC-003`, `SSC-004` | Success plus tamper/wrong-subject rejection | Fresh implementation agent | Not run |
| `T-SSC-004` | Fixture-only CI/repo gate and advisory summary | `SSC-005` | Network-independent check and freshness | Fresh implementation agent | Not run |
| `T-SSC-005` | Independent specification and security/quality review | `VAL-SSC-001`–`004` | C0/I0/M0 re-review | Separate reviewers | Not run |

## Work Log

| Date | Work unit | Result |
| --- | --- | --- |
| 2026-07-19 | Task activation | Contract recorded; no tool, image, key, network, workflow, or artifact action executed. |
| 2026-07-19 | `T-SSC-001`–`T-SSC-005` | `not_run`; actual evidence is appended only after exact execution. |

## Verification Evidence

Exact command envelope:

```bash
python3 -m unittest tests.validation.test_supply_chain_policy -v
python3 scripts/validation/check-supply-chain-policy.py --check
bash scripts/security/verify-sample-service-supply-chain.sh --preflight
bash scripts/security/verify-sample-service-supply-chain.sh --fixture-only
bash scripts/security/verify-sample-service-supply-chain.sh --advisory
bash scripts/security/verify-sample-service-supply-chain.sh --scorecard-advisory
```

The final command is optional and requires a Task update confirming read-only
network scope. Otherwise it is recorded as skipped; a score never controls the
deterministic fixture policy verdict.

Expected evidence: tests reject unpinned tools, subject mismatch, invalid or
expired exceptions, tamper, wrong subject, and Scorecard blocking. Advisory
execution emits distinct baseline/candidate accepted verdicts for the same
40-hex source revision, different image/archive digests, policy
`sample-service-local-v1`, no exception, and `redaction_status=passed`.

Actual evidence: `not_run`.

Verification results: `not_run`. Exit classes are `0=pass/accepted`,
`2=usage`, `10=policy/preflight`, `20=build/export`, `30=SBOM`,
`40=vulnerability verdict`, `50=provenance`, `60=signature verification`, and
`70=Scorecard observation`.

## Controlled Agent Pre-commit Evidence

Controlled wrapper command: not owned by this domain Task. The program Task
owns the one final all-files invocation.

Allowed prefixes: `not_applicable` at domain activation.

Wrapper exit status: `not_run`.

Snapshot result and path sets: `not_run`.

Observation boundary: only Git-visible, non-ignored repository paths are
observable when the program wrapper later runs.

Disposition: defer to the
[program Task](./2026-07-19-operational-readiness-closure-program.md); direct
`pre-commit run --all-files` is prohibited.

## Review Evidence

Implementation review verdict: `not_run`.

Specification review verdict: `not_run`; a fresh reviewer must verify Spec 126,
the exact pins and subjects, fixture semantics, verdict schema, and downstream
handoff.

Quality/security review verdict: `not_run`; a separate reviewer must inspect
input parsing, image/tool identity, exception logic, key lifecycle, redaction,
negative tests, and cleanup.

Findings and disposition: none because review has not run. All findings must be
remediated and re-reviewed to C0/I0/M0.

## Commit Ledger

Commit identity: `not_committed`.

Logical unit: `feat(security): add local supply-chain verification`.

Commit validation: `not_run`; record fixture tests, local verification modes,
summary freshness, cleanup/key deletion, and review verdicts after commit.

## Deferred and Blocked Items

Deferred items: registry push, remote attestation, keyless/OIDC, transparency
log, publication, live Scorecard blocking, GitHub Release, deployment, and SLSA
level claims.

Blocked items: advisory build/verification is blocked until deterministic
fixtures and preflight pass. `--scorecard-advisory` is blocked until read-only
network scope is confirmed. Delivery consumption is blocked until both typed
verdicts are accepted and distinct.

Deferral destination: remote identity, publication, or enforcement needs a new
approved Stage 01-04 chain; local accepted verdicts are consumed only by
[Spec 127](../../03.specs/127-deployment-release-engineering-remediation/spec.md).

## Related Documents

- [Spec 126](../../03.specs/126-security-supply-chain-remediation/spec.md)
- [Supply-chain Plan](../plans/2026-07-11-security-supply-chain-remediation.md)
- [Program Task](./2026-07-19-operational-readiness-closure-program.md)
- [Delivery Task](./2026-07-19-deployment-release-engineering-remediation.md)
- [Security audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md)
