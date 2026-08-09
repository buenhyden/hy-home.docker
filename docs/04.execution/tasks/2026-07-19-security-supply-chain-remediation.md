---
status: completed
artifact_id: task:2026-07-19-security-supply-chain-remediation
artifact_type: task
parent_ids:
  - plan:2026-07-11-security-supply-chain-remediation
  - spec:126-security-supply-chain-remediation
---

# Task: Security Supply-Chain Remediation

## Overview

This completed Task records local, digest-bound supply-chain evidence for
`examples/sample-web-service` baseline and candidate variants. Deterministic
implementation and the current offline advisory pass are complete. Schema-v2
accepted verdicts and their schema-v3 pair manifest now exist for source
revision `b070a06ceac2f3e60fdb5bdb3fa87b4b0433545b`. Fresh specification and
quality/security reviews of the exact Task 7 range
`b070a06ceac2f3e60fdb5bdb3fa87b4b0433545b..086744f8bd20370262ce297dd5b6dc101a5b54dc`
both returned `APPROVED C0/I0/M0`. This Task does not claim ownership of the
later Task 5 runtime; the delivery Task records that historical local sequence,
its exact-range review closure, and its current reopening after corrected
readiness/recovery hashes superseded the record inputs. No publication, remote
dispatch, release, or deployment is claimed.

The Task owns two concise consumer verdicts plus their atomic pair manifest under
`_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/`.
Raw scanner output, private keys, and response payloads are not tracked Task
evidence.

## Inputs

- [Spec 126](../../98.archive/03.specs/126-security-supply-chain-remediation/spec.md)
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
- expose only two accepted/rejected typed verdicts and their atomic pair
  manifest to the delivery Task;
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
- [ADR 0028](../../02.architecture/decisions/adr-0028-local-isolated-readiness-evidence.md),
  [Spec 126](../../98.archive/03.specs/126-security-supply-chain-remediation/spec.md), and
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
the OCI manifest/config/archive and deterministic Docker-load archive digests,
deterministic local reference, runtime image ID/kind, policy ID, exception ID,
concise verdict, timestamp, cleanup, and review results. Raw scanner findings,
SBOM contents, provenance payloads, signature bundles, keys, logs, tokens,
credentials, and Scorecard response bodies remain transient.

## Work Breakdown

| Task ID | Description | Parent requirement | Validation / evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| `T-SSC-001` | Tool registry, policies, exceptions, checker, and fixtures | `SSC-001`–`SSC-005` | Deterministic fixture RED/GREEN suite | Fresh implementation agent | Complete; current focused suite 67/67 and checker 13/13 pass |
| `T-SSC-002` | Distinct builds, OCI/Docker portable handoff, SBOM, and scan verdict | `SSC-001`, `SSC-002` | Two full portable subject tuples and verdicts | Fresh implementation agent | Complete; current preflight/advisory pass and publish two distinct accepted schema-v2 verdicts plus pair v3 |
| `T-SSC-003` | Provenance and local signature verification | `SSC-003`, `SSC-004` | Success plus tamper/wrong-subject rejection | Fresh implementation agent | Complete; current Cosign v3.0.6 new-format offline bundle path verifies both originals and rejects tampered/wrong subjects |
| `T-SSC-004` | Fixture-only CI/repo gate and advisory summary | `SSC-005` | Network-independent check and freshness | Fresh implementation agent | Complete; CI/local/repository wiring and generated summaries pass |
| `T-SSC-005` | Independent specification and security/quality review | `VAL-SSC-001`–`004` | C0/I0/M0 re-review | Separate reviewers | Complete for the local Task boundary; domain and final implementation re-reviews are approved while post-evidence branch confirmation remains pending |

## Work Log

