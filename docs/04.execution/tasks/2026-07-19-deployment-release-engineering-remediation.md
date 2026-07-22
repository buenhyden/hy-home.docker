---
status: active
artifact_id: task:2026-07-19-deployment-release-engineering-remediation
artifact_type: task
parent_ids:
  - spec:127-deployment-release-engineering-remediation
  - plan:2026-07-11-deployment-release-engineering-remediation
---

# Task: Deployment and Release Engineering Remediation

## Overview

This active Task records the completed local pair-bound baseline/canary
promotion and previous-runtime-image-ID rollback rehearsal for
`examples/sample-web-service`. The approved sequence ran exactly once in each
mode: a positive promotion followed by an injected canary-health failure and
verified rollback. No GitHub Release, registry publication, remote deployment,
or remote environment was created.

Fresh independent specification and quality/security reviews of the Task 5
runtime evidence are both `APPROVED C0/I0/M0` with no findings. This Task stays
active until the Program-owned controlled wrapper and lifecycle closure are
complete; the wrapper remains `not_run`.

The Task owns the concise
`_workspace/repo-support/task-2026-07-19-deployment-release-engineering-remediation/delivery/rehearsal-record.json`
output. It consumes typed verdicts from Specs 124-126 without copying their raw
evidence, and requires the Spec 126 pair manifest to bind both verdict byte
identities to one source revision, build context, and producer generation.

## Inputs

- [Spec 127](../../03.specs/127-deployment-release-engineering-remediation/spec.md)
- [Deployment/release Plan](../plans/2026-07-11-deployment-release-engineering-remediation.md)
- [Program Plan](../plans/2026-07-19-operational-readiness-closure-program.md)
- Accepted baseline/candidate Spec 126 verification verdicts
- Passing Spec 124 readiness verdict and the Spec 125 recovery boundary
- `examples/sample-web-service/docker-compose.yml`

## Goals and Non-goals

Goals:

- make the sample Compose service project-scopable without changing its
  hardening, health, resource, logging, or network semantics;
- reject missing, rejected, mismatched, mutable, equal-subject, or
  wrong-revision supply-chain inputs;
- start separate baseline/canary projects and require container plus HTTP marker
  health before local promotion;
- record a typed local rehearsal decision and prove rollback to the previous
  pair-bound runtime image ID after bounded canary failure;
- verify post-rollback health and owned cleanup with `data_impact=none`.

Non-goals:

- GitHub Environment/Release, workflow or ruleset mutation, registry push,
  remote deployment, credentials, OIDC, or production target;
- a real release event, production-readiness claim, or mutable-tag promotion;
- data rollback; any stateful impact stops and routes to Spec 125.

## Scope and Change Boundaries

Allowed authored paths:

- `scripts/operations/rehearse-sample-service-delivery.sh`;
- `tests/fixtures/sample-service-delivery/**`;
- `tests/validation/test_sample_service_delivery_rehearsal.py`;
- `examples/sample-web-service/docker-compose.yml`, `README.md`, and
  `service.md` only as declared by the Plan;
- the narrow release-management runbook handoff;
- this Task and directly supported lifecycle/index evidence during closure.

Allowed transient path: only
`_workspace/repo-support/task-2026-07-19-deployment-release-engineering-remediation/`.

Forbidden paths/actions: remote workflows/environments/releases, registry
publication, remote image references, mutable tags, credentials, production
targets, unscoped cleanup, data migration/recovery, and release claims.

Compose impact: remove only the sample Compose top-level `name` and service
`container_name`; use task/role labels, verified local image identities, and
separate task-owned projects. Baseline/canary loopback ports are `18080` and
`18081`; collision fails preflight.

Security impact: promotion fails closed unless both Spec 126 verdicts are
accepted, distinct, same-revision, no-exception, and redaction-passed. No
credential or remote identity exists.

Operations impact: a local application/config rollback rehearsal and narrow
runbook handoff only. Stateful data recovery remains Spec 125-owned.

Runtime impact: local projects use names derived from
`hyhome-dre-20260719-<decimal-pid>-baseline|canary`. Cleanup removes only both
owned projects matching
`^hyhome-dre-20260719-[0-9]+-(baseline|canary)$` and task artifacts.

