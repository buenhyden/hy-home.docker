---
status: active
artifact_id: task:2026-07-19-compose-runtime-readiness-remediation
artifact_type: task
parent_ids:
  - spec:124-compose-runtime-readiness-remediation
  - plan:2026-07-11-compose-runtime-readiness-remediation
---

# Task: Compose Runtime Readiness Remediation

## Overview

This active Task will record implementation and execution evidence for the
exact local-isolated `core` service set: `keycloak`, `oauth2-proxy`, `traefik`,
`vault`, and `vault-agent`. At activation, no service has been started and no
readiness, recovery, timeout, or cleanup result is claimed.

The Task owns the concise
`_workspace/repo-support/task-2026-07-19-compose-runtime-readiness-remediation/compose/readiness-verdict.json`
handoff. Raw logs and synthetic secret bodies are not evidence consumers.

## Inputs

- [Spec 124](../../03.specs/124-compose-runtime-readiness-remediation/spec.md)
- [Compose runtime readiness Plan](../plans/2026-07-11-compose-runtime-readiness-remediation.md)
- [Program Plan](../plans/2026-07-19-operational-readiness-closure-program.md)
- Root `docker-compose.yml` and the approved task-only override
- Static Compose validation and profile/service inventory

## Goals and Non-goals

Goals:

- prove startup and initialization for only the exact five services;
- observe container and service-specific endpoint readiness;
- prove a bounded Vault restart recovery and a stable timeout stop path;
- verify cleanup of only the wrapper-created project and task-owned paths;
- emit a redacted, typed readiness verdict for the delivery Task.

Non-goals:

- production/shared-host readiness, default-profile expansion, or any sixth
  service;
- use of external `mng-pg`, `mng-valkey`, `k3d-hyhome`, host ports 80/443, or
  repository data-volume paths;
- data restore, registry access, remote observability, deployment, or secret
  value inspection.

## Scope and Change Boundaries

Allowed authored paths:

- `scripts/validation/run-compose-core-readiness.sh`;
- `scripts/validation/compose-core-readiness.lib.sh`;
- `tests/fixtures/compose-core-readiness/**`;
- `tests/validation/test_compose_core_readiness.py`;
- this Task and directly supported lifecycle/index evidence during closure.

Allowed transient path: only
`_workspace/repo-support/task-2026-07-19-compose-runtime-readiness-remediation/`.
Synthetic secret files and raw diagnostics stay under `/tmp` or task-owned
ignored storage and their bodies are never promoted.

Forbidden paths/actions: shared Docker resources, fixed or nonmatching project
names, external networks/databases/session stores, broad cleanup, root
repository data mounts, live secrets, remote targets, and deployment.

Compose impact: a test-only override may change the rendered local model. The
root production render remains unchanged. The override publishes only loopback
ports `18000`, `18443`, `18082`, `18083`, and `18200`.

Security impact: synthetic local credentials, read-only Docker socket exposure
for Traefik, no secret-body evidence, and fail-closed project ownership checks.

Operations impact: local startup/readiness/recovery observation only. Stateful
restore or ambiguous teardown stops and escalates.

Runtime impact: the wrapper creates one project named
`hyhome-crr-20260719-<decimal-pid>`, starts only the exact service set, and
removes only resources matching its owned project identity.

## Approval Evidence

Approval source:

- The user approved protected-surface changes and implementation of the local
  operational-readiness program.
- [ADR 0028](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md),
  [Spec 124](../../03.specs/124-compose-runtime-readiness-remediation/spec.md),
  and the active Plan define the accepted isolated topology and exact commands.

Protected surfaces: local Docker runtime, test-only Compose override, synthetic
secret files, high loopback ports, validation scripts, tests, and concise
runtime evidence are authorized. Shared/production runtime, live state,
credential values, remote targets, and broad cleanup are not authorized.

Approval boundary: the only runtime command forms are `--preflight`,
`--scenario startup-readiness`, `--scenario vault-restart-recovery`,
`--scenario negative-timeout`, and owned `--cleanup-only --project-name` with
project regex `^hyhome-crr-20260719-[0-9]+$`. Any changed service, port,
network, path, target, or failure injection requires stop and new approval.

Rollback or recovery: the wrapper trap and explicit cleanup may remove only
the matching project and task-owned paths. Revert the one logical harness
commit to remove authored changes. If ownership or state is ambiguous, stop,
preserve concise non-secret evidence, and do not prune or delete resources.

Redaction boundary: record service states, endpoint verdicts, elapsed time,
stable exit class, cleanup, and redaction result. Never record synthetic secret
bodies, raw environment, raw logs, tokens, credentials, response bodies, or
private endpoint payloads.

