---
title: "Laboratory Open Notebook"
version: "1.0.1"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
created: "2026-05-09"
---

# Laboratory Open Notebook

> Local knowledge notebook and SurrealDB-backed laboratory service.

## Overview

Open Notebook provides an admin/laboratory notebook interface for local knowledge workflows. The stack runs the `open_notebook` application and a dedicated `surrealdb` database backend for persistence, both interconnected via `ai_net`.

Lifecycle: **OPTIONAL**. Root Compose includes this definition; explicit profiles (`notebook`, `surrealdb`) control activation.

## Audience

- **Operators**: Managing local laboratory services, data persistence, and credential custody.
- **Developers**: Testing notebook-driven AI or knowledge workflows.
- **AI Agents**: Discovering service boundaries, secrets, and validation paths.

## Scope

### In Scope

- Docker Compose definitions for `open_notebook` and `surrealdb`.
- Local persistent volumes under `${DEFAULT_MANAGEMENT_DIR}` (`open-notebook-data` and `surrealdb-data`).
- Gateway exposure for Open Notebook through Traefik routing, the admin IP allowlist, and the application password.
- Docker secret consumption for notebook password, encryption key, and database credentials.
- Multi-stage build context for custom SurrealDB runtime (`surrealdb/Dockerfile`).

### Out of Scope

- Production notebook promotion policy.
- User content governance inside notebook data.
- External model provider credentials or private notebook exports.

## Structure

```text
open-notebook/
├── docker-compose.yml        # Open Notebook and SurrealDB service definitions
├── surrealdb/                # SurrealDB custom build context
│   ├── Dockerfile            # Multi-stage build definition
│   ├── docker-entrypoint.sh  # Secret-aware entrypoint script
│   └── README.md             # SurrealDB package documentation
└── README.md                 # This file
```

- [docker-compose.yml](docker-compose.yml)
- [surrealdb/Dockerfile](surrealdb/Dockerfile)
- [surrealdb/docker-entrypoint.sh](surrealdb/docker-entrypoint.sh)
- [surrealdb/README.md](surrealdb/README.md)

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Laboratory Open Notebook service leaf in `11-laboratory`; services: `open_notebook`, `surrealdb`; root include active via [root docker-compose.yml](../../../docker-compose.yml) -> `infra/11-laboratory/open-notebook/docker-compose.yml` |
| Config files | `docker-compose.yml`, `surrealdb/Dockerfile`, `surrealdb/docker-entrypoint.sh` |
| Config values | env keys: `SURREALDB_USERNAME`, `SURREALDB_NAMESPACE`, `SURREALDB_DATABASE`, `OPEN_NOTEBOOK_PASSWORD_FILE`, `OPEN_NOTEBOOK_ENCRYPTION_KEY_FILE`, `API_URL`, `SURREAL_URL`, `SURREAL_USER`, `OLLAMA_API_BASE`; profiles: `notebook`, `surrealdb` |
| Compose linkage | root include active via [root docker-compose.yml](../../../docker-compose.yml) -> `infra/11-laboratory/open-notebook/docker-compose.yml` |
| Networks | `ai_net`, `edge_net` |
| Volumes | `open-notebook-data:/app/data`, `surrealdb-data:/mydata` |
| Ports | Loopback-only API port `127.0.0.1:${OPEN_NOTEBOOK_API_URL:-5055}:5055`; Traefik targets web internal `${OPEN_NOTEBOOK_WEB_URL:-8502}` via `expose`; SurrealDB internal port `8000` via `expose` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.open-notebook.rule`, `traefik.http.routers.open-notebook.entrypoints`, `traefik.http.routers.open-notebook.tls`, `traefik.http.middlewares.open-notebook-admin-ip.ipallowlist.sourcerange`, `traefik.http.routers.open-notebook.middlewares`, `traefik.http.services.open-notebook.loadbalancer.server.port` |
| Secret refs | names: `surreal_db_password`, `open_notebook_password`, `open_notebook_encryption_key`; mounts: `/run/secrets/surreal_db_password`, `/run/secrets/open_notebook_password`, `/run/secrets/open_notebook_encryption_key` |
| Healthcheck | Compose healthcheck declared for `surrealdb` and `open_notebook` |
| Operations | Guide (`docs/05.operations/catalog/11-laboratory/0073-open-notebook/guide.md`), Policy (`docs/05.operations/catalog/11-laboratory/0073-open-notebook/policy.md`), Runbook (`docs/05.operations/catalog/11-laboratory/0073-open-notebook/runbook.md`) |
| Validation | [check-all-hardening.sh](../../../scripts/hardening/check-all-hardening.sh) tier `11-laboratory`; [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh) root `notebook` profile; [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | Start with the hardening check, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. Validate the root-active laboratory profile with `HYHOME_COMPOSE_PROFILES="notebook" bash scripts/validation/validate-docker-compose.sh`.
2. Start only when the `notebook` profile is intentionally selected; `admin` no longer selects Open Notebook or SurrealDB.
3. Access the Open Notebook UI at `https://open-notebook.${DEFAULT_URL}` from the permitted CIDR range and sign in with the Open Notebook password; the route intentionally has no shared SSO middleware. The API host port answers on loopback only.
4. Keep floating image usage reviewed through `infra/image-tag-policy.exceptions.json`.
5. Keep credentials in Docker secrets and environment variables; do not commit plaintext values.

## Tech Stack

Runtime image pins are declared in [Compose](docker-compose.yml) and referenced Dockerfiles. The [version registry](../../tech-stack.versions.json) is a derived Compose image projection.

