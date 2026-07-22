---
status: active
artifact_id: plan:2026-07-11-deployment-release-engineering-remediation
artifact_type: plan
parent_ids:
  - prd:025-operational-readiness-closure
  - ard:0028-operational-readiness-closure
  - adr:0028-local-isolated-readiness-evidence
  - spec:127-deployment-release-engineering-remediation
---

# Deployment and Release Engineering Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` (recommended) or
> `superpowers:executing-plans` to implement this plan task-by-task. Sequence
> steps become Task evidence only after execution.

**Goal:** Rehearse verified-digest baseline/canary delivery and previous-digest
rollback for `examples/sample-web-service` without creating a real release or
remote deployment.

**Architecture:** The sample Compose file becomes project-scopable by removing
its fixed top-level/project container identity. A task-owned wrapper consumes
the concise accepted verdict from Spec 126, runs independent baseline and
canary Compose projects, checks container plus HTTP health, records a local
promotion decision, injects bounded failure, restores the previous digest, and
cleans only labelled task resources.

**Tech Stack:** Docker Compose; Bash; Python `unittest`; sample web service;
typed JSON handoff/record fixtures; local HTTP and container-health probes.

## Global Constraints

- Candidate and previous artifacts must be immutable digests; mutable tags are
  never promotion inputs.
- Baseline and canary project names are constructed as
  `hyhome-dre-20260719-<decimal-pid>-baseline` and
  `hyhome-dre-20260719-<decimal-pid>-canary`. Preflight and cleanup accept only
  `^hyhome-dre-20260719-[0-9]+-(baseline|canary)$`; their host ports are
  `18080` and `18081` unless preflight proves a collision and fails.
- The local rehearsal record ID is constructed as `local-rehearsal-20260719-`
  followed by the first 12 hexadecimal characters of the source revision; it
  is not a GitHub Release, registry tag, deployment record, or production
  release event.
- Any stateful/data impact stops and routes to Spec 125; this plan only restores
  application/config artifact identity.

## Overview

This active plan turns Spec 127 into an executable local sequence for
`examples/sample-web-service` baseline/canary environments, verified-digest
promotion, health gates, release/deployment evidence records, and previous
digest rollback. It is prospective; actual local runtime evidence belongs in
`docs/04.execution/tasks/2026-07-19-deployment-release-engineering-remediation.md`.

The implementation rehearses delivery mechanics only. It does not create a
GitHub Environment, GitHub Release, registry publication, remote deployment,
production release event, paid job, or credential change.

## Context and Inputs

Inputs:

- [PRD 025](../../01.requirements/025-operational-readiness-closure.md)
- [ARD 0028](../../02.architecture/requirements/0028-operational-readiness-closure.md)
- [ADR 0028](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
- [Spec 127](../../03.specs/127-deployment-release-engineering-remediation/spec.md)
- [examples/sample-web-service/docker-compose.yml](../../../examples/sample-web-service/docker-compose.yml)
- Spec 124 readiness result, Spec 125 recovery boundary, and Spec 126 verified
  artifact verdict when available.

Planning implication: CI/build success, changelog text, and local image
existence are inputs, not deployment evidence. The rehearsal must require an
immutable verified digest, promote only after gates pass, and prove rollback to
the previous verified digest.

## Goals and Non-goals

Goals:

- Prove `DRE-001` with explicit local baseline/canary/stable environments,
  separation of gates, and deployment history.
- Prove `DRE-002` with a local release-iteration evidence record that binds
  the deterministic local rehearsal ID, source revision, artifact digest, approval, verifier
  verdict, outcome, and rollback disposition.
- Prove `DRE-003` with a local promotion wrapper that fails closed on missing
  approval, security verdict, readiness, health, or rollback.
- Prove `DRE-004` with previous verified digest rollback and post-rollback
  health; data recovery remains a Spec 125 handoff.

Non-goals:

- No real GitHub Release or production deployment.
- No GitHub Actions workflow/environment/ruleset mutation.
- No registry push, remote target, secret-value, OIDC, or deployment credential.
- No claim that local canary equals production release readiness.

## Work Breakdown

| Unit | Purpose | Planned owned files | Requirements | RED/GREEN evidence | Commit boundary |
| --- | --- | --- | --- | --- | --- |
| `T-DRE-001` | Define typed handoff/record fixtures, gate contract, wrapper CLI, and tests. | `scripts/operations/rehearse-sample-service-delivery.sh`; `tests/fixtures/sample-service-delivery/spec126-verdict.baseline.accepted.json`; `tests/fixtures/sample-service-delivery/spec126-verdict.candidate.accepted.json`; `tests/fixtures/sample-service-delivery/spec126-verdict.candidate.rejected.json`; `tests/fixtures/sample-service-delivery/spec126-verdict.candidate.digest-mismatch.json`; `tests/fixtures/sample-service-delivery/compose.delivery.override.yml`; `tests/validation/test_sample_service_delivery_rehearsal.py`; `docs/04.execution/tasks/2026-07-19-deployment-release-engineering-remediation.md`. | `DRE-001`–`DRE-004` | RED: mutable tag, missing/rejected/mismatched verifier verdict, equal baseline/candidate digests, remote target, or unscoped cleanup. GREEN: preflight resolves revision, two accepted distinct digests, projects, gates, ports, cleanup, and rollback. | `feat(release): add local promotion and rollback` |
| `T-DRE-002` | Make the sample Compose service project-scopable and implement baseline/canary health. | `examples/sample-web-service/docker-compose.yml`; `README.md`; `service.md`; delivery override/wrapper/tests. | `DRE-001`, `DRE-003` | RED: fixed `name`/`container_name` prevents parallel projects or canary starts without an accepted Spec 126 verdict. GREEN: separate projects use the verified digest and pass container plus HTTP marker health before promotion. | Same DRE commit. |
| `T-DRE-003` | Implement promotion record, failure injection, previous-digest rollback, and cleanup. | The wrapper, typed fixtures/tests, and ignored runtime evidence. | `DRE-002`, `DRE-004` | RED: promotion succeeds without complete gates/record or rollback cannot restore the previous digest. GREEN: local record is complete; injected failure rolls back and post-rollback health passes. | Same DRE commit. |
| `T-DRE-004` | Update the narrow release-management handoff and complete reviews. | `docs/05.operations/runbooks/00-workspace/release-management.md`; domain Task; lifecycle/index updates only when supported. | `VAL-DRE-001`–`004` | Specification and release/security reviews finish C0/I0/M0. | Program closure evidence commit. |

### Implementation contract

The wrapper accepts only these subcommands:

```text
rehearse-sample-service-delivery.sh preflight --task-id 2026-07-19-dre --baseline-verdict tests/fixtures/sample-service-delivery/spec126-verdict.baseline.accepted.json --candidate-verdict tests/fixtures/sample-service-delivery/spec126-verdict.candidate.accepted.json
rehearse-sample-service-delivery.sh rehearse --task-id 2026-07-19-dre --baseline-verdict _workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.baseline.json --candidate-verdict _workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.candidate.json --failure-mode none
rehearse-sample-service-delivery.sh rehearse --task-id 2026-07-19-dre-negative --baseline-verdict _workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.baseline.json --candidate-verdict _workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.candidate.json --failure-mode canary-health-timeout
rehearse-sample-service-delivery.sh cleanup --task-id 2026-07-19-dre
rehearse-sample-service-delivery.sh cleanup --task-id 2026-07-19-dre-negative
```

`--task-id` must match `^[a-z0-9-]+$`. The wrapper creates
project names by combining `hyhome-dre-20260719-`, its decimal process ID, and
`-baseline`/`-canary`; both resolved names must match
`^hyhome-dre-20260719-[0-9]+-(baseline|canary)$` and are recorded before
startup. Preflight rejects any resolved name outside that pattern. Cleanup
accepts and removes only the exact baseline/canary pair recorded for the task
run; a missing, additional, or nonmatching project fails closed.
It automatically loads the program-contract readiness and recovery verdict
paths from the orchestration Plan; missing or non-passing readiness fails
preflight, while the synthetic recovery verdict is recorded only as a boundary.
Exit classes are `0=pass`, `2=usage`, `10=verdict/preflight`, `20=baseline`,
`30=canary/health`, `40=promotion record`, `50=rollback`, and `60=cleanup`.

The sample Compose change deletes only top-level `name` and service
`container_name`; build, hardening, healthcheck, resource, logging, and network
semantics remain unchanged. The delivery override sets `image` from the
verified local image config digest, disables `build`, adds task/role labels,
sets `pull_policy: never`, and maps baseline/canary to loopback ports
`18080`/`18081`. Before either start, the wrapper performs bounded local-only
image inspection for both digests and requires exactly one object whose `.Id`
equals the accepted config digest; starts also use `--pull never --no-build`.

Both input verdicts use the exact Spec 126 schema. Preflight requires:

- producer `spec:126-security-supply-chain-remediation`;
- roles `baseline` and `candidate` respectively;
- equal 40-hex source revisions;
- two different image config and archive digests;
- policy `sample-service-local-v1`;
- `verdict=accepted`, `exception_id=null`, and `redaction_status=passed`.

Required wrapper symbols and order:

```bash
parse_subcommand
load_and_validate_verdict baseline
load_and_validate_verdict candidate
assert_distinct_subjects_and_same_revision
validate_local_image_object
validate_local_image_objects
assert_ports_and_owned_project_names
start_baseline
wait_container_and_http_health baseline
start_canary
wait_container_and_http_health candidate
record_promotion_decision
inject_canary_timeout_when_requested
rollback_to_baseline_digest
verify_post_rollback_health
write_rehearsal_record
cleanup_owned_projects
```

In-process cleanup first proves exact all-versus-owned container/network IDs,
single-resource cardinality, and zero volumes, then removes only those exact
IDs. Standalone cleanup rejects absent, incomplete, additional, or nonmatching
project pairs with class `60`; it never treats missing resources as success.

HTTP acceptance requires status 200 and the literal marker
`<h1>sample-web-service</h1>`; tracked evidence records only marker presence,
not the response body. `canary-health-timeout` overrides only the canary health
probe, prohibits promotion, stops the canary, verifies the baseline previous
digest and health, and returns the stable expected failure class `30` while
cleanup remains `passed`.

`rehearsal-record.json` has exactly these top-level keys:

```json
{
  "schema_version": 1,
  "producer_spec": "spec:127-deployment-release-engineering-remediation",
  "release_rehearsal_id": "local-rehearsal-20260719-0123456789ab",
  "source_revision": "0123456789abcdef0123456789abcdef01234567",
  "baseline_verdict_ref": "verification-verdict.baseline.json",
  "candidate_verdict_ref": "verification-verdict.candidate.json",
  "readiness_verdict_ref": "readiness-verdict.json",
  "baseline_project": "hyhome-dre-20260719-12345-baseline",
  "canary_project": "hyhome-dre-20260719-12345-canary",
  "promotion_decision": "promoted",
  "rollback_decision": "not_required",
  "post_rollback_health": "not_applicable",
  "data_impact": "none",
  "recovery_boundary_ref": "recovery-verdict.json",
  "cleanup_status": "passed",
  "remote_non_goals_confirmed": true
}
```

Tests expose `test_rejects_fixed_compose_identity`,
`test_rejects_missing_rejected_or_mismatched_verdict`,
`test_rejects_equal_baseline_candidate_subjects`,
`test_requires_same_source_revision`, `test_rejects_remote_image_reference`,
`test_health_requires_container_and_http_marker`,
`test_promotion_record_requires_all_gates`,
`test_failure_mode_rolls_back_previous_digest`,
`test_cleanup_accepts_only_owned_projects`, and
`test_rehearsal_record_schema`.

## Sequence

- [x] Create the active Task with the Spec 126 verdict dependency, Spec 124
      readiness boundary, Spec 125 data handoff, exact project identities,
      ports, health criteria, rollback, cleanup, and redaction.
- [x] Write failing tests in
      `tests/validation/test_sample_service_delivery_rehearsal.py` for fixed
      container identity, missing/rejected/mismatched verdict, mutable digest,
      port collision, failed health, partial promotion, incomplete record,
      rollback failure, and cleanup ambiguity.
- [x] Run
      `python3 -m unittest tests.validation.test_sample_service_delivery_rehearsal -v`
      and confirm failure before the wrapper/fixtures exist.
- [x] Remove fixed project/container identity from the sample Compose file,
      update its contract docs, implement fixtures and wrapper `preflight`, and
      rerun focused tests until static positive/negative cases pass.
- [x] Run
      `bash scripts/operations/rehearse-sample-service-delivery.sh preflight --task-id 2026-07-19-dre --baseline-verdict tests/fixtures/sample-service-delivery/spec126-verdict.baseline.accepted.json --candidate-verdict tests/fixtures/sample-service-delivery/spec126-verdict.candidate.accepted.json`.
- [ ] Run
      `bash scripts/operations/rehearse-sample-service-delivery.sh rehearse --task-id 2026-07-19-dre --baseline-verdict _workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.baseline.json --candidate-verdict _workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.candidate.json --failure-mode none`.
- [ ] Run
      `bash scripts/operations/rehearse-sample-service-delivery.sh rehearse --task-id 2026-07-19-dre-negative --baseline-verdict _workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.baseline.json --candidate-verdict _workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.candidate.json --failure-mode canary-health-timeout`
      and require rollback to the previous digest plus post-rollback health.
- [ ] Run
      `bash scripts/operations/rehearse-sample-service-delivery.sh cleanup --task-id 2026-07-19-dre`
      and the matching `2026-07-19-dre-negative` cleanup; reject unowned
      resources rather than deleting them.
- [x] Record only concise digest, revision, gate, project, health,
      promotion/rollback, cleanup, and data-impact fields in the Task.
- [ ] Run independent specification review, then release/security review; fix
      and re-review all findings before lifecycle closure.

Implementation, focused/static validation, and fixture-only preflight are
complete. The positive and injected-failure runtime commands remain unchecked:
Spec 126 truthfully rejected the baseline at 14 critical vulnerabilities with
no approved exception, so the required accepted canonical pair is absent. The
runtime path therefore stops at class `10` before Docker/Compose and publishes
no rehearsal record; runtime evidence and review results remain Task-owned.

## Verification Plan

| Gate | Command / method | Expected pass evidence |
| --- | --- | --- |
| Metadata and lifecycle | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 758aa0d2` | Changed Stage 04 docs remain valid. |
| Traceability | `bash scripts/validation/check-doc-traceability.sh` and `bash scripts/validation/check-doc-implementation-alignment.sh` | `DRE-001`–`DRE-004` map to implemented files and Task evidence. |
| Repository contract | `bash scripts/validation/check-repo-contracts.sh` | No new contract breakage. |
| Fixture/unit tests | `python3 -m unittest tests.validation.test_sample_service_delivery_rehearsal -v` | Gate, promotion, record, and rollback fixtures pass. |
| Local runtime rehearsal | the four exact wrapper commands in Sequence | Canary, promotion, health, local rehearsal record, rollback, and cleanup pass. |
| Review | Independent spec and quality/security review | C0/I0/M0 or all findings resolved and re-reviewed. |

## Risks and Rollback

| Risk | Impact | Mitigation / rollback |
| --- | --- | --- |
| Mutable or unverified artifact promoted | Critical | Require Spec 126 digest/verifier verdict; reject tags without digest. |
| Local rehearsal confused with production release | High | Evidence labels local-only; no GitHub Release or environment mutation. |
| Partial promotion without rollback | Critical | Previous digest is mandatory input; injected failure proves rollback. |
| Health gate too shallow | High | Health probes are explicit and independent from build success. |
| Data rollback overclaim | Critical | Config/application rollback only; data impact routes to Spec 125. |

Rollback is by running the task-owned rollback wrapper to the previous digest,
then reverting the logical commit if implementation files must be removed.
Cleanup may remove only task-owned local projects, networks, and containers.

## Approval Gates

- Human approval exists for this active Plan conversion.
- The future Task must approve exact local runtime commands, artifact digest,
  health gates, ports, project names, cleanup, and rollback before execution.
- GitHub Environments/Releases, workflow mutation, registry push, remote
  deployment, OIDC/secret identity, and production targets remain unapproved.

## Completion Criteria

- [x] Active Task maps `DRE-001`–`DRE-004` to exact files, commands, rollback,
      redaction, and reviews.
- [x] Dry-run/preflight and fixtures reject mutable artifact, missing verifier,
      failed health, missing record, and rollback failure.
- [ ] Local canary starts only with a verified digest and health gate.
- [ ] Promotion produces a local release/deployment evidence record.
- [ ] Injected failure rolls back to previous digest and post-rollback health
      passes.
- [ ] Independent specification and quality/security reviews pass.
- [ ] Spec 127 lifecycle reflects only local delivery mechanics; remote,
      production, registry, GitHub Release, and environment exclusions remain
      explicit.

## Related Documents

- **PRD**: [Operational readiness closure](../../01.requirements/025-operational-readiness-closure.md)
- **ARD**: [Operational readiness closure architecture](../../02.architecture/requirements/0028-operational-readiness-closure.md)
- **ADR**: [ADR-0028 local-isolated readiness evidence](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
- **Spec**: [Spec 127](../../03.specs/127-deployment-release-engineering-remediation/spec.md)
- **Runtime dependency**: [Spec 124](../../03.specs/124-compose-runtime-readiness-remediation/spec.md)
- **Recovery dependency**: [Spec 125](../../03.specs/125-infrastructure-operations-readiness-remediation/spec.md)
- **Security dependency**: [Spec 126](../../03.specs/126-security-supply-chain-remediation/spec.md)
- **Sample service Compose file**: [examples/sample-web-service/docker-compose.yml](../../../examples/sample-web-service/docker-compose.yml)