## Work Breakdown

| Task ID | Description | Parent requirement | Validation / evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| `T-CRR-001` | Wrapper, override, synthetic environment, and verdict contract | `CRR-001`–`CRR-003` | Focused RED/GREEN tests and preflight | Fresh implementation agent | Not run |
| `T-CRR-002` | Exact five-service startup and endpoint readiness | `CRR-001`, `CRR-002` | Startup/readiness scenario and typed verdict | Fresh implementation agent | Not run |
| `T-CRR-003` | Vault restart, timeout, and cleanup ambiguity | `CRR-003` | Recovery and expected non-zero timeout scenarios | Fresh implementation agent | Not run |
| `T-CRR-004` | Independent specification and quality/security review | `VAL-CRR-001`–`004` | C0/I0/M0 re-review | Separate reviewers | Not run |

## Work Log

| Date | Work unit | Result |
| --- | --- | --- |
| 2026-07-19 | Task activation | Contract recorded; no Compose command or service runtime executed. |
| 2026-07-19 | `T-CRR-001`–`T-CRR-004` | `not_run`; append actual commands and outcomes only after execution. |

## Verification Evidence

Exact command envelope:

```bash
python3 -m unittest tests.validation.test_compose_core_readiness -v
bash scripts/validation/validate-docker-compose.sh
bash scripts/validation/run-compose-core-readiness.sh --preflight
bash scripts/validation/run-compose-core-readiness.sh --scenario startup-readiness
bash scripts/validation/run-compose-core-readiness.sh --scenario vault-restart-recovery
bash scripts/validation/run-compose-core-readiness.sh --scenario negative-timeout
```

An explicit recovery-only cleanup may use:

```bash
bash scripts/validation/run-compose-core-readiness.sh --cleanup-only --project-name hyhome-crr-20260719-<decimal-pid>
```

Expected evidence: focused tests pass; static Compose validation remains
labeled static; positive scenarios produce the exact five-service verdict with
`overall_status=ready`, `cleanup_status=passed`, and
`redaction_status=passed`; the negative timeout returns class `30`, records
`overall_status=timed_out`, and still verifies cleanup.

Actual evidence: `not_run`.

Verification results: `not_run`. Exit classes are `0=pass`, `2=usage`,
`10=preflight/scope`, `20=startup`, `30=readiness`, `40=recovery`, and
`50=cleanup ambiguity`.

## Controlled Agent Pre-commit Evidence

Controlled wrapper command: not owned by this domain Task. The program Task
owns the single final all-files invocation after all domains and reviews pass.

Allowed prefixes: `not_applicable` at domain activation.

Wrapper exit status: `not_run`.

Snapshot result and path sets: `not_run`.

Observation boundary: if the program wrapper later runs, it observes only
Git-visible, non-ignored repository paths.

Disposition: defer to the
[program Task](./2026-07-19-operational-readiness-closure-program.md); never run
`pre-commit run --all-files` directly.

## Review Evidence

Implementation review verdict: `not_run`.

Specification review verdict: `not_run`; fresh reviewer must check Spec 124,
the Plan, exact service/port/path set, negative cases, and verdict schema.

Quality/security review verdict: `not_run`; a separate reviewer must check
shell safety, scope assertions, secret handling, teardown, tests, and evidence.

Findings and disposition: none because review has not run. All C/I/M findings
must be remediated and re-reviewed to C0/I0/M0.

## Commit Ledger

Commit identity: `not_committed`.

Logical unit: `feat(harness): add compose runtime acceptance`.

Commit validation: `not_run`; record focused tests, static Compose validation,
runtime scenarios, cleanup, and reviewer verdicts after the commit exists.

## Deferred and Blocked Items

Deferred items: production/shared-host startup, broader profiles, data restore,
remote observability, registry access, deployment, and live secret integration.

Blocked items: runtime execution remains blocked until the harness and RED tests
exist, preflight resolves the exact service/resource model, and no scope drift
is present.

Deferral destination: data restore routes to [Spec 125](../../03.specs/125-infrastructure-operations-readiness-remediation/spec.md);
remote or broader runtime requires a new approved design chain and Task.

## Related Documents

- [Spec 124](../../03.specs/124-compose-runtime-readiness-remediation/spec.md)
- [Compose Plan](../plans/2026-07-11-compose-runtime-readiness-remediation.md)
- [Program Task](./2026-07-19-operational-readiness-closure-program.md)
- [Infrastructure Task](./2026-07-19-infrastructure-operations-readiness-remediation.md)
- [Delivery Task](./2026-07-19-deployment-release-engineering-remediation.md)
