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

---

## Overview

`infra/09-tooling/terraform`는 Docker Compose 서비스, 설정, 운영 문서의 구현 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Compose 서비스 정의와 관련 설정 설명
- 서비스별 README와 운영 문서 연결
- 검증 시 참고해야 할 구성 파일 인벤토리

### Out of Scope

- secret 값 원문
- 사용자 승인 없는 runtime 동작 변경
- 다른 tier의 서비스 정책 중복 정의

## Structure

```text
infra/09-tooling/terraform/
├── workspace/  # 하위 구성 영역
├── docker-compose.yml  # Docker Compose 정의
└── README.md  # This file
```

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

## Related References

- [infra/README.md](../../README.md)
- [docs/07.guides/README.md](../../../docs/07.guides/README.md)
- [docs/08.operations/README.md](../../../docs/08.operations/README.md)
- [docs/09.runbooks/README.md](../../../docs/09.runbooks/README.md)
