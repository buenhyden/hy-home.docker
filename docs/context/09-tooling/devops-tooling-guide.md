# DevOps Tooling & Static Analysis Guide

> **Components**: `sonarqube`, `terraform`, `terrakube`

## 1. Static Analysis (SonarQube)

SonarQube provides continuous inspection of code quality.

### Technical Specifications

| Attribute | Internal DNS | Port | External Proxy |
| --- | --- | --- | --- |
| **Web UI** | `sonarqube` | `9000` | `sonarqube.${DEFAULT_URL}` |
| **Static IP** | `172.19.0.41` | - | - |

- **Setup Node**: Upon initial boot, SonarQube initializes its PostgreSQL schema. Use `admin / admin` for initial login and change the password immediately.

## 2. Infrastructure as Code (Terraform)

We utilize Terraform for managing production-equivalent resources.

- **Execution Mode**: Local-within-Docker or distributed via Terrakube.
- **State Integrity**: Managed via a remote backend (S3/MinIO). Maintain your local state files or rely on the Terrakube API.

## 3. Automation Layer (Terrakube)

Terrakube acts as the private automation engine for Terraform runs.

- **UI Interface**: `https://terrakube-ui.${DEFAULT_URL}`
- **Security**: Redirects to the centralized Keycloak provider for authentication.

## 4. Maintenance & Integration

| Action | Reference | Link |
| --- | --- | --- |
| **Manual** | Tooling Ops | [Operations Guide](tooling-operations.md) |
| **Troubleshoot**| Infra Recovery | [Runbooks](../../../runbooks/README.md) |

Always audit the `SONAR_TOKEN` and `TERRAFORM_SECRET` stored in Docker Secrets before initiating large-scale infra changes.