## Approval Evidence

Approval source:

- The user approved protected-surface changes and local promotion/rollback
  implementation within the operational-readiness program.
- [ADR 0028](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md),
  [Spec 127](../../03.specs/127-deployment-release-engineering-remediation/spec.md),
  and the active Plan define the exact local rehearsal contract.

Protected surfaces: the sample Compose identity, local verified image
selection, task-owned baseline/canary projects, high loopback ports, bounded
failure injection, wrapper/tests, and runbook handoff may change within the
Plan. GitHub, registry, remote deployment, credentials, Releases, production,
and data state remain protected.

Approval boundary: wrapper subcommands are only the exact `preflight`,
`rehearse`, and `cleanup` forms in the Plan. `--task-id` matches
`^[a-z0-9-]+$`; `--failure-mode` is only `none` or
`canary-health-timeout`. Input verdict paths, projects, ports, health marker,
rollback runtime image ID, and cleanup must resolve before startup. Preflight
and cleanup accept only the exact baseline/canary pair matching
`^hyhome-dre-20260719-[0-9]+-(baseline|canary)$`; any missing, additional, or
nonmatching project fails closed. Any remote or stateful surface requires stop
and new approval.

Rollback or recovery: on failed canary health, prohibit promotion, stop the
canary, restore/verify the baseline previous runtime image ID and HTTP health,
then clean both owned projects. Revert the single DRE commit to remove authored changes.
Ambiguous data impact stops and hands off to Spec 125 without deletion.

Redaction boundary: tracked evidence may contain source revision, digest and
verdict references, project names, marker presence, decisions, data impact,
cleanup, commit, and reviews. Raw HTTP bodies, logs, image contents, keys,
tokens, credentials, environment values, and upstream raw evidence remain
untracked.

## Work Breakdown

| Task ID | Description | Parent requirement | Validation / evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| `T-DRE-001` | Typed verdict/record fixtures, gates, CLI, and tests | `DRE-001`–`DRE-004` | Focused RED/GREEN and preflight | Fresh implementation agent | Complete; current focused suite 54/54 and fixture-only preflight pass |
| `T-DRE-002` | Project-scopable service and baseline/canary health | `DRE-001`, `DRE-003` | Separate projects and two-part health | Fresh implementation agent | Complete; one positive and one injected-negative runtime executed with exact owned cleanup |
| `T-DRE-003` | Promotion record, failure injection, rollback, cleanup | `DRE-002`, `DRE-004` | Positive and expected-failure rehearsal | Fresh implementation agent | Complete; positive promoted and negative rolled back to the healthy baseline with canonical replacement proof |
| `T-DRE-004` | Runbook handoff and independent reviews | `VAL-DRE-001`–`004` | Spec plus release/security C0/I0/M0 | Separate reviewers | Complete; runbook/runtime evidence reconciled and both exact-range reviews are `APPROVED C0/I0/M0` with no findings |

## Work Log