| Date | Work unit | Result |
| --- | --- | --- |
| 2026-07-19 | Task activation | Contract recorded; no tool, image, key, network, workflow, or artifact action executed. |
| 2026-07-19 | `T-SSC-001`–`T-SSC-005` | Initially `not_run`; actual evidence is appended only after exact execution. |
| 2026-07-22 | `T-SSC-001` | RED was the expected missing-checker error; the remediation RED added archive/index/manifest, stale-verdict, multi-match exception, cross-role signature, and exact Scorecard identity failures. GREEN is `27/27` focused tests and `13` deterministic fixtures. Tool pins, policy, exception, SBOM, provenance, signature, and Scorecard advisory-only semantics pass locally without network. |
| 2026-07-22 | `T-SSC-002`–`T-SSC-004` | Preflight and fixture-only wrapper modes pass. An authorized bounded local pull cached exact pinned tool/material images. The first advisory run exposed and fixed a local SBOM-subject binding defect. A separately authorized read-only retrieval using only pinned Grype then seeded the ignored task cache; its status records schema `v6.1.9`, built `2026-07-21T07:05:18Z`, and package SHA-256 `724e5d99c799d7e9b98ae8eb11930cf8ae427c4218b1e4db9d70e711dce63ce9`. The final offline advisory built/exported distinct baseline/candidate subjects, bound the baseline SBOM, and rejected the baseline at class `40` with `grype-policy-rejected` (14 critical matches; no exception). Raw scan material, redacted result, and DB identity remain only under the ignored task directory; the task-owned `/tmp` key directory was removed and no consumer verdict remains. Scorecard was explicitly skipped because this Task has not confirmed read-only network approval. CI/local/repository fixture gates and generated-summary freshness pass. |
| 2026-07-22 | Combined review remediation | Combined review findings `C3/I1/M1` were addressed without relaxing policy: config identity now comes from the exact scanned/signed OCI archive's verified index-to-manifest-to-config chain; both consumer verdict paths are invalidated before advisory work and published only as a completed pair from run-scoped outputs; every Grype match is evaluated; wrong-subject verification crosses roles; and Scorecard uses `github.com/buenhyden/hy-home.docker`. The rerun bound the baseline SBOM to archive config `sha256:6e7a5cc7b701219126e0442e5a49e3ba6a1b6cb79fe8c1a5c6ddc090ad77633d` and again stopped at the truthful baseline class `40` rejection. Review closure was then pending. |
| 2026-07-22 | Re-review C1 remediation | Two re-reviews identified that an accepted Grype result with a non-null exception ID could have been reduced to a null consumer exception and published downstream. New wrapper RED/GREEN coverage preserves the internal `vulnerability-verdict.json` exception ID, exits class `40` with `grype-exception-requires-manual-review`, and proves both fixed consumer verdict paths remain absent. |
| 2026-07-22 | Historical domain-review closure | The initial/combined review findings `C3/I1/M1` and first re-review C1 were remediated. Terminal specification and quality/security reviews both returned `APPROVED C0/I0/M0`. At that revision this closed the historical review unit only; the active Task and then-unsatisfied Task 5 accepted-pair prerequisite remained unchanged. |
| 2026-07-22 | Program closure advisory rerun (historical pre-hardening evidence) | The 27/27 suite and offline advisory class-40 `grype-policy-rejected` observation remain historical evidence for the pre-hardening committed state: 167 baseline matches included 14 Critical and 73 High, with no exception and no accepted pair. It is not the current runtime result and grants no exception. |
| 2026-07-22 | Whole-review hardening RED/GREEN ledger (historical, superseded) | RED `c8aa52b9` captured hardened supply-chain boundaries; GREEN `df1dd8c1` enforced offline immutable handoffs. RED `4de5c04d` reproduced protected cache cleanup failure; GREEN `ae354a00` moved that cleanup behind the gated runtime. RED `552e3867` captured private tool-temp and seed preflight; historical interim GREEN identity `f966266e129b11da198904b7076ca3c224f3e468` was superseded by final GREEN `e5a4d739`, which provided private tool temporary storage and the early seed gate. Its 39/39 result remains exact historical evidence. |
| 2026-07-22 | Immutable build-context RED/GREEN | RED `abc1dd21` captured mutable-context and mixed input-generation gaps. GREEN `c8342c09` records independent manifest and configuration image identities, constructs one deterministic mode-0600 `.dockerignore`-aware tar inside a mode-0700 private runtime, snapshots device/inode/size/mtime/ctime/mode/UID/hash metadata, passes that exact tar to Buildx over stdin, and immediately revalidates it after build. A mutate-and-restore attempt fails class 50 without publishing a pair. That committed state passed 44/44 with 13 fixtures plus Bash/static/Python/diff and preflight gates; the later portable suite supersedes only the focused count. |
| 2026-07-22 | Historical committed-tree advisory boundary (superseded) | At that revision, exactly one hardened advisory exited class `10` with `grype-db-seed-unavailable-advisory-blocked` before Docker because the one-time approved seed was absent and no reusable local database existed. No accepted baseline/candidate verdict, committed pair manifest, transient run verdict, signing key, private runtime tree, or tool container remained. The later Task 7 source-bound advisory below supersedes this prerequisite state. |
| 2026-07-23 | Historical terminal whole-branch review closure | Quality/security review v3 returned `APPROVED C0/I0/M0` for the full branch range through `20022458` plus the then-current 26-document reconciliation diff. Specification review v5 returned `APPROVED C0/I0/M0` for the full branch range through `20022458` plus the final 26-document reconciliation diff. Earlier `CHANGES REQUIRED` iterations remain historical remediation evidence. At that reviewed revision the database seed/policy pass/pair were still absent; later Task 7 evidence below supersedes only that runtime prerequisite state. |
| 2026-07-23 | Portable handoff RED/GREEN and review | RED `2ae6e883` required a cross-store local image handoff. GREEN `1937ec75` and consumer `a6c12e18` bind verdict schema v2, pair schema/generation v3, and rehearsal-record schema v4 to the full OCI/Docker/runtime tuple. Review remediation `d156aca8..b070a06c` added canonical-record preservation, gzip DiffID verification, bounded uncompressed OCI/USTAR/PAX parsing, and hidden-metadata rejection. At that portable-handoff checkpoint supply-chain tests passed 61/61, checker fixtures passed 13/13, and independent reviews were C0/I0/M0. |
| 2026-07-23 | Current Task 7 source-bound offline advisory | At source revision `b070a06ceac2f3e60fdb5bdb3fa87b4b0433545b`, preflight exited 0 with `supply_chain_preflight=pass` and advisory exited 0 with `supply_chain_verification=pass roles=baseline,candidate redaction=passed`. Grype seed `v6.1.9` was built `2026-07-22T07:06:24Z` from package SHA-256 `8496f58655ba6b5d1ed133e8591629d729a53021e7f1b20063b0577ca7c0f02f`; both roles had 0 Critical, 0 High, and 3 Medium, no exception, and `reason=outside-policy`. The mode-0600 pair is schema 3/generation `hyhome-verification-verdict-pair-v3`, size 1,806, SHA-256 `ac61c1763f1c14cc8d07b3e58421d1f7355bf22b47632da67f8aad061f6b1220`, and binds build context `sha256:1e2ff714895bb6352d101a6f0a7b5beb45dd9f414ade788d77a7d6e9df650034`. Docker inspection matched each pair-bound runtime ID and role label. Task-owned container inventory and `/tmp/hyhome-supply-chain.*` were empty and tracked worktree state was clean after the run. The former pair at `6803949d` with hash `729ca2e3…` is historical/superseded. Task 5 and the controlled wrapper were not run within this Task; the delivery Task later consumed the pair in its separately approved runtime sequence. |
| 2026-07-23 | Task 7 runtime-evidence review closure | Fresh independent specification and quality/security reviewers each approved exact range `b070a06ceac2f3e60fdb5bdb3fa87b4b0433545b..086744f8bd20370262ce297dd5b6dc101a5b54dc` at `C0/I0/M0`. At that review checkpoint, their safe, non-runtime evidence confirmed delivery 54/54, seed 8/8, checker 13/13, generated-summary freshness, ignored handoff mode/hash/full-tuple equality, Task 5 record absence, and clean diff hygiene. No Docker, advisory, Task 5, wrapper, or remote action ran during the review. The later Task 5 runtime is owned by the delivery Task and is outside this review range. |
| 2026-07-23 | Downstream Task 5 review/document closure | Fresh delivery specification and quality/security reviews each returned `APPROVED C0/I0/M0` with no findings for exact range `f3e4701115734e71f8848e706e9d37d499f0c2ac..a5c97e0a62bb71029c73e84f5dbe07b4c1dc0efe`. Specification checks passed delivery 54/54, metadata 6/0 plus one unchanged legacy exception, traceability 46/0, alignment 667/5,524/141/0, diff hygiene, and read-only canonical/upstream reconciliation. Quality/security checks passed delivery 54/54, fixture preflight at exit 0, Bash syntax, Python compilation, diff hygiene, and stat/hash/ignore/`jq`/tuple reconciliation. This supply-chain Task did not run Task 5 or the controlled wrapper. |
| 2026-07-26 | Final lifecycle review remediation (historical checkpoint) | The local digest-bound supply-chain boundary is complete and this Task transitions to `completed`; registry publication, remote trust, live Scorecard enforcement, credentials, release, and deployment remain deferred to a new Stage 01-04 chain. The initial final Program specification review returned `CHANGES REQUIRED C0/I2/M0` for stale generated owners and still-active lifecycle metadata; generated-owner remediation is `78265090`, and this lifecycle logical unit closes the status/index finding. The initial final quality review returned `CHANGES REQUIRED C0/I1/M0` because OCI config-digest inspection bypassed the bounded stable-private reader; RED `9a24b0cb` and GREEN `73f4ea68` close that helper boundary. At that checkpoint fresh final re-review had not approved the remediations; the later dual-ID and CI/governance row records the exact approved re-reviews. |
| 2026-07-26 | Final-review typed identity and seed reconciliation | RED `163f434b` proves that manifest/target/config identity must remain distinct and that private Docker-save config observations must fail closed. GREEN `e8934783` upgrades the tool registry to schema 3, binds repo digest, target descriptor, and independently hashed config JSON for every exact tool/material image, and reuses the bounded stable-private reader plus strict uncompressed-tar validation. At that correction checkpoint the focused supply-chain suite passed 65/65 and the Grype seed suite passed 9/9. Local read-only preflight validated all exact immutable tool/material tuples without pull, build, or network. The ignored seed was atomically republished as generation `a2eccd73475a39aea051be83b3fc1a51524c69e036e032a9a49704b5803fa7e4`; its 1,949,126,944 cache bytes, three files, tree SHA-256 `d4ddbc75da746cff08eb90e6ed998dd82a888dd242055114770bf2ed197aeb52`, database build/package identity, and seeded timestamp are unchanged, while its Grype tool record now contains distinct target and config digests. Read-only pair reconciliation confirms the existing mode-0600 schema-v3 pair SHA-256 `ac61c1763f1c14cc8d07b3e58421d1f7355bf22b47632da67f8aad061f6b1220`, both verdict hashes, and both full seven-field subject tuples remain exact. Independent private Docker-save config-body hashes match the pair's baseline/candidate config digests, and local runtime target IDs match the pair. No new advisory, build, pull, or network action ran. The pair remains current; the corrected downstream Task 5 successor and its scoped reviews later restored local closure. The dual-ID row supersedes only the focused counts and final review disposition. |
| 2026-07-26 | Dual-ID compatibility RED/GREEN and review closure | Initial whole-branch quality review at `0828857657611e570e2a654efff4b17ff95083ca` returned `CHANGES REQUIRED C0/I1/M0` because the supply-chain image predicate accepted `.Id` only as the target descriptor. RED `ffc1cf130e64db3d61d2de067239c7d720fa3ee5` added target-ID acceptance, config-ID acceptance, and unrelated-ID rejection; the config-ID case was the one intended supply-chain failure. GREEN `d186644e6243b0598e54303ee9bec5344516cb99` accepts `.Id` only when equal to the expected target or expected config while keeping RepoDigest, Descriptor/target, and independently hashed config-body gates separate and mandatory. The supply-chain suite passes 67/67 and the Grype seed suite passes 12/12; all four focused modules pass 176/176. Exact quality re-review of `0828857657611e570e2a654efff4b17ff95083ca..d186644e6243b0598e54303ee9bec5344516cb99` returned `APPROVED C0/I0/M0`, and exact specification re-review of `d186644e6243b0598e54303ee9bec5344516cb99..8a0bd6f440e884fec875f442c55906c0dec48edd` returned `APPROVED C0/I0/M0`. Existing pair and seed runtime evidence used `.Id=target`, remains a valid accepted form, and was not rerun or regenerated; no config-ID runtime or fresh advisory is claimed. Final post-evidence whole-branch confirmation remains pending. |

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

