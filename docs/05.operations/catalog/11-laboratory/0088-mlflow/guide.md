---
title: "MLflow Usage Guide"
version: "1.0.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-22"
layer: "operations"
artifact_id: "GDE-0088"
parent_ids:
- "POL-0088"
implementation_services:
  infra/11-laboratory/mlflow/docker-compose.yml:
  - mlflow
  - mlflow-db-provision
  - mlflow-artifact-provision
created: "2026-09-21"
---

# MLflow Usage Guide

## Usage

### Purpose and classification

MLflow is an OPTIONAL experiment tracking server selected by `mlops` or
`data-science`. It is outside HOME and outside the current eight-profile
operating command; adding it is a separate activation decision.

### Current implementation

- [MLflow Compose](../../../../../infra/11-laboratory/mlflow/docker-compose.yml)
  owns three services: `mlflow-db-provision` runs the feature SQL, then
  `mlflow-artifact-provision` creates the bucket and a bucket-scoped MinIO
  identity, then `mlflow` starts.
- The tracking store is the `MLFLOW_DB_NAME` database on `mng-pg`, owned by
  `MLFLOW_DB_USER`. Other login roles lose the default `PUBLIC` connect right.
- Artifacts go to `s3://${MLFLOW_ARTIFACT_BUCKET}` through the server's artifact
  proxy. SDK clients upload and download through MLflow and never hold MinIO
  credentials. The MLflow MinIO identity cannot read other buckets.
- The shared `mng-pg-init` job no longer creates MLflow objects and no longer
  reads MLflow secrets, so `core`/`mng`/`dev`/`local` start without them.

### Sizing

Measured on first start (2026-09-21): with default settings MLflow 3.x starts
server-job consumers (`huey`, about 200 MB each) and uvicorn workers, and the
512 MB template limit caused repeated OOM kills. The Compose file disables
server-side jobs (`MLFLOW_SERVER_ENABLE_JOB_EXECUTION=false`; GenAI scheduled
scorers and trace archival are not used), runs two workers and sets
`mem_limit: 1g` (steady state about 560 MB). Re-enable jobs only with a measured
memory budget.

### Authentication and identity

| Path | Control | Limitation |
| --- | --- | --- |
| Browser `https://mlflow.${DEFAULT_URL}` | Gateway SSO (`sso-auth`); any realm user passes | No MLflow-level user, experiment permission or group authorization |
| SDK inside `infra_net` (`http://mlflow:5000`) | None; Host header must match `--allowed-hosts` | Any container on `infra_net` can read and write every experiment |
| Artifact storage | Bucket-scoped MinIO user held only by the server | Deleting runs through MLflow deletes artifacts |

MLflow's documented OIDC route is the community `mlflow-oidc-auth` plugin
(`--app-name oidc-auth`); the built-in alternative is `basic-auth`. The plugin
is **not adopted**: its compatibility with the pinned server release, the UI,
REST API and SDK token flow, its maintenance and security review, and a
Keycloak client with session and authorization design are all unverified. Until
an owner-approved change proves those conditions, keep gateway SSO for the
browser and treat `infra_net` reachability as the SDK trust boundary. Do not
open the route without SSO to make an SDK work.

### Normal use, backup, and upgrade

Set `MLFLOW_TRACKING_URI` to the internal URL for notebooks and jobs. Existing
experiment and artifact URIs stay valid only while `MLFLOW_ARTIFACT_BUCKET` and
the database name are unchanged; renaming either is a migration.

Back up the tracking database with `pg_dump` of `MLFLOW_DB_NAME` and the bucket
with a MinIO mirror, taken together, because runs reference artifact paths.
Restore into an isolated `mng-pg` and MinIO first and compare run and artifact
counts. Before an upgrade, read the release notes; the server applies database
migrations on start, so take the backup first. No backup or restore has been run
for this service.

## Common Checks

- `HYHOME_COMPOSE_PROFILES="mlops data-science" bash scripts/validation/validate-docker-compose.sh`
- `python3 -m unittest tests.validation.test_compose_baseline_gates`
- `docker compose --profile core --profile mlops ps mlflow mlflow-db-provision mlflow-artifact-provision`

## Runbook Handoff

Use the [runbook](runbook.md) for provisioning failures, credential rotation,
restore and upgrade.

## Traceability

- [Policy](policy.md) (`POL-0088`)
- [Runbook](runbook.md) (`RUN-0088`)
- [Laboratory architecture](../../../../02.architecture/descriptions/0011-laboratory-architecture.md)
- [Current Task](../../../../03.specs/0180-home-dev-convergence/tasks/tsk-0007-optional-capability-restructure.md)

## Related Documents

- [Image Dockerfile](../../../../../infra/11-laboratory/mlflow/Dockerfile) and [derived version projection](../../../../../infra/tech-stack.versions.json)
- [MLflow self-hosting network security](https://mlflow.org/docs/latest/self-hosting/security/network)
- [MLflow SSO and the OIDC plugin](https://mlflow.org/docs/latest/self-hosting/security/sso)
- [MLflow tracking server architecture and artifact proxy](https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server)
