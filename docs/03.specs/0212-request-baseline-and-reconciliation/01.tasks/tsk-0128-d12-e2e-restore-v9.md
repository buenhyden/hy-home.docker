---
title: "D12 v9 Runtime and Restore Acceptance Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-28"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0128"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-28"
---

# D12 v9 Runtime and Restore Acceptance Task

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the task payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Scope

##### Objective and Parent

Own criterion185/W201 in the [Spec](../spec.md) and [Plan](../plan.md). Apply
D12 of the v9 task prompts: one HOME Airflow to n8n business run (SI-18),
isolated restores of the HOME backup population that had no independent
restore evidence (SI-29), the OpenBao audit reopening and backup observations
left after the 2026-11-25 window, and an exact condition for every step that
does not run.

##### Inputs and Authority

On 2026-11-28 the user directly requested D12 from
`_workspace/workspace_task_prompts_20261127_progress_v9/` (prompt
`12_e2e_runtime_deployment_acceptance.md`), limited to that prompt's scope,
with commit, push, PR and merge after checks. Asked in this chat, the owner
chose: run the SI-18 HOME business run now, keep real SMTP delivery NOT_RUN,
run all four isolated restore groups (R2 offsite to scratch, MNG PostgreSQL
and Valkey, observability stores, SeaweedFS and model manifests), and leave
the criterion 85 reboot check blocked until a planned reboot. Work ran in the
primary checkout on branch `docs/d12-v9-e2e-restore` from `main` `191ecab99`;
brief `d12-v9` bound this Task and the Spec and Plan rows. No secret value was
read or printed; the S3 admin upload needs the owner credential. Direct user
authorization is authority; this record is not.

#### Execution Log

##### Work Performed

###### Reused acceptance

| Area | Reused evidence | Not repeated |
| --- | --- | --- |
| SI-18 outbox, claim, Mailpit capture | SPEC-0212 TSK-0051 criterion 103 (HOME install, 2026-11-10); TSK-0044 HOME one-claim delivery to Mailpit with no duplicate (2026-11-11) and criteria 73 to 75 (isolated recovery, STARTTLS) | Isolated rehearsals |
| Observability | TSK-0046 criteria 82, 83 and 84 accepted | Promtool and alert review |
| OpenBao restore | SPEC-0204 TSK-0006 restores `-06` and `-07` accepted (2026-11-25) | Snapshot restore |
| Prometheus and Gatus restore | SPEC-0245 TSK-0001 | Both |

###### SI-18 HOME business run

The input `manifest-input/hy-home.docker/2026-11-28.json` (SHA-256
`41be5679…cebf5ee`, kept at
`/home/hyunyoun/storage/volumes/backups/d12-si18/2026-11-28.json`) was written
for an unused business date. The owner reported three upload attempts with the
SeaweedFS admin identity. Run `d12-si18-2026-11-28` of
`source_manifest_ingest` (unpaused, pool `manifest_ingest` 1 slot) failed all
three tries with `manifest_task_failed`. A dry diagnosis in `airflow-worker` as
the worker identity (uid 1000, groups 0 and 1000), with no write, found
`s3_input_missing`: HEAD returned 404. The filer listing of
`/buckets/opsflow-dev/` held only `manifest-quarantine` and
`manifest-validated`, and the gateway log showed no `opsflow-dev` request in
that window, so the uploads never reached HOME SeaweedFS. An anonymous request
from `object_net` to `seaweedfs-s3:8333` returned 403, so the route works.
`ops_flow.runs`, `documents` and `outbox` stayed at 1, 1 and 1. The notifier
workflow `WSyLpKMPsWUaS0dX` stays inactive and was not published. The likely
client cause is the AWS CLI virtual-hosted addressing against a custom
endpoint; the next attempt sets path-style addressing (Remaining Conditions).

###### SI-29 restore population

| Target | This run | Result |
| --- | --- | --- |
| R2 offsite | `restic-offsite restore 4e6347d0 d057ab44` (host and state pair of the 2026-11-28 03:58 KST run) into an owned empty 0700 scratch | host 199 files, 489,697 bytes, 16 s; state 19,631 files, 2,037,706,972 bytes, 136 s; 175 s total; nothing written to R2 |
| MNG PostgreSQL | `mng-pg-immediate-restore-rehearsal.py --label 20261124-111938F_20261127-185716D` (RUN-0021 step 5a, local repository) | PASS in 756 s: system ID and database list match, `app_db`, `mlflow`, heartbeat and dbt objects present, counts stable, 10 extensions and 136 sequences observed, one-time login probe PASS, cleanup removed; scratch PGDATA kept 0700 for the 7-day owner review |
| MNG and DEV Valkey | The R2 copies of `mng-valkey.rdb` and `dev-valkey.rdb` loaded into disposable `valkey/valkey:9.1.4-alpine` (HOME image ID), `--network none` | MNG 16 keys loaded and 5 expired, 21 at dump time, against 19 to 21 live `redis_db_keys` at 18:50 to 18:51 UTC; DEV 0 against live 0; write, read and delete round trip; containers removed |
| Grafana | The R2 copy of `grafana.db` under disposable `grafana/grafana:13.3.2` (HOME image ID), `--network none`, plugin preinstall off | `integrity_check` ok; 7 data sources, 5 users, 728 migrations; `/api/health` `database: ok`; dashboards are file-provisioned; container removed |
| Loki, Tempo, Alertmanager | Policy check | Telemetry history is excluded from the state snapshot (POL-0021, RUN-0024); configuration comes from Git; no restore applies |
| SeaweedFS | `weed export` of every restored volume in the 4.54 image, read-only, `--network none` | 35 of 35 volumes readable, 93,865 needles; filer metadata load, `volume.fsck` and S3 reads NOT_RUN because RUN-0024 steps 5 to 8 have no registered executor and the runbook forbids an improvised one |
| Model manifests | Restored Ollama `manifests` and `manifests-v2` against the live `ollama` container | 8 of 8 names and 8 of 8 files identical |
| Configuration and keys | Restored host set file names against live `secrets/` and `.env` | 198 of 198 secret file names match, `.env` present; contents not compared |