| Date | Work unit | Result |
| --- | --- | --- |
| 2026-07-19 | Task activation | Contract recorded; no build, project, promotion, rollback, release, or remote action executed. |
| 2026-07-19 | `T-DRE-001`–`T-DRE-004` | Initially `not_run`; append actual evidence only after upstream verdicts and exact execution. |
| 2026-07-22 | `T-DRE-001` focused implementation | Existing 21-test RED was 22 failures and 3 errors with only the fixture-schema method passing. The first wrapper reduced this to 1 failure, then passed 21/21. Expanded contract RED was 8 failures in 26 tests and GREEN was 26/26. Four state-machine guarantees were RED across 3 unittest failures, then GREEN reached 27/27; the final service/network label cardinality guard brought the suite to 28/28. |
| 2026-07-22 | Historical `T-DRE-002`–`T-DRE-004` implementation boundary | Removed only fixed Compose `name`/`container_name`; added exact digest, gate, project, port, label, health-marker, promotion, rollback, cleanup, record, timeout, and runbook contracts. Fixture-only preflight passed without Docker. At that revision the real command stopped at class 10 because the accepted Spec 126 pair was absent; no project or record was created. Later accepted-pair and runtime rows supersede that prerequisite state. |
| 2026-07-22 | Historical independent-review remediation | Specification returned C0/I2/M0 and release/security returned C1/I2/M0, deduplicated to four findings. The isolated canonical-mutation scan was RED 1/1; expanded RED was 38 tests with 13 failures and 0 errors. GREEN reached 38/38 after exact local image-object validation and pull/build denial, interpolation-free ID cleanup, fail-closed missing-pair cleanup, immutable real-canonical snapshots, and stable no-follow directory-FD publication. No project or accepted canonical was created at that checkpoint; terminal re-reviews were then pending. |
| 2026-07-22 | Historical terminal independent review closure | Terminal specification and release/security reviews both returned APPROVED C0/I0/M0 for historical implementation commit `b5441c53`. At that checkpoint fail-closed implementation/static/fixture proof was complete while positive/negative runtime remained `blocked/not_run`, with no project, accepted canonical, release, or deployment. The later runtime row supersedes that execution state. |
| 2026-07-22 | Program closure fail-closed rerun (historical implementation state) | The 38/38 suite, fixture preflight, and real class-10 missing-pair result remain valid historical evidence. The later immutable-input and strict-record remediation below supersedes its implementation identity and focused-suite count. |
| 2026-07-22 | Delivery evidence tamper and TOCTOU RED | RED `37b023ec` captured delivery-record tamper gaps; supporting schema-value RED `94858299` specified bound record values; micro-RED `8701ade6` proved a valid-format substituted verdict hash could otherwise be published. |
| 2026-07-22 | Immutable-input and record-binding GREEN (historical, superseded) | GREEN `692ae759` bound schema-v2 records and seven snapshotted inputs for that committed state. Its 42/42 result and class-10 `verdict-file-missing` observation remain historical evidence; the pair-manifest contract below supersedes both the schema and blocker code. |
| 2026-07-22 | Historical verdict pair-manifest RED/GREEN (superseded record schema) | RED `f0c3e032` required a source/context/generation-bound manifest with exact baseline/candidate verdict hashes and fd-relative canonical invalidation. GREEN `20022458` requires, snapshots, and revalidates that manifest; rejects missing, stale, mixed, or substituted generations at class 10 before Docker; and records its SHA-256 and generation in then-current strict schema-v3 output. Canonical invalidation uses validated parent directory FDs with relative `stat`/`unlink`/`fsync`, while an absent evidence directory remains absent. Focused tests passed 45/45 and the shared Task 3 compatibility suite passed 44/44; Bash syntax, ShellCheck, Python compilation, diff hygiene, and fixture-only preflight passed. The portable v2/v3/v4 row supersedes only the output schema and counts. |
| 2026-07-22 | Historical real canonical blocker proof (superseded) | Exactly one real canonical command exited class `10` with `code=pair-manifest-missing` before Docker because no accepted committed pair existed at that revision. No positive or rollback runtime ran. The rehearsal evidence directory, record, temporary record, and `/tmp/hyhome-dre-*` paths were absent; owner/task-scoped containers, networks, and volumes were zero. The later accepted portable pair supersedes only this prerequisite state. |
| 2026-07-23 | Terminal whole-branch review closure | Quality/security review v3 returned `APPROVED C0/I0/M0` for the full branch range through `20022458` plus the then-current 26-document reconciliation diff. Specification review v5 returned `APPROVED C0/I0/M0` for the full branch range through `20022458` plus the final 26-document reconciliation diff. Earlier `CHANGES REQUIRED` iterations remain historical remediation evidence. These historical approvals did not create the then-missing accepted pair or Task 5 runtime. |
| 2026-07-23 | Portable consumer migration and review | Producer `1937ec75` and consumer `a6c12e18` migrated the handoff to verdict schema v2, pair schema/generation v3, and rehearsal-record schema v4 with the full OCI/Docker/runtime tuple. Review remediation `b192c0db` preserves a valid canonical record when a later invalid attempt fails. The current focused delivery suite passes 54/54 after test-isolation fix `4f7284a9`; portable-handoff specification and quality/security reviews are `C0/I0/M0`. |
| 2026-07-23 | Accepted input readiness | Task 7 published a mode-0600 schema-v3 pair for source `b070a06ceac2f3e60fdb5bdb3fa87b4b0433545b`, generation `hyhome-verification-verdict-pair-v3`, SHA-256 `ac61c1763f1c14cc8d07b3e58421d1f7355bf22b47632da67f8aad061f6b1220`. Its baseline/candidate verdict hashes are `057f301edbb1475a398c41d16272986580f754d149473263be6ca29b5728497b` and `89db847616e1533240edeb060f008c21406de5703cf49d09a7590839c3df27ce`; the full pair-bound local refs and runtime IDs satisfy the static Task 5 consumer contract. At this checkpoint no real Task 5 rehearsal had run; the later runtime row supersedes that prerequisite-only state. |
| 2026-07-23 | Approved Task 5 runtime sequence | The focused unit suite passed 54/54 at exit 0, followed by fixture-only preflight at exit 0. Exactly one positive real rehearsal then exited 0 for projects `hyhome-dre-20260719-1709404-baseline` and `hyhome-dre-20260719-1709404-canary`. It ran from `2026-07-22T20:54:30Z` through `2026-07-22T20:54:46Z`; baseline/candidate both passed, promotion was `promoted`, rollback was `not_required`, post-rollback health was `not_applicable`, result was `promoted`, cleanup passed, and `data_impact=none`. Its mode-0600, 3,295-byte canonical record had inode `1290126` and SHA-256 `6bc6de4b34bd6fe6439c682de33eb580e2b5074e12762cd25ad9c1b4a9eeb5c1`. Exactly one injected `canary-health-timeout` rehearsal then exited expected class 30 with `health-deadline-exceeded` for projects `hyhome-dre-20260719-1731921-baseline` and `hyhome-dre-20260719-1731921-canary`. It ran from `2026-07-22T20:56:27Z` through `2026-07-22T20:58:59Z`; baseline passed, candidate failed, promotion was `not_promoted`, rollback was `rolled_back_to_baseline`, post-rollback health passed, result was `rolled_back`, cleanup passed, and `data_impact=none`. The replacement mode-0600, 3,305-byte record has inode `538673` and SHA-256 `e6c3efd320014eb7b89324974c3c8a7e71e4ac32ff122a0432e5dc21ac16e823`; changed inode and hash prove replacement rather than stale-record reuse. Both records bind source `b070a06ceac2f3e60fdb5bdb3fa87b4b0433545b`, pair hash `ac61c1763f1c14cc8d07b3e58421d1f7355bf22b47632da67f8aad061f6b1220`, readiness hash `12fbe9fa47eb0e96a8a2ed23d033dc176bf279fce8e9a8d6b91ccd1d166e76a0`, and recovery hash `bf7109f5fd15cf04615ed331cb63be7c7848d8656749e427c2a54a1aecd2d18a`. After both runs, all owner/task/name-scoped containers, networks, volumes, and `/tmp` publication paths were empty. Tracked HEAD remained `f3e4701115734e71f8848e706e9d37d499f0c2ac` and clean. No standalone cleanup, rerun, remote action, release, registry operation, controlled wrapper, or pre-commit command ran. |
| 2026-07-23 | `T-DRE-004` Task 5 runtime-evidence review closure | Fresh independent specification and quality/security reviewers each returned `APPROVED C0/I0/M0` with no findings for exact range `f3e4701115734e71f8848e706e9d37d499f0c2ac..a5c97e0a62bb71029c73e84f5dbe07b4c1dc0efe`. The specification review passed delivery 54/54, metadata 6/0 with one unchanged legacy exception, traceability 46/0, alignment 667 documents / 5,524 links / 141 operations documents / 0, diff hygiene, and read-only canonical/upstream reconciliation. The quality/security review passed delivery 54/54, fixture preflight at exit 0, Bash syntax, Python compilation, diff hygiene, and stat/hash/ignore/`jq`/tuple reconciliation. Neither review ran Docker, Compose, rehearsal, cleanup, advisory, Task 4, the controlled wrapper, pre-commit, or any remote action. |

