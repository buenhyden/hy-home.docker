---
title: "Backup and Cross-tier Operations Task"
version: "1.0.3"
type: "sdlc/task"
status: "completed"
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
and the current Restic/pgBackRest source. The user approved this Task source
scope on 2026-10-03, and the closure branch applied the SPEC-0202 lifecycle
handoff before backup source writing. No existing/HOME/production backup
repository contents, key values, HOME logs or production rows are read by this
Task.

## Work Log

| Service and source evidence | Exact writer or read-only source | Regression and rollback | Approval boundary |
| --- | --- | --- | --- |
| dev-pg has a separate `dev-pgbackrest` repository; Restic state set originally mounted/listed only management `pgbackrest`; host scheduler originally backed up only mng-pg | SOURCE COMPLETED after protected delivery: `infra/09-platform-ops/restic/docker-compose.yml`, `backup.sh`, `infra/09-platform-ops/restic/bin/hyhome-backup.sh`; `sets/state-include.txt` remains read-only unless a later exact amendment proves it necessary; source variable `BACKUP_STATE_REPO_DIR`, `dev-pg`/Restic consumers | Synthetic missing/present repository, backup failure, disk budget, globals and offsite set identity; revert scoped source before live scheduler deployment, never delete a repository | SPEC-0202 handoff under approved Task scope; live backup/offsite/restore separately approved |
| Management PITR and dev-pg isolated synthetic restore are distinct evidence | SOURCE/DOC COMPLETED after protected delivery: existing `docs/05.operations/policies/0021-backup-and-restore.md`, `docs/05.operations/runbooks/0021-backup-and-restore.md`, `docs/05.operations/guides/0021-backup-and-restore.md`; development DB owner docs are read-only; selected stanza, image digest, extension/role/migration revision, backup/WAL range | Separate-volume restore, application reader denial/success, no `latest` selection; source rollback cannot undo data mutation | HOME and actual repository verify/restore need exact preflight and permission |
| Debezium source changed in SPEC-0202; Avro consumers retain Schema Registry | READ_ONLY: `infra/05-messaging/kafka/connect/debezium/postgres-connector.json` and Kafka service docs; any source edit needs a later exact Task after SPEC-0202 handoff | Synthetic restart/duplicate/replay/schema evolution and lag measurement; do not reuse old LSN on a new DB; revert fixture/source, preserve offsets | No live connector registration, slot deletion or broker restart |
| Airflow and n8n have separate batch/integration purposes | READ_ONLY: current Airflow/n8n Compose and GDE/POL/RUN-0050/0053; no workflow source write in this Task | Inventory worker DB/S3/mail reachability and payload/retention ownership; fixture and rollback belong to a later exact Task | Workflow data or service restart separately approved |
| Open WebUI/Ollama/ComfyUI and Qdrant have current optional paths | READ_ONLY: current Open WebUI/Ollama/ComfyUI/Qdrant source and AI operations owners; no AI source write in this Task | Inventory permission/embedding-version and GPU budget gaps; fixture belongs to a later exact Task; no speech activation | Real documents, user voice, GPU reservation and product scope separately approved |
| Mailpit captures development mail; Stalwart owns delivery | READ_ONLY: current Stalwart Compose and mail operations owners; no mail source write in this Task | Inventory accepted/failed/uncertain-send state and replay owner; fixture/rollback belong to a later exact Task | External relay, DNS and real send separately approved |
| Trino/GX readers and Spark/Flink writers have different authority | READ_ONLY: current Trino/GX/Spark/Flink Compose and analytics operations owners; no analytics source write in this Task | Inventory reader/writer and checkpoint owner; fixture belongs to a later exact Task; no default command counted as success | No new business DB or live pipeline job |

Only the three exact Restic source files, the three named Stage 05 backup
documents and `tests/validation/test_compose_baseline_gates.py` may be writers
under this Task. The Debezium connector and consumer-dependent workflow, AI,
mail and analytics changes require a later Task with exact files and approvals.
The source fix must use the existing backup state set and offsite copy path; it
must not copy live PGDATA or lower retention. Account for backup growth in
alerts and measured capacity before HOME scheduling. A Korean Restic README
change, if needed, requires an exact Task amendment.

## Verification Evidence

### Closure source evidence imported during 2026-10-04 integration

Closure commit `451b1ec7e4c5509e088a17c9c0f33e3dab93ddd7` recorded backup
source commit `ce001be7af93aebe6430f586b56a5c443fa9f386` plus a later
sanitized isolated replay receipt. PR359 now carries that source side, current
static QA and the protected delivery receipt below.

