---
status: active
---
<!-- Target: docs/05.operations/guides/09-tooling/terrakube.md -->

# Operations: Terrakube Policy Usage Guide

## Usage

### Overview

이 가이드는 Operations: Terrakube Policy Usage Guide의 사용 맥락, 전제 조건, 일반 점검, runbook handoff 기준을 설명한다.

<!-- [ID:09-tooling:terrakube] -->

### Usage Type

`system-guide | how-to`

### Target Audience

- Operators
- Developers
- Contributors
- AI Agents

### Purpose

- Operations: Terrakube Policy Usage Guide의 운영 사용 맥락을 빠르게 파악한다.
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

이 문서는 `docs/05.operations/guides/09-tooling/terrakube.md` 주제의 사용 가이드다. 기존 본문을 기준으로 작업자가 필요한 배경, 절차, 주의사항을 빠르게 찾도록 보강한다.

### Terrakube Platform Usage

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

## Common Checks

- Step-by-step Instructions 의 검증 단계를 따른다.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/09-tooling/terrakube.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/09-tooling/terrakube.md)
- [Recovery runbook](../../runbooks/09-tooling/terrakube.md)
