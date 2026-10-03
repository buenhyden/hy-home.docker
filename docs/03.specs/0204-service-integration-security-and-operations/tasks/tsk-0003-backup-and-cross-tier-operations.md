---
title: "Backup and Cross-tier Operations Task"
version: "0.1.4"
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

After SPEC-0202 transfers backup/Kafka ownership, include the development
PostgreSQL repository in the existing backup source chain. Close confirmed cross-tier service contracts only where a real
consumer and bounded fixture exist. Source changes cannot prove HOME recovery
or authorize data migration.

## Inputs

Baseline `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`, SPEC-0202 synthetic
dev-pg restore receipt, current POL/RUN-0021, SPEC-0201 W5 service ledger,
and the current Restic/pgBackRest source. The user approved this Task source scope on 2026-10-03. The closure integration
branch applies SPEC-0202 lifecycle completion before this source handoff.
No existing/HOME/production backup repository contents, key values, HOME logs or production rows are
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
| Initial read-only comparison before approved handoff (2026-10-03), `d2a5dfc79` | HISTORICAL READ_ONLY | `restic/docker-compose.yml` mounts only `/pgbackrest`, `backup.sh` lists only that repository, and `hyhome-backup.sh` invokes only mng-pg stanza. `dev-pgbackrest` was declared separately; SPEC-0202 was `draft` at that baseline and the writer handoff had not yet occurred. The current approved handoff and source chain are recorded separately below. |
| Current Kafka/analytics/mail source inspection | READ_ONLY | Debezium connector uses Avro with Schema Registry and has a named slot/publication/heartbeat; no live connector registration or lag evidence. Flink wrapper sets a 60s checkpoint interval but no restore result. Stalwart relay is disabled while Mailpit remains development capture; no real send result. |
| `python3 -m unittest tests.validation.test_compose_baseline_gates.BackupContractTests.test_dev_repository_mount_and_scheduler_failure_contract` before implementation | RED, exit 1 | Missing development mount raised StopIteration; the failure established the missing source chain. |
| `python3 -m unittest tests.validation.test_compose_baseline_gates.BackupContractTests` after implementation | PASS, exit 0; 11 tests | Synthetic shell shim checks success, check/backup/globals/schema failure, stopped dev-pg and stale export removal. Static assertions check RO mount/create-host-path false, time limits, existing budget ordering, source exclusions and offsite identity. This does not execute pgBackRest or Restic. |
| `bash -n infra/09-platform-ops/restic/bin/hyhome-backup.sh`; `sh -n infra/09-platform-ops/restic/backup.sh`; `git diff --check` | PASS, each exit 0 | Syntax and whitespace only. |
| `bash .agents/skills/infra-validate/scripts/static-checks.sh` | BLOCKED, exit 2 | 9 PASS, 0 FAIL, 6 BLOCKED: unsupported tracked input graph and missing YAML/shell lint tools; dependent Compose checks not executed. Fixture cleanup PASS. |
| Updated isolated Restic round-trip fixture | NOT_RUN | Fixture now mounts both distinct synthetic pgBackRest repositories and asserts development repository snapshot inclusion. This unittest fixture itself was not executed; the separate authorized fresh synthetic chain below provides current recovery evidence. |
| HOME backup, actual capacity, HOME selected-image dev restore and WAL/PITR | NOT_RUN | Source readiness is not an operational receipt. archive_mode remains off; separate preflight and approval required. |
| HOME backup, offsite copy, PITR, credential rotation, data migration | NOT_RUN | Separate exact operational approval required |

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W4 | PASS: approved backup writer ledger and source handoff are recorded | [Backup policy](../../../05.operations/policies/0021-backup-and-restore.md) |
| 6 | W4 | PASS: consumer-backed decisions retain honest unverified runtime states without speculative services | [Architecture owner](../../../02.architecture/descriptions/0031-home-development-host.md) |
| 7 | W4 | PASS: current Restic chain restores a selected synthetic dev-pg set into a fresh volume with data and authority comparison | [Backup runbook](../../../05.operations/runbooks/0021-backup-and-restore.md) |
| 8 | W4 | PASS: focused tests and final independent review match the source and isolated receipts; unsupported static helper remains BLOCKED | [Backup guide](../../../05.operations/guides/0021-backup-and-restore.md) |

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


