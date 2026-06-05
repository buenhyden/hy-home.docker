---
status: active
---
<!-- Target: docs/05.operations/guides/09-tooling/terraform.md -->

# Operations: Terraform Policy Usage Guide

## Usage

### Overview

이 가이드는 Operations: Terraform Policy Usage Guide의 사용 맥락, 전제 조건, 일반 점검, runbook handoff 기준을 설명한다.

<!-- [ID:09-tooling:terraform] -->

### Usage Type

`system-guide | how-to`

### Target Audience

- Operators
- Developers
- Contributors
- AI Agents

### Purpose

- Operations: Terraform Policy Usage Guide의 운영 사용 맥락을 빠르게 파악한다.
- 반복 실행 절차와 장애 대응은 연결된 runbook으로 넘긴다.
- 통제 기준은 연결된 policy 문서와 분리해 유지한다.

### Prerequisites

- Repository checkout 접근 가능
- 관련 `docs/03.specs/` 또는 operations 문서 확인 가능
- 필요한 경우 Docker/Docker Compose 명령 실행 권한

### Step-by-step Instructions

1. 이 문서의 overview와 usage context를 확인한다.
2. 관련 service, configuration, 또는 documentation target을 식별한다.
3. `## Common Checks`의 검증 항목을 실행하거나 검토한다.
4. 반복 절차, 장애 대응, rollback, escalation이 필요하면 `## Runbook Handoff`의 runbook으로 이동한다.

### Common Pitfalls

- guide에 policy control이나 복구 절차를 직접 섞어 목적 프로파일을 흐리는 경우
- target-relative link를 템플릿 위치 기준으로 계산하는 경우
- 검증 명령 실행 결과 없이 운영 가능 상태를 단정하는 경우

### Implementation Context (KR)

이 문서는 `docs/05.operations/guides/09-tooling/terraform.md` 주제의 사용 가이드다. 기존 본문을 기준으로 작업자가 필요한 배경, 절차, 주의사항을 빠르게 찾도록 보강한다.

### Terraform System Usage

> Comprehensive guide for managing Infrastructure as Code (IaC) using the containerized Terraform environment.

### Overview

Terraform is used in `hy-home.docker` to provision and manage cloud resources (AWS, Azure) and local infrastructure (Docker, Kubernetes). To ensure environment parity and eliminate "works on my machine" issues, we use a containerized CLI approach.

### Key Concepts

#### 1. Job-based Execution

Instead of a long-running service, Terraform is treated as a **job**.

- Use root compose plus the Terraform leaf compose so the optional `infra_net` context is present.
- Profiles: specify `tooling` and `iac` when rendering or running the helper.

#### 2. State Management

- **Local State**: Stored in `infra/09-tooling/terraform/workspace/terraform.tfstate`.
- **Remote Backend**: It is highly recommended to use the `s3` backend (integrated with MinIO in `04-data`) for shared state and locking.

#### 3. Credential Handling

Credentials are not stored in the container. They are mounted from the host:

- AWS: `/root/.aws` maps to your host `$HOME/.aws`.
- Azure: `/root/.azure` maps to your host `$HOME/.azure`.

### Common Workflows

#### Initializing a Project

```bash
TERRAFORM_COMPOSE_FILES="-f docker-compose.yml -f infra/09-tooling/terraform/docker-compose.yml"
docker compose $TERRAFORM_COMPOSE_FILES --profile tooling --profile iac run --rm terraform init
```

#### Resource Provisioning (Plan & Apply)

Always generate a plan file before applying to prevent accidental changes.

```bash
## 1. Generate plan
TERRAFORM_COMPOSE_FILES="-f docker-compose.yml -f infra/09-tooling/terraform/docker-compose.yml"
docker compose $TERRAFORM_COMPOSE_FILES --profile tooling --profile iac run --rm terraform plan -out=tfplan

## 2. Review the plan
## 3. Apply the plan
docker compose $TERRAFORM_COMPOSE_FILES --profile tooling --profile iac run --rm terraform apply tfplan
```

### Formatting and Validation

Maintain code quality by using built-in tools.

```bash
TERRAFORM_COMPOSE_FILES="-f docker-compose.yml -f infra/09-tooling/terraform/docker-compose.yml"
docker compose $TERRAFORM_COMPOSE_FILES --profile tooling --profile iac run --rm terraform fmt
docker compose $TERRAFORM_COMPOSE_FILES --profile tooling --profile iac run --rm terraform validate
```

### Troubleshooting

#### Lock File Issues

If Terraform fails with "Error acquiring the state lock", ensure no other group members are applying changes. If a process crashed, refer to the [force unlock procedure](../../runbooks/09-tooling/terraform.md#3-force-unlocking-state).

#### Network Connectivity

The container uses `infra_net`. If local services are unreachable, verify that runtime rendering uses root network/secret/dependency context rather than the Terraform leaf compose file alone.

## Common Checks

- `bash scripts/hardening/check-all-hardening.sh 09-tooling`
- `bash scripts/validation/check-repo-contracts.sh`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/09-tooling/terraform.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/09-tooling/terraform.md)
- [Recovery runbook](../../runbooks/09-tooling/terraform.md)