| Component | Image / Source | Purpose |
| --- | --- | --- |
| `open_notebook` | [declared runtime image](../../tech-stack.versions.json) | Notebook UI and API runtime |
| `surrealdb` | [Dockerfile](surrealdb/Dockerfile) | Local metadata and notebook persistence (pinned to SurrealDB v2 for Open Notebook compatibility) |

## Configuration

### Services

| Service | Profiles | Networks | `ai_net`, `edge_net` | Volumes | Secrets |
| --- | --- | --- | --- | --- | --- |
| `open_notebook` | `notebook` | `ai_net`, `edge_net` | `127.0.0.1:${OPEN_NOTEBOOK_API_URL:-5055}:5055` | `open-notebook-data:/app/data` | `surreal_db_password`, `open_notebook_password`, `open_notebook_encryption_key` |
| `surrealdb` | `notebook`, `surrealdb` | `ai_net` | None (`expose: 8000`) | `surrealdb-data:/mydata` | `surreal_db_password` |

### Environment Variables

| Variable | Required | Service | Description |
| --- | :---: | --- | --- |
| `SURREALDB_USERNAME` | Yes | `open_notebook`, `surrealdb` | Database username for SurrealDB |
| `SURREALDB_NAMESPACE` | Yes | `open_notebook` | Namespace used by Open Notebook |
| `SURREALDB_DATABASE` | Yes | `open_notebook` | Database name within namespace |
| `DEFAULT_URL` | Yes | `open_notebook` | Base domain for Traefik routing |
| `DEFAULT_MANAGEMENT_DIR` | Yes | Global | Base host directory for persistent bind mounts |
| `OPEN_NOTEBOOK_API_URL` | No | `open_notebook` | Loopback host port for API (default: 5055) |
| `OPEN_NOTEBOOK_WEB_URL` | No | `open_notebook` | Web UI internal port (default: 8502) |
| `LAB_ALLOWED_CIDRS` | No | Traefik | IP allowlist for admin endpoints |

### Traefik Routing

Open Notebook routes via Traefik on `websecure` with `gateway-standard-chain@file`, `open-notebook-admin-ip@docker`, and `large-body@file`. Shared SSO is intentionally absent (owner decision, commit `b90b74837`); access control is the CIDR allowlist plus the Open Notebook password.

### Database Compatibility

Open Notebook upstream only supports SurrealDB v2. SurrealDB v3 is incompatible and not supported. The local build context in [Dockerfile](surrealdb/Dockerfile) fixes the base image to `surrealdb/surrealdb:v2`. Upgrading SurrealDB beyond v2 is prohibited until upstream Open Notebook explicitly adds support.

### Secret Management

- `surreal_db_password`: Used by SurrealDB for root authentication and by Open Notebook to establish database connection.
- `open_notebook_password`: Password used for application-level access control.
- `open_notebook_encryption_key`: Used by Open Notebook to encrypt and decrypt model API keys. Losing this key renders stored credentials unrecoverable.

## Image Tag Review

- `infra/11-laboratory/open-notebook/docker-compose.yml` currently uses [declared runtime image](../../tech-stack.versions.json), which is a latest-like tag.
- The tag is registered in `infra/image-tag-policy.exceptions.json` for monthly Laboratory Operator review; keep it unchanged unless a later approved pass pins a stable tag or removes the exception.

## Validation

- Run `bash scripts/hardening/check-all-hardening.sh 11-laboratory` after any Compose or config reference changes.
- Run `HYHOME_COMPOSE_PROFILES="notebook" bash scripts/validation/validate-docker-compose.sh` for root-active laboratory profile validation.
- Run `python3 scripts/validation/run-ci-gate.py --profile changed` to keep service documentation and operation links synchronized.
- Confirm persistence by checking `docker logs --tail=200 open-notebook` after config changes.
- Verify SurrealDB readiness via healthcheck endpoint `http://127.0.0.1:8000`.

## Troubleshooting

- Start with the hardening check to confirm Open Notebook, SurrealDB, network, and secret references.
- Check Open Notebook and SurrealDB logs before changing API URL, encryption, or database settings.
- **SurrealDB Version Compatibility**: Open Notebook requires SurrealDB v2. Using SurrealDB v3 causes protocol and query incompatibilities.
- **Encryption Key Loss**: Changing or losing `OPEN_NOTEBOOK_ENCRYPTION_KEY` renders existing encrypted provider API keys unreadable. Retain key custody separate from database backups.
- **Database Dependency**: Open Notebook waits for SurrealDB to pass its healthcheck (`ws://surrealdb:8000/rpc`). Inspect SurrealDB container logs if Open Notebook fails to start.

## Related Documents

- **Guide**: Open Notebook usage guide (`docs/05.operations/catalog/11-laboratory/0073-open-notebook/guide.md`)
- **Policy**: Open Notebook operations policy (`docs/05.operations/catalog/11-laboratory/0073-open-notebook/policy.md`)
- **Runbook**: Open Notebook recovery runbook (`docs/05.operations/catalog/11-laboratory/0073-open-notebook/runbook.md`)
- **SurrealDB Guide**: SurrealDB usage guide (`docs/05.operations/catalog/11-laboratory/0080-surrealdb/guide.md`)
- **SurrealDB Policy**: SurrealDB operations policy (`docs/05.operations/catalog/11-laboratory/0080-surrealdb/policy.md`)
- **SurrealDB Runbook**: SurrealDB recovery runbook (`docs/05.operations/catalog/11-laboratory/0080-surrealdb/runbook.md`)
- [Image tag exceptions](../../image-tag-policy.exceptions.json)
- [Documentation index](../../../docs/README.md)
- [Infrastructure index](../../README.md)

Runtime pins are owned by the Compose/Dockerfile declarations; the [derived Compose image projection](../../tech-stack.versions.json) provides drift verification.