Current verification results: deterministic implementation, 67/67
focused/static checks, 12/12 Grype seed compatibility tests, preflight, and the
source-bound advisory pass. Task 7 supplied the
approved reusable database seed, official runtime-material remediation, the
Cosign v3 offline new-format bundle path, and the portable local-image
handoff. At source revision
`b070a06ceac2f3e60fdb5bdb3fa87b4b0433545b`, the exact concise evidence is:

- baseline verdict: mode `0600`, 1,086 bytes, SHA-256
  `057f301edbb1475a398c41d16272986580f754d149473263be6ca29b5728497b`;
  OCI manifest
  `sha256:bc16f11ed3205aa454e5a2c4c10edfbc8160b350deb3e5f84363bae8a1e8f693`,
  image config
  `sha256:c2717b5d74b5ee64bf6f8f44903976751134ad3d4b02fcbe53cdbf630cc100fc`,
  OCI archive
  `sha256:c2059fab70b0d3257c9735ecdb90673514360be6990b03451e8b7957ca5a76ed`,
  Docker archive
  `sha256:bc35eff9b998ec454c737cd33123d5d1dff116bf042b2678d5a040e6e534bcaa`,
  local reference
  `hyhome.local/sample-web-service:baseline-c2717b5d74b5ee64bf6f8f44903976751134ad3d4b02fcbe53cdbf630cc100fc`,
  and `docker-target-digest` runtime ID
  `sha256:8aa958c5ac49f9ce32be435005f95415b88256b101ba90390ef281d045254d98`;
