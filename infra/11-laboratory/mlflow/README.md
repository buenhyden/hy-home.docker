---
title: "Laboratory MLflow Tracking Server"
version: "1.0.1"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
created: "2026-09-21"
---

# Laboratory MLflow Tracking Server

> Experiment tracking and model registry backed by the management PostgreSQL and a dedicated SeaweedFS bucket.

## Overview

MLflow records runs, parameters, metrics, registered models and artifacts. The
tracking store lives in its own database on `mng-pg`; artifacts live in the
`mlflow-artifacts` SeaweedFS bucket and are proxied through the server
(`--serve-artifacts`), so SDK clients never hold object-storage credentials.
Lifecycle: **OPTIONAL**, selected only by the `mlops` or `data-science` profile;
it is not part of HOME or the current eight-profile operating selection.

## Audience

- **Data scientists and ML engineers** logging experiments from JupyterLab or scripts.
- **Operators** provisioning, backing up and restoring the tracking store and artifacts.
- **AI agents** changing this package under the owning Guide, Policy and Runbook.

## Scope

- **Included**: tracking server, feature-owned database provisioning job, gateway route.
- **Excluded**: SeaweedFS (bucket and identity) and `mng-pg` server operation (their own packages), JupyterLab, model serving,
  MLflow authentication plugins (not adopted; see the Guide).

## Structure

```text
.
├── Dockerfile                    # Official MLflow image + PostgreSQL/S3 client libraries
├── requirements.txt              # Pinned client libraries for the server image
├── docker-compose.yml            # mlflow, mlflow-db-provision
├── provisioning/
│   └── mng-pg.sql                # Role, database and CONNECT policy (feature-owned)
└── README.md
```

## Tech Stack

| Component | Source | Purpose |
| --- | --- | --- |
| `mlflow` | [Dockerfile](Dockerfile) over the official MLflow image | Tracking server and artifact proxy |
| `mlflow-db-provision` | [Compose](docker-compose.yml), PostgreSQL client image | Runs [mng-pg.sql](provisioning/mng-pg.sql) through the shared [provisioning runner](../../04-data/operational/mng-db/pg/provision/run-feature-provision.sh) |

Runtime pins are owned by the Compose/Dockerfile declarations; the
[derived Compose image projection](../../tech-stack.versions.json) provides drift verification.

## Configuration

| Field | Value |
| --- | --- |
| Profiles | `mlops`, `data-science` (both also select `mng-pg`, `mng-pg-init` and SeaweedFS for dependency closure) |
| Start order | `mng-pg` healthy → `mng-pg-init` → `mlflow-db-provision`; `seaweedfs-buckets` completed; then `mlflow` |
| Network / port | `ai_net`, `edge_net`, `mng_data_net`, `object_net`; internal `${MLFLOW_PORT:-5000}` via `expose`; no host port |
| Route | `https://mlflow.${DEFAULT_URL}` with `gateway-standard-chain`, `sso-errors`, `sso-auth` |
| Allowed hosts | `mlflow:*`, `mlflow.${DEFAULT_URL}`, `localhost:*`, `127.0.0.1:*` (DNS-rebinding guard) |
| Environment keys | `MLFLOW_PORT`, `MLFLOW_DB_USER`, `MLFLOW_DB_NAME`, `MLFLOW_ARTIFACT_BUCKET`, `MLFLOW_S3_ENDPOINT_URL`, `MLFLOW_S3_REGION`; admin connection uses `POSTGRES_DEFAULT_USER`, `POSTGRES_DEFAULT_DB` |
| Secrets | `mlflow_db_password` (PG-021), `seaweedfs_s3_mlflow_secret_key` (STRG-013); the provisioning job also reads `mng_postgres_password` |
| Credential handling | Database password reaches libpq as `PGPASSWORD`, S3 secret as `AWS_SECRET_ACCESS_KEY`; neither appears in the backend URI or argv |
| Persistence | None in the container; state is the `mng-pg` database and the SeaweedFS bucket |
| Health | `GET /health` on the internal port; proves the process answers, not DB/bucket write access |

The SeaweedFS identity `mlflow` (access key ID `mlflow`) may only read, write
and list `mlflow-artifacts`
([identities](../../04-data/lake-and-object/seaweedfs/config/s3-identities.conf));
it cannot reach any other bucket.

## Validation

- `HYHOME_COMPOSE_PROFILES="mlops data-science" bash scripts/validation/validate-docker-compose.sh`
- `python3 -m unittest tests.validation.test_compose_baseline_gates` (static provisioning contracts)
- `HYHOME_PG_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.FeatureProvisioningRehearsalTests` (disposable PostgreSQL; needs Docker)
- `python3 scripts/validation/run-ci-gate.py --profile changed`

## How to Work in This Area

1. Make sure `secrets/db/postgres/mlflow_password.txt` and `secrets/storage/seaweedfs_s3_mlflow_secret_key.txt`
   exist through the registered secret workflow before selecting the profile.
2. Validate the selection statically, then start only with an approved target, for example
   `docker compose --profile core --profile mlops up -d mlflow` in the owner's environment.
3. Point SDK clients at `MLFLOW_TRACKING_URI`; browser users use the gateway route.
4. Keep feature SQL in `provisioning/`; do not add MLflow statements to the shared `mng-pg-init` SQL.

## Related Documents

- **Guide**: MLflow usage guide (`docs/05.operations/catalog/11-laboratory/0088-mlflow/guide.md`)
- **Policy**: MLflow operations policy (`docs/05.operations/catalog/11-laboratory/0088-mlflow/policy.md`)
- **Runbook**: MLflow recovery runbook (`docs/05.operations/catalog/11-laboratory/0088-mlflow/runbook.md`)
- [Documentation index](../../../docs/README.md)