## Verification Evidence

Exact command envelope:

```bash
python3 -m unittest tests.validation.test_sample_service_delivery_rehearsal -v
bash scripts/operations/rehearse-sample-service-delivery.sh preflight --task-id 2026-07-19-dre --baseline-verdict tests/fixtures/sample-service-delivery/spec126-verdict.baseline.accepted.json --candidate-verdict tests/fixtures/sample-service-delivery/spec126-verdict.candidate.accepted.json
bash scripts/operations/rehearse-sample-service-delivery.sh rehearse --task-id 2026-07-19-dre --baseline-verdict _workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.baseline.json --candidate-verdict _workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.candidate.json --failure-mode none
bash scripts/operations/rehearse-sample-service-delivery.sh rehearse --task-id 2026-07-19-dre-negative --baseline-verdict _workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.baseline.json --candidate-verdict _workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.candidate.json --failure-mode canary-health-timeout
```

Standalone `cleanup --task-id ...` is rescue-only for an interrupted or
partial exact owned project pair. It is not an expected command after either
successful in-process cleanup and returns class `60` when that exact pair is
absent.

Expected evidence: preflight rejects incomplete or mismatched verdicts, equal
subjects, remote references, fixed Compose identity, and port collision. The
positive rehearsal requires container health plus HTTP 200 and marker presence,
then records `promotion_decision=promoted`, `data_impact=none`, and cleanup. The
negative rehearsal returns class `30`, prohibits promotion, verifies the prior
runtime image ID and post-rollback health, and records cleanup. Because the
record path is singular, Task evidence captures the positive record hash and
concise fields before the injected-rollback run replaces it.

