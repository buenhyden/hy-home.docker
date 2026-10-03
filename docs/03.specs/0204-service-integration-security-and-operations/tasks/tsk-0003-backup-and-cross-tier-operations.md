---
title: "Backup and Cross-tier Operations Task"
version: "0.1.2"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0003"
parent_ids:
- "SPEC-0204"
- "SPEC-0204-PLAN-0001"
created: "2026-10-03"
---

# Backup and Cross-tier Operations Task

## Objective

After SPEC-0202 transfers backup/Kafka ownership, include the development
PostgreSQL repository in the existing backup source chain. Close confirmed cross-tier service contracts only where a real
consumer and bounded fixture exist. Source changes cannot prove HOME recovery
or authorize data migration.

## Inputs

Baseline `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`, SPEC-0202 synthetic
dev-pg restore receipt, current POL/RUN-0021, SPEC-0201 W5 service ledger,
and the current Restic/pgBackRest source. The user approved this Task source scope on 2026-10-03. The closure integration
branch applies SPEC-0202 lifecycle completion before this source handoff.
No backup repository contents, key values, HOME logs or production rows are
read by this Task.

## Work Log

| Service and source evidence | Exact writer or read-only source | Regression and rollback | Approval boundary |
| --- | --- | --- | --- |
| dev-pg has a separate `dev-pgbackrest` repository; Restic state set mounts/lists only management `pgbackrest`; host scheduler backs up only mng-pg | WRITE: `infra/09-platform-ops/restic/docker-compose.yml`, `backup.sh`, `infra/09-platform-ops/restic/bin/hyhome-backup.sh`; `sets/state-include.txt` is read-only unless a later exact amendment proves it necessary; source variable `BACKUP_STATE_REPO_DIR`, `dev-pg`/Restic consumers | Synthetic missing/present repository, backup failure, disk budget, globals and offsite set identity; revert scoped source before live scheduler deployment, never delete a repository | SPEC-0202 handoff under the approved Task scope; live backup/offsite/restore separately approved |
| Management PITR and dev-pg isolated synthetic restore are distinct evidence | WRITE: existing `docs/05.operations/policies/0021-backup-and-restore.md`, `docs/05.operations/runbooks/0021-backup-and-restore.md`, `docs/05.operations/guides/0021-backup-and-restore.md`; development DB owner docs are read-only; selected stanza, image digest, extension/role/migration revision, backup/WAL range | Separate-volume restore, application reader denial/success, no `latest` selection; source rollback cannot undo data mutation | HOME and actual repository verify/restore need exact preflight and permission |
| Debezium source changed in SPEC-0202; Avro consumers retain Schema Registry | READ_ONLY: `infra/05-messaging/kafka/connect/debezium/postgres-connector.json` and Kafka service docs; any source edit needs a later exact Task after SPEC-0202 handoff | Synthetic restart/duplicate/replay/schema evolution and lag measurement; do not reuse old LSN on a new DB; revert fixture/source, preserve offsets | No live connector registration, slot deletion or broker restart |
| Airflow and n8n have separate batch/integration purposes | READ_ONLY: current Airflow/n8n Compose and GDE/POL/RUN-0050/0053; no workflow source write in this Task | Inventory worker DB/S3/mail reachability and payload/retention ownership; fixture and rollback belong to a later exact Task | Workflow data or service restart separately approved |
| Open WebUI/Ollama/ComfyUI and Qdrant have current optional paths | READ_ONLY: current Open WebUI/Ollama/ComfyUI/Qdrant source and AI operations owners; no AI source write in this Task | Inventory permission/embedding-version and GPU budget gaps; fixture belongs to a later exact Task; no speech activation | Real documents, user voice, GPU reservation and product scope separately approved |
| Mailpit captures development mail; Stalwart owns delivery | READ_ONLY: current Stalwart Compose and mail operations owners; no mail source write in this Task | Inventory accepted/failed/uncertain-send state and replay owner; fixture/rollback belong to a later exact Task | External relay, DNS and real send separately approved |
| Trino/GX readers and Spark/Flink writers have different authority | READ_ONLY: current Trino/GX/Spark/Flink Compose and analytics operations owners; no analytics source write in this Task | Inventory reader/writer and checkpoint owner; fixture belongs to a later exact Task; no default command counted as success | No new business DB or live pipeline job |

The SPEC-0202 source/lifecycle handoff is applied in the current closure branch.
Only the three exact Restic source files, the three named Stage 05 backup
documents and `tests/validation/test_compose_baseline_gates.py` may be
writers after SPEC-0202 handoff under the 2026-10-03 Task approval. The
Debezium connector and consumer-dependent workflow, AI,
mail and analytics changes require a later Task with exact files and approvals.
The source fix must use the existing backup state set and offsite copy path;
it must not copy live PGDATA or lower retention. Account for backup growth in
alerts and measured capacity before HOME scheduling. A Korean Restic README
change, if needed, requires an exact Task amendment. Reuse
`tests/validation/test_compose_baseline_gates.py` for the backup branch.
Any additional test file or parser requires an exact Task amendment.

