---
status: active
artifact_id: task:2026-07-23-security-supply-chain-runtime-closure
artifact_type: task
parent_ids:
  - spec:126-security-supply-chain-remediation
  - plan:2026-07-11-security-supply-chain-remediation
---

# Task: Security Supply-Chain Runtime Closure

## Overview

This Task owns the separately approved, read-only network step required to
seed a current Grype vulnerability database and close the local runtime portion
of Spec 126. It extends the existing supply-chain Task without weakening its
offline advisory, no-exception policy, immutable subject binding, or atomic
accepted-pair contract.

The Task may retrieve only a Grype database through the exact pinned Grype
image and, if a policy rejection proves remediation necessary, inspect and pull
only official sample-service base images before committing their exact immutable
digests. It does not authorize Task 5 execution, registry push, signing
publication, release, deployment, credentials, remote repository mutation, or
the controlled all-files wrapper.

## Inputs

- [Spec 126](../../03.specs/126-security-supply-chain-remediation/spec.md)
- [Security supply-chain Plan](../plans/2026-07-11-security-supply-chain-remediation.md)
- [Existing supply-chain Task](./2026-07-19-security-supply-chain-remediation.md)
- [Operational-readiness Program Task](./2026-07-19-operational-readiness-closure-program.md)
- `infra/supply-chain.tool-images.json`
- `infra/supply-chain.sample-service-policy.json`
- `examples/sample-web-service/`

## Goals and Non-goals

Goals:

- replace the historical manual database handoff with a reproducible,
  task-bound seed harness;
- retrieve through the exact pinned Grype image with application update checks
  disabled and a bounded database-update command;
- publish a private mode-0700 cache generation and an atomic mode-0600
  minimized identity handoff containing exact tool, schema, build time, package
  checksum, and cache-tree identity;
- preserve the last valid generation and pointer when retrieval, validation, or
  publication fails;
- run the unchanged offline `--advisory` consumer and obtain two distinct,
  same-revision, no-exception accepted verdicts plus the schema-v2 pair manifest;
- remediate only sample-service image materials if the current policy rejects.

Non-goals:

- changing the vulnerability threshold or creating an exception;
- making `--advisory` download data or use a network;
- executing delivery promotion/rollback, the controlled all-files wrapper, a
  remote workflow, a release, or a deployment;
- registry push, attestation publication, OIDC/keyless signing, credentials, or
  shared/production runtime mutation;
- retaining raw scanner/database logs in tracked or handoff surfaces.

## Scope and Change Boundaries

Allowed authored paths:

- this Task, `docs/04.execution/tasks/README.md`, the existing supply-chain
  Task, the Program Task, and the bounded progress entry;
- `scripts/security/seed-grype-db-cache.sh`, its dedicated validation helper and
  tests, and the existing supply-chain wrapper/checker/tests;
- the exact Spec 126 policy/tool registry, generated supply-chain summary, and
  sample-service Dockerfile/source documentation when directly required by a
  current policy rejection;
- directly affected lifecycle/generated owners only after their canonical
  generators identify them.

Allowed transient paths are exactly `/tmp/hyhome-grype-db-seed.*`,
`/tmp/hyhome-supply-chain.*`, and
`_workspace/repo-support/task-2026-07-23-security-supply-chain-runtime-closure/`.
The accepted pair remains owned by the existing supply-chain Task under its
existing ignored output directory.

Forbidden paths and actions include Task 5 implementation/runtime, production
or shared services, credentials, registry push, publication, GitHub mutation,
remote dispatch, release, deployment, broad Docker cleanup, and direct or
wrapped all-files pre-commit execution.

Compose impact: none. Local Docker runs, image inspection/pull, Buildx export,
and task-owned cleanup only.

Security impact: one bounded read-only database retrieval and, only after an
observed rejection, read-only official image metadata/pull. Every durable
consumer remains offline and fail-closed.

Operations impact: ignored private local evidence only; no shared service or
operator state.

Runtime impact: task-owned Docker containers/images and local OCI archives.
No container may remain after each command and no named network or volume may
be created.

## Approval Evidence