- candidate verdict: mode `0600`, 1,088 bytes, SHA-256
  `89db847616e1533240edeb060f008c21406de5703cf49d09a7590839c3df27ce`;
  OCI manifest
  `sha256:77e785a1e1e89692b24d4b7f718899c426c7badbe0a53078ec63f1af09f99ab3`,
  image config
  `sha256:18a325c1cf27cdbacef105ee3ff64386bab17d9418a5a7fe16fdc9ac6fe5311b`,
  OCI archive
  `sha256:f1c9bb534c8bfa9f7538de2f87e99310c827ace4bea17ea6ebd275e522091fdf`,
  Docker archive
  `sha256:b4461cdd5637319990ee2bcc7d08c242ef17ef0965a3b4e4f757119e347f84eb`,
  local reference
  `hyhome.local/sample-web-service:candidate-18a325c1cf27cdbacef105ee3ff64386bab17d9418a5a7fe16fdc9ac6fe5311b`,
  and `docker-target-digest` runtime ID
  `sha256:043375a625567b772bd805a1a3138b69d8ddf2b3a8e1354767d8ad2430ef4355`;
- pair manifest: mode `0600`, 1,806 bytes, schema 3/generation
  `hyhome-verification-verdict-pair-v3`, SHA-256
  `ac61c1763f1c14cc8d07b3e58421d1f7355bf22b47632da67f8aad061f6b1220`,
  and build-context SHA-256
  `sha256:1e2ff714895bb6352d101a6f0a7b5beb45dd9f414ade788d77a7d6e9df650034`.

