# IaC Deployment Policy

Infrastructure as Code (IaC) standards for the `hy-home.docker` ecosystem.

## 1. Tool Selection

- **Local Execution**: Use `terraform` (infra/09-tooling/terraform) for ad-hoc or development-stage changes.
- **Automation**: Use `terrakube` (infra/09-tooling/terrakube) for production state management and team collaboration.

## 2. State Management

- **SSoT**: All production state MUST be stored in the internal MinIO `tfstate` bucket via Terrakube.
- **Encryption**: Secrets must never be stored in plaintext variables. Use specialized secret providers (Vault, etc.) or environment variables.

## 3. Code Review Requirements

- All `.tf` changes must be reviewed and passed through SonarQube quality gates (where applicable).
