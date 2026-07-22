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

This active Task records local, digest-bound supply-chain evidence for
`examples/sample-web-service` baseline and candidate variants. Deterministic
implementation is complete, while current committed-tree runtime remains
blocked before Docker by the absent approved offline Grype database seed. No
accepted pair, publication, remote dispatch, release, or deployment is claimed.

The Task owns two concise consumer verdicts plus their atomic pair manifest under
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
| Runtime material | `nginxinc/nginx-unprivileged:1.31.3-alpine3.24-slim@sha256:90d82b3358df5758b3c57d20f2565082ce6f744906e7dc09afd0096c1b8eb2b5` |

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
| `T-SSC-001` | Tool registry, policies, exceptions, checker, and fixtures | `SSC-001`–`SSC-005` | Deterministic fixture RED/GREEN suite | Fresh implementation agent | Complete; current focused suite 44/44 and static/preflight gates pass |
| `T-SSC-002` | Distinct builds, OCI export, SBOM, and scan verdict | `SSC-001`, `SSC-002` | Two subject tuples and verdicts | Fresh implementation agent | Implementation complete; current advisory blocks before Docker on the absent approved database seed, while the earlier class-40 run remains historical rejection evidence |
| `T-SSC-003` | Provenance and local signature verification | `SSC-003`, `SSC-004` | Success plus tamper/wrong-subject rejection | Fresh implementation agent | Complete for deterministic positive/negative fixtures, including cross-role archive rejection; live provenance/signing correctly does not proceed after the baseline policy rejection |
| `T-SSC-004` | Fixture-only CI/repo gate and advisory summary | `SSC-005` | Network-independent check and freshness | Fresh implementation agent | Complete; CI/local/repository wiring and generated summaries pass |
| `T-SSC-005` | Independent specification and security/quality review | `VAL-SSC-001`–`004` | C0/I0/M0 re-review | Separate reviewers | Current terminal reviews approved C0/I0/M0; Task remains active on runtime prerequisites |

## Work Log

| Date | Work unit | Result |
| --- | --- | --- |
| 2026-07-19 | Task activation | Contract recorded; no tool, image, key, network, workflow, or artifact action executed. |
| 2026-07-19 | `T-SSC-001`–`T-SSC-005` | Initially `not_run`; actual evidence is appended only after exact execution. |
| 2026-07-22 | `T-SSC-001` | RED was the expected missing-checker error; the remediation RED added archive/index/manifest, stale-verdict, multi-match exception, cross-role signature, and exact Scorecard identity failures. GREEN is `27/27` focused tests and `13` deterministic fixtures. Tool pins, policy, exception, SBOM, provenance, signature, and Scorecard advisory-only semantics pass locally without network. |
| 2026-07-22 | `T-SSC-002`–`T-SSC-004` | Preflight and fixture-only wrapper modes pass. An authorized bounded local pull cached exact pinned tool/material images. The first advisory run exposed and fixed a local SBOM-subject binding defect. A separately authorized read-only retrieval using only pinned Grype then seeded the ignored task cache; its status records schema `v6.1.9`, built `2026-07-21T07:05:18Z`, and package SHA-256 `724e5d99c799d7e9b98ae8eb11930cf8ae427c4218b1e4db9d70e711dce63ce9`. The final offline advisory built/exported distinct baseline/candidate subjects, bound the baseline SBOM, and rejected the baseline at class `40` with `grype-policy-rejected` (14 critical matches; no exception). Raw scan material, redacted result, and DB identity remain only under the ignored task directory; the task-owned `/tmp` key directory was removed and no consumer verdict remains. Scorecard was explicitly skipped because this Task has not confirmed read-only network approval. CI/local/repository fixture gates and generated-summary freshness pass. |
| 2026-07-22 | Combined review remediation | Combined review findings `C3/I1/M1` were addressed without relaxing policy: config identity now comes from the exact scanned/signed OCI archive's verified index-to-manifest-to-config chain; both consumer verdict paths are invalidated before advisory work and published only as a completed pair from run-scoped outputs; every Grype match is evaluated; wrong-subject verification crosses roles; and Scorecard uses `github.com/buenhyden/hy-home.docker`. The rerun bound the baseline SBOM to archive config `sha256:6e7a5cc7b701219126e0442e5a49e3ba6a1b6cb79fe8c1a5c6ddc090ad77633d` and again stopped at the truthful baseline class `40` rejection. Review closure was then pending. |
| 2026-07-22 | Re-review C1 remediation | Two re-reviews identified that an accepted Grype result with a non-null exception ID could have been reduced to a null consumer exception and published downstream. New wrapper RED/GREEN coverage preserves the internal `vulnerability-verdict.json` exception ID, exits class `40` with `grype-exception-requires-manual-review`, and proves both fixed consumer verdict paths remain absent. |
| 2026-07-22 | Terminal review closure | The initial/combined review findings `C3/I1/M1` and first re-review C1 were remediated. Terminal specification and quality/security reviews both returned `APPROVED C0/I0/M0`. This closes `T-SSC-005` only; the active Task and Task 5 accepted-pair prerequisite remain unchanged. |
| 2026-07-22 | Program closure advisory rerun (historical pre-hardening evidence) | The 27/27 suite and offline advisory class-40 `grype-policy-rejected` observation remain historical evidence for the pre-hardening committed state: 167 baseline matches included 14 Critical and 73 High, with no exception and no accepted pair. It is not the current runtime result and grants no exception. |
| 2026-07-22 | Whole-review hardening RED/GREEN ledger (historical, superseded) | RED `c8aa52b9` captured hardened supply-chain boundaries; GREEN `df1dd8c1` enforced offline immutable handoffs. RED `4de5c04d` reproduced protected cache cleanup failure; GREEN `ae354a00` moved that cleanup behind the gated runtime. RED `552e3867` captured private tool-temp and seed preflight; historical interim GREEN identity `f966266e129b11da198904b7076ca3c224f3e468` was superseded by final GREEN `e5a4d739`, which provided private tool temporary storage and the early seed gate. Its 39/39 result remains exact historical evidence. |
| 2026-07-22 | Immutable build-context RED/GREEN | RED `abc1dd21` captured mutable-context and mixed input-generation gaps. GREEN `c8342c09` records independent manifest and configuration image identities, constructs one deterministic mode-0600 `.dockerignore`-aware tar inside a mode-0700 private runtime, snapshots device/inode/size/mtime/ctime/mode/UID/hash metadata, passes that exact tar to Buildx over stdin, and immediately revalidates it after build. A mutate-and-restore attempt fails class 50 without publishing a pair. The current focused suite passes 44/44 with 13 fixtures; Bash/static/Python/diff and preflight gates pass. |
| 2026-07-22 | Current committed-tree advisory boundary | Exactly one current hardened advisory exits class `10` with `grype-db-seed-unavailable-advisory-blocked` before Docker because the one-time approved seed is absent and no reusable local database exists. No accepted baseline/candidate verdict, committed pair manifest, transient run verdict, signing key, private runtime tree, or tool container remains. The Task stays active pending a current approved seed and a passing policy verdict. |
| 2026-07-23 | Terminal whole-branch review closure | Quality/security review v3 returned `APPROVED C0/I0/M0` for the full branch range through `20022458` plus the then-current 26-document reconciliation diff. Specification review v5 returned `APPROVED C0/I0/M0` for the full branch range through `20022458` plus the final 26-document reconciliation diff. Earlier `CHANGES REQUIRED` iterations remain historical remediation evidence. These approvals do not create the missing database seed, current policy pass, accepted verdict pair, or pair manifest; the Task and Program remain active and the controlled wrapper remains blocked/not_run. |

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