The final changed metadata gate initially exited 1 for two receipt headings
outside the Task template. Moving both receipts under Verification Evidence
fixed the contract without altering runtime results; the recheck exited 0,
11 selected documents and 0 violations. Final corpus lifecycle and link checks
exited 0; the pre-existing unverified historical-link warning remains visible.

### Fresh Isolated Recovery Receipt — 2026-10-04 KST

The user renewed SPEC-0201–0205 completion and the existing synthetic-isolation
scope. No actual BKP-001, private environment, HOME service mount or production
repository was read or connected. All database rows and secret files were newly
created fixture data. The executed source revision was
`ce001be7af93aebe6430f586b56a5c443fa9f386`.

#### Preflight and exact identity

- Docker context `default`, local `unix:///var/run/docker.sock`, daemon
  `hy-home-server`; cached image identities were explicitly inspected:
  dev PG `sha256:19ffce2ca8d8eb820b0ea784c869ea20afe24e526594e7d4267b18ea22ca43f2`,
  Restic `sha256:136600b6ff6843d61d355f7f71f460a166429f35de6fd11b568fece3c9a4d510`,
  both linux/amd64. No image update or new production stack was introduced.
- Root filesystem had approximately 75 GiB available, Docker storage 2.5 TiB,
  available RAM approximately 13 GiB. These are preflight observations, not
  workload benchmarks or recovery objectives.
- Earlier successful source fixture `hyhome-p04-restore-_2a24h9a`, internal network
  `hyhome-p04-restore-_2a24h9a-net`, source/first target volumes
  `hyhome-p04-restore-_2a24h9a-source-pg` and
  `hyhome-p04-restore-_2a24h9a-restore-pg`. Final recovery used the independently
  created empty volume `hyhome-p04-restore-_2a24h9a-continuation-restore-pg` and
  internal network `hyhome-p04-restore-_2a24h9a-continuation-net`.
- Zero host ports; PostgreSQL 2 CPUs/2 GiB/shm256 MiB; Restic 1 CPU/1 GiB,
  network none, read-only container and tmpfs256 MiB. Backup/restore jobs used
  network none. Paths were limited to newly owned `/tmp/hyhome-p04-restore-*`
  synthetic scratch and the exact new named volumes. Existing entrypoint,
  `project.py`/`platform.json`, `backup.sh` and Restic sets were reused read-only.

#### Executed command and result chain

The exact top-level earlier two-stage harness invocations were:

```bash
python3 /tmp/hyhome-p04-restore-_2a24h9a/rehearsal.py
python3 /tmp/hyhome-p04-restore-_2a24h9a/continue-restore.py
```

The first invocation returned1 at the protected metadata host-side assertion
after Restic snapshot restore had returned0. The continuation returned0 after
the selected pgBackRest restore, functional comparisons and exact cleanup.
A temporary stdlib Python subprocess harness supplied the following arguments;
all subprocess results and comparisons were checked before this receipt.
No credential value appeared in arguments or this document.

