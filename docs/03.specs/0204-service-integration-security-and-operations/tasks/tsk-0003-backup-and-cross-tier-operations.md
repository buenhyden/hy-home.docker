---
title: "Backup and Cross-tier Operations Task"
version: "1.0.1"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-04"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0003"
parent_ids:
- "SPEC-0204"
- "SPEC-0204-PLAN-0001"
created: "2026-10-03"
---

# Backup and Cross-tier Operations Task

## Objective

After SPEC-0202 transfers backup/Kafka ownership and the owner approves this
Task, include the development PostgreSQL repository in the existing backup
source chain. Close confirmed cross-tier service contracts only where a real
consumer and bounded fixture exist. Source changes cannot prove HOME recovery
or authorize data migration.

## Inputs

Baseline `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`, SPEC-0202 synthetic
dev-pg restore receipt, current POL/RUN-0021, SPEC-0201 W5 service ledger,
and the current Restic/pgBackRest source. SPEC-0202 lifecycle remains draft at
this baseline; Kafka connector and backup policy writer handoff is not closed.
No backup repository contents, key values, HOME logs or production rows are
read by this draft.

## Work Log

| Service and source evidence | Exact writer or read-only source | Regression and rollback | Approval boundary |
| --- | --- | --- | --- |
| dev-pg has a separate `dev-pgbackrest` repository; Restic state set mounts/lists only management `pgbackrest`; host scheduler backs up only mng-pg | WRITE AFTER APPROVAL: `infra/09-platform-ops/restic/docker-compose.yml`, `backup.sh`, `infra/09-platform-ops/restic/bin/hyhome-backup.sh`; `sets/state-include.txt` is read-only unless a later exact amendment proves it necessary; source variable `BACKUP_STATE_REPO_DIR`, `dev-pg`/Restic consumers | Synthetic missing/present repository, backup failure, disk budget, globals and offsite set identity; revert scoped source before live scheduler deployment, never delete a repository | SPEC-0202 handoff plus Task source approval; live backup/offsite/restore separately approved |
| Management PITR and dev-pg isolated synthetic restore are distinct evidence | WRITE AFTER APPROVAL: existing `docs/05.operations/policies/0021-backup-and-restore.md`, `docs/05.operations/runbooks/0021-backup-and-restore.md`, `docs/05.operations/guides/0021-backup-and-restore.md`; development DB owner docs are read-only; selected stanza, image digest, extension/role/migration revision, backup/WAL range | Separate-volume restore, application reader denial/success, no `latest` selection; source rollback cannot undo data mutation | HOME and actual repository verify/restore need exact preflight and permission |
| Debezium source changed in SPEC-0202; Avro consumers retain Schema Registry | READ_ONLY: `infra/05-messaging/kafka/connect/debezium/postgres-connector.json` and Kafka service docs; any source edit needs a later exact Task after SPEC-0202 handoff | Synthetic restart/duplicate/replay/schema evolution and lag measurement; do not reuse old LSN on a new DB; revert fixture/source, preserve offsets | No live connector registration, slot deletion or broker restart |
| Airflow and n8n have separate batch/integration purposes | READ_ONLY: current Airflow/n8n Compose and GDE/POL/RUN-0050/0053; no workflow source write in this Task | Inventory worker DB/S3/mail reachability and payload/retention ownership; fixture and rollback belong to a later exact Task | Workflow data or service restart separately approved |
| Open WebUI/Ollama/ComfyUI and Qdrant have current optional paths | READ_ONLY: current Open WebUI/Ollama/ComfyUI/Qdrant source and AI operations owners; no AI source write in this Task | Inventory permission/embedding-version and GPU budget gaps; fixture belongs to a later exact Task; no speech activation | Real documents, user voice, GPU reservation and product scope separately approved |
| Mailpit captures development mail; Stalwart owns delivery | READ_ONLY: current Stalwart Compose and mail operations owners; no mail source write in this Task | Inventory accepted/failed/uncertain-send state and replay owner; fixture/rollback belong to a later exact Task | External relay, DNS and real send separately approved |
| Trino/GX readers and Spark/Flink writers have different authority | READ_ONLY: current Trino/GX/Spark/Flink Compose and analytics operations owners; no analytics source write in this Task | Inventory reader/writer and checkpoint owner; fixture belongs to a later exact Task; no default command counted as success | No new business DB or live pipeline job |

Only the three exact Restic source files, the three named Stage 05 backup
documents and `tests/validation/test_compose_baseline_gates.py` may be
writers after SPEC-0202 handoff and Task approval. The Debezium connector and
consumer-dependent workflow, AI,
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
| Current Restic/dev-pg declaration comparison | READ_ONLY | Separate dev repository is omitted from Restic mount/list and scheduler |
| Synthetic backup failure/capacity/restore fixture | NOT_RUN | Await handoff, Task approval and exact fixture preflight; other tiers are read-only |
| HOME backup, offsite copy, PITR, credential rotation, data migration | NOT_RUN | Separate exact operational approval required |

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1/W5 | DRAFT source ledger | This Task and current service READMEs |
| 6 | W4/W5 | PARTIAL design; consumer-specific source changes pending | Existing messaging/workflow/AI/mail/analytics owners |
| 7 | W4/W5 | NOT_RUN | POL/RUN-0021 and Restic source |
| 8 | W5 | NOT_RUN | This Task verification receipts |

## Review Evidence

Independent backup/infra/security review is pending an approved source diff.
The synthetic SPEC-0202 restore is not a current HOME or offsite receipt.

## Commit Ledger

No Prompt 04 commit. Baseline only: `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`.

## Rulings

No new backup stack, live PGDATA copy, `latest` restore, retention deletion,
new analytics engine or duplicate observability component. A missing consumer
is a design/verification gap, not authority to provision one.

## Deferred Items

SPEC-0202 lifecycle handoff; approved capacity and backup schedule; actual
restoration target/image/WAL range; project S3/search/reader access; HOME and
external mail/connector operations remain separate.