Approval source: on 2026-07-23 KST the user explicitly approved the proposed
follow-up after the Program reported the missing Grype seed and accepted-pair
blocker. The parent implementation brief narrows that approval to read-only
retrieval of the pinned Grype database and official base images genuinely
required for policy remediation.

Protected surfaces: the Grype network boundary, official image registry reads,
sample-service digest pins, ignored database cache, and accepted verdict pair
are approved only within this Task. Task 5, CI enforcement, the controlled
wrapper, publication, remote repository state, credentials, Releases, and
deployments remain protected and unapproved here.

Approval boundary:

- Grype identity is exactly
  `anchore/grype:v0.116.0@sha256:fd4ab4d1042b522c896e73bdf09ab8bf384fa417df99d6dd0d6e1008c7e7c821`;
- the only networked Grype operation is its native `db update`, with
  `GRYPE_CHECK_FOR_APP_UPDATE=false`, a private cache mount, and no source or
  artifact input;
- allowed database traffic is the Grype-configured Anchore database endpoint;
- official image discovery is limited to `library/alpine` and
  `nginxinc/nginx-unprivileged`; a chosen image is pulled only by exact digest
  and committed only as `repository:version@sha256:...`;
- allowed command classes are exact local tests/checks, `docker image inspect`,
  pinned `docker run`, read-only `docker buildx imagetools inspect`, and
  exact-digest `docker pull` for the two approved repositories;
- no exception, mutable committed tag, registry write, or remote mutation is
  allowed.

Grype DB network approval: confirmed

Rollback or recovery: a failed seed must leave the prior atomic current pointer
and generation untouched. A successful but unused new generation may be
removed only by its exact task-owned identity. Code/material remediation rolls
back by reverting its logical commit; no Docker prune, shared cleanup, remote
deletion, or artifact revocation is applicable.

Redaction boundary: tracked evidence may contain public image references,
digests, Grype database schema/build/status/package checksum, cache-tree
checksum/counts, source revision, vulnerability severity counts, concise
verdicts, handoff hashes/modes, cleanup, and review results. Raw database or
scanner logs, raw findings, SBOM bodies, provenance bodies, signature bundles,
keys, tokens, credentials, response bodies, and shell history are prohibited.

## Work Breakdown

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `T-SSC-006` | Activate the exact network, identity, output, rollback, and redaction contract | Governance | Spec 126 approval gates | Plan approval gates | Metadata, lifecycle, Markdown, and diff gates | Fresh implementation agent | Complete |
| `T-SSC-007` | TDD the dedicated database seed and atomic private handoff | Implementation | `SSC-001` | `T-SSC-002` | Focused RED/GREEN tests, static checks, failed-seed preservation | Fresh implementation agent | Complete |
| `T-SSC-008` | Seed the current database and execute the hardened offline advisory | Runtime | `SSC-001`–`SSC-004` | `T-SSC-002`–`T-SSC-003` | Exact DB identity, policy verdicts, pair manifest, cleanup inventory | Fresh implementation agent | In progress; current seed and first rejected advisory recorded, committed-head rerun pending |
| `T-SSC-009` | Remediate only rejected sample-service materials when necessary | Implementation | `SSC-001`–`SSC-004` | `T-SSC-002` | Digest/source TDD and repeated offline advisory | Fresh implementation agent | In progress; exact runtime pin and isolated policy pass implemented, committed-head rerun pending |
| `T-SSC-010` | Independent specification and quality/security review | Review | `VAL-SSC-001`–`VAL-SSC-004` | `T-SSC-005` | Separate C0/I0/M0 reviews and remediation ledger | Separate reviewers | Pending |

## Work Log