Historical evidence: the initial RED command produced the expected
`FileNotFoundError` for the absent checker before any implementation existed.
The focused GREEN command passed `27/27`; the deterministic checker printed
`supply_chain_policy=pass fixtures=13`; wrapper `--preflight` and
`--fixture-only` passed; and `--scorecard-advisory` printed an explicit skipped
result because read-only network approval is not recorded. An authorized bounded
local pull cached the exact pinned tool/material images. The first advisory run
reached SBOM generation and exposed a subject-binding defect, which was fixed.
A separately authorized read-only retrieval using only pinned Grype seeded the
ignored task cache; the recorded database identity is schema `v6.1.9`, built
`2026-07-21T07:05:18Z`, and package SHA-256
`724e5d99c799d7e9b98ae8eb11930cf8ae427c4218b1e4db9d70e711dce63ce9`.
The final offline `--advisory` built/exported distinct baseline/candidate
subjects and bound the baseline SBOM, then exited class `40` with
`grype-policy-rejected`: the redacted baseline summary has 14 critical matches
and no exception. Raw scan material, redacted result, and database identity
remain only under the ignored task directory; the task-owned `/tmp` key
directory was removed and no consumer verdict remains. No registry push,
publication, OIDC, Scorecard request, or other remote mutation occurred.

Combined-review remediation reran the advisory with config identity derived
from the exact OCI archive. The baseline archive index/manifest config digest
and bound SBOM property both equal
`sha256:6e7a5cc7b701219126e0442e5a49e3ba6a1b6cb79fe8c1a5c6ddc090ad77633d`;
the archive SHA-256 is
`sha256:76d1b253167529006cf55a588195720ae461904c3e5dd461a5f153778cf2ba36`.
The rerun again exited class `40` at the baseline policy gate. Fixed verdict
paths were absent after failure, and no task-owned `/tmp` key directory
remained.

The re-review C1 regression simulates an otherwise accepted baseline Grype
result with `exception_id` `EXC-SSC-0001`. The wrapper preserves that ID in the
transient `vulnerability-verdict.json`, exits class `40` with
`grype-exception-requires-manual-review`, and leaves both fixed consumer paths
absent; it therefore never converts an exception-approved scan into a Task 5
consumer verdict.

