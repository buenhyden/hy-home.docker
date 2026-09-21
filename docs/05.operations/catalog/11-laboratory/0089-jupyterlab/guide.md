---
title: "JupyterLab Usage Guide"
version: "1.0.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-21"
layer: "operations"
artifact_id: "GDE-0089"
parent_ids:
- "POL-0089"
implementation_services:
  infra/11-laboratory/jupyterlab/docker-compose.yml:
  - jupyterlab
created: "2026-09-21"
---

# JupyterLab Usage Guide

## Usage

### Purpose and classification

JupyterLab is an OPTIONAL single-user notebook server selected only by
`data-science`, which also selects MLflow. It is outside HOME and the current
eight-profile operating command.

### Current implementation

- [JupyterLab Compose](../../../../../infra/11-laboratory/jupyterlab/docker-compose.yml)
  builds a scipy-notebook image with pinned libraries and runs one Jupyter Server.
- Notebooks live in `${DEFAULT_MANAGEMENT_DIR}/jupyterlab/work`, outside the
  repository. The bind uses `create_host_path: false`, so a missing directory
  fails the start instead of creating a root-owned one that UID 1000 cannot write.
- The server requires the `jupyter_token` secret. Startup refuses a token
  shorter than 16 characters.

### Access paths and isolation

| Path | Control | What it does not provide |
| --- | --- | --- |
| Browser route | Gateway SSO, then the server token (cookie afterwards); REST and kernel WebSockets follow the same route | Per-user identity inside Jupyter; every SSO user who knows the token is the same UID 1000 |
| Direct `infra_net` access to port 8888 | Server token | Network isolation; peers can attempt the API |
| Kernels and terminals | Run as UID 1000 in the container | Isolation between people, CPU/memory quotas per user |

SSO proves who reached the gateway; it does not isolate kernels or files. Real
multi-user isolation needs JupyterHub with a spawner and per-user storage. That
is a separate design and dependency decision; do not paste JupyterHub settings
into this single-user server.

### MLflow from notebooks

`MLFLOW_TRACKING_URI` points to `http://mlflow:5000` on `infra_net`, which
bypasses the browser SSO route and has no MLflow-level authentication. Runs
logged from a notebook are not attributed to an SSO user. Artifacts upload
through the MLflow proxy, so the notebook holds no MinIO credential. If MLflow
authentication is adopted later, give notebooks a dedicated MLflow identity
instead of reopening an unauthenticated API.

### Normal use and backup

Stop the server before copying the work directory. Treat notebooks and outputs
as potentially sensitive data. Rebuild the image to change libraries; keep the
MLflow client version aligned with the server.

## Common Checks

- `HYHOME_COMPOSE_PROFILES=data-science bash scripts/validation/validate-docker-compose.sh`
- Unauthenticated request to the route returns 401 (gateway); a request to `/api/status` without the token returns 403 (server).

## Runbook Handoff

Use the [runbook](runbook.md) for token, start, kernel and restore problems.

## Traceability

- [Policy](policy.md) (`POL-0089`)
- [Runbook](runbook.md) (`RUN-0089`)
- [MLflow guide](../0088-mlflow/guide.md) (`GDE-0088`)
- [Laboratory architecture](../../../../02.architecture/descriptions/0011-laboratory-architecture.md)

## Related Documents

- [Jupyter Server security](https://jupyter-server.readthedocs.io/en/latest/operators/security.html)
- [Jupyter Docker Stacks common options](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html)