Actual evidence:

- focused RED/GREEN progressed from the inherited 21-test RED
  (`failures=22`, `errors=3`, one fixture-schema pass), through 21/21 and 26/26,
  to final 28/28 GREEN after the label-cardinality guard;
- review remediation first proved the test mutation with an isolated 1/1 RED,
  then produced 13 intended failures and 0 errors across 38 tests. Final GREEN
  reached 38/38, including exact two-role non-starting render, local image identity,
  direct partial/error cleanup, stable rollback/cleanup classes, invalid-pair
  rejection, unchanged real-canonical snapshots, and directory-FD publication;
- immutable-input and strict-record RED commits then closed raw hash
  substitution and TOCTOU publication gaps; pair-manifest RED/GREEN closes
  mixed-generation and path-relative invalidation gaps; portable tuple
  migration and isolation correction bring the current GREEN suite to 54/54;
- Bash syntax, ShellCheck, Python compilation, and diff hygiene pass with zero diagnostics;
- fixture-only preflight exits 0 and reports exact revision, passing readiness
  and recovery boundaries, valid project-scopable Compose, and loopback ports
  `18080,18081`, with no Docker call;
- the historical sole real command exited `10` with
  `code=pair-manifest-missing`; Docker was not reached and the Task 5 canonical
  directory/record remained absent;
- the Spec 124 readiness v2 and Spec 125 recovery v1 canonical inputs pass the
  exact consumer schemas. Spec 126 supplies accepted baseline/candidate
  schema-v2 verdicts and a schema-v3 pair; the positive and injected-negative
  runs consumed the same source-bound portable tuple;
- the positive run exited 0 and published a mode-0600, 3,295-byte record with
  inode `1290126` and SHA-256
  `6bc6de4b34bd6fe6439c682de33eb580e2b5074e12762cd25ad9c1b4a9eeb5c1`;
  the injected-negative run exited expected class 30 with
  `health-deadline-exceeded`, rolled back to the healthy baseline, and replaced
  it with the current mode-0600, 3,305-byte record at inode `538673` and
  SHA-256
  `e6c3efd320014eb7b89324974c3c8a7e71e4ac32ff122a0432e5dc21ac16e823`;
- direct read-only reconciliation of the current canonical record confirmed
  schema 4, pair generation v3/hash, readiness and recovery hashes, full
  portable role tuples, negative decisions, cleanup, and `data_impact=none`;
  all scoped Docker resources and `/tmp` publication paths were empty;
