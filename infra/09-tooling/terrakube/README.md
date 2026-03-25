<!-- [ID:09-tooling:terrakube] -->
# Terrakube

> Open-source alternative to Terraform Cloud/Enterprise.

## 1. Overview (KR)

이 서비스는 Terraform 워크플로우를 자동화하고 관리하는 **Self-hosted IaC 오케스트레이션 플랫폼**입니다. 팀 단위의 인프라 협업 및 상태 관리를 지원합니다.

## 2. Overview

The `terrakube` stack provides a complete IaC management platform for `hy-home.docker`. It manages state files, execution policies, and workspace organization, supporting scheduled runs and team-based infrastructure governance.

## 3. Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **terrakube-api** | Java/Spring | Platform Logic & API |
| **terrakube-ui** | React | Management Dashboard |
| **terrakube-executor** | Docker / TF | Terraform Execution Node |

## 4. Networking

| Service | Port | Description |
| :--- | :--- | :--- |
| **API** | `8080` | Backend API (`terrakube-api.${DEFAULT_URL}`). |
| **UI** | `3000` | Dashboard (`terrakube-ui.${DEFAULT_URL}`). |
| **Executor** | `8090` | Job processing node (`terrakube-executor.${DEFAULT_URL}`). |

## 5. Persistence & Dependencies

- **Volumes**: State stored in MinIO (`tfstate` bucket).
- **Secrets**: `terrakube_db_password`, `minio_app_user_password`, `terrakube_valkey_password`, `terrakube_pat_secret`.
- **Integrations**: Keycloak (Auth), MinIO (Storage), Valkey (Cache), PostgreSQL (DB).

## 6. File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | Full Terrakube stack definition. |
| `README.md` | Service overview (this file). |

---

## Documentation References

- [IaC Deployment Policy](../../../docs/08.operations/09-tooling/iac-deployment-policy.md)
- [Tooling Context](../../../docs/07.guides/09-tooling/README.md)
