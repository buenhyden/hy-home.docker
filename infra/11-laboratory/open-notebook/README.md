# Laboratory Open Notebook

> Local knowledge notebook and SurrealDB-backed laboratory service.

## Overview

Open Notebook provides an admin/laboratory notebook UI for local knowledge workflows. The stack includes the `open_notebook` application and a local `surrealdb` data store, both connected to `infra_net` and exposed through the gateway profile when enabled.

## Audience

- **Operators**: Managing local laboratory services and data persistence.
- **Developers**: Testing notebook-driven AI or knowledge workflows.
- **AI Agents**: Discovering service boundaries, secrets, and validation paths.

## Scope

### In Scope

- Docker Compose definitions for `open_notebook` and `surrealdb`.
- Local persistent volumes under `${DEFAULT_MANAGEMENT_DIR}`.
- Gateway exposure through Traefik labels.
- Docker secret consumption for notebook and database credentials.

### Out of Scope

- Production notebook promotion policy.
- User content governance inside notebook data.
- External model provider credentials or private notebook exports.

## Structure

```text
open-notebook/
├── docker-compose.yml     # Open Notebook and SurrealDB service definitions
├── surrealdb/             # Custom SurrealDB image context
└── README.md              # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Laboratory Open Notebook service leaf in `11-laboratory`; services: `surrealdb`, `open_notebook`; root include active via [root docker-compose.yml](../../../docker-compose.yml) -> `infra/11-laboratory/open-notebook/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | env keys: `SURREALDB_USERNAME`, `OPEN_NOTEBOOK_PASSWORD_FILE`, `OPEN_NOTEBOOK_ENCRYPTION_KEY_FILE`, `API_URL`, `SURREAL_URL`, `SURREAL_USER`, `SURREAL_NAMESPACE`, `SURREAL_DATABASE`; profiles: `admin`, `dev` |
| Compose linkage | root include active via [root docker-compose.yml](../../../docker-compose.yml) -> `infra/11-laboratory/open-notebook/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `surrealdb-data:/mydata`, `open-notebook-data:/app/data`, `open-notebook-data`, `surrealdb-data` |
| Ports | Host-bound API/DB ports `${SURREALDB_HOST_PORT:-8000}:8000`, `${OPEN_NOTEBOOK_API_URL:-5055}:5055`; Traefik targets web internal `${OPEN_NOTEBOOK_WEB_URL:-8502}` via `expose` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.open-notebook.rule`, `traefik.http.routers.open-notebook.entrypoints`, `traefik.http.routers.open-notebook.tls`, `traefik.http.routers.open-notebook.middlewares`, `traefik.http.services.open-notebook.loadbalancer.server.port` |
| Secret refs | names: `surreal_db_password`, `open_notebook_password`, `open_notebook_encryption_key`; mounts: `/run/secrets/surreal_db_password`, `/run/secrets/open_notebook_password`, `/run/secrets/open_notebook_encryption_key` |
| Healthcheck | Compose healthcheck declared for `surrealdb` and `open_notebook` |
| Operations | [Guide](../../../docs/05.operations/guides/11-laboratory/open-notebook.md), [Policy](../../../docs/05.operations/policies/11-laboratory/open-notebook.md), [Runbook](../../../docs/05.operations/runbooks/11-laboratory/open-notebook.md) |
| Validation | [check-all-hardening.sh](../../../scripts/hardening/check-all-hardening.sh) tier `11-laboratory`; [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh) root `admin` profile; [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with the hardening check, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. Validate the root-active admin profile with `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh`.
2. Start only when the `admin` or `dev` profile is intentionally selected and host-bound API/DB ports are approved for the target environment.
3. Keep floating image usage reviewed through `infra/image-tag-policy.exceptions.json`.
4. Keep credentials in Docker secrets and environment variables; do not commit plaintext values.

## Service Configuration

| Component | Image / Source | Purpose |
| --- | --- | --- |
| `open_notebook` | `lfnovo/open_notebook:v1-latest-single` | Notebook UI and API runtime |
| `surrealdb` | `./surrealdb/Dockerfile` | Local metadata and notebook persistence |

## Image Tag Review

- `infra/11-laboratory/open-notebook/docker-compose.yml` currently uses `lfnovo/open_notebook:v1-latest-single`, which is a latest-like tag.
- The tag is registered in `infra/image-tag-policy.exceptions.json` for monthly Laboratory Operator review; keep it unchanged unless a later approved pass pins a stable tag or removes the exception.

## Validation

- Run `bash scripts/hardening/check-all-hardening.sh 11-laboratory` after any Compose or config reference changes.
- Run `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh` for root-active laboratory profile validation.
- Verify kernel connectivity by opening a notebook and confirming the kernel starts without errors.
- Confirm persistence by checking `docker logs open-notebook | grep -i 'error\|warn'` after config changes.
- Verify the notebook data volume is mounted and notebooks persist across container restarts.

## Troubleshooting

- Start with the hardening check to confirm Open Notebook, SurrealDB, network, and secret references.
- Check Open Notebook and SurrealDB logs before changing API URL, encryption, or database settings.

## Related Documents

- [Laboratory guides](../../../docs/05.operations/guides/11-laboratory/README.md)
- [Laboratory policies](../../../docs/05.operations/policies/11-laboratory/README.md)
- [Laboratory runbooks](../../../docs/05.operations/runbooks/11-laboratory/README.md)
- [Image tag exceptions](../../image-tag-policy.exceptions.json)
