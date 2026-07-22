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

This active Task will record a local verified-digest baseline/canary promotion
and previous-digest rollback rehearsal for `examples/sample-web-service`. At
activation, no baseline or canary project has started, no promotion or rollback
decision has been made, and no GitHub Release, registry object, deployment, or
remote environment exists.

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
  digest after bounded canary failure;
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
rollback digest, and cleanup must resolve before startup. Preflight and cleanup
accept only the exact baseline/canary pair matching
`^hyhome-dre-20260719-[0-9]+-(baseline|canary)$`; any missing, additional, or
nonmatching project fails closed. Any remote or stateful surface requires stop
and new approval.

Rollback or recovery: on failed canary health, prohibit promotion, stop the
canary, restore/verify the baseline previous digest and HTTP health, then clean
both owned projects. Revert the single DRE commit to remove authored changes.
Ambiguous data impact stops and hands off to Spec 125 without deletion.

Redaction boundary: tracked evidence may contain source revision, digest and
verdict references, project names, marker presence, decisions, data impact,
cleanup, commit, and reviews. Raw HTTP bodies, logs, image contents, keys,
tokens, credentials, environment values, and upstream raw evidence remain
untracked.

## Work Breakdown

| Task ID | Description | Parent requirement | Validation / evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| `T-DRE-001` | Typed verdict/record fixtures, gates, CLI, and tests | `DRE-001`–`DRE-004` | Focused RED/GREEN and preflight | Fresh implementation agent | Complete; current focused suite 45/45 and fixture-only preflight pass |
| `T-DRE-002` | Project-scopable service and baseline/canary health | `DRE-001`, `DRE-003` | Separate projects and two-part health | Fresh implementation agent | Implementation complete; positive runtime blocked/not_run |
| `T-DRE-003` | Promotion record, failure injection, rollback, cleanup | `DRE-002`, `DRE-004` | Positive and expected-failure rehearsal | Fresh implementation agent | Implementation complete; promotion/rollback runtime blocked/not_run |
| `T-DRE-004` | Runbook handoff and independent reviews | `VAL-DRE-001`–`004` | Spec plus release/security C0/I0/M0 | Separate reviewers | Current terminal reviews approved C0/I0/M0; Task remains active on runtime prerequisites |

## Work Log

| Date | Work unit | Result |
| --- | --- | --- |
| 2026-07-19 | Task activation | Contract recorded; no build, project, promotion, rollback, release, or remote action executed. |
| 2026-07-19 | `T-DRE-001`–`T-DRE-004` | Initially `not_run`; append actual evidence only after upstream verdicts and exact execution. |
| 2026-07-22 | `T-DRE-001` focused implementation | Existing 21-test RED was 22 failures and 3 errors with only the fixture-schema method passing. The first wrapper reduced this to 1 failure, then passed 21/21. Expanded contract RED was 8 failures in 26 tests and GREEN was 26/26. Four state-machine guarantees were RED across 3 unittest failures, then GREEN reached 27/27; the final service/network label cardinality guard brought the suite to 28/28. |
| 2026-07-22 | `T-DRE-002`–`T-DRE-004` implementation boundary | Removed only fixed Compose `name`/`container_name`; added exact digest, gate, project, port, label, health-marker, promotion, rollback, cleanup, record, timeout, and runbook contracts. Fixture-only preflight passed without Docker. The real command stopped at class 10 because the accepted Spec 126 pair is absent; no project or record was created. Reviews were then pending. |
| 2026-07-22 | Independent-review remediation | Specification returned C0/I2/M0 and release/security returned C1/I2/M0, deduplicated to four findings. The isolated canonical-mutation scan was RED 1/1; expanded RED was 38 tests with 13 failures and 0 errors. GREEN is 38/38 after exact local image-object validation and pull/build denial, interpolation-free ID cleanup, fail-closed missing-pair cleanup, immutable real-canonical snapshots, and stable no-follow directory-FD publication. No project or accepted canonical was created; terminal re-reviews were then pending. |
| 2026-07-22 | Terminal independent review closure | Terminal specification and release/security reviews both returned APPROVED C0/I0/M0 for historical implementation commit `b5441c53`. Fail-closed implementation/static/fixture proof is complete; positive/negative runtime remains `blocked/not_run`, with no project, accepted canonical, release, or deployment. |
| 2026-07-22 | Program closure fail-closed rerun (historical implementation state) | The 38/38 suite, fixture preflight, and real class-10 missing-pair result remain valid historical evidence. The later immutable-input and strict-record remediation below supersedes its implementation identity and focused-suite count. |
| 2026-07-22 | Delivery evidence tamper and TOCTOU RED | RED `37b023ec` captured delivery-record tamper gaps; supporting schema-value RED `94858299` specified bound record values; micro-RED `8701ade6` proved a valid-format substituted verdict hash could otherwise be published. |
| 2026-07-22 | Immutable-input and record-binding GREEN (historical, superseded) | GREEN `692ae759` bound schema-v2 records and seven snapshotted inputs for that committed state. Its 42/42 result and class-10 `verdict-file-missing` observation remain historical evidence; the pair-manifest contract below supersedes both the schema and blocker code. |
| 2026-07-22 | Verdict pair-manifest RED/GREEN | RED `f0c3e032` required a source/context/generation-bound manifest with exact baseline/candidate verdict hashes and fd-relative canonical invalidation. GREEN `20022458` requires, snapshots, and revalidates that manifest; rejects missing, stale, mixed, or substituted generations at class 10 before Docker; and records its SHA-256 and generation in strict schema-v3 output. Canonical invalidation uses validated parent directory FDs with relative `stat`/`unlink`/`fsync`, while an absent evidence directory remains absent. Focused tests pass 45/45 and the shared Task 3 compatibility suite passes 44/44; Bash syntax, ShellCheck, Python compilation, diff hygiene, and fixture-only preflight pass. |
| 2026-07-22 | Current real canonical blocker proof | Exactly one real canonical command exited class `10` with `code=pair-manifest-missing` before Docker because no accepted committed pair exists. No positive or rollback runtime ran. The rehearsal evidence directory, record, temporary record, and `/tmp/hyhome-dre-*` paths are absent; owner/task-scoped containers, networks, and volumes are zero. The Task stays active pending accepted inputs and positive plus rollback runtime evidence. |
| 2026-07-23 | Terminal whole-branch review closure | Quality/security review v3 returned `APPROVED C0/I0/M0` for the full branch range through `20022458` plus the then-current 26-document reconciliation diff. Specification review v5 returned `APPROVED C0/I0/M0` for the full branch range through `20022458` plus the final 26-document reconciliation diff. Earlier `CHANGES REQUIRED` iterations remain historical remediation evidence. These approvals do not create the missing accepted pair or Task 5 positive/rollback runtime; the Task and Program remain active and the controlled wrapper remains blocked/not_run. |