| Executed command or comparison | Exit/result | Scope and meaning |
| --- | --- | --- |
| `docker exec <source> python3 /work/project.py /work/platform.json`, twice | 0, 0 | Existing provision helper, four restricted platform roles; only synthetic secrets and isolated DB. |
| Final TCP `pg_isready -h 127.0.0.1 -U postgres -d postgres` | 0 | Excludes the temporary socket-only initialization server; functional SQL checks followed. |
| Source SQL: one `app.recovery_probe` row, `app.schema_migrations` version 1, extension version, DB owner and four role flags | PASS | Baseline `1|1|2.30.2|platform_owner`; owner NOLOGIN and other privilege flags were captured and compared after recovery. |
| Source reader INSERT/DDL denial | 1, 1 expected | `SET ROLE platform_reader`; source authorization refused writes and table creation. |
| `pg_dumpall --globals-only`; `pg_dumpall --schema-only` | 0, 0 | Synthetic globals/schema only, private staging, never printed. |
| `pgbackrest --stanza=dev stanza-create` | 0 | Separate encrypted fixture repository and synthetic cipher secret. |
| `pgbackrest --stanza=dev --type=full backup` while archive_mode off | 87 expected | Online backup refusal retained; no WAL setting/restart of HOME. |
| Stop exact source; `gosu postgres pgbackrest --stanza=dev --no-online --force --type=full backup` | 0, 0 | Offline consistent backup of stopped fixture; stale PID explicitly handled, no other container used that volume. |
| Existing `backup.sh init` | 0 | Two new synthetic state/host repositories initialized. |
| Existing `backup.sh backup` with development source mount deliberately absent | 3 expected | Restic incomplete-snapshot result propagated; partial state snapshot is not full success and host step was not accepted as success. |
| Existing `backup.sh backup`; `backup.sh check` with source present | 0, 0 | Current state allowlist chain included encrypted dev repository and synthetic globals/schema; existing host set also passed. |
| `backup.sh cmd state restore <selected-snapshot> --target /out` | 0 | Explicit snapshot `acd8fc798dbf5f4e97f445e05a7ced64bb3d63a616451852a6218262d5102910`; restored `/src/state/dev-pgbackrest`, not live PGDATA. |
| Metadata container check and new restore-volume emptiness check | 0, 0 | Stanza metadata is `backup/dev/backup.info`; verified under container permissions. Target was a separately created empty volume. |
| `gosu postgres pgbackrest --stanza=dev --set=19700101-000000F restore` | 75 expected | Unknown selected label rejected before accepting recovery. |
| `gosu postgres pgbackrest --stanza=dev --set=20261003-160007F restore` | 0 | Actual repository input was the Restic-restored development copy, read-only; exact compatible image/default secret-aware wrapper, fresh target. |
| Recovered PG TCP readiness; before/after SQL and four role-flag comparison | 0, PASS | One row, migration version1, Timescale2.30.2, platform_owner and role flags match source. Reader SELECT succeeded; INSERT/DDL each returned1 as expected. |
| Exact fixture `docker rm -f`, named `docker volume rm`, `docker network rm`, followed by inspect-absence checks | 0, PASS | Removed only owned fixture resources, including continuation target. No down-v, prune, HOME stop or old-volume removal. |

