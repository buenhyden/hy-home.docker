---
status: archived
artifact_id: plan-0090
artifact_type: archive
parent_ids: []
archived_from: docs/04.execution/plans/2026-07-11-compose-runtime-readiness-remediation.md
archived_at: 2026-08-11
archive_reason: "Move baseline completed source to stable typed target docs/98.archive/changes/chg-0090-compose-runtime-readiness-remediation/plan.md; migrate 8 resolved inbound link(s) with it."
archive_disposition: evidence-preserve
archived_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
archived_blob: 75a7fa8a70eead86974b1c80e43809fc147bc31d
preservation_class: git-history
---
# Compose Runtime Readiness Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` (recommended) or
> `superpowers:executing-plans` to implement this plan task-by-task. Steps use
> checkbox syntax in the Sequence section.

**Goal:** Produce repeatable local startup, readiness, bounded failure, and
owned-teardown evidence for the exact five-service `core` path.

**Architecture:** A task-owned override replaces shared hosts, ports, networks,
volumes, and secrets with synthetic isolated inputs. A single wrapper renders
and asserts scope before startup, classifies service and endpoint readiness,
executes one Vault restart recovery and one timeout stop path, and cleans only
the unique Compose project it created.

**Tech Stack:** Docker Compose; Bash; Python `unittest`; the existing root
Compose graph; ignored `_workspace/repo-support` runtime evidence.

## Global Constraints

- Resolve exactly `keycloak`, `oauth2-proxy`, `traefik`, `vault`, and
  `vault-agent`; fail closed on any additional service.
- Do not use the production root render unmodified: it references shared
  `mng-pg`, `mng-valkey`, host ports 80/443, `k3d-hyhome`, and repository volume
  paths.
- Use synthetic secret files only; never print file bodies or raw logs.
- Cleanup is limited to the wrapper-created project and task-owned paths.

Target host class: a local Docker Engine reached from a linked Git worktree,
with at least 4 logical CPUs, 4 GiB available memory, and 8 GiB available
storage before rehearsal. Remote engines, shared CI runners, and production
hosts are outside this plan.

Resource limits: the task-only override caps `keycloak` at 1.00 CPU/768 MiB;
`oauth2-proxy`, `traefik`, and `vault` at 0.50 CPU/256 MiB each; and
`vault-agent` at 0.25 CPU/128 MiB. The approved aggregate ceiling is 2.75 CPUs
and 1,664 MiB. A changed limit or host class requires a new Task approval.

## Overview

This active transition plan defines the approved local implementation order,
risks, and acceptance gates for Spec 124. The sequence covers the exact `core`
five-service Compose set: `keycloak`, `oauth2-proxy`, `traefik`, `vault`, and
`vault-agent`. Observed execution and lifecycle evidence belongs only in the
[domain Task](task.md).

The implementation goal is local-isolated evidence only. The plan does not
authorize production startup, default-profile expansion, host-global cleanup,
secret-value inspection, remote observability, registry access, or deployment.

## Context and Inputs

Inputs:

- [PRD 025](../../../01.requirements/prd-025-operational-readiness-closure.md)
- [Architecture Description 0028](../../../02.architecture/descriptions/ad-0028-operational-readiness-closure.md)
- [ADR 0028](../../../02.architecture/decisions/adr-0028-local-isolated-readiness-evidence.md)
- [Spec 124](../../tombstones/03.specs/spec-0124-compose-runtime-readiness-remediation.md)
- root [docker-compose.yml](../../../../docker-compose.yml)
- [validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh)
- existing static evidence in
  [compose-profile-service-coverage.md](../../../90.references/data/docker/compose-profile-service-coverage.md)

Official behavior anchors:

- Docker documents `docker compose up --wait` as waiting for services to be
  running or healthy and implying detached mode.
- Docker documents that ordinary startup order does not mean service readiness;
  `depends_on.condition: service_healthy` waits for dependency healthchecks.

Planning implication: the runtime harness must combine `docker compose
--profile core up --wait` with service-specific endpoint assertions. A passing
container health state alone is not sufficient for `CRR-002`.

## Goals and Non-goals

Goals:

- Prove `CRR-001` startup/initialization for only the approved five services.
- Prove `CRR-002` observed readiness with endpoint/container criteria and
  explicit ready/degraded/failed/timed-out states.
- Prove `CRR-003` using one bounded local failure/recovery or stop-path
  scenario with deterministic teardown evidence.
- Produce task-owned wrapper, fixture, test, and evidence schema changes that
  reviewers can re-run.

Non-goals:

- No production/shared-host readiness claim.
- No broad `core` profile expansion beyond the five Spec 124 services.
- No secret-value read, raw log promotion, persistent data mutation, remote
  target, registry, or deployment action.
- No data restore claim; Spec 125 owns state recovery.

## Work Breakdown

| Unit | Purpose | Planned owned files | Requirements | RED/GREEN evidence | Commit boundary |
| --- | --- | --- | --- | --- | --- |
| `T-CRR-001` | Define the wrapper, override, synthetic environment, and evidence contract. | `scripts/validation/run-compose-core-readiness.sh`; `scripts/validation/compose-core-readiness.lib.sh`; `tests/fixtures/compose-core-readiness/compose.core-runtime.override.yml`; `tests/fixtures/compose-core-readiness/env.runtime.example`; `tests/validation/test_compose_core_readiness.py`; `docs/04.execution/tasks/2026-07-19-compose-runtime-readiness-remediation.md`. | `CRR-001`–`CRR-003` | RED: missing/ambiguous service set, shared path/port/network, missing teardown, or redaction failure. GREEN: preflight emits the exact project, services, timeouts, and cleanup plan. | `feat(harness): add compose runtime acceptance` |
| `T-CRR-002` | Add isolated five-service startup and readiness checks. | The same wrapper, library, override, and focused tests. | `CRR-001`, `CRR-002` | RED: omitted service, default project, endpoint unchecked, or timeout mishandled. GREEN: only the approved project starts, service and endpoint criteria are classified, and owned teardown completes. | Same CRR commit. |
| `T-CRR-003` | Add Vault restart recovery, negative timeout, and cleanup ambiguity handling. | The same wrapper/library/tests and Task evidence. | `CRR-003` | RED: unowned cleanup is allowed or a failure is recorded as success. GREEN: restart recovery passes; timeout fails with a stable non-zero class and still cleans owned resources. | Same CRR commit. |
| `T-CRR-004` | Complete independent reviews and local lifecycle evidence. | Domain Task, Specs/Plans indexes only when supported. | `VAL-CRR-001`–`004` | Every finding is resolved and independently re-reviewed before closure. | Evidence-only closure unit after approval. |

### Implementation contract

The wrapper CLI is closed to these forms:

```text
run-compose-core-readiness.sh --preflight
run-compose-core-readiness.sh --scenario startup-readiness
run-compose-core-readiness.sh --scenario vault-restart-recovery
run-compose-core-readiness.sh --scenario negative-timeout
run-compose-core-readiness.sh --cleanup-only --project-name hyhome-crr-20260719-12345-abcd1234
```

The wrapper itself constructs the project name from the fixed prefix
`hyhome-crr-20260719-`, its decimal process ID, and a collision-resistant
eight-character lowercase alphanumeric token derived from a `mktemp -d`
allocation and claimed with an atomic `mkdir`. User-supplied
project names are accepted only by `--cleanup-only` and must match
`^hyhome-crr-20260719-[0-9]+-[a-z0-9]{8}$`. Exit classes are `0=pass`, `2=usage`,
`10=preflight/scope`, `20=startup`, `30=readiness`, `40=recovery`, and
`50=cleanup ambiguity`.

Required library symbols and control flow:

```bash
parse_args
assert_linked_worktree
assert_docker_compose
prepare_owned_paths
prepare_synthetic_secrets
render_core_model
assert_exact_service_set
assert_isolated_paths_ports_networks
start_vault
initialize_unseal_and_configure_synthetic_vault
start_remaining_services
wait_container_health
probe_service_endpoint
write_readiness_verdict
cleanup_owned_project
```

`main` calls every assertion before the first `docker compose up`, installs an
`EXIT HUP INT TERM` trap that calls `cleanup_owned_project`, and dispatches only
the four modes above. `negative-timeout` must invert only the readiness
expectation: the wrapper returns `30`, writes `overall_status=timed_out`, then
requires cleanup success, and prints the scenario-specific evidence path. It
does not replace the ready canonical handoff consumed by Task 5.

The override must produce this isolated model:

| Service | Test-only replacement | Limit | Required acceptance |
| --- | --- | --- | --- |
| `keycloak` | direct `kc.sh start-dev`, `KC_DB=dev-file`, health enabled, task-owned data, no external PostgreSQL | 1.00 CPU / 768 MiB | container healthy plus HTTP ready endpoint |
| `oauth2-proxy` | cookie session store, synthetic client/cookie values, skip discovery with explicit local Keycloak URLs, no Valkey | 0.50 CPU / 256 MiB | container healthy plus `/ping` success |
| `traefik` | localhost high ports, isolated network only, file provider, no raw Docker socket, no `k3d-hyhome` | 0.50 CPU / 256 MiB | container health plus ping success |
| `vault` | task-owned file/raft data and synthetic init/unseal only | 0.50 CPU / 256 MiB | initialized, unsealed, active, HTTP health success |
| `vault-agent` | task-owned AppRole files and output, configured only after synthetic Vault initialization | 0.25 CPU / 128 MiB | process healthy and rendered non-secret sentinel exists |