## Verification Evidence

Exact command envelope:

```bash
python3 -m unittest tests.validation.test_sample_service_delivery_rehearsal -v
bash scripts/operations/rehearse-sample-service-delivery.sh preflight --task-id 2026-07-19-dre --baseline-verdict tests/fixtures/sample-service-delivery/spec126-verdict.baseline.accepted.json --candidate-verdict tests/fixtures/sample-service-delivery/spec126-verdict.candidate.accepted.json
bash scripts/operations/rehearse-sample-service-delivery.sh rehearse --task-id 2026-07-19-dre --baseline-verdict _workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.baseline.json --candidate-verdict _workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.candidate.json --failure-mode none
bash scripts/operations/rehearse-sample-service-delivery.sh rehearse --task-id 2026-07-19-dre-negative --baseline-verdict _workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.baseline.json --candidate-verdict _workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.candidate.json --failure-mode canary-health-timeout
bash scripts/operations/rehearse-sample-service-delivery.sh cleanup --task-id 2026-07-19-dre
bash scripts/operations/rehearse-sample-service-delivery.sh cleanup --task-id 2026-07-19-dre-negative
```

Expected evidence: preflight rejects incomplete or mismatched verdicts, equal
subjects, remote references, fixed Compose identity, and port collision. The
positive rehearsal requires container health plus HTTP 200 and marker presence,
then records `promotion_decision=promoted`, `data_impact=none`, and cleanup. The
negative rehearsal returns class `30`, prohibits promotion, verifies the prior
digest and post-rollback health, and records cleanup.

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
  mixed-generation and path-relative invalidation gaps, and the current GREEN
  suite is 45/45;
- Bash syntax, ShellCheck, Python compilation, and diff hygiene pass with zero diagnostics;
- fixture-only preflight exits 0 and reports exact revision, passing readiness
  and recovery boundaries, valid project-scopable Compose, and loopback ports
  `18080,18081`, with no Docker call;
- the exact sole current real command exits `10` with
  `code=pair-manifest-missing`; Docker is not reached and the Task 5 canonical
  directory/record remains absent;
- the Spec 124 readiness v2 and Spec 125 recovery v1 canonical inputs pass the
  exact consumer schemas. Spec 126's accepted baseline/candidate canonical
  files remain absent after its truthful 14-critical/no-exception policy result.
