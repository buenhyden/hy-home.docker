---
status: active
artifact_id: task:2026-07-19-infrastructure-operations-readiness-remediation
artifact_type: task
parent_ids:
  - spec:125-infrastructure-operations-readiness-remediation
  - plan:2026-07-11-infrastructure-operations-readiness-remediation
---

# Task: Infrastructure Operations Readiness Remediation

## Overview

This active Task will record the synthetic local PostgreSQL 17-to-18 logical
backup, restore, integrity, upgrade, and negative-path rehearsal. At activation,
no database container has started, no dump or row data has been produced, and
no recovery or elapsed-time result is claimed.

The Task owns the concise
`_workspace/repo-support/task-2026-07-19-infrastructure-operations-readiness-remediation/postgres/recovery-verdict.json`
handoff. Dumps, row payloads, credentials, and raw database logs never enter
tracked evidence.

## Inputs

- [Spec 125](../../03.specs/125-infrastructure-operations-readiness-remediation/spec.md)
- [Infrastructure operations Plan](../plans/2026-07-11-infrastructure-operations-readiness-remediation.md)
- [Program Plan](../plans/2026-07-19-operational-readiness-closure-program.md)
- Exact PostgreSQL source/target pins and deterministic SQL contract in the Plan
- Spec 124 readiness semantics as an upstream runtime boundary

## Goals and Non-goals

Goals:

- prove a deterministic custom-format logical backup and separate restore;
- compare a metadata-only integrity oracle across PostgreSQL 17.6 and 18.4;
- reject checksum mismatch, partial state, wrong target major, timeout, unsafe
  paths, and project collisions with stable failure classes;
- record observed local backup/restore timing, checksums, cleanup, and redaction;
- provide a recovery-boundary verdict without making a deployment claim.

Non-goals:

- production/shared data, live Supabase/Spilo state, or `${DEFAULT_DATA_DIR}`;
- physical backup, PITR, HA, replication, retention, encryption-at-rest, remote
  storage, or organization RTO/RPO certification;
- secret-value, raw dump, row payload, registry, cloud, or deployment action.

## Scope and Change Boundaries

Allowed authored paths:

- `scripts/validation/rehearse-postgres-logical-upgrade.sh`;
- `tests/fixtures/postgres-logical-upgrade/**`;
- `tests/validation/test_postgres_logical_upgrade_rehearsal.py`;
- the bounded PostgreSQL rehearsal runbook and its direct index;
- this Task and directly supported lifecycle/index evidence during closure.

Allowed transient paths are `/tmp/hyhome-ior-evidence.<decimal-pid>` and the
exact program handoff directory. The dump remains under `/tmp`, is represented
only by SHA-256 and byte size, and is deleted after successful evidence capture.

Forbidden paths/actions: live databases, bind mounts, external networks,
restart policies, host ports, shared or named persistent volumes, remote backup
destinations, secret values, raw database output, and unscoped cleanup.

Compose impact: one test fixture with only `source` and `target`, anonymous
volumes, no host ports, no `container_name`, no external network, and no restart
policy.

Security impact: process-local synthetic password, no secret-value evidence,
checksum-only dump identity, and fail-closed path/project validation.

Operations impact: representative logical backup/restore mechanics and a
bounded runbook only. No live recovery authority, retention control, or RTO/RPO
commitment changes.

Runtime impact: task-scoped local PostgreSQL containers using only the pinned
images and synthetic fixture. Cleanup removes only owned projects, anonymous
volumes, and the task `/tmp` directory.

## Approval Evidence

Approval source:

- The user approved protected-surface changes and the local representative
  recovery implementation in this program.
- [ADR 0028](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md),
  [Spec 125](../../03.specs/125-infrastructure-operations-readiness-remediation/spec.md),
  and the active Plan approve the synthetic local topology.

Protected surfaces: the exact PostgreSQL test images, anonymous volumes,
synthetic SQL, `/tmp` dump/evidence, validation wrapper/tests, and bounded
runbook may change within the Plan. Live data, production volumes, remote
storage, credentials, and shared runtime remain protected.

Approval boundary: source is exactly
`postgres:17.6-alpine@sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94`;
target is exactly
`postgres:18.4-alpine@sha256:9a8afca54e7861fd90fab5fdf4c42477a6b1cb7d293595148e674e0a3181de15`.
Commands are normal execution, `--check`, or one
`--negative-case checksum-mismatch|partial-state|bad-target-major|timeout`.
Changed image, data, storage, target, or cleanup requires stop and new approval.

Rollback or recovery: the wrapper trap removes only project-prefix resources
and its `/tmp` directory. Revert the single logical IOR commit to remove
authored changes. On ambiguous state or cleanup ownership, stop and retain only
concise non-secret evidence rather than deleting the database state.