The override must publish only loopback ports `18000`, `18443`, `18082`,
`18083`, and `18200`; preflight rejects host ports `80`/`443`, root repository
volume paths, external `mng-pg`/`mng-valkey`, `k3d-hyhome`, fixed
`container_name`, or any sixth service.

Each `readiness-verdict.<scenario>.json` record and the eligible ready
`readiness-verdict.json` handoff have exactly these top-level keys:

```json
{
  "schema_version": 2,
  "producer_spec": "spec:124-compose-runtime-readiness-remediation",
  "producer_task": "task:2026-07-19-compose-runtime-readiness-remediation",
  "approval_ref": "task:2026-07-19-compose-runtime-readiness-remediation#approval-2026-07-19",
  "scenario": "startup-readiness",
  "target_class": "local-linked-worktree-docker-engine",
  "project_name": "hyhome-crr-20260719-12345-abcd1234",
  "started_at": "2026-07-19T01:00:00Z",
  "completed_at": "2026-07-19T01:00:03Z",
  "services": {},
  "endpoint_verdicts": {},
  "observed_state": "ready",
  "recovery_status": "not_applicable",
  "teardown_status": "passed",
  "overall_status": "ready",
  "elapsed_seconds": 0,
  "cleanup_status": "passed",
  "redaction_status": "passed"
}
```

The startup and recovery scenarios write their own scenario records; after a
successful ready result, the wrapper atomically publishes that record as
`readiness-verdict.json`. Starting either positive scenario first invalidates
the prior canonical handoff, so a failed rerun cannot leave stale readiness.
The negative scenario writes only
`readiness-verdict.negative-timeout.json` and reports that exact path. Task 5
accepts the canonical handoff only when
`scenario=vault-restart-recovery`, `overall_status=ready`,
`recovery_status=passed`, `cleanup_status=passed`, and
`redaction_status=passed`, and `services` contains exactly `keycloak`,
`oauth2-proxy`, `traefik`, `vault`, and `vault-agent`.

Tests must expose methods named
`test_exact_five_service_allowlist`, `test_rejects_shared_paths_ports_networks`,
`test_synthetic_secret_bodies_never_reach_summary`,
`test_cleanup_accepts_only_owned_project_name`,
`test_runtime_identity_is_collision_resistant_and_symlink_safe`,
`test_endpoint_observations_are_complete_and_classified`,
`test_override_and_approval_contract_declare_resource_limits`,
`test_timeout_has_stable_exit_and_cleanup`, and
`test_readiness_verdict_schema`.

## Sequence

- [ ] Create the active Task from
   [task.template.md](../../../99.templates/templates/sdlc/task.template.md) with
   explicit protected-surface approval, runtime boundary, redaction boundary,
   rollback/cleanup, and skipped remote scope.
- [ ] Write failing tests in
   `tests/validation/test_compose_core_readiness.py` for exact service set,
   forbidden shared paths, external `k3d-hyhome`, ports 80/443, synthetic
   secret handling, scoped cleanup, timeout classification, and redaction.
- [ ] Run
   `python3 -m unittest tests.validation.test_compose_core_readiness -v` and
   confirm the new tests fail because the wrapper and fixture do not exist.
- [ ] Implement dry-run/preflight first. It must resolve the exact worktree,
   Compose files, profile, five service names, project name, labels, timeouts,
   ports, transient directory, and teardown commands before any startup.
- [ ] Run the focused tests until all positive and negative preflight cases pass.
- [ ] Run static Compose validation before runtime rehearsal:
   `bash scripts/validation/validate-docker-compose.sh`.
- [ ] Execute `bash scripts/validation/run-compose-core-readiness.sh --preflight`.
- [ ] Execute
   `bash scripts/validation/run-compose-core-readiness.sh --scenario startup-readiness`.
- [ ] Execute
   `bash scripts/validation/run-compose-core-readiness.sh --scenario vault-restart-recovery`.
- [ ] Execute
   `bash scripts/validation/run-compose-core-readiness.sh --scenario negative-timeout`;
    require the documented stable non-zero result and successful cleanup.
