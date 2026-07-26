---
status: completed
artifact_id: plan:2026-07-11-infrastructure-operations-readiness-remediation
artifact_type: plan
parent_ids:
  - prd:025-operational-readiness-closure
  - ard:0028-operational-readiness-closure
  - adr:0028-local-isolated-readiness-evidence
  - spec:125-infrastructure-operations-readiness-remediation
---

# Infrastructure Operations Readiness Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` (recommended) or
> `superpowers:executing-plans` to implement this plan task-by-task. Sequence
> steps become Task evidence only after execution.

**Goal:** Prove a synthetic PostgreSQL 17-to-18 logical backup, restore,
integrity, negative-path, and observed-recovery rehearsal without touching live
workspace databases.

**Architecture:** A repository-owned Compose fixture runs separate task-scoped
source and target PostgreSQL services. A single wrapper seeds deterministic SQL,
captures a custom-format dump, restores it into the newer major, compares a
metadata-only integrity oracle, injects corruption/partial-state failures, and
cleans only its projects and exclusively owned `/tmp` artifacts. Before runtime
it validates the complete machine-readable Compose render and reserves cleanup
time inside one end-to-end deadline.

**Tech Stack:** PostgreSQL `17.6-alpine` and `18.4-alpine`; Docker Compose; Bash;
SQL; Python `unittest`; SHA-256 evidence.

## Global Constraints

- Source image:
  `postgres:17.6-alpine@sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94`.
- Target image:
  `postgres:18.4-alpine@sha256:9a8afca54e7861fd90fab5fdf4c42477a6b1cb7d293595148e674e0a3181de15`.
- Use synthetic data, anonymous Compose volumes, and `/tmp` evidence only. Do
  not mount `${DEFAULT_DATA_DIR}`, live Supabase/Spilo volumes, or remote backup
  storage.
- Store oracle outputs, dump checksum/size, timing, and verdict only; never
  track the dump, row payloads, credentials, or raw logs.
- Create the exact `/tmp/hyhome-ior-evidence.<decimal-run-id>` directory
  exclusively and retain its current UID, private mode, device, and inode.
  Never read or mutate a pre-existing, symlinked, or identity-changed path.
- Initialize one 420-second deadline before the first Docker call. Normal and
  preflight operations receive 360 seconds; the final 60 seconds are reserved
  for accumulated cleanup and absence verification, never added afterward.

## Overview

This active transition plan defines the approved synthetic-local implementation
order, risks, and acceptance gates for Spec 125. The sequence uses a
representative PostgreSQL logical backup, restore, major-version upgrade, and
integrity rehearsal on synthetic state. Observed execution and lifecycle
evidence belongs only in the
[domain Task](../tasks/2026-07-19-infrastructure-operations-readiness-remediation.md).

The implementation proves local mechanics and evidence discipline. It does not
claim production backup readiness, physical backup coverage, HA recovery,
retention compliance, organization RTO/RPO, live data safety, or remote storage
control.

## Context and Inputs

Inputs:

- [PRD 025](../../01.requirements/025-operational-readiness-closure.md)
- [ARD 0028](../../02.architecture/requirements/0028-operational-readiness-closure.md)
- [ADR 0028](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
- [Spec 125](../../03.specs/125-infrastructure-operations-readiness-remediation/spec.md)
- PostgreSQL service reference:
  [infra/04-data/relational/postgresql-cluster/docker-compose.yml](../../../infra/04-data/relational/postgresql-cluster/docker-compose.yml)
- Spec 124 readiness result, once available.

Planning implication: this lane should use a small repository-owned synthetic
PostgreSQL fixture and logical tooling rather than production volumes or the HA
cluster as the first runtime subject. Backup capture and restore must remain
separate gates.

## Goals and Non-goals

Goals:

- Prove `IOR-001` with an approved source/target version rehearsal and
  rollback/stop decision.
- Prove `IOR-002` with deterministic migration/integrity assertions on
  synthetic state.
- Prove `IOR-003` backup inventory/capture evidence for the representative
  fixture.
- Prove `IOR-004` restore integrity and observed local recovery timing.

Non-goals:

- No production or shared database data.
- No physical backup, PITR, HA, replication, encryption-at-rest, or retention
  certification.
- No remote storage, secret-value, registry, or cloud action.
- No organization RTO/RPO commitment beyond observed local elapsed time.

## Work Breakdown

| Unit | Purpose | Planned owned files | Requirements | RED/GREEN evidence | Commit boundary |
| --- | --- | --- | --- | --- | --- |
| `T-IOR-001` | Define the fixture, integrity oracle, wrapper contract, and tests. | `scripts/validation/rehearse-postgres-logical-upgrade.sh`; `tests/fixtures/postgres-logical-upgrade/docker-compose.yml`; `tests/fixtures/postgres-logical-upgrade/sql/001_schema_and_seed.sql`; `tests/fixtures/postgres-logical-upgrade/sql/010_integrity_oracle.sql`; `tests/fixtures/postgres-logical-upgrade/sql/020_negative_partial_state.sql`; `tests/validation/test_postgres_logical_upgrade_rehearsal.py`; `docs/04.execution/tasks/2026-07-19-infrastructure-operations-readiness-remediation.md`. | `IOR-001`–`IOR-004` | RED: missing version/digest, unsafe path, absent oracle, raw payload evidence, or unscoped cleanup. GREEN: `--check` emits the exact versions, fixture checksum, timeout, evidence class, and cleanup plan. | `feat(ops): add postgres recovery rehearsal` |
| `T-IOR-002` | Implement logical backup and isolated restore. | The wrapper, Compose fixture, SQL, and focused tests. | `IOR-003`, `IOR-004` | RED: capture success counted without restore/integrity. GREEN: custom-format dump, restore, schema/row/digest/constraint/query checks, timing, and cleanup pass. | Same IOR commit. |
| `T-IOR-003` | Add 17-to-18 upgrade and corrupted/partial-state negative paths. | The same wrapper/fixtures/tests and Task evidence. | `IOR-001`, `IOR-002` | RED: invalid target major, corruption, partial state, collision, or timeout is recorded as success. GREEN: each fails with a stable class and owned cleanup/preservation disposition. | Same IOR commit. |
| `T-IOR-004` | Add the bounded rehearsal runbook and complete reviews. | `docs/05.operations/runbooks/04-data/relational/postgresql-logical-upgrade-restore-rehearsal.md`; relational runbook index; domain Task; lifecycle/index updates only when supported. | `VAL-IOR-001`–`004` | Every finding is resolved and independently re-reviewed before closure. | Evidence-only closure unit after approval. |

### Implementation contract

The wrapper accepts `--check` and optional
`--negative-case checksum-mismatch|partial-state|bad-target-major|timeout`.
The normal run has no arguments. Defaults are source/target pins above,
project prefix `hyhome-ior-20260719`, total timeout 420 seconds, evidence under
`/tmp/hyhome-ior-evidence.` followed by the decimal process ID, and cleanup
`always`. Exit classes are `0=pass`, `2=usage`, `10=preflight`, `20=readiness`,
`30=backup`, `40=restore`, `50=integrity/negative case`, and `60=cleanup`.
Every Docker/Compose command, including version/render preflight, collision
queries, client discovery, waits, cleanup, and absence verification, consumes
that same deadline. The timeout negative uses a real failing readiness probe
with a short 20-second total and an 8-second cleanup reserve.

The Compose fixture defines only `source` and `target`, uses the two pinned
images, anonymous `pgdata` volumes, no host ports, `POSTGRES_DB=rehearsal`,
`POSTGRES_USER=rehearsal`, a process-local synthetic password, and
`pg_isready -U rehearsal -d rehearsal` healthchecks. It contains no
`container_name`, bind mount, external network, or restart policy.
The wrapper does not treat that healthcheck alone as database readiness:
source and target must each return the same authenticated
`pg_postmaster_start_time()` twice, two seconds apart, and their exact
container must still be running and healthy. Identity drift or terminal state
stays in readiness class 20 and cannot advance to seed or restore.
The wrapper validates the full `docker compose config --format json` render:
exactly two services and the exact digest pins; only anonymous volumes at the
approved PostgreSQL targets; and no host port, bind, `container_name`, restart,
privileged mode, host PID/IPC/network namespace, external network, or undeclared
service option. Render or Docker query errors fail closed rather than meaning
"absent."

`001_schema_and_seed.sql` creates:

- `rehearsal_schema_version(version integer primary key)` with row `1`;
- `accounts(id bigint primary key, code text unique not null, balance numeric
  not null check (balance >= 0))` with three deterministic rows;
- `orders(id bigint primary key, account_id bigint not null references
  accounts(id), amount numeric not null check (amount > 0), state text not null
  check (state in ('open','paid')))` with four deterministic rows.

`010_integrity_oracle.sql` returns a single JSON object containing
`schema_version`, `server_version_num`, table count, account count, order count,
sum of balances, sum of order amounts, sorted account/order MD5 digests,
foreign-key orphan count, and constraint count. It never returns row payloads.
`020_negative_partial_state.sql` creates a temporary target-only marker and
then raises an error so the wrapper can prove partial-state detection.

Required wrapper symbols and order:

```bash
parse_args
assert_safe_images_paths_and_project
start_source_and_wait
apply_seed_sql
capture_source_oracle
dump_custom_format_with_pg18_client
start_target_and_wait
restore_without_owner_or_acl
capture_target_oracle
compare_oracles
run_selected_negative_case
write_recovery_verdict
cleanup_owned_projects_and_tmp
```

The backup command contract is `pg_dump -Fc --no-owner --no-acl`; restore is
`pg_restore --clean --if-exists --no-owner --no-acl`. The wrapper stores the
dump only in its `/tmp` directory, computes SHA-256 and byte size, and deletes
the dump on successful evidence capture.

The verdict candidate remains in memory. Cleanup attempts the labeled client,
target project, source project, networks, anonymous volumes, and each owned
temporary artifact independently, accumulates failures, verifies absence, and
removes the retained evidence directory. Only after `cleanup_complete` and
`evidence_removed` are true may an exact 12-key canonical be atomically created
in a validated non-symlink parent. Stale canonical invalidation and publication
both reject symlinks, directories, unsafe parents, and command errors.

`recovery-verdict.json` has exactly these top-level keys:

```json
{
  "schema_version": 1,
  "producer_spec": "spec:125-infrastructure-operations-readiness-remediation",
  "scope": "synthetic-local",
  "source_image": "postgres:17.6-alpine@sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94",
  "target_image": "postgres:18.4-alpine@sha256:9a8afca54e7861fd90fab5fdf4c42477a6b1cb7d293595148e674e0a3181de15",
  "fixture_sha256": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "dump_sha256": "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "integrity_status": "passed",
  "backup_seconds": 0,
  "restore_seconds": 0,
  "cleanup_status": "passed",
  "redaction_status": "passed"
}
```

Tests expose `test_fixture_uses_only_pinned_source_and_target`,
`test_rejects_unsafe_evidence_path`, `test_rejects_project_collision`,
`test_oracle_contains_no_row_payload`, `test_bad_target_major_fails_preflight`,
`test_checksum_mismatch_is_nonzero`, `test_partial_state_is_nonzero`,
`test_timeout_still_cleans`, and `test_recovery_verdict_schema`.

## Sequence

- [ ] Create the active Task with the exact image pins above, synthetic-data
      approval, runtime boundary, redaction, cleanup, and rollback.
- [ ] Write failing tests in
      `tests/validation/test_postgres_logical_upgrade_rehearsal.py` for version
      order, image pins, unsafe evidence path, project collision, missing
      cleanup, timeout, corrupt dump, partial state, checksum mismatch, and raw
      payload leakage.
- [ ] Run
      `python3 -m unittest tests.validation.test_postgres_logical_upgrade_rehearsal -v`
      and confirm failure before the wrapper/fixtures exist.
- [ ] Implement the Compose/SQL fixtures and wrapper `--check` mode; rerun the
      focused tests until all static positive/negative cases pass.
- [ ] Run `bash scripts/validation/rehearse-postgres-logical-upgrade.sh --check`.
- [ ] Run `bash scripts/validation/rehearse-postgres-logical-upgrade.sh` and
      require independent backup capture, restore, oracle comparison, timing,
      and cleanup verdicts.
- [ ] Run
      `bash scripts/validation/rehearse-postgres-logical-upgrade.sh --negative-case checksum-mismatch`
      and require a stable non-zero integrity failure with cleanup.
- [ ] Run
      `bash scripts/validation/rehearse-postgres-logical-upgrade.sh --negative-case partial-state`
      and require a stable non-zero partial-state failure with the documented
      evidence-preservation/cleanup disposition.
- [ ] Run
      `bash scripts/validation/rehearse-postgres-logical-upgrade.sh --negative-case bad-target-major`
      through the rendered-topology validator and require class 10 with cleanup.
- [ ] Run
      `bash scripts/validation/rehearse-postgres-logical-upgrade.sh --negative-case timeout`
      through the real bounded readiness loop and require class 20 with cleanup.
- [ ] Write the narrow local rehearsal runbook; do not broaden the existing
      live cluster/Supabase destructive-recovery authority.
- [ ] Record concise Task evidence and obtain fresh independent specification
      plus operations/quality reviews for the independent image-identity
      controls. The domain Task alone owns observed execution, review, and
      lifecycle evidence.

## Verification Plan

`$COMPARISON_BASE_REF` denotes the explicit reviewed comparison ref recorded by
the [Program Task](../tasks/2026-07-19-operational-readiness-closure-program.md);
this Plan does not own a concrete base identity.

| Gate | Command / method | Expected pass evidence |
| --- | --- | --- |
| Metadata and lifecycle | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref "$COMPARISON_BASE_REF"` | Changed Stage 04 docs remain valid. |
| Traceability | `bash scripts/validation/check-doc-traceability.sh` and `bash scripts/validation/check-doc-implementation-alignment.sh` | `IOR-001`–`IOR-004` map to implemented files and Task evidence. |
| Repository contract | `bash scripts/validation/check-repo-contracts.sh` | No new contract breakage. |
| Fixture/unit tests | `python3 -m unittest tests.validation.test_postgres_logical_upgrade_rehearsal -v` | Positive and negative recovery fixtures pass. |
| Runtime rehearsal | the four exact wrapper commands in Sequence | Backup, restore, integrity, upgrade, negative-path, elapsed-time, and cleanup evidence pass. |
| Review | Independent spec and quality/security review | All findings are resolved and independently re-reviewed. |

## Risks and Rollback

| Risk | Impact | Mitigation / rollback |
| --- | --- | --- |
| Production/shared data selected | Critical | Synthetic fixture only; fail closed on external path or unapproved volume. |
| Backup-only false confidence | High | Restore and integrity are mandatory separate gates. |
| Partial migration/data loss | Critical | Fixture checksum/oracle, non-zero failure, preserve evidence when cleanup could hide loss. |
| Secret or raw dump leakage | Critical | No raw dumps in tracked docs; checksum/metadata only. |
| RTO/RPO overclaim | High | Record observed local elapsed time only and explicit non-goal. |

Rollback is by removing task-owned harness files, reverting the logical commit,
and cleaning only resources with the task project identity and labels. If
database state is ambiguous, stop and escalate rather than deleting evidence.

## Approval Gates

- Plan activation requires recorded human approval.
- The future Task must approve exact source/target images, fixture, command
  envelope, cleanup, and evidence boundary before runtime.
- Live data, production volumes, remote backup destinations, secret values, and
  cloud/registry operations remain unapproved.

## Completion Criteria

- [ ] Active Task maps `IOR-001`–`IOR-004` to exact files, commands, rollback,
      redaction, and reviews.
- [ ] Synthetic fixture and integrity oracle are deterministic and implementation-reviewed.
- [ ] Backup capture and restore integrity pass as separate gates.
- [ ] Representative major-version logical upgrade rehearsal passes or fails
      closed with complete evidence.
- [ ] Cleanup is owned and verified.
- [ ] Independent specification and quality/security findings are resolved and
      independently re-reviewed.
- [ ] Spec 125 lifecycle reflects only local representative evidence; remote,
      production, HA, physical backup, and RTO/RPO exclusions remain explicit.

## Related Documents

- **PRD**: [Operational readiness closure](../../01.requirements/025-operational-readiness-closure.md)
- **ARD**: [Operational readiness closure architecture](../../02.architecture/requirements/0028-operational-readiness-closure.md)
- **ADR**: [ADR-0028 local-isolated readiness evidence](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
- **Spec**: [Spec 125](../../03.specs/125-infrastructure-operations-readiness-remediation/spec.md)
- **Runtime dependency**: [Spec 124](../../03.specs/124-compose-runtime-readiness-remediation/spec.md)
- **PostgreSQL reference compose file**: [postgresql-cluster/docker-compose.yml](../../../infra/04-data/relational/postgresql-cluster/docker-compose.yml)