| Check | Result | Limit |
| --- | --- | --- |
| Initial read-only comparison before approved handoff, `d2a5dfc79` | HISTORICAL READ_ONLY | Restic mounted/listed only management `pgbackrest`; `dev-pgbackrest` was declared separately; SPEC-0202 was draft at that baseline. |
| Current Kafka/analytics/mail source inspection | READ_ONLY | Debezium uses Avro/Schema Registry with named slot/publication/heartbeat; no live registration or lag evidence. Flink checkpoint, Stalwart relay and Mailpit remain unverified runtime paths. |
| `python3 -m unittest tests.validation.test_compose_baseline_gates.BackupContractTests.test_dev_repository_mount_and_scheduler_failure_contract` before implementation | HISTORICAL RED, exit 1 | Missing development mount established the missing source chain. |
| `python3 -m unittest tests.validation.test_compose_baseline_gates.BackupContractTests` after implementation | HISTORICAL PASS, exit 0, 11 tests | Synthetic shell shim and static assertions only; no pgBackRest or Restic execution. |
| `bash -n infra/09-platform-ops/restic/bin/hyhome-backup.sh`; `sh -n infra/09-platform-ops/restic/backup.sh`; `git diff --check` | HISTORICAL PASS, each exit 0 | Syntax and whitespace only. |
| `bash .agents/skills/infra-validate/scripts/static-checks.sh` | HISTORICAL BLOCKED, exit 2 | 9 PASS, 0 FAIL, 6 BLOCKED because unsupported input graph and missing lint tools blocked dependent Compose checks. |
| Isolated synthetic offline recovery replay, final sanitized run `python3 /tmp/hyhome-p04-sanitized-btujdqhh/rehearsal.py` | HISTORICAL PASS, exit 0 | Fresh fixture only: synthetic DB/roles/secrets, cached images, internal network, no HOME repository, no actual BKP-001, no production data. |
| HOME backup, offsite copy, online WAL/PITR, credential rotation, retention activation, RPO/RTO measurement, data migration | NOT_RUN | Separate exact operational approval required. |

### Historical isolated recovery summary

The sanitized replay used explicit minimal child environment, empty invocation
HOME and Docker config, `DOCKER_HOST=unix:///var/run/docker.sock`, root-owned
`/usr/bin/docker`, internal network, no host ports, and new fixture volumes. It
exercised provision/rerun, source SQL/metadata, expected reader write/DDL
denials, expected online-backup refusal while `archive_mode` stayed off,
offline pgBackRest backup, expected missing-source Restic exit 3, complete
state/host backup and check, explicit snapshot restore, metadata and empty target
checks, expected unknown-label restore refusal, selected pgBackRest restore,
recovered SQL/role comparison, and cleanup/absence checks. Baseline and
restored result both were `1|1|2.30.2|platform_owner`, with the same four role
login/privilege flags. This is a source and isolated synthetic recovery receipt
only; it is not actual HOME backup, online WAL/PITR, offsite restore,
application cutover, credential rotation, retention activation, RPO/RTO proof or
data migration.

### Protected completion receipt — 2026-10-04

PR359 delivered as `467bd644b071f9dfa02ca1af2d622502c3445d28` after required CI `required CI run37180461557 PASS`. Candidate
source head `0ff55fa8378365ee6a9eb81c34c837bc494aa006` includes the approved
Restic dev-pgbackrest source chain and Stage 05 backup documents. Task1 records
combined QA with baseline tests passing and 21 optional Docker skips; the exact
backup failure harness passed after `check=False`. Independent source review
returned PASS separately from protected CI. Historical closure evidence at
`451b1ec7e4c5509e088a17c9c0f33e3dab93ddd7` remains the selected synthetic
offline restore receipt. This completes source and isolated synthetic backup
acceptance only. HOME backup, offsite copy, online WAL/PITR, retention
activation, RPO/RTO, credential rotation and data migration remain `NOT_RUN`.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W4 | PASS: approved backup writer ledger and source handoff are recorded | [Backup policy](../../../05.operations/policies/0021-backup-and-restore.md) |
| 6 | W4 | PARTIAL: consumer-backed decisions retain honest unverified runtime states without speculative services | [Architecture owner](../../../02.architecture/descriptions/0031-home-development-host.md) |
| 7 | W4 | PASS for source and isolated synthetic selected-set recovery; actual HOME/offsite/WAL/PITR remain NOT_RUN | [Backup runbook](../../../05.operations/runbooks/0021-backup-and-restore.md) |
| 8 | W4 | PASS: focused source checks, independent review and protected delivery receipt recorded | [Backup guide](../../../05.operations/guides/0021-backup-and-restore.md) |

## Review Evidence

Closure-side independent backup/infra/security review approved the exact source
diff with operational follow-up. The reviewer reran 11 backup tests, shell
syntax, static backup render, catalog and corpus lifecycle; all exited 0. Final
independent review on 2026-10-04 approved the sanitized replay and
POL/GDE/RUN-0021 summaries with no open CRITICAL/HIGH/MEDIUM finding. Independent current integration review returned PASS. The continuing backup schedule, capacity,
WAL/PITR, offsite and actual HOME restore obligations remain with POL/RUN-0021
and require separate approval.

## Commit Ledger

Baseline `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`; package draft
`0f67cb297`; review transition `2157e62c5`; backup source and first static
receipt `ce001be7af93aebe6430f586b56a5c443fa9f386`; closure
`451b1ec7e4c5509e088a17c9c0f33e3dab93ddd7`; PR359 delivery `467bd644b071f9dfa02ca1af2d622502c3445d28`; CI `required CI run37180461557 PASS`.

## Rulings

No new backup stack, live PGDATA copy, `latest` restore, retention deletion,
new analytics engine or duplicate observability component. A missing consumer
is a design/verification gap, not authority to provision one.

## Deferred Items

Approved capacity and backup schedule; actual restoration target/image/WAL
range; project S3/search/reader access; HOME and external mail/connector
operations remain separate.