Current verification results: deterministic implementation, focused/static
checks, and preflight pass at 44/44. The hardened committed-tree advisory exits
class `10` with `grype-db-seed-unavailable-advisory-blocked` before Docker;
the approved one-time seed and a reusable local database are absent. The prior
class-40 14-Critical/73-High/no-exception policy rejection is preserved only as
historical pre-hardening evidence. No accepted baseline/candidate consumer
verdicts exist, no exception is invented, and Task 5 remains fail-closed. Exit
classes are `0=pass/accepted`,
`2=usage`, `10=policy/preflight`, `20=build/export`, `30=SBOM`,
`40=vulnerability verdict`, `50=provenance`, `60=signature verification`, and
`70=Scorecard observation`.

Historical domain-stage local quality evidence: the repository-contract supply-chain section and
all Task-owned generated checks pass, while the aggregate repository contract
remains at `failures=5` for four pre-existing lifecycle manifest-consumer
mismatches and the missing `html5lib` provider renderer; the full local QA
runner stops at that same renderer. Targeted pre-commit passed all non-Docker
hooks, and the root implementation owner separately recorded an exact
`hadolint-docker` pass for `examples/sample-web-service/Dockerfile`.

Task 6 documentation, owner regeneration, safe gates, and whole-branch
re-review are recorded by the Program Task. They cannot create the missing
database seed, policy pass, or accepted verdict pair. The controlled all-files
wrapper remains blocked and `not_run`.

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

Implementation review verdict: deterministic policy, preflight, fixture-only
wiring, summary freshness, protected-cache handling, private temporary paths,
and the early seed gate are implemented. Current runtime stops at the missing
approved seed before Docker.

Combined review remediation: `C3/I1/M1` findings were remediated with new
archive-binding, stale-verdict, multi-match, cross-role, and exact-repository
regressions. Two re-reviews then returned the same C1 for accepted-by-exception
consumer publication; its wrapper-level fail-closed regression is remediated.
The terminal specification and quality/security reviews both returned
`APPROVED C0/I0/M0` for the historical implementation unit. The subsequent
whole-review and immutable-input hardening commits are covered by the terminal
whole-branch approvals below.

Specification review verdict: historical domain review `APPROVED C0/I0/M0`;
terminal specification review v5 `APPROVED C0/I0/M0` for the full branch range
through `20022458` plus the final 26-document reconciliation diff.

Quality/security review verdict: historical domain review `APPROVED C0/I0/M0`;
terminal quality/security review v3 `APPROVED C0/I0/M0` for the full branch
range through `20022458` plus the then-current 26-document reconciliation diff.

Findings and disposition: the initial/combined `C3/I1/M1` findings and the
first re-review C1 are remediated and closed. Terminal review closure does not
create accepted runtime verdicts, change the active lifecycle, or satisfy Task
5's separate accepted-pair prerequisite. Earlier `CHANGES REQUIRED` iterations
remain historical remediation evidence.

## Commit Ledger

Historical implementation identity:
`72e584f51badfd194c0a1b6d32510a3bf3ab395c`. Earlier remediation ledger:
`c8aa52b9`, `df1dd8c1`, `4de5c04d`, `ae354a00`, `552e3867`, historical
interim `f966266e129b11da198904b7076ca3c224f3e468`, and `e5a4d739`.
Current immutable-input hardening is RED `abc1dd21` followed by GREEN
`c8342c09`.
The separate evidence update does not embed its own SHA.

Logical unit: `feat(security): add local supply-chain verification`.

Commit validation: 44/44 focused fixture and wrapper tests, deterministic
checker, static checks, preflight, fixture-only, summary freshness, immutable
context revalidation, and the truthful blocked advisory result are recorded
above. Historical terminal reviews are APPROVED C0/I0/M0 for their exact
reviewed commits; terminal whole-branch specification v5 and quality/security
v3 reviews are APPROVED C0/I0/M0 for the current range.

## Deferred and Blocked Items

Deferred items: registry push, remote attestation, keyless/OIDC, transparency
log, publication, live Scorecard blocking, GitHub Release, deployment, and SLSA
level claims.

Blocked items: the current approved offline Grype database seed is absent, so
the hardened advisory stops before Docker and cannot reach the policy gate.
Delivery remains blocked until a current seeded run passes policy and produces
both accepted, distinct, same-revision verdicts. The historical policy result
was rejected with no exception and does not satisfy that prerequisite.
`--scorecard-advisory` remains skipped until read-only network scope is
confirmed. Current specification and quality/security review of `abc1dd21` and
`c8342c09` is complete under the v3/v5 whole-branch approvals; this does not
relax the runtime blockers above.

Deferral destination: remote identity, publication, or enforcement needs a new
approved Stage 01-04 chain; local accepted verdicts are consumed only by
[Spec 127](../../03.specs/127-deployment-release-engineering-remediation/spec.md).

## Related Documents

- [Spec 126](../../03.specs/126-security-supply-chain-remediation/spec.md)
- [Supply-chain Plan](../plans/2026-07-11-security-supply-chain-remediation.md)
- [Program Task](./2026-07-19-operational-readiness-closure-program.md)
- [Approved-network runtime closure Task](./2026-07-23-security-supply-chain-runtime-closure.md)
- [Delivery Task](./2026-07-19-deployment-release-engineering-remediation.md)
- [Security audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md)