| Date | Work unit | Result |
| --- | --- | --- |
| 2026-07-23 | `T-SSC-006` discovery | Confirmed the current hardened advisory blocks before Docker when no approved seed exists. The historical seed identity is evidence-only; there is no committed reproducible seed harness. No network, Docker runtime, image pull, Task 5, wrapper, or remote action ran during discovery. |
| 2026-07-23 | `T-SSC-007` seed harness | RED reproduced the absent bounded seed interface. GREEN added a two-mode pinned-Grype harness, validated immutable mode-0700 generations, mode-0600 atomic pointer publication, exact cache-tree identity, and failed-seed preservation. The current focused seed suite passes 8/8. |
| 2026-07-23 | `T-SSC-008` seed and first advisory | The one approved pinned-Grype update published schema `v6.1.9`, database build `2026-07-22T07:06:24Z`, package SHA-256 `8496f58655ba6b5d1ed133e8591629d729a53021e7f1b20063b0577ca7c0f02f`, and cache-tree SHA-256 `d4ddbc75da746cff08eb90e6ed998dd82a888dd242055114770bf2ed197aeb52`. The first hardened offline advisory then rejected the baseline at class 40 with 14 Critical, 73 High, 69 Medium, and 11 Low findings, no exception, and no candidate or pair publication. |
| 2026-07-23 | `T-SSC-009` official runtime remediation | Read-only official registry inspection selected the versioned slim multi-architecture index `nginxinc/nginx-unprivileged:1.31.3-alpine3.24-slim@sha256:90d82b3358df5758b3c57d20f2565082ce6f744906e7dc09afd0096c1b8eb2b5`; linux/amd64 child is `sha256:bc38ccd3a649cce1062519734e1ad088bf0cc20d6cb5f2f3645f64466ab27c57`. One exact-digest pull resolved local RepoDigest and config ID to the approved index digest. A no-pull, network-none isolated build plus pinned Syft/Grype scan against the validated seed returned 0 Critical, 0 High, 3 Medium, 0 Low, and policy accepted. It did not publish advisory summaries or an accepted pair. The optional Alpine candidate was inspected but neither pulled nor changed. |
| 2026-07-23 | Material source gates | Combined focused tests pass 54/54 and policy fixtures pass 13/13. Python compilation, Ruff, Bash syntax, ShellCheck, generated supply-chain summary freshness, seed preflight, exact-image preflight, fixture-only policy, Markdownlint, Hadolint, metadata 5/0, traceability 46/0, alignment 667 documents and 5,519 links with zero failures, Foundation manifest/summary/promoted checks, and impacted lifecycle pass. A mistakenly attempted nonexistent `check-task-template-compliance.py` command exited 2 without changing repository state; the canonical metadata contract checker passed instead. Advisory `shfmt -d` reported existing whole-wrapper formatting outside the three changed identity constants, so no unrelated reformat was applied; Bash syntax and ShellCheck remain clean. Task7's direct README-consumer drift was corrected separately through the canonical Foundation scan in commit `c7ebb9b2`; generated owners were refreshed in `8481df02`; the seed script inventory was reconciled in `96464337`. The final dependency-locked aggregate used `scripts/requirements.txt`, passed every section with `failures=0`, and reported only the configured task-directory budget warning. |
| 2026-07-23 | Cosign v3 offline signing correction | The first post-material advisory reached signature verification and failed class `60` because Cosign v3.0.6 no longer supports the historical `--tlog-upload=false` flow. Pinned local `sign-blob`, `verify-blob`, and `signing-config create` help plus a one-blob smoke established the current offline path: a tracked signing config with no Rekor service, `sign-blob --signing-config ... --new-bundle-format=false --bundle ...`, extraction of `messageSignature.signature`, and `verify-blob --insecure-ignore-tlog=true --signature ...`. The focused Cosign regressions pass 3/3, the full supply-chain suite passes 49/49, the checker passes 13 fixtures, Bash syntax/Python compile/diff hygiene pass, and the independent one-blob smoke verifies the original blob while rejecting tamper. The full advisory, accepted-pair publication, Task 5 runtime, and controlled all-files wrapper were not rerun in this correction. |
| 2026-07-23 | Current full offline advisory pass | After commit `6803949d92b5daeb522b328b098c5b357abbf4d6`, preflight passed and the full offline advisory completed with `supply_chain_verification=pass roles=baseline,candidate redaction=passed`. The current Grype seed is schema `v6.1.9`, built `2026-07-22T07:06:24Z`, package SHA-256 `8496f58655ba6b5d1ed133e8591629d729a53021e7f1b20063b0577ca7c0f02f`. Baseline and candidate each report 0 Critical, 0 High, 3 Medium, no exception, and `reason=outside-policy`. The accepted pair manifest is mode `0600`, size 432, SHA-256 `729ca2e33482d08939a68446761cf0964c6f91b07e2c1b5c5b263cf52e1bedab`, and references baseline verdict SHA-256 `2a87a841696451418e53af76d16a33f3fa64412ea0317a419a6a492ac2ff7f06` plus candidate verdict SHA-256 `e6847fb4ea501cb8e3ea44ed7a5497bdcbead5744ed990a506448b6abdc15a89`. Baseline config/archive are `sha256:c2717b5d74b5ee64bf6f8f44903976751134ad3d4b02fcbe53cdbf630cc100fc` and `sha256:a6aaead1f2ca2d42cb6bf9b7eacb23dc0d510b9357e7e1cced50c2cee1985feb`; candidate config/archive are `sha256:18a325c1cf27cdbacef105ee3ff64386bab17d9418a5a7fe16fdc9ac6fe5311b` and `sha256:33e6b2e24ad87791fa4961a0070e32624c253381dffd9cfc591afa395a6b6e00`. Build context SHA-256 is `sha256:1e2ff714895bb6352d101a6f0a7b5beb45dd9f414ade788d77a7d6e9df650034`. Direct container inventory and `/tmp/hyhome-supply-chain.*` inventory were empty afterward. Task 5 runtime and the controlled all-files wrapper were not run. |