- [ ] If recovery crosses into
   data restore, stop and hand off to Spec 125 instead of extending this lane.
- [ ] Record only concise Task evidence: command class, exit status, service
   states, endpoint summaries, timing, cleanup result, and stable failure class.
- [ ] Run fresh independent specification review, then quality/security review
   for the independent image-identity controls. Fix findings in the
   same logical lane and re-run the same reviewers.

## Verification Plan

`$COMPARISON_BASE_REF` denotes the explicit reviewed comparison ref recorded by
the [Program Task](../chg-0100-operational-readiness-closure-program/task.md);
this Plan does not own a concrete base identity.

| Gate | Command / method | Expected pass evidence |
| --- | --- | --- |
| Metadata and lifecycle | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref "$COMPARISON_BASE_REF"` | Changed Stage 04 docs have valid metadata and no lifecycle regression. |
| Traceability | `bash scripts/validation/check-doc-traceability.sh` and `bash scripts/validation/check-doc-implementation-alignment.sh` | Spec 124 requirements map to Plan/Task and implemented files. |
| Repository contract | `bash scripts/validation/check-repo-contracts.sh` | No new contract breakage; pre-existing unrelated failures are recorded in the Task if present. |
| Static Compose | `bash scripts/validation/validate-docker-compose.sh` | Approved `core` render still resolves; static result remains labeled non-runtime. |
| Harness unit/fixture | `python3 -m unittest tests.validation.test_compose_core_readiness -v` | Negative and positive fixture cases pass. |
| Runtime rehearsal | the four exact wrapper commands in Sequence | Only the five approved services start, reach readiness or bounded failure, and owned teardown completes. |
| Review | Independent spec and quality/security review | All findings are resolved and independently re-reviewed. |

The final all-files QA gate, if used for the overall closure chain, must use
`scripts/validation/run-agent-precommit-all-files.sh`; direct `pre-commit run`
is prohibited by Stage 00 governance.

## Risks and Rollback

| Risk | Impact | Mitigation / rollback |
| --- | --- | --- |
| Compose profile expands beyond five services | Critical | Resolve and assert exact services before startup; fail closed on drift. |
| Shared Docker resource mutation | Critical | Unique project name/labels; cleanup only resources matching both. |
| Secret or raw log exposure | Critical | No raw env/log promotion; redaction tests; concise evidence only. |
| Healthcheck passes but endpoint fails | High | Endpoint probes are separate acceptance checks; record degraded/failed. |
| Teardown leaves ambiguous state | High | Stop and escalate; no blind deletion outside owned labels. |

Rollback is by removing task-owned harness files, reverting the logical commit,
and running the owned cleanup command. Persistent data recovery is outside this
plan and routes to Spec 125.

## Approval Gates

- Plan activation requires recorded human approval.
- The active Task must authorize each runtime command envelope before execution.
- Secret values, remote targets, registry access, production services, and
  shared-host cleanup remain unapproved.

## Completion Criteria

- [ ] Active Task exists and maps `CRR-001`–`CRR-003` to exact files, commands,
      rollback, redaction, and reviews.
- [ ] Dry-run/preflight and fixture tests reject scope, teardown, timeout, and
      redaction violations.
- [ ] Static Compose validation passes and remains labeled static.
- [ ] Isolated five-service startup/readiness evidence is recorded.
- [ ] Bounded recovery/stop-path evidence is recorded.
- [ ] Independent specification and quality/security review acceptance for the
      independent image-identity controls is recorded in the Task after all
      findings are remediated and re-reviewed.
- [ ] Spec 124 lifecycle is updated only according to actual local evidence;
      remote/live exclusions remain explicit.

## Related Documents

- **PRD**: [Operational readiness closure](../../../01.requirements/prd-025-operational-readiness-closure.md)
- **ARD**: [Operational readiness closure architecture](../../../02.architecture/descriptions/ad-0028-operational-readiness-closure.md)
- **ADR**: [ADR-0028 local-isolated readiness evidence](../../../02.architecture/decisions/adr-0028-local-isolated-readiness-evidence.md)
- **Spec**: [Spec 124](../../tombstones/03.specs/spec-0124-compose-runtime-readiness-remediation.md)
- **Infrastructure dependency**: [Spec 125](../../tombstones/03.specs/spec-0125-infrastructure-operations-readiness-remediation.md)
- **Docker Compose `up --wait` reference**: <https://docs.docker.com/reference/cli/docker/compose/up/>
- **Docker Compose startup-order reference**: <https://docs.docker.com/compose/how-tos/startup-order/>