## Verification Evidence

| Check | Result | Limit |
| --- | --- | --- |
| Current Restic/dev-pg declaration comparison on `d2a5dfc79` | READ_ONLY | `restic/docker-compose.yml` mounts only `/pgbackrest`, `backup.sh` lists only that repository, and `hyhome-backup.sh` invokes only mng-pg stanza. `dev-pgbackrest` is declared separately; SPEC-0202 remains `draft`, so no writer handoff. |
| Current Kafka/analytics/mail source inspection | READ_ONLY | Debezium connector uses Avro with Schema Registry and has a named slot/publication/heartbeat; no live connector registration or lag evidence. Flink wrapper sets a 60s checkpoint interval but no restore result. Stalwart relay is disabled while Mailpit remains development capture; no real send result. |
| `python3 -m unittest tests.validation.test_compose_baseline_gates.BackupContractTests.test_dev_repository_mount_and_scheduler_failure_contract` before implementation | RED, exit 1 | Missing development mount raised StopIteration; the failure established the missing source chain. |
| `python3 -m unittest tests.validation.test_compose_baseline_gates.BackupContractTests` after implementation | PASS, exit 0; 11 tests | Synthetic shell shim checks success, check/backup/globals/schema failure, stopped dev-pg and stale export removal. Static assertions check RO mount/create-host-path false, time limits, existing budget ordering, source exclusions and offsite identity. This does not execute pgBackRest or Restic. |
| `bash -n infra/09-platform-ops/restic/bin/hyhome-backup.sh`; `sh -n infra/09-platform-ops/restic/backup.sh`; `git diff --check` | PASS, each exit 0 | Syntax and whitespace only. |
| `bash .agents/skills/infra-validate/scripts/static-checks.sh` | BLOCKED, exit 2 | 9 PASS, 0 FAIL, 6 BLOCKED: unsupported tracked input graph and missing YAML/shell lint tools; dependent Compose checks not executed. Fixture cleanup PASS. |
| Updated isolated Restic round-trip fixture | NOT_RUN | Fixture now mounts both distinct synthetic pgBackRest repositories and asserts development repository snapshot inclusion. No Docker execution authorized/performed by this Task. |
| HOME backup, actual capacity, selected-image dev restore and WAL/PITR | NOT_RUN | Source readiness is not an operational receipt. archive_mode remains off; separate preflight and approval required. |
| HOME backup, offsite copy, PITR, credential rotation, data migration | NOT_RUN | Separate exact operational approval required |

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1/W5 | Source ledger updated; exact writer paths retained | This Task and current service READMEs |
| 6 | W4/W5 | Consumer-backed inventory; named runtime checks BLOCKED pending actual consumer/approval | Existing messaging/workflow/AI/mail/analytics owners |
| 7 | W4/W5 | Source chain implemented; synthetic failure checks PASS; actual restore NOT_RUN | POL/RUN-0021 and Restic source |
| 8 | W5 | Focused tests PASS; static helper BLOCKED; independent review pending | This Task verification receipts |

### Source handoff receipt

The existing Restic state source now includes a read-only `dev-pgbackrest` bind
with no implicit directory creation. The scheduler requires the prepared separate
repository; if dev-pg is stopped, check/backup fails, or an export/image/source
metadata command fails, status remains nonzero and no complete-run timestamp is
written. Stale development exports are removed before the branch and failed partial
exports are discarded. One existing state budget covers both pgBackRest sources,
exports and Restic; existing offsite state copy carries the development repository.
No allowlist file, secret, image pin, retention, WAL setting or runtime is changed.

Globals/schema exports and image/infra revision metadata use private staging and
existing encrypted snapshots/cleanup. Physical catalog preserves extension versions
and applied migration state; external application migration source revision and
post-restore authorization checks remain that application's owner responsibility.
A source revision alone cannot assert that a migration was applied.

Rollback restores only the three source files and their focused test/document
contract before deployment. It does not delete either repository or reverse data.
The new bind requires approved directory provisioning before any future HOME
scheduler activation; initial full backup, stanza/key/WAL/retention and capacity
review are stop conditions, not automatically authorized provisioning.


## Review Evidence

Independent backup/infra/security review approved the exact source diff with
operational follow-up. The reviewer reran 11 backup tests, shell syntax,
static backup render, catalog and corpus lifecycle; all exited 0. An
unrelated Grafana descendant link was reported and corrected by its owner.
Dev source does not change archive_mode, retention, secret values or HOME scheduling.
The synthetic SPEC-0202 restore is not a current HOME or offsite receipt.

## Commit Ledger

Baseline `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`; package draft `0f67cb297`, review transition `2157e62c5`. SPEC-0202 handoff integrated locally before source writing; current source changes remain uncommitted for independent review.

## Rulings

No new backup stack, live PGDATA copy, `latest` restore, retention deletion,
new analytics engine or duplicate observability component. A missing consumer
is a design/verification gap, not authority to provision one.

## Deferred Items

Approved capacity and backup schedule; actual
restoration target/image/WAL range; project S3/search/reader access; HOME and
external mail/connector operations remain separate.