## Verification Evidence

Planned exact local gates:

```bash
python3 -m unittest tests.validation.test_grype_db_seed -v
python3 -m unittest tests.validation.test_supply_chain_policy -v
python3 scripts/validation/check-supply-chain-policy.py --check
bash scripts/security/seed-grype-db-cache.sh --preflight
bash scripts/security/verify-sample-service-supply-chain.sh --preflight
bash scripts/security/verify-sample-service-supply-chain.sh --fixture-only
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 5f26b0048d450318b7dc6dbe6a6d9484a3e3f1b8
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
git diff --check
```

The approved networked commands are invoked only after the seed harness tests
and preflight pass. Actual commands, exits, public identities, minimized
checksums, verdicts, and cleanup results will be appended without raw logs.

Current result: seed implementation and publication are complete. The first
current advisory truthfully rejected the stale runtime baseline. The exact
official runtime remediation passes its isolated no-pull policy gate at 0
Critical and 0 High. The Cosign v3.0.6 offline signing incompatibility is
corrected, and the current committed-head full advisory now publishes an
accepted schema-v2 pair for baseline and candidate with no exception and
redaction passed. Independent reviews remain `pending`; Task 5 runtime and the
controlled all-files wrapper remain `not_run` in this Task.

## Controlled Agent Pre-commit Evidence

Controlled wrapper command, allowed prefixes, exit status, snapshots, observed
path sets, and disposition: `not_applicable`. Task 6 remains the sole owner and
the wrapper is explicitly forbidden in this Task.

## Review Evidence

Implementation review verdict: `pending`.

Specification review verdict: `pending`.

Quality/security review verdict: `pending`.

Findings and disposition: none yet. Historical Task 3 reviews do not approve
this new network seed implementation or runtime evidence.

## Commit Ledger

Commit identity: `pending`.

Logical units: Task contract; TDD RED; seed GREEN; conditional sample-material
remediation; runtime/review evidence.

Validation: recorded per logical unit after exact execution.

## Deferred and Blocked Items

Deferred items: Task 5 positive/rollback runtime and the controlled all-files
wrapper remain owned by later separately bounded work.

Blocked items: no current Task-local blocker before the approved seed attempt.
If the official database or approved official image set cannot produce a
no-exception policy pass, stop with the exact irreducible public identity and
redacted counts; do not relax policy or create an exception.

Deferral destination: the existing Program Task owns Task 5 and final wrapper
sequencing after this Task reaches independent C0/I0/M0 review.

## Related Documents

- [Spec 126](../../03.specs/126-security-supply-chain-remediation/spec.md)
- [Security supply-chain Plan](../plans/2026-07-11-security-supply-chain-remediation.md)
- [Existing supply-chain Task](./2026-07-19-security-supply-chain-remediation.md)
- [Operational-readiness Program Task](./2026-07-19-operational-readiness-closure-program.md)
- [Task index](./README.md)
