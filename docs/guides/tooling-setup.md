# Tooling Initial Setup Guide

> Configuration and setup steps for generalized infrastructure tooling including SonarQube, Terraform runners, and Terrakube.

## 1. Description

The `infra/09-tooling` cluster contains peripheral CI/CD tooling. These tools typically sit outside the critical application path but are required for quality-assurance and secure infrastructure-as-code deployments.

## 2. SonarQube Initialization

SonarQube analyzes code quality utilizing an underlying PostgreSQL database.

1. Start the stack: `docker compose -f infra/09-tooling/sonarqube/docker-compose.yml up -d`.
2. Wait for SonarQube to become healthy (the initialization of the database schema takes significant time on first boot).
3. Access the UI via `https://sonarqube.${DEFAULT_URL}`.
4. Login using default credentials `admin / admin`. You will be immediately prompted to change this password.

## 3. Terrakube / Terraform Setup

Terrakube provides a local open-source alternative to Terraform Cloud.

1. Ensure the Terrakube identity dependencies (often connected back to Keycloak) are properly configured if SSO is enabled.
2. The UI is accessible at `https://terrakube-ui.${DEFAULT_URL}`.
3. Access the API for workspace configuration at `https://terrakube-api.${DEFAULT_URL}`.

### Executing Local Terraform

If you are running the `terraform` container directly to apply IaC to the local AWS mock or specific platforms:

- Ensure volume mounts accurately reflect the local `./terraform` configs on your host.
- Always execute `fmt` and `validate` before attempting `apply`.
- Maintain State: Rely on Terrakube or local mounted `tfstate` files. Losing state files will cause Terraform to recreate all bound infrastructure.
