# DevOps Tooling & Static Analysis Guide

> **Components**: `sonarqube`, `terraform`, `terrakube`

## 1. Static Analysis (SonarQube)

Provides real-time code quality and security feedback.

- **Portal**: `https://sonarqube.${DEFAULT_URL}`
- **Scanner Integration**: Use the standard `sonar-scanner` image in CI pipelines.

## 2. Infrastructure as Code (Terraform)

We utilize Terraform for managing production-equivalent resources on cloud providers.

- **Execution Mode**: Local-within-Docker or distributed via Terrakube.
- **State Integrity**: Managed via a remote backend (typically S3/MinIO) to prevent localized state conflicts.

## 3. Automation Layer (Terrakube)

Terrakube acts as the private automation engine for Terraform runs.

- **UI Interface**: `https://terrakube-ui.${DEFAULT_URL}`
- **Security**: Authentication is delegatd to the centralized Keycloak provider.

## 4. Maintenance Notes

Always audit the `SONAR_TOKEN` and `TERRAFORM_SECRET` stored in Docker Secrets before initiating large-scale infra changes.
