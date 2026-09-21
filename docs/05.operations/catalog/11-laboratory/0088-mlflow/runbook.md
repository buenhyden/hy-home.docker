---
title: "MLflow Recovery Runbook"
version: "1.0.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-21"
layer: "operations"
artifact_id: "RUN-0088"
parent_ids:
- "GDE-0088"
created: "2026-09-21"
---

# MLflow Recovery Runbook

## When to Use

Provisioning job failure, server start or health failure, credential rotation,
artifact access denial, tracking-store restore, or upgrade.

## Procedure

1. Validate and inspect from the repository root:

   ```bash
   docker compose --profile core --profile mlops config --quiet
   docker compose --profile core --profile mlops ps -a mlflow mlflow-db-provision mlflow-artifact-provision
   docker compose --profile core --profile mlops logs --tail=100 mlflow-db-provision mlflow-artifact-provision mlflow
   ```

2. Read the provisioning exit code. `64` is an input problem found before any
   database or MinIO change (missing, empty or multi-line secret, invalid name).
   `3` is a psql error; the log names the refused condition, such as a database
   owned by another role or an administrator role name.
3. `ON_ERROR_STOP` stops at the first error but does not undo statements that
   already committed. Fix the cause and re-run the job; every statement is
   idempotent:

   ```bash
   docker compose --profile core --profile mlops up --no-deps mlflow-db-provision
   docker compose --profile core --profile mlops up --no-deps mlflow-artifact-provision
   ```

4. Start or restart the server only after both jobs exit `0`.

### Credential rotation

1. Obtain approval naming the secret, services and restart.
2. Replace the secret file through the registered secret workflow.
3. Re-run the matching provisioning job; it resets only the MLflow role
   password or the MLflow MinIO user secret.
4. Recreate `mlflow` and confirm health and one artifact read.

### Restore and upgrade

1. Stop `mlflow`. Dump `MLFLOW_DB_NAME` and mirror the bucket; record the source
   commit, image, row counts and object count.
2. Restore both into an isolated environment and compare counts before any
   production restore. A database restore without the matching bucket leaves
   dangling artifact URIs.
3. For an upgrade, take step 1 first, then start the new image and watch its
   migration output.

## Evidence

Record command exits, job exit codes, image, source commit, counts and checksums.
Never record passwords, access keys or artifact contents.

## Rollback or Recovery

Configuration rollback restores the Compose files from Git. A database
migration run by an upgrade is reversed only by the pre-upgrade backup. Restore
and upgrade rehearsals are **planned but unexecuted**.

## Escalation

Stop on a refused foreign-owned database, any request to grant superuser or the
shared MinIO credential, a failed restore count comparison, or a request to
remove gateway SSO.

## Traceability

- [Guide](guide.md) (`GDE-0088`)
- [Policy](policy.md) (`POL-0088`)
- [MLflow Compose](../../../../../infra/11-laboratory/mlflow/docker-compose.yml)

## Related Documents

- [Image Dockerfile](../../../../../infra/11-laboratory/mlflow/Dockerfile) and [derived version projection](../../../../../infra/tech-stack.versions.json)
- [Management database runbook](../../04-data/0028-management-database/runbook.md)
- [MinIO runbook](../../04-data/0023-minio/runbook.md)
