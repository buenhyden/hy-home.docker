# DevOps Tooling & Static Analysis Guide

> **Components**: `sonarqube`, `terraform`, `terrakube`

## 1. Static Analysis (SonarQube)

Provides real-time code quality and security feedback.

- **Default Path**: `https://sonarqube.${DEFAULT_URL}`
- **Setup Node**: Upon initial boot, SonarQube initializes its PostgreSQL schema. Use `admin / admin` for initial login and change the password immediately.

## 2. Infrastructure as Code (Terraform)

We utilize Terraform for managing production-equivalent resources.

- **Execution Mode**: Local-within-Docker or distributed via Terrakube.
- **State Integrity**: Managed via a remote backend (S3/MinIO). Maintain your local state files or rely on the Terrakube API.

## 3. Automation Layer (Terrakube)

Terrakube acts as the private automation engine for Terraform runs.

- **UI Interface**: `https://terrakube-ui.${DEFAULT_URL}`
- **Security**: Redirects to the centralized Keycloak provider for authentication.

## 4. Maintenance Notes

Always audit the `SONAR_TOKEN` and `TERRAFORM_SECRET` stored in Docker Secrets before initiating large-scale infra changes.
