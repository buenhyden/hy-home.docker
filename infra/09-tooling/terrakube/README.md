<!-- [ID:09-tooling:terrakube] -->
# Terrakube IaC Automation Platform

> Terraform orchestration, remote state, and private registry service stack

## Overview

`infra/09-tooling/terrakube/` defines the Terrakube service stack for centralized Terraform workflows. The stack includes API, UI, and executor services using Terrakube 2.29.0 images, integrates with Keycloak for identity, stores metadata in the management PostgreSQL service, and uses MinIO-compatible S3 storage for Terraform state.

This README is the service-level entrypoint. It summarizes the Compose surface and links to the canonical guide, operations policy, and runbook.

## Audience

이 README의 주요 독자:

- Operators
- Developers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Terrakube API, UI, and executor Compose service boundaries
- Gateway hostnames and internal service relationships
- Metadata, state storage, and Docker secret usage at a high level
- Related guide, operation, and runbook links

### Out of Scope

- Secret values or credential material
- Terraform module authoring standards
- Long-form IaC governance policy
- Cloud provider account setup

## Structure

```text
terrakube/
├── docker-compose.yml  # Terrakube API, UI, and executor service definitions
└── README.md           # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Terrakube IaC Automation Platform service leaf in `09-tooling`; services: `terrakube-api`, `terrakube-ui`, `terrakube-executor`; root include optional/commented in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-tooling/terrakube/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | env keys: `ApiDataSourceType`, `DatasourceHostname`, `DatasourceDatabase`, `DatasourceUser`, `DatasourcePassword_FILE`, `GroupValidationType`, `UserValidationType`, `AuthenticationValidationType`, plus 43 more; profiles: `tooling`, `iac` |
| Compose linkage | root include optional/commented in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-tooling/terrakube/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `/var/run/docker.sock:/var/run/docker.sock` |
| Ports | Not declared |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.terrakube-api.rule`, `traefik.http.routers.terrakube-api.entrypoints`, `traefik.http.routers.terrakube-api.tls`, `traefik.http.routers.terrakube-api.middlewares`, `traefik.http.services.terrakube-api.loadbalancer.server.port`, `traefik.http.routers.terrakube-ui.rule`, plus 9 more |
| Secret refs | names: `terrakube_db_password`, `minio_app_user_password`, `terrakube_valkey_password`, `terrakube_pat_secret`, `terrakube_internal_secret`; mounts: `/run/secrets/terrakube_db_password`, `/run/secrets/minio_app_user_password`, `/run/secrets/terrakube_valkey_password`, `/run/secrets/terrakube_pat_secret`, `/run/secrets/terrakube_internal_secret` |
| Healthcheck | Compose healthcheck declared for `terrakube-api`, `terrakube-ui`, `terrakube-executor` |
| Operations | [Guide](../../../docs/05.operations/guides/09-tooling/terrakube.md), [Policy](../../../docs/05.operations/policies/09-tooling/terrakube.md), [Runbook](../../../docs/05.operations/runbooks/09-tooling/terrakube.md) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `docker compose config`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. Read the parent [`../README.md`](../README.md) and this service Compose file before changing Terrakube.
2. Keep secret material in Docker secrets; document only secret names and purpose.
3. Verify API, UI, executor, PostgreSQL, MinIO, Valkey, and Keycloak assumptions together when changing the stack.
4. Update the related guide, operation, or runbook when user access, state handling, or recovery behavior changes.

## Tech Stack

| Component | Image / Source | Role |
| --- | --- | --- |
| `terrakube-api` | `azbuilder/api-server:2.29.0` | API server and metadata orchestration |
| `terrakube-ui` | `azbuilder/terrakube-ui:2.29.0` | Web management UI |
| `terrakube-executor` | `azbuilder/executor:2.29.0` | Terraform job execution |
| Metadata | Management PostgreSQL | Terrakube database |
| State storage | MinIO S3-compatible bucket `tfstate` | Terraform state and output storage |
| Identity | Keycloak / DEX validation | SSO integration |

## Usage Instructions

After the stack is enabled with the `tooling` or `iac` profile, use these routed endpoints:

- API: `https://terrakube-api.${DEFAULT_URL}`
- UI: `https://terrakube-ui.${DEFAULT_URL}`
- API docs: `https://terrakube-api.${DEFAULT_URL}/swagger-ui.html`

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after any Compose or config reference changes.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking documentation ready.
- Verify workspace configuration by checking the Terrakube UI and confirming Terraform workspaces are registered with correct provider credentials.
- Confirm API connectivity by checking `docker logs terrakube | grep -i 'error\|warn'` after config changes.
- Verify OIDC authentication by confirming the Keycloak client configuration matches Terrakube's auth settings.

## Troubleshooting

- Start with `docker compose config` to confirm Terrakube network, database, and secret references render.
- Check Terrakube logs and the linked runbook before changing executor, PAT, or persistence settings.

## Related Documents

- [Tooling tier README](../README.md)
- [Terrakube guide](../../../docs/05.operations/guides/09-tooling/terrakube.md)
- [Terrakube operations policy](../../../docs/05.operations/policies/09-tooling/terrakube.md)
- [Terrakube recovery runbook](../../../docs/05.operations/runbooks/09-tooling/terrakube.md)
- [Root infra README](../../README.md)