- Python compilation and a non-starting merged Compose render pass. Changed-doc
  metadata is 23 selected / 0 violations with one unchanged legacy exception;
  traceability is 46/0, alignment is 666 documents / 5,446 links / 141
  operations docs / 0 failures, template contracts are 38/38, targeted
  Markdown lint and diff hygiene pass. The aggregate is `failures=4`, limited
  to the pre-existing lifecycle-consumer and missing-`html5lib` gates; Task 5
  script inventory has no remaining diagnostic. Declared owners are fresh at
  1,311 LLM Wiki paths, 1,310 safe coverage paths, and 13 security automation
  controls; their diffs contain only the newly tracked Task 5 wrapper counts.

Verification results: implementation, static validation, 45/45 focused tests,
44/44 Task 3 producer compatibility tests, fixture-only preflight,
immutable-input and pair-manifest revalidation, and fail-closed proof
pass. Exactly one current real command returned class `10` before Docker. No
positive promotion or injected rollback runtime ran; no Docker/Compose project
or canonical rehearsal record was created. Exit classes are `0=pass`, `2=usage`,
`10=verdict/pair-manifest/preflight`, `20=baseline`, `30=canary/health`,
`40=promotion record`, `50=rollback`, and `60=cleanup`.

Task 6 documentation, owner regeneration, safe gates, and whole-branch
re-review are recorded by the Program Task. They cannot create the accepted
pair or positive/rollback runtime evidence. The delivery record remains absent,
and the controlled all-files wrapper remains blocked and `not_run`.

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

Implementation review verdict: implementation and author self-check complete.
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
pair-manifest hardening.

Quality/security review verdict: initial review returned CHANGES REQUIRED
C1/I2/M0. All findings are remediated; the separate terminal release/security
re-review returned APPROVED C0/I0/M0 for `b5441c53`.
Terminal quality/security review v3 returned `APPROVED C0/I0/M0` for the full
branch range through `20022458` plus the then-current 26-document
reconciliation diff, covering the current immutable-input and pair-manifest
hardening.

Findings and disposition: the four unique findings are closed in implementation
and 38/38 tests: exact accepted digests must resolve to existing local image
objects with build/pull disabled; cleanup no longer depends on Compose
interpolation and removes only proven owned IDs; standalone missing or invalid
pairs return class `60`; and tests snapshot rather than mutate the real
canonical record/directory. Publication additionally uses a stable
`O_NOFOLLOW` parent directory FD for atomic mode-0600 replacement. Both
terminal reviews returned C0/I0/M0. This review closure does not replace the
missing accepted Spec 126 pair or supply promotion/rollback runtime evidence.
Earlier `CHANGES REQUIRED` iterations remain historical remediation evidence;
the separate v3/v5 whole-branch approvals cover the later immutable-input and
pair-manifest commits.

## Commit Ledger

Historical implementation identity: `b5441c53`, reviewed by both terminal
domain reviewers. Current remediation ledger: RED `37b023ec`, supporting
schema-value RED `94858299`, micro-RED `8701ade6`, GREEN `692ae759`,
pair-manifest RED `f0c3e032`, and pair-manifest GREEN `20022458`.
The separate evidence update intentionally does not self-record its final SHA.

Logical unit: `feat(release): add local promotion and rollback`.

Commit validation: 45/45 focused tests, 44/44 Task 3 producer compatibility
tests, fixture-only preflight, exact real class-10 no-record proof,
immutable-input/hash/pair-generation binding, two-role non-starting render,
Python compilation, Bash syntax, ShellCheck, and diff hygiene pass.
Historical terminal domain reviews are APPROVED C0/I0/M0; whole-branch
specification v5 and quality/security v3 reviews are also APPROVED C0/I0/M0.
Positive/rollback runtime remains `blocked/not_run`.

## Deferred and Blocked Items

Deferred items: GitHub workflows/environments/releases, registry publication,
remote deployment, production targets, OIDC/credentials, real Release records,
and stateful data rollback.

Blocked items: runtime is blocked until both Spec 126 verdicts are
accepted/distinct/same-revision and their schema-v2 pair manifest binds the
exact verdict bytes, source revision, build context, and generation. The
current committed-tree verification stops even earlier at the absent approved
Grype database seed, so neither accepted canonical nor pair manifest exists.
The historical baseline rejection found 14 critical findings with no approved
exception and remains non-acceptance evidence. Spec 124 readiness is
ready/cleaned and Spec 125's synthetic
recovery boundary is present; these passing dependencies do not override the
missing security pair. Any stateful impact also blocks promotion.

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