The current Cosign v3.0.6 path signs with the tracked no-service signing
configuration and tracked minimal offline trusted root, then verifies the
new-format bundle with `--insecure-ignore-tlog=true`; it does not use the
historical detached-signature compatibility path. The former accepted pair at
`6803949d92b5daeb522b328b098c5b357abbf4d6` with hash
`729ca2e33482d08939a68446761cf0964c6f91b07e2c1b5c5b263cf52e1bedab`,
the class-40 14-Critical/73-High/no-exception policy rejection, and the class-10
missing-seed result remain historical/superseded evidence only. Task 5 later
consumed the current pair in its separately approved positive-then-injected-
rollback sequence; this supply-chain Task did not execute or review that
runtime. Exit classes are `0=pass/accepted`,
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

The corrected Grype seed publication passes `--check-current` and
`--resolve-current`; its pointer and generation identity bytes are identical,
mode `0600`, and SHA-256
`da0c3e31d3dd7183acec4d5ce7955601bdf268f1e2615797d02c0ea031fb4334`.
The existing accepted pair was not regenerated: read-only pair/verdict/hash,
runtime-target, and independent config-body reconciliation proved that its
typed subject identities are unchanged. No fresh advisory result is inferred
from preflight.

Task 6 documentation, owner regeneration, safe gates, and whole-branch
re-review are recorded by the Program Task. The database-seed, policy-pass,
and accepted-pair prerequisites are now satisfied by the Task 7 evidence
above. Task 5's prior positive promotion and injected rollback plus their
reviews remain historical evidence for the old readiness/recovery hashes. The
corrected successor later completed exactly one actual positive exit `0` and
one injected negative exit `30`, published the current mode-0600 record with
SHA-256
`f2625d260494e1eb6c16af75ebcf287f3deebc0fd034210df62f24d712d08082`,
and received approved scoped reviews.
The Program-owned controlled all-files wrapper
passed on 2026-07-26 from clean checkpoint
`263e046f64f249b0e771e4f0c5d77a91c967e10f`, with hook exit 0, snapshot pass,
zero observed path counts, and all four path sets empty. That PASS covers only
the exact checkpoint. Later code commits `9a24b0cb`/`73f4ea68`, generated-owner
commit `78265090`, and this lifecycle logical unit were not covered; they use
targeted gates and exact re-reviews. The later quality re-review of
`08288576..d186644e` and specification re-review of
`d186644e..8a0bd6f4` are both `APPROVED C0/I0/M0`. The wrapper is not rerun
because its contract is exact-once.

