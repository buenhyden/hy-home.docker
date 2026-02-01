# Tooling (09-tooling)

## Overview

DevOps and tooling services for infrastructure management and code quality. Terrakube and SonarQube are optional profiles. A standalone Terraform CLI container is provided for local runs.

## Services

| Service       | Profile      | Path          | Notes                             |
| ------------- | ------------ | ------------- | --------------------------------- |
| Terraform CLI | (standalone) | `./terraform` | Local Terraform runner container  |
| Terrakube     | `terrakube`  | `./terrakube` | Terraform orchestration platform  |
| SonarQube     | `sonarqube`  | `./sonarqube` | Code quality and security scanner |

## Run

```bash
# Terrakube / SonarQube (optional)
docker compose --profile terrakube up -d
docker compose --profile sonarqube up -d

# Standalone Terraform (not included at root)
cd infra/09-tooling/terraform
docker compose run --rm terraform version
```

## File Map

| Path         | Description              |
| ------------ | ------------------------ |
| `terraform/` | Terraform CLI container. |
| `terrakube/` | Terrakube stack.         |
| `sonarqube/` | SonarQube service.       |
| `README.md`  | Category overview.       |