- At the historical Task 5 implementation checkpoint, Python compilation,
  non-starting merged Compose render, metadata 23/0, traceability 46/0,
  alignment 666 documents / 5,446 links / 141 operations documents / 0,
  template contracts 38/38, targeted Markdown lint, and diff hygiene passed;
  its then-current aggregate `failures=4` was later superseded by Task 6's
  metadata 41/0 and 35/0, alignment 666 documents / 5,507 links / 141
  operations documents / 0, and dependency-locked aggregate `failures=0`
  checkpoint. For this portable evidence reconciliation, changed metadata
  passes 12/0 with one unchanged legacy exception, traceability passes 46/0,
  alignment passes at 667 documents / 5,521 links / 141 operations documents /
  0, and diff hygiene passes. Full Task 7 runtime-evidence specification and
  quality/security reviews are both `APPROVED C0/I0/M0` for exact range
  `b070a06c..086744f8`;
- fresh Task 5 specification review is `APPROVED C0/I0/M0` with no findings for
  exact range
  `f3e4701115734e71f8848e706e9d37d499f0c2ac..a5c97e0a62bb71029c73e84f5dbe07b4c1dc0efe`.
  Delivery passed 54/54; metadata passed 6/0 with one unchanged legacy
  exception; traceability passed 46/0; alignment passed at 667 documents / 5,524
  links / 141 operations documents / 0; diff hygiene and read-only
  canonical/upstream reconciliation passed;
- fresh Task 5 quality/security review is `APPROVED C0/I0/M0` with no findings
  for the same exact range. Delivery passed 54/54; fixture preflight exited 0;
  Bash syntax, Python compilation, diff hygiene, and
  stat/hash/ignore/`jq`/tuple reconciliation passed.

Verification results: implementation, static validation, 54/54 focused tests at
exit 0, fixture-only preflight at exit 0, 61/61 Task 3 producer compatibility
tests, immutable-input and portable pair-manifest revalidation, and fail-closed
proof pass. The approved runtime order also completed exactly once: positive
exit 0 followed by injected-negative exit 30. The current canonical ignored
record is the negative replacement; it was read and hash/mode/size/inode checked
without modification. Exit classes are `0=pass`, `2=usage`,
`10=verdict/pair-manifest/preflight`, `20=baseline`, `30=canary/health`,
`40=promotion record`, `50=rollback`, and `60=cleanup`.

Task 7 created the accepted portable pair but did not itself execute Task 5.
The later approved delivery sequence created both positive and rollback
evidence, with the negative replacement retained as the canonical record. The
Task 5 runtime, independent reviews, and tracked document closure are complete.
The Program-owned controlled all-files wrapper is `READY / not_run` for the
exact clean checkpoint containing this five-file closure; its full commit
identity is recorded only in the ignored Task 6 report after that commit exists.

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

Implementation review verdict: implementation, runtime execution, evidence
reconciliation, author self-check, and both fresh independent runtime-evidence
reviews are complete with no finding.
The self-check found and remediated direct evidence-path redirection and an
immediate-return failure injection; subsequent whole-review remediation binds
the strict record to immutable snapshots and revalidates all inputs immediately
before publication.

Specification review verdict: initial review returned CHANGES REQUIRED
C0/I2/M0. Both findings are included in the four-item remediation below;
terminal re-review returned APPROVED C0/I0/M0 for historical implementation
commit `b5441c53`. Terminal specification review v5 returned
`APPROVED C0/I0/M0` for the full branch range through `20022458` plus the final
26-document reconciliation diff, covering the current immutable-input and
pair-manifest hardening. The fresh specification review of exact Task 5 range
`f3e4701115734e71f8848e706e9d37d499f0c2ac..a5c97e0a62bb71029c73e84f5dbe07b4c1dc0efe`
returned `APPROVED C0/I0/M0` with no findings after delivery 54/54, metadata 6/0
with one unchanged legacy exception, traceability 46/0, alignment
667/5,524/141/0, diff hygiene, and read-only canonical/upstream reconciliation.