Redaction boundary: tracked evidence may contain image pins, fixture/dump
checksums, dump size, aggregate oracle values/digests, observed timing, stable
failure class, cleanup, redaction, commits, and reviews. It must not contain the
dump, SQL row payloads, passwords, environment values, raw queries, or logs.

## Work Breakdown

| Task ID | Description | Parent requirement | Validation / evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| `T-IOR-001` | Fixture, oracle, wrapper, verdict, and tests | `IOR-001`–`IOR-004` | Focused RED/GREEN suite and `--check` | Fresh implementation agent | Not run |
| `T-IOR-002` | Logical backup and isolated restore | `IOR-003`, `IOR-004` | Dump, restore, oracle, timing, cleanup | Fresh implementation agent | Not run |
| `T-IOR-003` | 17-to-18 and corrupted/partial negative paths | `IOR-001`, `IOR-002` | Stable failures and cleanup disposition | Fresh implementation agent | Not run |
| `T-IOR-004` | Bounded runbook and independent reviews | `VAL-IOR-001`–`004` | Spec plus operations/security C0/I0/M0 | Separate reviewers | Not run |

## Work Log

| Date | Work unit | Result |
| --- | --- | --- |
| 2026-07-19 | Task activation | Contract recorded; no database runtime, dump, restore, or destructive action executed. |
| 2026-07-19 | `T-IOR-001`–`T-IOR-004` | `not_run`; actual evidence is appended only after exact execution. |

## Verification Evidence

Exact command envelope:

```bash
python3 -m unittest tests.validation.test_postgres_logical_upgrade_rehearsal -v
bash scripts/validation/rehearse-postgres-logical-upgrade.sh --check
bash scripts/validation/rehearse-postgres-logical-upgrade.sh
bash scripts/validation/rehearse-postgres-logical-upgrade.sh --negative-case checksum-mismatch
bash scripts/validation/rehearse-postgres-logical-upgrade.sh --negative-case partial-state
```

The implemented wrapper may also execute the planned negative cases
`bad-target-major` and `timeout`; both must fail non-zero and still apply the
owned cleanup rule.

Expected evidence: focused positive/negative tests pass; the normal rehearsal
uses `pg_dump -Fc --no-owner --no-acl` and
`pg_restore --clean --if-exists --no-owner --no-acl`; source and target oracles
match on all integrity fields except declared server version; the verdict has
`scope=synthetic-local`, `integrity_status=passed`,
`cleanup_status=passed`, and `redaction_status=passed`.

Actual evidence: `not_run`.

Verification results: `not_run`. Exit classes are `0=pass`, `2=usage`,
`10=preflight`, `20=readiness`, `30=backup`, `40=restore`,
`50=integrity/negative case`, and `60=cleanup`.

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

Specification review verdict: `not_run`; a fresh reviewer must verify Spec 125,
image pins, fixture/oracle schema, backup/restore separation, negative cases,
verdict schema, and data/remote exclusions.

Quality/security review verdict: `not_run`; a separate reviewer must check
shell/SQL safety, path/project ownership, cleanup, redaction, error handling,
tests, and runbook limits.

Findings and disposition: none because review has not run. All findings must be
remediated and re-reviewed to C0/I0/M0.

## Commit Ledger

Commit identity: `not_committed`.

Logical unit: `feat(ops): add postgres recovery rehearsal`.

Commit validation: `not_run`; record focused tests, normal/negative rehearsal,
checksums/timing, cleanup, runbook validation, and review after commit.

## Deferred and Blocked Items

Deferred items: live data, physical backup, PITR, HA/replication, remote
storage, retention/encryption certification, production recovery, and
organization RTO/RPO.

Blocked items: runtime remains blocked until fixture/tests and `--check` pass.
Delivery may reference this verdict only as a recovery boundary and must not
claim database recovery for the stateless sample service.

Deferral destination: broader/live recovery requires a new approved Stage
01-04 chain and operations/security review. Stateful delivery impact routes to
[Spec 125](../../03.specs/125-infrastructure-operations-readiness-remediation/spec.md)
rather than expanding Spec 127.

## Related Documents

- [Spec 125](../../03.specs/125-infrastructure-operations-readiness-remediation/spec.md)
- [Infrastructure Plan](../plans/2026-07-11-infrastructure-operations-readiness-remediation.md)
- [Program Task](./2026-07-19-operational-readiness-closure-program.md)
- [Compose Task](./2026-07-19-compose-runtime-readiness-remediation.md)
- [Delivery Task](./2026-07-19-deployment-release-engineering-remediation.md)
