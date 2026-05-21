<!-- Target: docs/05.operations/guides/09-tooling/terraform.md -->
# Operations: Terraform Policy Usage Guide

<!-- [ID:09-tooling:terraform] -->
## Usage: Terraform System

> Comprehensive guide for managing Infrastructure as Code (IaC) using the containerized Terraform environment.

### Overview

Terraform is used in `hy-home.docker` to provision and manage cloud resources (AWS, Azure) and local infrastructure (Docker, Kubernetes). To ensure environment parity and eliminate "works on my machine" issues, we use a containerized CLI approach.

### Key Concepts

#### 1. Job-based Execution

Instead of a long-running service, Terraform is treated as a **job**.

- Always use `docker compose run --rm terraform` to clean up containers after execution.
- Profiles: Ensure the `tooling` profile is active or specified if needed.

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
cd infra/09-tooling/terraform
docker compose run --rm terraform init
```

#### Resource Provisioning (Plan & Apply)

Always generate a plan file before applying to prevent accidental changes.

```bash
## 1. Generate plan
docker compose run --rm terraform plan -out=tfplan

## 2. Review the plan
## 3. Apply the plan
docker compose run --rm terraform apply tfplan
```

#### Formating and Validation

Maintain code quality by using built-in tools.

```bash
docker compose run --rm terraform fmt
docker compose run --rm terraform validate
```

### Troubleshooting

#### Lock File Issues

If Terraform fails with "Error acquiring the state lock", ensure no other group members are applying changes. If a process crashed, refer to the [force unlock procedure](../../runbooks/09-tooling/terraform.md#1-force-unlocking-state).

#### Network Connectivity

The container uses `infra_net`. If you cannot reach local services (like MinIO), verify the network labels in `docker-compose.yml`.

### Overview (KR)

이 문서는 `docs/05.operations/guides/09-tooling/terraform.md` 주제의 사용 가이드다. 기존 본문을 기준으로 작업자가 필요한 배경, 절차, 주의사항을 빠르게 찾도록 보강한다.

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- AI Agent

### Purpose

관련 인프라 서비스나 문서 영역을 이해하고 안전하게 변경 또는 운영할 수 있도록 돕는다.

### Prerequisites

- Repository root README 확인
- 관련 `infra/` 서비스 README 확인
- 필요한 경우 대응 operation/runbook 문서 확인

### Step-by-step Instructions

1. 관련 README와 기존 본문을 먼저 읽는다.
2. 실제 compose/config 경로와 문서 설명이 일치하는지 확인한다.
3. 변경이 필요하면 대응 템플릿과 상위 README 링크를 함께 갱신한다.
4. 관련 검증 스크립트 또는 문서 audit를 실행한다.

### Common Pitfalls

- guide 문서에 운영 정책이나 incident timeline을 섞지 않는다.
- secret 값, token, 인증서 원문을 열람하거나 문서화하지 않는다.
- runtime 변경이 필요한 경우 문서 보강과 별도 작업으로 분리한다.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/09-tooling/terraform.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/09-tooling/terraform.md)
- [Recovery runbook](../../runbooks/09-tooling/terraform.md)
- [Operations template](../../../99.templates/operation.template.md)
