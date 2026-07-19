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
evidence.

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
| `T-DRE-001` | Typed verdict/record fixtures, gates, CLI, and tests | `DRE-001`–`DRE-004` | Focused RED/GREEN and preflight | Fresh implementation agent | Not run |
| `T-DRE-002` | Project-scopable service and baseline/canary health | `DRE-001`, `DRE-003` | Separate projects and two-part health | Fresh implementation agent | Not run |
| `T-DRE-003` | Promotion record, failure injection, rollback, cleanup | `DRE-002`, `DRE-004` | Positive and expected-failure rehearsal | Fresh implementation agent | Not run |
| `T-DRE-004` | Runbook handoff and independent reviews | `VAL-DRE-001`–`004` | Spec plus release/security C0/I0/M0 | Separate reviewers | Not run |

## Work Log

| Date | Work unit | Result |
| --- | --- | --- |
| 2026-07-19 | Task activation | Contract recorded; no build, project, promotion, rollback, release, or remote action executed. |
| 2026-07-19 | `T-DRE-001`–`T-DRE-004` | `not_run`; append actual evidence only after upstream verdicts and exact execution. |

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

Actual evidence: `not_run`.

Verification results: `not_run`. Exit classes are `0=pass`, `2=usage`,
`10=verdict/preflight`, `20=baseline`, `30=canary/health`,
`40=promotion record`, `50=rollback`, and `60=cleanup`.

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

Specification review verdict: `not_run`; a fresh reviewer must verify Spec 127,
upstream typed handoffs, project/health/promotion/rollback contracts, record
schema, and remote/data exclusions.

Quality/security review verdict: `not_run`; a separate reviewer must inspect
input parsing, digest checks, shell/Compose safety, health/failure semantics,
cleanup ownership, redaction, tests, and runbook scope.

Findings and disposition: none because review has not run. All findings must be
remediated and re-reviewed to C0/I0/M0.

## Commit Ledger

Commit identity: `not_committed`.

Logical unit: `feat(release): add local promotion and rollback`.

Commit validation: `not_run`; record focused tests, preflight, positive and
negative rehearsals, rollback/cleanup, runbook validation, and review after the
commit exists.

## Deferred and Blocked Items

Deferred items: GitHub workflows/environments/releases, registry publication,
remote deployment, production targets, OIDC/credentials, real Release records,
and stateful data rollback.

Blocked items: preflight and runtime are blocked until both Spec 126 verdicts
are accepted/distinct/same-revision, Spec 124 readiness is ready and cleaned,
and Spec 125's synthetic recovery boundary is present. Any stateful impact
blocks promotion.

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