The missing-source exit3 semantics are documented by the official
[Restic scripting contract](https://github.com/restic/restic/blob/master/doc/075_scripting.rst).
Existing bounded scheduler failure/capacity assertions remain covered by the
11-test `BackupContractTests` receipt; this fixture does not emulate an operational
capacity failure or actual scheduler deployment.

#### Harness corrections and limits

Initial attempts are not hidden as successful runs. Socket-only readiness allowed
an initialization-phase connection failure (provision exit2), corrected to final TCP
readiness. The next harness expected missing-source exit1, but the observed supported
Restic exit3 was the intended negative result. A metadata assertion initially used
the repository root instead of the stanza path; its corrected host-side check then
met the existing UID70 directory permission boundary. That check was moved inside a
container, and recovery continued from the already verified restored repository on
a new empty target. These were fixture assertions/readiness errors; no backup source
or authorization control was weakened. Every failed attempt's exact containers,
volumes and networks was removed before proceeding.

This is fresh synthetic **offline immediate consistency recovery** evidence through
the existing Restic source chain. It is not actual HOME backup, online WAL/PITR,
remote R2 copy/restore, application cutover, credential rotation, retention activation,
RPO/RTO measurement or data migration. Those remain NOT_RUN with the durable
POL/RUN-0021 owners. Source readiness and isolated recovery PASS apply only to the
observed image, selected backup/snapshot and fixture schema.

The invocation-owned ephemeral harness and synthetic payload are cleanup artifacts,
not a maintained reusable acceptance entrypoint. They are removed after the
consumer confirms helper inspection. This receipt preserves observed commands,
exit codes, identities and comparisons, but a later rerun must prepare a newly
reviewed fixture with fresh names/credentials/empty targets. Copying the former
temporary path or reusing an old snapshot/volume name is not a reproducibility
guarantee. No frozen Spec/Task body is changed to hide these limits.

### Client Configuration Isolation Replay

Earlier temporary harnesses inherited the controller environment. Their cached-image
functional result did not prove exclusion of Docker user-client configuration.
The final replay on 2026-10-04 KST closes that evidence gap: every Docker call,
including readiness/inspect/cleanup routes, used root-owned mode0755 verified
`/usr/bin/docker` and an explicit minimal child environment: PATH `/usr/bin:/bin`,
invocation-owned empty HOME and DOCKER_CONFIG directories, and
DOCKER_HOST `unix:///var/run/docker.sock`. Three subprocess routes were checked
to have that explicit environment. No caller HOME/config/proxy/auth helper
configuration was inherited; no user-global setting was changed.

```bash
python3 /tmp/hyhome-p04-sanitized-btujdqhh/rehearsal.py
```

This exact top-level invocation returned0. The complete chain ran serially from
a fresh source and new empty target without a continuation: provision/rerun0,
source SQL/metadata0, reader write/DDL1 expected, online-backup87 expected,
offline full0, missing-source Restic3 expected, complete state/host backup0/check0,
explicit snapshot restore0, container metadata/empty target checks0, unknown-label75
expected, selected-label pgBackRest restore0, recovered readiness/SQL/role comparison0,
reader SELECT0/write/DDL1 expected. Baseline and restored result both were
`1|1|2.30.2|platform_owner`, with the same four role login/privilege flags.

Final fixture `hyhome-p04-sanitized-btujdqhh` used internal network
`hyhome-p04-sanitized-btujdqhh-net`, exact new volumes
`hyhome-p04-sanitized-btujdqhh-source-pg` and `hyhome-p04-sanitized-btujdqhh-restore-pg`,
backup label `20261003-161637F`, Restic snapshot
`27e5a2ac77f7c5aebaeaceee57f317c281497e98bdb4c5fcda769dc33b42c5d6`. Exact image identities were unchanged from the
receipt above. Actual inspect confirmed internal=true, host ports empty,
PG memory2147483648 bytes/NanoCpus2000000000/shm268435456 bytes.

Source/restored containers, named volumes and internal network cleanup each
returned0, and explicit inspect checks confirmed absence of all named transient
containers/volumes/networks. Four earlier owned scratches and the final
`/tmp/hyhome-p04-sanitized-btujdqhh` scratch were removed after helper-consumer
inspection and receipt recording. Only owned synthetic material was removed.
The ephemeral-script reproducibility limit above also applies to this final replay.
All HOME/online WAL/PITR/offsite/real-data exclusions remain NOT_RUN.

## Review Evidence

Independent backup/infra/security review approved the exact source diff with
operational follow-up. The reviewer reran 11 backup tests, shell syntax,
static backup render, catalog and corpus lifecycle; all exited 0. An
unrelated Grafana descendant link was reported and corrected by its owner.
Dev source does not change archive_mode, retention, secret values or HOME scheduling.
The synthetic SPEC-0202 restore is not a current HOME or offsite receipt.

Final independent review on 2026-10-04 approved the sanitized replay and
POL/GDE/RUN-0021 summaries with no open CRITICAL/HIGH/MEDIUM finding. The
trusted Docker client, fresh source/target, exact selected snapshot/set,
SQL/role comparisons and cleanup establish criterion 7 only for this fixture.
The continuing backup schedule, capacity, WAL/PITR, offsite and actual HOME
restore obligations remain with POL/RUN-0021 and require separate approval.
Completing this Task does not complete SPEC-0204 Task1's security acceptance.

## Commit Ledger

Baseline `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`; package draft `0f67cb297`, review transition `2157e62c5`. SPEC-0202 handoff integrated locally before source writing; backup source and first static receipt are committed at `ce001be7af93aebe6430f586b56a5c443fa9f386`; the fresh synthetic receipt below follows that source revision.

## Rulings

No new backup stack, live PGDATA copy, `latest` restore, retention deletion,
new analytics engine or duplicate observability component. A missing consumer
is a design/verification gap, not authority to provision one.

## Deferred Items

Approved capacity and backup schedule; actual
restoration target/image/WAL range; project S3/search/reader access; HOME and
external mail/connector operations remain separate.
