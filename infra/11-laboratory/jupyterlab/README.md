---
title: "Laboratory JupyterLab Workspace"
version: "1.0.1"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-22"
created: "2026-09-21"
---

# Laboratory JupyterLab Workspace

> Single-user JupyterLab for data-science notebooks with an internal MLflow tracking client.

## Overview

JupyterLab runs one Jupyter Server for one operator. It is **not** JupyterHub:
there is no per-user spawning, kernel isolation or filesystem isolation between
people who reach it. Every authenticated browser session and every holder of the
server token can run code, open terminals and read the whole work directory with
the container's UID 1000. Lifecycle: **OPTIONAL**, selected only by
`data-science`; it is not part of HOME or the current eight-profile selection.

## Audience

- **Data scientists** using notebooks, DuckDB/Polars and the MLflow SDK.
- **Operators** managing the token, work directory backup and image rebuilds.
- **AI agents** changing this package under the owning Guide, Policy and Runbook.

## Scope

- **Included**: JupyterLab server image, Python dependency pins, gateway route, token handling, work volume.
- **Excluded**: MLflow server (sibling package), JupyterHub or multi-user isolation, GPU kernels.

## Structure

```text
.
├── Dockerfile          # scipy-notebook base + pinned requirements
├── requirements.txt    # Pinned notebook libraries (MLflow client matches the server)
├── docker-compose.yml  # jupyterlab service
└── README.md
```

## Tech Stack

| Component | Source | Purpose |
| --- | --- | --- |
| `jupyterlab` | [Dockerfile](Dockerfile) over the Jupyter Docker Stacks scipy image | Notebook server |
| Libraries | [requirements.txt](requirements.txt) | MLflow client, Polars, DuckDB, PyArrow, psycopg, boto3/s3fs, confluent-kafka, JupySQL, Optuna |

Runtime pins are owned by the Compose/Dockerfile declarations; the
[derived Compose image projection](../../tech-stack.versions.json) provides drift verification.

## Configuration

| Field | Value |
| --- | --- |
| Profile | `data-science` (also selects MLflow and its dependency closure) |
| Network / port | `infra_net`; internal `${JUPYTER_PORT:-8888}` via `expose`; no host port |
| Route | `https://jupyter.${DEFAULT_URL}` with `gateway-standard-chain`, `sso-errors`, `sso-auth`; WebSockets pass through Traefik |
| Authentication | Gateway SSO for the browser route **and** a Jupyter Server token from secret `jupyter_token` (AI-007), exported as `JUPYTER_TOKEN`; startup fails when it is shorter than 16 characters. An empty token is not allowed because `infra_net` peers could otherwise reach kernels, terminals and the REST API directly |
| Work directory | Bind `${DEFAULT_MANAGEMENT_DIR}/jupyterlab/work` → `/home/jovyan/work`, `create_host_path: false`; create it owned by UID 1000 before first start |
| MLflow client | `MLFLOW_TRACKING_URI=http://mlflow:${MLFLOW_PORT}` — an internal path that does not pass the gateway SSO route |
| Object storage | No object-storage credential is injected; artifacts are uploaded through the MLflow artifact proxy |
| Health | `GET /api` (unauthenticated version endpoint); proves the server answers, not kernel health |

## Validation

- `HYHOME_COMPOSE_PROFILES=data-science bash scripts/validation/validate-docker-compose.sh`
- `python3 scripts/validation/run-ci-gate.py --profile changed`
- The image build is not exercised by repository checks; build only in an approved environment.

## How to Work in This Area

1. Create `secrets/tools/jupyter_token.txt` through the registered secret workflow and the work
   directory with owner UID 1000.
2. Validate statically, then start only with an approved target, for example
   `docker compose --profile core --profile data-science up -d jupyterlab`.
3. Open the route, pass SSO, then enter the server token once per browser session.
4. Keep library pins aligned with the MLflow server version when upgrading.

## Related Documents

- **Guide**: JupyterLab usage guide (`docs/05.operations/catalog/11-laboratory/0089-jupyterlab/guide.md`)
- **Policy**: JupyterLab operations policy (`docs/05.operations/catalog/11-laboratory/0089-jupyterlab/policy.md`)
- **Runbook**: JupyterLab recovery runbook (`docs/05.operations/catalog/11-laboratory/0089-jupyterlab/runbook.md`)
- [MLflow package](../mlflow/README.md)
- [Documentation index](../../../docs/README.md)
