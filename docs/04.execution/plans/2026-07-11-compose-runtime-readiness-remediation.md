---
status: active
artifact_id: plan:2026-07-11-compose-runtime-readiness-remediation
artifact_type: plan
parent_ids:
  - prd:025-operational-readiness-closure
  - ard:0028-operational-readiness-closure
  - adr:0028-local-isolated-readiness-evidence
  - spec:124-compose-runtime-readiness-remediation
---

# Compose Runtime Readiness Remediation Implementation Plan

## Overview

This active plan turns Spec 124 into an executable local implementation sequence
for the exact `core` five-service Compose set: `keycloak`, `oauth2-proxy`,
`traefik`, `vault`, and `vault-agent`. It remains prospective. Actual startup,
readiness, recovery, teardown, review, and commit evidence belongs in the
future sibling Task.

The implementation goal is local-isolated evidence only. The plan does not
authorize production startup, default-profile expansion, host-global cleanup,
secret-value inspection, remote observability, registry access, or deployment.

## Context and Inputs

Inputs:

- [PRD 025](../../01.requirements/025-operational-readiness-closure.md)
- [ARD 0028](../../02.architecture/requirements/0028-operational-readiness-closure.md)
- [ADR 0028](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
- [Spec 124](../../03.specs/124-compose-runtime-readiness-remediation/spec.md)
- root [docker-compose.yml](../../../docker-compose.yml)
- [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh)
- existing static evidence in
  [compose-profile-service-coverage.md](../../90.references/data/docker/compose-profile-service-coverage.md)

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
| `T-CRR-001` | Define the Compose runtime acceptance harness and evidence schema. | `scripts/validation/compose-runtime-readiness.*`, `scripts/validation/fixtures/compose-runtime/**`, `_workspace/repo-support/README.md` if needed, Task evidence file. | `CRR-001`–`CRR-003` | RED: missing/ambiguous service set, missing teardown, or schema rejection. GREEN: dry-run/preflight emits exact project/services/timeouts/cleanup plan. | `feat(harness): add compose runtime acceptance` |
| `T-CRR-002` | Add isolated five-service startup and readiness checks. | Same harness plus focused tests; no root Compose default expansion unless review requires a test-only overlay. | `CRR-001`, `CRR-002` | RED: service omitted, default project selected, endpoint unchecked, timeout mishandled. GREEN: wrapper starts only approved project, waits, probes endpoints, records result, tears down owned resources. | Same CRR commit unless split by review. |
| `T-CRR-003` | Add bounded failure/stop-path rehearsal and cleanup ambiguity handling. | Harness tests and task evidence. | `CRR-003` | RED: unowned cleanup allowed or failure recorded as success. GREEN: injected bounded failure recovers or fails closed with escalation class and owned cleanup attempt. | Same CRR commit unless split by review. |
| `T-CRR-004` | Independent reviews and SDLC closure for Spec 124 local scope. | Task evidence, Plan/README lifecycle updates only after evidence. | `VAL-CRR-001`–`004` | Spec review C0/I0/M0 and quality/security review C0/I0/M0. | `docs(evidence): record compose readiness closure` if separate evidence-only commit is needed. |

## Sequence

1. Create the active Task from
   [task.template.md](../../99.templates/templates/sdlc/task.template.md) with
   explicit protected-surface approval, runtime boundary, redaction boundary,
   rollback/cleanup, and skipped remote scope.
2. Implement dry-run/preflight first. It must resolve the exact worktree,
   Compose files, profile, five service names, project name, labels, timeouts,
   ports, transient directory, and teardown commands before any startup.
3. Add unit/fixture tests for service-set rejection, profile expansion, missing
   teardown, secret-bearing output rejection, timeout classification, and
   cleanup scope.
4. Run static Compose validation before runtime rehearsal:
   `bash scripts/validation/validate-docker-compose.sh`.
5. Execute one isolated runtime rehearsal only from the approved Task. The
   expected command class is `docker compose --profile core up --wait` with a
   task-scoped project name and timeout, followed by endpoint probes and owned
   teardown.
6. Execute one bounded failure/stop-path scenario. If recovery crosses into
   data restore, stop and hand off to Spec 125 instead of extending this lane.
7. Record only concise Task evidence: command class, exit status, service
   states, endpoint summaries, timing, cleanup result, and stable failure class.
8. Run independent specification review, then quality/security review. Fix
   findings in the same logical lane and re-run the same reviewers.

## Verification Plan

| Gate | Command / method | Expected pass evidence |
| --- | --- | --- |
| Metadata and lifecycle | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref <safe-base>` | Changed Stage 04 docs have valid metadata and no lifecycle regression. |
| Traceability | `bash scripts/validation/check-doc-traceability.sh` and `bash scripts/validation/check-doc-implementation-alignment.sh` | Spec 124 requirements map to Plan/Task and implemented files. |
| Repository contract | `bash scripts/validation/check-repo-contracts.sh` | No new contract breakage; pre-existing unrelated failures are recorded in the Task if present. |
| Static Compose | `bash scripts/validation/validate-docker-compose.sh` | Approved `core` render still resolves; static result remains labeled non-runtime. |
| Harness unit/fixture | Future focused test command owned by `T-CRR-001` | Negative and positive fixture cases pass. |
| Runtime rehearsal | Future Task-approved Docker command envelope | Only the five approved services start, reach readiness or bounded failure, and owned teardown completes. |
| Review | Independent spec and quality/security review | C0/I0/M0 or all findings resolved and re-reviewed. |

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

- Human approval already exists for converting the draft Plan to an active
  implementation plan.
- The future Task must still authorize each runtime command envelope before it
  is executed.
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
- [ ] Independent specification and quality/security reviews pass.
- [ ] Spec 124 lifecycle is updated only according to actual local evidence;
      remote/live exclusions remain explicit.

## Related Documents

- **PRD**: [Operational readiness closure](../../01.requirements/025-operational-readiness-closure.md)
- **ARD**: [Operational readiness closure architecture](../../02.architecture/requirements/0028-operational-readiness-closure.md)
- **ADR**: [ADR-0028 local-isolated readiness evidence](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
- **Spec**: [Spec 124](../../03.specs/124-compose-runtime-readiness-remediation/spec.md)
- **Infrastructure dependency**: [Spec 125](../../03.specs/125-infrastructure-operations-readiness-remediation/spec.md)
- **Docker Compose `up --wait` reference**: <https://docs.docker.com/reference/cli/docker/compose/up/>
- **Docker Compose startup-order reference**: <https://docs.docker.com/compose/how-tos/startup-order/>