## Controlled Agent Pre-commit Evidence

Controlled wrapper command: not owned by this domain Task. The Program Task
owned the sole exact-once all-files invocation.

Allowed prefixes: `not_applicable` at domain activation.

Program wrapper result: `hook_result=passed hook_exit=0`;
`snapshot_result=passed`.

Observed counts were
`before_count=0 after_count=0 changed_count=0 unexpected_count=0`; all four
Git-visible non-ignored path sets were `(none)`.

Observation boundary:
`observation=git-visible-non-ignored-repository-status`.

Disposition: Program-owned wrapper **PASS** only for exact clean checkpoint
`263e046f64f249b0e771e4f0c5d77a91c967e10f`; see the
[program Task](./2026-07-19-operational-readiness-closure-program.md) for the
full command and exact allowed prefixes. Post-wrapper code, generated-owner,
and lifecycle commits use targeted gates plus exact re-review. The wrapper is
not rerun under its exact-once contract, and direct
`pre-commit run --all-files` remains prohibited.

## Review Evidence

Implementation review verdict: deterministic policy, preflight, fixture-only
wiring, summary freshness, protected-cache handling, private temporary paths,
the seed gate, portable OCI-to-Docker handoff, and current accepted pair are
implemented. The portable-handoff reviews returned `C0/I0/M0`. Fresh full
Task 7 runtime-evidence reviews of exact range
`b070a06ceac2f3e60fdb5bdb3fa87b4b0433545b..086744f8bd20370262ce297dd5b6dc101a5b54dc`
also returned `APPROVED C0/I0/M0` for both review dimensions.

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
through `20022458` plus the final 26-document reconciliation diff; fresh Task 7
runtime-evidence review `APPROVED C0/I0/M0` for exact range
`b070a06ceac2f3e60fdb5bdb3fa87b4b0433545b..086744f8bd20370262ce297dd5b6dc101a5b54dc`.

Quality/security review verdict: historical domain review `APPROVED C0/I0/M0`;
terminal quality/security review v3 `APPROVED C0/I0/M0` for the full branch
range through `20022458` plus the then-current 26-document reconciliation diff;
fresh Task 7 runtime-evidence review `APPROVED C0/I0/M0` for the same exact
`b070a06c..086744f8` range.

Findings and disposition: the initial/combined `C3/I1/M1` findings and the
first re-review C1 are remediated and closed. Later portable-handoff review is
also `C0/I0/M0`. The full Task 7 runtime-evidence reviews are now closed at
`C0/I0/M0` with no open finding. Those reviews do not cover the later Task 5
positive promotion and injected rollback; their execution evidence is recorded
by the delivery Task. Separate fresh Task 5 specification and quality/security
reviews of exact range
`f3e4701115734e71f8848e706e9d37d499f0c2ac..a5c97e0a62bb71029c73e84f5dbe07b4c1dc0efe`
are both `APPROVED C0/I0/M0` with no findings.
Earlier `CHANGES REQUIRED` iterations remain historical remediation evidence.

The initial final Program specification review after the controlled-wrapper
checkpoint returned `CHANGES REQUIRED C0/I2/M0`: generated navigation owners
were stale, and the 15 local-isolated lifecycle documents still reported
`active`. Commit `78265090` refreshed the generated owners; this lifecycle
logical unit transitions the exact 15 Specs, Plans, and Tasks and synchronizes
their indexes. The initial final quality review returned
`CHANGES REQUIRED C0/I1/M0` because OCI config-digest inspection used an
unbounded, symlink-following read. RED `9a24b0cb` and GREEN `73f4ea68` route it
through the bounded stable-private reader. This paragraph preserves that
historical checkpoint. The later initial post-closure review at `08288576`
returned specification `CHANGES REQUIRED C0/I1/M1` and quality
`CHANGES REQUIRED C0/I1/M0`; dual-ID RED/GREEN
`ffc1cf13`/`d186644e` and CI/governance correction `8a0bd6f4` close them.
Exact quality re-review `08288576..d186644e` and exact specification re-review
`d186644e..8a0bd6f4` are both `APPROVED C0/I0/M0`.

