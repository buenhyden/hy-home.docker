---
status: active
artifact_id: plan:2026-07-11-infrastructure-operations-readiness-remediation
artifact_type: plan
parent_ids:
  - prd:025-operational-readiness-closure
  - ard:0028-operational-readiness-closure
  - adr:0028-local-isolated-readiness-evidence
  - spec:125-infrastructure-operations-readiness-remediation
---

# Infrastructure Operations Readiness Remediation Implementation Plan

## Overview

This active plan turns Spec 125 into an executable local sequence for a
representative PostgreSQL logical backup, restore, major-version upgrade, and
integrity rehearsal on synthetic state. It is prospective; actual database
runtime evidence belongs in the future sibling Task.

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
| `T-IOR-001` | Define synthetic PostgreSQL fixture, integrity oracle, and evidence schema. | `scripts/validation/postgres-recovery-readiness.*`, `scripts/validation/fixtures/postgres-recovery/**`, Task evidence file. | `IOR-001`–`IOR-004` | RED: fixture lacks expected schema/row/digest oracle or admits payloads in evidence. GREEN: dry-run shows source/target versions, fixture checksum, backup path class, cleanup plan. | `feat(ops): add postgres recovery rehearsal` |
| `T-IOR-002` | Implement logical backup and isolated restore path. | Same harness and tests. | `IOR-003`, `IOR-004` | RED: backup success counted without restore or integrity. GREEN: dump, restore, schema/row/digest/query checks, elapsed time, cleanup result pass. | Same IOR commit unless split by review. |
| `T-IOR-003` | Implement representative major-version logical upgrade rehearsal. | Harness tests and fixture SQL. | `IOR-001`, `IOR-002` | RED: partial migration or integrity mismatch recorded as success. GREEN: source dump, target restore/upgrade, compatibility/integrity checks, rollback/stop decision pass. | Same IOR commit unless split by review. |
| `T-IOR-004` | Independent operations/data/security review and SDLC closure. | Task evidence and lifecycle updates only after evidence. | `VAL-IOR-001`–`004` | Spec review C0/I0/M0 and quality/security review C0/I0/M0. | `docs(evidence): record postgres recovery closure` if separate evidence-only commit is needed. |

## Sequence

1. Create the active Task with synthetic data approval, runtime boundary,
   allowed PostgreSQL image/version set, redaction, cleanup, and rollback.
2. Add fixture SQL containing schema, constraints, representative rows, and
   deterministic expected integrity outputs.
3. Implement dry-run/preflight. It must resolve worktree revision, image tags
   or digests, source/target projects, ports, volumes, backup path class,
   timeout, and cleanup labels before startup.
4. Add negative fixtures for target ambiguity, missing cleanup, corrupted dump,
   partial restore, integrity mismatch, and evidence payload leakage.
5. Run logical backup and restore as separate acceptance gates. Do not count
   capture success as recoverability.
6. Run the representative source-to-target logical upgrade rehearsal and record
   compatibility, integrity, elapsed time, and stop/rollback decision.
7. Record concise Task evidence only: command class, image/version identity,
   fixture checksum, dump checksum, integrity results, elapsed time, cleanup
   result, and stable error class.
8. Run independent specification review, then quality/security review. Fix and
   re-review findings before lifecycle closure.

## Verification Plan

| Gate | Command / method | Expected pass evidence |
| --- | --- | --- |
| Metadata and lifecycle | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref <safe-base>` | Changed Stage 04 docs remain valid. |
| Traceability | `bash scripts/validation/check-doc-traceability.sh` and `bash scripts/validation/check-doc-implementation-alignment.sh` | `IOR-001`–`IOR-004` map to implemented files and Task evidence. |
| Repository contract | `bash scripts/validation/check-repo-contracts.sh` | No new contract breakage. |
| Fixture/unit tests | Future focused test command owned by `T-IOR-001` | Positive and negative recovery fixtures pass. |
| Runtime rehearsal | Future Task-approved Docker/PostgreSQL command envelope | Backup, restore, integrity, upgrade, elapsed-time, and cleanup evidence pass. |
| Review | Independent spec and quality/security review | C0/I0/M0 or all findings resolved and re-reviewed. |

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

- Human approval exists for this active Plan conversion.
- The future Task must approve exact source/target images, fixture, command
  envelope, cleanup, and evidence boundary before runtime.
- Live data, production volumes, remote backup destinations, secret values, and
  cloud/registry operations remain unapproved.

## Completion Criteria

- [ ] Active Task maps `IOR-001`–`IOR-004` to exact files, commands, rollback,
      redaction, and reviews.
- [ ] Synthetic fixture and integrity oracle are deterministic and reviewed.
- [ ] Backup capture and restore integrity pass as separate gates.
- [ ] Representative major-version logical upgrade rehearsal passes or fails
      closed with complete evidence.
- [ ] Cleanup is owned and verified.
- [ ] Independent specification and quality/security reviews pass.
- [ ] Spec 125 lifecycle reflects only local representative evidence; remote,
      production, HA, physical backup, and RTO/RPO exclusions remain explicit.

## Related Documents

- **PRD**: [Operational readiness closure](../../01.requirements/025-operational-readiness-closure.md)
- **ARD**: [Operational readiness closure architecture](../../02.architecture/requirements/0028-operational-readiness-closure.md)
- **ADR**: [ADR-0028 local-isolated readiness evidence](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
- **Spec**: [Spec 125](../../03.specs/125-infrastructure-operations-readiness-remediation/spec.md)
- **Runtime dependency**: [Spec 124](../../03.specs/124-compose-runtime-readiness-remediation/spec.md)
- **PostgreSQL reference compose file**: [postgresql-cluster/docker-compose.yml](../../../infra/04-data/relational/postgresql-cluster/docker-compose.yml)