Quality/security review verdict: initial review returned CHANGES REQUIRED
C1/I2/M0. All findings are remediated; the separate terminal release/security
re-review returned APPROVED C0/I0/M0 for `b5441c53`.
Terminal quality/security review v3 returned `APPROVED C0/I0/M0` for the full
branch range through `20022458` plus the then-current 26-document
reconciliation diff, covering the current immutable-input and pair-manifest
hardening. The fresh quality/security review of the same exact Task 5 range
returned `APPROVED C0/I0/M0` with no findings after delivery 54/54, fixture
preflight at exit 0, Bash syntax, Python compilation, diff hygiene, and
stat/hash/ignore/`jq`/tuple reconciliation.

Findings and disposition: the four unique findings are closed in implementation
and 38/38 tests: exact accepted digests must resolve to existing local image
objects with build/pull disabled; cleanup no longer depends on Compose
interpolation and removes only proven owned IDs; standalone missing or invalid
pairs return class `60`; and tests snapshot rather than mutate the real
canonical record/directory. Publication additionally uses a stable
`O_NOFOLLOW` parent directory FD for atomic mode-0600 replacement. Both
terminal reviews returned C0/I0/M0. Portable-handoff reviews also returned
C0/I0/M0. The later exact positive and injected-rollback runs and their fresh
independent specification and quality/security reviews are closed at
`APPROVED C0/I0/M0` with no findings. Earlier `CHANGES REQUIRED` iterations
remain historical remediation evidence.

## Commit Ledger

Historical implementation identity: `b5441c53`, reviewed by both terminal
domain reviewers. Current remediation ledger: RED `37b023ec`, supporting
schema-value RED `94858299`, micro-RED `8701ade6`, GREEN `692ae759`,
pair-manifest RED `f0c3e032`, and pair-manifest GREEN `20022458`.
Portable consumer GREEN is `a6c12e18`; canonical-preservation remediation is
`b192c0db`; test isolation is `4f7284a9`; contract reconciliation is
`fb0b59f3`; the exact reviewed runtime-evidence commit is
`a5c97e0a62bb71029c73e84f5dbe07b4c1dc0efe`.
This five-file review/document closure intentionally does not self-record its
final SHA.

Logical unit: `feat(release): add local promotion and rollback`.

Commit validation: 54/54 focused tests, 61/61 Task 3 producer compatibility
tests, fixture-only preflight, historical exact class-10 no-record proof,
immutable-input/hash/pair-generation binding, two-role non-starting render,
Python compilation, Bash syntax, ShellCheck, and diff hygiene pass.
Historical terminal domain reviews are APPROVED C0/I0/M0; whole-branch
specification v5 and quality/security v3 reviews are also APPROVED C0/I0/M0.
The later positive/rollback runtime evidence has fresh exact-range specification
and quality/security approvals at C0/I0/M0 with no findings.

## Deferred and Blocked Items

Deferred items: GitHub workflows/environments/releases, registry publication,
remote deployment, production targets, OIDC/credentials, real Release records,
and stateful data rollback.

Blocked items: none of the Spec 126 seed/policy/pair or Task 5 runtime, review,
or tracked document-closure gates remain blocked. The approved
positive-first/injected-negative-second sequence is complete, with healthy
baseline restoration and canonical replacement proved. Any future stateful
impact still blocks promotion and routes to Spec 125. The Program-owned
controlled all-files wrapper is `READY / not_run` for its exact clean checkpoint;
this Task remains active until wrapper and lifecycle closure and does not
authorize a rehearsal rerun.

Deferral destination: data recovery routes to
[Spec 125](../../03.specs/125-infrastructure-operations-readiness-remediation/spec.md);
remote delivery requires a new approved Stage 01-04 chain and explicit external
action approval.

## Related Documents

- [Spec 127](../../03.specs/127-deployment-release-engineering-remediation/spec.md)
- [Deployment/release Plan](../plans/2026-07-11-deployment-release-engineering-remediation.md)
- [Program Task](./2026-07-19-operational-readiness-closure-program.md)
- [Compose Task](./2026-07-19-compose-runtime-readiness-remediation.md)
- [Infrastructure Task](./2026-07-19-infrastructure-operations-readiness-remediation.md)
- [Supply-chain Task](./2026-07-19-security-supply-chain-remediation.md)
