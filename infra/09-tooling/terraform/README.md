<!-- [ID:09-tooling:terraform] -->
# Terraform Infrastructure Tool

> Infrastructure as Code (IaC) execution environment for automated provisioning.

## 1. Overview (KR)

이 서비스는 인프라를 코드(IaC)로 정의하고 관리하는 **Terraform 실행 환경**입니다. 컨테이너화된 환경(`hashicorp/terraform:1.14.4`)을 통해 일관된 IaC 실행, 상태(State) 관리 및 클라우드 프로바이드 인증을 지원합니다.

## 2. Overview

The `terraform` service provides a standardized, containerized CLI environment for executing HashiCorp Terraform commands. It ensures version consistency across the team and simplifies the mounting of workspaces and cloud credentials (AWS/Azure) for infrastructure-as-code (IaC) operations within the `hy-home.docker` ecosystem.

## 3. Tech Stack

| Component | Technology | Version | Role |
| :--- | :--- | :--- | :--- |
| **Engine** | HashiCorp Terraform | 1.14.4 | IaC Provisioning Engine |
| **Environment** | Docker (Alpine) | - | Containerized Execution |

## 4. Networking

| Name | Type | Target | Description |
| :--- | :--- | :--- | :--- |
| **Outbound** | `infra_net` | Internet / Local APIs | Access to cloud providers and local backends. |
| **Backend** | S3 / MinIO | `9000` | Remote state storage access (if configured). |

## 5. Persistence

- **Workspace**: `./workspace` (State and `.tf` configuration files).
- **Credentials**: `$HOME/.aws`, `$HOME/.azure` (ReadOnly mounts from host).

## 6. Usage

```bash
# Initialize project
docker compose run --rm terraform init

# Plan changes
docker compose run --rm terraform plan

# Apply changes
docker compose run --rm terraform apply
```

## 7. File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | CLI service definition with profile `tooling`. |
| `workspace/` | Working directory for terraform configuration. |
| `README.md` | Infrastructure-level documentation (this file). |

---

## Documentation References

- **Guide**: [Terraform System Guide](../../../docs/07.guides/09-tooling/terraform.md)
- **Operation**: [IaC Operations Policy](../../../docs/08.operations/09-tooling/terraform.md)
- **Runbook**: [Terraform Recovery Runbook](../../../docs/09.runbooks/09-tooling/terraform.md)