###### OpenBao and backup observations

- W6 audit reopening: logrotate runs hourly with the daily rule; the
  2026-11-27 15:00 rotation left `audit.json.1` (inode 115607799) and OpenBao's
  write descriptor points at the new `audit.json` (inode 115607912), which kept
  growing. The postrotate failure alert was not observed.
- W7 next backup: the 2026-11-27 03:34 KST run failed because `pg_dumpall`
  could not load `timescaledb-2.30.3` in `template1` of `dev-pg`; every
  `dev-pg` database now reports TimescaleDB 2.32.1, matching the image, and
  the dev-pg README already requires `ALTER EXTENSION timescaledb UPDATE` in
  every database including `template1`. The 2026-11-27 19:51 and 2026-11-28
  04:00 KST runs finished, with the R2 copy, its 73 snapshots and the size
  line.

##### Blockers and Decisions

- The SI-18 run needs an input that reaches `opsflow-dev`; only the owner holds
  the admin credential.
- Real SMTP delivery and final receipt stay NOT_RUN: no approved external
  target or credential (owner decision).
- The criterion 85 reboot check stays blocked until a planned reboot of server
  A (owner decision).
- The SeaweedFS four-service restore needs a registered restore executor.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 185 | W201 | method=observation; tool=docker, airflow, psql, weed shell; command=DAG trigger d12-si18-2026-11-28, dry read in airflow-worker, filer listing, row counts | HOME, 2026-11-28 13:17 to 13:45 KST | FAIL | Input 404; no rows written | required | - |
| E02 | 185 | W201 | method=automated; tool=docker compose; command=restic-offsite restore 4e6347d0 d057ab44 | R2, owned scratch | PASS | 175 s, both sets rc 0 | required | - |
| E03 | 185 | W201 | method=automated; tool=Python3; command=mng-pg-immediate-restore-rehearsal.py --label 20261124-111938F_20261127-185716D | Local pgBackRest repository | PASS | result=PASS, 756 s | required | - |
| E04 | 185 | W201 | method=automated; tool=docker; command=disposable valkey-server on the R2 RDB copies | R2 copy | PASS | MNG 16 loaded, DEV 0 | required | - |
| E05 | 185 | W201 | method=automated; tool=docker, sqlite3; command=integrity_check and disposable Grafana /api/health | R2 copy | PASS | database ok | required | - |
| E06 | 185 | W201 | method=automated; tool=docker; command=weed export of each restored volume | R2 copy | PASS | 35 volumes, 93,865 needles | required | - |
| E07 | 185 | W201 | method=observation; tool=-; command=filer meta load, volume.fsck and S3 read in an isolated four-service SeaweedFS | R2 copy | NOT_RUN | No registered restore executor (RUN-0024) | required | - |
| E08 | 185 | W201 | method=automated; tool=sha256sum, ls; command=manifest and key-name comparison | R2 copy and live | PASS | 8 of 8 manifests, 198 of 198 names | required | - |
| E09 | 185 | W201 | method=observation; tool=docker, journalctl; command=audit file inodes and descriptor; hyhome-backup runs | HOME, 2026-11-28 | PASS | Reopened after rotation; backups 11-27 19:51 and 11-28 04:00 finished | required | - |
| E10 | 185 | W201 | method=observation; tool=-; command=real SMTP send and final receipt | - | NOT_RUN | No approved target or credential | optional | - |

##### Resolution Links

E01 is resolved by a new run whose input reaches `opsflow-dev`; E07 by a
registered SeaweedFS restore executor.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 185 | pending | E01,E02,E03,E04,E05,E06,E07,E08,E09,E10 | Awaiting the SI-18 rerun and owner acceptance | @buenhyden |

##### Remaining Conditions

- SI-18: upload the input with path-style addressing (`aws configure set
  default.s3.addressing_style path` before `aws s3 cp`), confirm it with a
  filer listing, trigger one run, read back `runs`, `documents` and `outbox`,
  then publish the notifier for one claim, confirm one Mailpit message and
  `accepted_by_smtp`, unpublish and confirm the next poll sends nothing.
- SeaweedFS filer metadata and S3 read restore: needs a registered executor.
- Criterion 85 reboot regression and the OpenBao postrotate failure alert.
- Cleanup: the R2 scratch `/home/hyunyoun/storage/backups/r2-restore-scratch/r2-restore-mYTk3E`
  (holds restored secrets) and the Valkey and Grafana copies under
  `/home/hyunyoun/storage/backups/restore-scratch-d12/` are removed after owner
  approval; the MNG PostgreSQL scratch stays for the 7-day review.

#### Handoff

##### Promotion Receipt

None: this Task records runtime and restore evidence only.

##### Next Owner

The owner reruns the SI-18 upload and decides criterion185. D13 and D14 are
not started automatically.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
