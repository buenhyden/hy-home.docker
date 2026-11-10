---
title: "Opsflow First HOME Installation Task"
version: "0.1.3"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-10"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0051"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-06"
---

# Opsflow First HOME Installation Task

## Overview

### Objective

Record the D12 execution contract for the first installation of the Opsflow
manifest workload (`source_manifest_ingest`) in HOME. TSK-0043 handed this
installation off; this Task owns its six ordered steps, their checks and their
evidence. No step has run.

## Inputs and Authorization

On 2026-11-06 the owner (@buenhyden) decided that for D12 the execution Task and
the Runbook are written first and opened for review, and that the actual run
happens later in an owner-approved window, one step at a time. That decision
authorizes this document and the runbook procedure only. It does not approve
any change to HOME: no state-changing container command, SQL, bucket change,
credential issue or file install into the DAG directory.

Execution needs a named operator and an approved window recorded in this Task
before step 1, under the
[approval boundaries](../../../../.agents/governance/approval-boundaries.md).
Each later step starts only after the previous step's check is recorded as PASS.

The procedure source is the
[TSK-0043 handoff](tsk-0043-opsflow-data-path.md#operating-installation-handoff-to-d12).
The step-by-step commands live in the
[Airflow Runbook](../../../05.operations/runbooks/08-workflows-and-automation/0050-airflow.md);
this Task does not copy them.

## Work Log

### Ordered steps

| Step | Scope | Check | Open owner items | Status |
| --- | --- | --- | --- | --- |
| 1 | Back up `opsflow_dev` on `dev-pg`, the Airflow metadata DB `airflow` on `mng-pg` and the `opsflow-dev` bucket listing | Backup files exist, have nonzero size and recorded SHA-256; listing saved | O6 | PASS |
| 2 | Apply migrations `001`, `003`, `004`, `005`, `007` from `infra/07-workflow/airflow/workloads/manifest-pipeline/sql/` to `opsflow_dev` with session_user `opsflow_migrator` and current_user `opsflow_owner`, each with its own SHA-256; `002` and `006` are isolated-only and do not run in HOME | `008_checks.sql`, run as the audit administrator with the `007` SHA-256, ends its read-only transaction in ROLLBACK without error | O1, O2, O8 | PASS |
| 3 | Create bucket `opsflow-dev`, apply the worker identity and the `WorkerCannotDelete` bucket policy | Eight permission canaries return the expected statuses | O3 | PASS |
| 4 | Install `dags/source_manifest_ingest.py` and `workflow_lib/` at the reviewed commit, image unchanged, recording every installed path in the backup directory | File SHA-256 match the commit; `airflow dags list` shows the DAG paused with no import error | O1, O4, O5 | not run |
| 5 | Create pool `manifest_ingest` (1 slot), keep the DAG paused, run one synthetic business date and one invalid input on `airflow-worker` through Celery | Raw, validated, published and outbox rows exist; the invalid input is quarantined with `application/json` | O7 | not run |
| 6 | Unpause `source_manifest_ingest` | DAG reports unpaused; no unplanned run started | - | not run |

Rollback removes the installed files, keeps every backup and drops nothing that
existed before step 1.

### 2026-11-10 owner decisions

On 2026-11-10 the owner (@buenhyden) approved the recommended answers to
O1 through O8. They set what each step does; they do not approve any HOME
change, which still needs the per-step owner approval below.

- O1: four login secrets, `dev_pg_opsflow_migrator_password`,
  `dev_pg_opsflow_ingest_password`, `dev_pg_opsflow_notifier_password` and
  `dev_pg_opsflow_reader_password`, referenced by `opsflow.json`. The owner
  role stays NOLOGIN. The owner creates the four value files; the tracked
  wiring is in the `feat/opsflow-credential-wiring` change.
- O3: one bucket-scoped S3 identity `opsflow-worker` for `opsflow-dev` with no
  delete permission (the `WorkerCannotDelete` bucket policy), secret
  `seaweedfs_s3_opsflow_worker_secret_key`. The owner creates its value file.
- O6: backups go to `~/storage/backups/opsflow-pre-install-<timestamp>/`, each
  file with its size and SHA-256 recorded.
- O7: step 5 briefly unpauses the DAG, runs the `fixtures/2026-10-10.json`
  fixture, pauses it again, then runs the invalid input with business_date
  `2026-10-11`; the final unpause happens only in step 6.
- O8: migrations `001` to `008` are first rehearsed on a throwaway isolated
  postgres container; the HOME apply follows under a recorded owner approval,
  with the `dev-pg` administrator `postgres` running `008` read-only.
- Executor and window: the agent runs each step with per-step owner approval,
  in a 60 to 90 minute window that avoids the 08:00 Hermes cron.

Still open after these answers: O2 (whether the roles already exist), O4, O5,
and where the worker `pg.json` and `s3.json` under `OPSFLOW_SECRET_DIR` come
from; the repository does not define that source.

### Execution 2026-11-10

Operator: the agent, with the owner (@buenhyden) approving each step in the
session on 2026-11-10; the window opened at 13:00 KST and avoids the 08:00
Hermes cron. Repository revision at the start: `7f93e6080`.

Prerequisites the owner completed before step 1:

- The four dev-pg login secret files (PG-038 to PG-041, created by hand as
  `automation: X`, mode 640) and STRG-016 (generated by
  `scripts/operations/gen-secrets.sh` after `--sync-metadata` added its private
  registry row).
- The worker `pg.json` and `s3.json` in `/home/hyunyoun/storage/secrets/opsflow-worker`
  (directory 750, files 640, owner 1000:1000), written by a value-free helper that
  validates both files with `workflow_lib.adapters._validated` and refuses to
  overwrite. This answers the open source question for `OPSFLOW_SECRET_DIR`.

Step record:

- O8 rehearsal: `tests.validation.test_opsflow_database_rehearsal` with the
  reviewed `postgres:18.6-alpine` image ran 13 tests; 11 passed on the first run
  and the two cross-database cases failed before any SQL because the throwaway
  container was not ready; both passed when rerun alone. No rehearsal container
  remained.
- Step 1: backups in
  `~/storage/backups/opsflow-pre-install-20261110T130330/` (mode 600):
  `airflow.dump` (335 234 bytes, SHA-256 `909f6e239633…`, 73 table-data entries
  in `pg_restore --list`), `dev-pg-roles.sql` (SHA-256 `85b151295246…`),
  `seaweedfs-buckets.listing` (`opsflow-dev` absent) and
  `dev-pg-opsflow_dev.exists` (`0`); full hashes in `SHA256SUMS`.
- Step 1-a-0 (separately approved): the first provisioning run stopped on
  `cross_database_connect_requires_cluster_review` because `PUBLIC` still held
  CONNECT on the `postgres` database. A read-only review found only
  `dev_pg_monitor` (explicit grant) and the superuser using it, so
  `infra/04-data/dev-db/pg/provision/cluster-connect.sql` ran with
  `reviewed_connect_consumers=reviewed`. Rollback: `GRANT CONNECT ON DATABASE
  postgres TO PUBLIC`. `dev-pg-exporter` still reported `pg_up 1`.
- Step 1-a: `project.py /work/opsflow.json` (validate-only passed first) created
  `opsflow_dev`, schema `ops_flow` owned by `opsflow_owner` (NOLOGIN) and four
  login roles; each of the five roles can CONNECT only to `opsflow_dev`.
- Step 2: `001`, `003`, `004`, `005`, `007` committed as `opsflow_migrator` with
  `role=opsflow_owner`; `ops_flow.schema_version` holds versions 1-5 with the
  matching file SHA-256 values. `008_checks.sql` ran as `postgres` with the `007`
  SHA-256 and ended in ROLLBACK with 0 rows, rc 0.
- Step 3: `seaweedfs-s3` was recreated to load the `opsflow-worker` identity
  (healthy; Loki, Tempo and MLflow logged no S3 errors), `opsflow-dev` was created
  with the `seaweedfs-buckets` job, and the `WorkerCannotDelete` policy with
  principal `arn:aws:iam::000000000000:user/opsflow-worker` was applied. The eight
  repository canaries plus a read of `loki-bucket` as the worker all matched
  (`ALL_PASS`). Two canary objects remain in `opsflow-dev`.
- Step 4 is on hold: the owner forbade adding the workflow override to `.env`
  `COMPOSE_FILE` and asked for an explicit overlay rule, so the override is being
  folded into the base Airflow Compose file in a separate change. Step 4 runs
  after that change merges.

### Open owner items

These facts were not confirmed from the repository. Each stays open until the
owner records an answer here, and the step that needs it does not start before.

| Item | Question | Needed by |
| --- | --- | --- |
| O1 | `infra/04-data/dev-db/pg/provision/opsflow.json` has `password_secrets: null`, so no migrator or ingest credential is issued. Which files under `secrets/` hold them? | Steps 2, 4 |
| O2 | Do `opsflow_dev` and the five `opsflow_*` roles already exist in HOME `dev-pg`? | Step 2 |
| O3 | The worker S3 identity is not in the SeaweedFS S3 configuration. What is its access key name, its secret file path, and how is it loaded into `seaweedfs-s3`? | Step 3 |
| O4 | The workload README installs the code through `compose.workflow.override.yml` bind mounts (`OPSFLOW_CODE_DIR`); the handoff copies files into `${DEFAULT_WORKFLOW_DIR}/airflow/dags`. Which one? Either way `airflow-worker` needs `/run/opsflow` (`pg.json`, `s3.json`) and `dev_data_net`/`object_net`, which the base Compose file does not give it. | Step 4 |
| O5 | Does the running Airflow image carry the workload's Python dependencies, or is a reviewed `OPSFLOW_AIRFLOW_IMAGE` required? | Step 4 |
| O6 | What are the admin user names on `dev-pg` and `mng-pg`, and the backup target directory, and is that admin password file mounted inside each container? | Step 1 |
| O7 | Which synthetic input key and body are used (the repository fixture is `fixtures/2026-10-10.json` for source `hy-home.docker`), and how does the one triggered run proceed while the DAG stays paused? The invalid-input case needs a different `business_date` and starts only after the first run ends (`max_active_runs=1`, source and business-date uniqueness); any run still queued must be recorded before step 6 unpauses. | Step 5 |
| O8 | Which existing audit administrator login runs `008_checks.sql`? Its header and the `005`/`007` headers limit them to an approved isolated DB; does the owner approve running them on HOME `opsflow_dev`? | Step 2 |

### Read-only answers 2026-11-10

These came from read-only checks against HOME on 2026-11-10 and from the
repository at `0b7ffe8bc`. None of them changed HOME, and none of them approves a
step. O1, O7 and O8 stay open for the owner; O3 still needs the owner's
credential decision.

| Item | Observed fact | Effect on the steps |
| --- | --- | --- |
| O2 | A `psql` read on HOME `dev-pg` as the admin user returned no database matching `opsflow%` and no role matching `opsflow%`. | Step 2 needs `opsflow_dev` and the five `opsflow_*` roles provisioned first; the migrations cannot run against roles that do not exist. |
| O3 | No `opsflow` entry exists under `infra/04-data/seaweedfs`. | The worker S3 identity must be created; the owner chooses its access key name and secret file. |
| O4 | `airflow-worker` is attached only to `airflow_net` and `mng_data_net` and has no `/run/opsflow` mount. `compose.workflow.override.yml` binds the DAG and `workflow_lib` from `${OPSFLOW_CODE_DIR}` and requires `${OPSFLOW_AIRFLOW_IMAGE}`. | Step 4 follows the override route, which recreates `airflow-worker` with the extra networks and mounts; copying files into the DAG directory alone would leave the worker without database and object-store access. |
| O5 | The running `airflow-worker` image imports `boto3`, `psycopg2`, `jsonschema` and `pydantic`. | The current image may be named as `OPSFLOW_AIRFLOW_IMAGE`; a separate reviewed image is needed only if the workload adds a dependency the image lacks. |
| O6 | The admin user is `postgres` on both `dev-pg` and `mng-pg`, and each container can read its mounted `POSTGRES_PASSWORD_FILE` (`/run/secrets/dev_pg_admin_password`, `/run/secrets/mng_postgres_password`). The values were not read. The backup target directory is still the owner's choice. | Step 1 can run inside each container with its own admin file once the owner names the backup directory. |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Step 1 backups | 103 | W108 | Backup existence, size and SHA-256 | HOME `dev-pg`, `mng-pg`, `opsflow-dev` at `7f93e6080` | PASS | `~/storage/backups/opsflow-pre-install-20261110T130330/SHA256SUMS`; see Execution 2026-11-10. | required | - |
| Step 2 migrations | 103 | W108 | `008_checks.sql` | `opsflow_dev` after `001`, `003`, `004`, `005` and `007` at `7f93e6080` | PASS | `step2-migrate.log`, `step2-008.log` in the step 1 backup directory; `ops_flow.schema_version` 1-5. | required | - |
| Step 3 bucket and canaries | 103 | W108 | Permission canaries | `opsflow-dev` bucket and worker identity at `7f93e6080` | PASS | `step3-canary.json` in the step 1 backup directory (`ALL_PASS`). | required | - |
| O8 isolated rehearsal | 103 | W108 | `tests.validation.test_opsflow_database_rehearsal` | reviewed `postgres:18.6-alpine` image at `7f93e6080` | PASS | 13 of 13 after rerunning two container-readiness failures alone; see Execution 2026-11-10. | required | - |
| Step 1-a provisioning | 103 | W108 | Database, role login flags and cross-database CONNECT | HOME `dev-pg` after `cluster-connect.sql` at `7f93e6080` | PASS | See Execution 2026-11-10 (steps 1-a-0 and 1-a). | required | - |
| Step 4 code install | 103 | W108 | File hashes and paused DAG import | DAG directory and `airflow-worker` mounts | NOT_RUN | Not started; waits for O1, O4 and O5. | required | - |
| Step 5 synthetic run | 103 | W108 | Rows and quarantine readback | Pool `manifest_ingest`, one synthetic and one invalid input | NOT_RUN | Not started; waits for O7. | required | - |
| Step 6 unpause | 103 | W108 | DAG pause state | `source_manifest_ingest` | NOT_RUN | Not started; only after step 5 PASS. | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 103 | pending | Step 1 backups, Step 2 migrations, Step 3 bucket and canaries, Step 4 code install, Step 5 synthetic run, Step 6 unpause | No step has run. | SPEC-0212 TSK-0051 |

## Review and Completion

The Task and the runbook section are open for owner review. Completion needs
every step's Evidence row recorded as PASS in an approved window. A failed step
stops the run, applies that step's rollback and records the failure here.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Opsflow data path Task](tsk-0043-opsflow-data-path.md)
- [Airflow Runbook](../../../05.operations/runbooks/08-workflows-and-automation/0050-airflow.md)
- [Manifest pipeline README](../../../../infra/07-workflow/airflow/workloads/manifest-pipeline/README.md)
