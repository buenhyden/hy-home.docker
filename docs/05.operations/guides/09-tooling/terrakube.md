---
status: active
---
<!-- Target: docs/05.operations/guides/09-tooling/terrakube.md -->

# Operations: Terrakube Policy Usage Guide

<!-- [ID:09-tooling:terrakube] -->
## Usage: Terrakube Platform

> User guide for managing infrastructure automation workflows via the Terrakube platform.

### Overview

Terrakube is an open-source alternative to Terraform Cloud, providing a centralized control plane for Infrastructure as Code (IaC). It manages workspaces, variables, team access, and private modules.

### Getting Started

#### 1. Initial Login

Access the UI at `https://terrakube-ui.${DEFAULT_URL}`. Authentication is integrated with Keycloak; use your engineering credentials.

#### 2. Organizations and Workspaces

- **Organizations**: High-level groups (e.g., `prod`, `dev`, `shared`).
- **Workspaces**: Individual projects mapped to a specific Git repository and set of variables.

### Feature Breakdown

#### Private Module Registry

Terrakube allows you to host internal Terraform modules.

- To publish: Tag your module repository (e.g., `terraform-aws-s3-v1.0.0`).
- To consume: Reference the module using the Terrakube API URL in your `.tf` code.

#### Variable Management

- **Environment Variables**: For provider credentials (AWS_ACCESS_KEY, etc.).
- **Terraform Variables**: For specific infrastructure parameters.
- **Sensitive Variables**: Marked as "Sensitive" are stored encrypted and never displayed in logs.

#### UI-Driven Workflows

- **Plan**: Trigger a `terraform plan` to view proposed changes in the UI logs.
- **Apply**: Manual or automatic approval of plans to execute changes.

### Integration Details

#### Remote State (MinIO)

Terrakube automatically manages its own internal state storage in the `tfstate` bucket of MinIO. Manual configuration of the `s3` backend in your `.tf` files is not required when running through the platform.

#### Executor Model

The `terrakube-executor` spins up ephemeral Docker containers for every job. It requires access to `/var/run/docker.sock` on the host to manage these child containers.

### Troubleshooting

#### Executor Timeout

If a job is stuck in "Pending" status, verify that the `terrakube-executor` container is healthy:

```bash
docker compose logs -f terrakube-executor
```

#### SSO Failures

If OIDC logout occurs frequently, check the token expiration settings in the `hy-home.realm` of Keycloak.

### Overview (KR)

이 문서는 `docs/05.operations/guides/09-tooling/terrakube.md` 주제의 사용 가이드다. 기존 본문을 기준으로 작업자가 필요한 배경, 절차, 주의사항을 빠르게 찾도록 보강한다.

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

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/09-tooling/terrakube.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/09-tooling/terrakube.md)
- [Recovery runbook](../../runbooks/09-tooling/terrakube.md)
- [Operations template](../../../99.templates/operation.template.md)
