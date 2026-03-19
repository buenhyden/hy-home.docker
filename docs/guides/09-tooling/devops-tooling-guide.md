---
layer: infra
---
# DevOps Tooling & Static Analysis Guide

**Overview (KR):** SonarQube, Terraform, Locust, Syncthing, Registry 등 프로젝트 전체에서 사용되는 DevOps 도구들의 구성 및 가이드입니다.

> **Components**: `sonarqube`, `terraform`, `terrakube`, `locust`, `syncthing`, `registry`

## 1. Static Analysis (SonarQube)

SonarQube provides continuous inspection of code quality.

### Technical Specifications

| Attribute | Internal DNS | Port | External Proxy |
| --- | --- | --- | --- |
| **Web UI** | `sonarqube` | `9000` | `sonarqube.${DEFAULT_URL}` |

- **Setup Node**: Upon initial boot, SonarQube initializes its PostgreSQL schema. Use `admin / admin` for initial login and change the password immediately.

## 2. Infrastructure as Code (Terraform)

We utilize Terraform for managing production-equivalent resources.

- **Execution Mode**: Local-within-Docker or distributed via Terrakube.
- **State Integrity**: Managed via a remote backend (S3/MinIO). Maintain your local state files or rely on the Terrakube API.

## 3. Automation Layer (Terrakube)

Terrakube acts as the private automation engine for Terraform runs.

- **UI Interface**: `https://terrakube-ui.${DEFAULT_URL}`
- **API Interface**: `https://terrakube-api.${DEFAULT_URL}`
- **Security**: Redirects to the centralized Keycloak provider for authentication.
- **State Storage**: MinIO (`infra/04-data/minio`) for Terraform state and plan logs.
- **Cache**: Management Valkey (`infra/04-data/mng-db`) for distributed locking.

## 4. Load Testing (Locust)

Locust is an open-source load testing tool configured in master-worker mode.

- **Web UI**: `http://localhost:${LOCUST_HOST_PORT}` (direct port exposure, no Traefik proxy).
- **Mode**: 1 master + 2 worker replicas.
- **Metrics**: Integrates with InfluxDB (`infra/06-observability`) for real-time metrics storage.
- **Locustfile**: Injected via bind-mounted volume (`${DEFAULT_TOOLING_DIR}/locust`).

## 5. File Synchronization (Syncthing)

Syncthing provides continuous peer-to-peer file synchronization.

- **Web GUI**: `https://syncthing.${DEFAULT_URL}` via Traefik.
- **Sync Ports**: TCP/UDP `${SYNCTHING_SYNC_HOST_PORT}` (default 22000), UDP `${SYNCTHING_BROADCASTS_HOST_PORT}` (default 21027).
- **Synced Directory**: `${DEFAULT_RESOURCES_DIR}` (shared resource storage).

## 6. Container Registry

A private Docker container image registry for locally-built custom images.

- **Port**: `${REGISTRY_PORT}` (default 5000), exposed directly (no Traefik proxy).
- **Use Case**: Stores custom images such as `hy/loki`, `hy/tempo`, etc.
- **Storage**: `${DEFAULT_REGISTRY_DIR}` bind-mounted.

## 7. Maintenance & Integration

| Action | Reference | Link |
| --- | --- | --- |
| **Manual** | Tooling Ops | [Operations Guide](tooling-operations.md) |
| **Context** | Service Context | [Tooling Context](tooling-context.md) |
| **Lifecycle** | Startup & Secrets | [Tooling Lifecycle](tooling-lifecycle.md) |
| **Troubleshoot**| Infra Recovery | [Runbooks](../runbooks/README.md) |

Always audit the `sonarqube_db_password`, `terrakube_internal_secret`, `terrakube_pat_secret`, and `syncthing_password` secrets before initiating large-scale infra changes.
