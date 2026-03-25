<!-- [ID:09-tooling:terraform] -->
# Terraform CLI

> Infrastructure as Code (IaC) execution environment.

## 1. Overview (KR)

이 서비스는 인프라를 코드(IaC)로 정의하고 관리하는 **Terraform 실행 환경**입니다. 컨테이너화된 환경을 통해 일관된 IaC 실행 및 워크스페이스 관리를 지원합니다.

## 2. Overview

The `terraform` service provides a containerized CLI environment for executing HashiCorp Terraform commands. It ensures a consistent binary version and standardized workspace/credential mounting for infrastructure provisioning in `hy-home.docker`.

## 3. Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **terraform** | Terraform 1.14 | IaC Provisioning CLI |

## 4. Networking

| Service | Protocol | Description |
| :--- | :--- | :--- |
| **CLI** | N/A | Job mode only, no persistent exposure. |
| **Network** | `infra_net` | Access to providers and remote backends (MinIO). |

## 5. Persistence

- **Workspace**: `./workspace` (Code and local state).
- **Credentials**: `$HOME/.aws`, `$HOME/.azure` (Host mounts).

## 6. Usage

```bash
docker compose run --rm terraform plan
docker compose run --rm terraform apply
```

## 7. File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | CLI execution service definition. |
| `workspace/` | Local directory for `.tf` files. |
| `README.md` | Usage notes and setup (this file). |

---

## Documentation References

- [IaC Deployment Policy](../../../docs/08.operations/09-tooling/iac-deployment-policy.md)
- [Tooling Context](../../../docs/07.guides/09-tooling/README.md)
