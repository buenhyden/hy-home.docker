---
title: "Opsflow First HOME Installation Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-06"
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
| 1 | Back up `opsflow_dev` on `dev-pg`, the Airflow metadata DB `airflow` on `mng-pg` and the `opsflow-dev` bucket listing | Backup files exist, have nonzero size and recorded SHA-256; listing saved | O6 | not run |
| 2 | Apply `001`-`008` from `infra/07-workflow/airflow/workloads/manifest-pipeline/sql/` to `opsflow_dev` as `opsflow_migrator`, in the order the SQL README sets | `008_checks.sql` with the `007` SHA-256 ends in ROLLBACK without error | O1, O2 | not run |
| 3 | Create bucket `opsflow-dev`, apply the worker identity and the `WorkerCannotDelete` bucket policy | Eight permission canaries return the expected statuses | O3 | not run |
| 4 | Install `dags/source_manifest_ingest.py` and `workflow_lib/` at the reviewed commit, image unchanged | File SHA-256 match the commit; `airflow dags list` shows the DAG paused with no import error | O1, O4, O5 | not run |
| 5 | Create pool `manifest_ingest` (1 slot), keep the DAG paused, run one synthetic business date and one invalid input | Raw, validated, published and outbox rows exist; the invalid input is quarantined with `application/json` | O7 | not run |
| 6 | Unpause `source_manifest_ingest` | DAG reports unpaused; no unplanned run started | - | not run |

Rollback removes the installed files, keeps every backup and drops nothing that
existed before step 1.

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
| O6 | What are the admin user names on `dev-pg` and `mng-pg`, and the backup target directory? | Step 1 |
| O7 | Which synthetic input key and body are used? The repository fixture is `fixtures/2026-10-10.json` for source `hy-home.docker`. | Step 5 |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Step 1 backups | 103 | W108 | Backup existence, size and SHA-256 | HOME `dev-pg`, `mng-pg`, `opsflow-dev` | NOT_RUN | Not started; waits for an approved operator, window and O6. | required | - |
| Step 2 migrations | 103 | W108 | `008_checks.sql` | `opsflow_dev` after `001`-`007` | NOT_RUN | Not started; waits for O1 and O2. | required | - |
| Step 3 bucket and canaries | 103 | W108 | Permission canaries | `opsflow-dev` bucket and worker identity | NOT_RUN | Not started; waits for O3. | required | - |
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