## Commit Ledger

Historical implementation identity:
`72e584f51badfd194c0a1b6d32510a3bf3ab395c`. Earlier remediation ledger:
`c8aa52b9`, `df1dd8c1`, `4de5c04d`, `ae354a00`, `552e3867`, historical
interim `f966266e129b11da198904b7076ca3c224f3e468`, and `e5a4d739`.
Current immutable-input hardening is RED `abc1dd21` followed by GREEN
`c8342c09`. Portable-handoff and runtime-hardening history is RED `2ae6e883`,
producer GREEN `1937ec75`, consumer GREEN `a6c12e18`, and remediation
`d156aca8`, `b192c0db`, `8bb94ded`, `e70008f3`, `df0fd186`, `664babbc`, and
`b070a06c`.
The separate evidence update does not embed its own SHA.
Post-wrapper remediation identities are OCI reader RED/GREEN
`9a24b0cb`/`73f4ea68`, generated-owner refresh `78265090`, this lifecycle
logical unit, dual-ID RED/GREEN `ffc1cf13`/`d186644e`, and CI/governance
correction `8a0bd6f4`. They are validated by targeted gates and exact approved
re-reviews, not by the exact-once wrapper.
Evidence reconciliation then found that the CI routing test was absent from the
Foundation manifest's `github-governance.md` consumers. Commit
`e46a0e5a4356b8439cefdc26ed6a5fa23fd0f2d9` adds that exact consumer only;
the Foundation summary remains byte-identical. Fresh manifest/summary checks
pass, impacted lifecycle passes 159/0 with only the expected Task-directory
warning, and promoted lifecycle passes at zero.

Logical unit: `feat(security): add local supply-chain verification`.

Commit validation: the current 67/67 focused fixture/wrapper tests, 12/12
Grype seed compatibility tests, 13/13 deterministic checker fixtures, static
checks, preflight, fixture-only, summary freshness, immutable-context
revalidation, and source-bound accepted advisory are recorded above.
Historical terminal reviews are `APPROVED C0/I0/M0` for
their exact reviewed commits; portable-handoff reviews are `C0/I0/M0`; and the
fresh full Task 7 specification and quality/security reviews of
`b070a06c..086744f8` are both `APPROVED C0/I0/M0`.

## Deferred and Blocked Items

Deferred items: registry push, remote attestation, keyless/OIDC, transparency
log, publication, live Scorecard blocking, GitHub Release, deployment, and SLSA
level claims.

Blocked items: the approved offline Grype seed, policy pass, and accepted
distinct same-revision verdict pair remain complete and current. Task 5's prior
delivery runtime and reviews are historical for the superseded readiness and
recovery hashes; the corrected successor's `0/30` rehearsal and scoped reviews
restored downstream local closure.
`--scorecard-advisory` remains skipped until read-only network scope is
confirmed. The Program-owned controlled all-files wrapper passed on 2026-07-26
only for checkpoint `263e046f`; this Task is completed at the approved local
boundary. Exact implementation re-reviews through `8a0bd6f4` are approved;
final post-evidence whole-branch confirmation remains pending.

Deferral destination: remote identity, publication, enforcement, registry,
credential, live, release, or deployment work needs a new approved Stage 01-04
chain and explicit human approval; local accepted verdicts are consumed only by
[Spec 127](../../98.archive/03.specs/127-deployment-release-engineering-remediation/spec.md).

## Related Documents

- [Spec 126](../../98.archive/03.specs/126-security-supply-chain-remediation/spec.md)
- [Supply-chain Plan](../plans/2026-07-11-security-supply-chain-remediation.md)
- [Program Task](./2026-07-19-operational-readiness-closure-program.md)
- [Approved-network runtime closure Task](./2026-07-23-security-supply-chain-runtime-closure.md)
- [Delivery Task](./2026-07-19-deployment-release-engineering-remediation.md)
- [Security audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md)
