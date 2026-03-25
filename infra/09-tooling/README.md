# Tooling Infrastructure Tier (09-tooling)

> Developer tools, code quality analyzers, IaC automation, and load testing.

## Overview

The `09-tooling` tier provides the auxiliary services that support the development lifecycle and infrastructure automation in the `hy-home.docker` ecosystem. It consolidates management tools for infrastructure as code (Terrakube), code quality (SonarQube), and performance benchmarking (Locust).

## Audience

이 README의 주요 독자:

- DevOps Engineers (IaC & CI/CD automation)
- Developers (Code quality & Sync)
- QA/Performance Engineers (Load testing)

## Scope

### In Scope

- Terrakube (Terraform automation)
- SonarQube (Static Analysis)
- Locust (Distributed Load Testing)
- Syncthing (P2P File Sync)
- Private OCI Registry

### Out of Scope

- Core CI/CD runners (external to this tier)
- Production monitoring (managed in `06-observability`)
- Business application code

## Structure

```text
09-tooling/
├── sonarqube/        # Code quality inspection
├── terrakube/        # Terraform automation
├── locust/           # Load testing
├── syncthing/        # File synchronization
├── registry/Internal # Private image registry
└── README.md         # This file
```

## How to Work in This Area

1. Read the [IaC Automation Guide](../../docs/07.guides/09-tooling/01.iac-automation.md).
2. Follow the [Performance Testing Guide](../../docs/07.guides/09-tooling/02.performance-testing.md).
3. Check the [Operations Policy](../../docs/08.operations/09-tooling/README.md) for maintenance.
4. Consult the [Tooling Runbook](../../docs/09.runbooks/09-tooling/README.md) for failure recovery.

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| IaC | Terrakube / Terraform | v2.29 / v1.14 |
| Quality | SonarQube | v10.7 Community |
| Testing | Locust | Python-based distributed |
| Storage | MinIO | Remote state backend |

## Service Matrix

| Service | Protocol | Profile | Port |
| :--- | :--- | :--- | :--- |
| `sonarqube` | HTTP | `tooling` | 9000 |
| `terrakube-ui` | HTTP | `tooling` | 3000 |
| `terrakube-api` | HTTP | `tooling` | 8080 |
| `locust-master` | HTTP | `tooling` | 8089 |
| `registry` | HTTP | `tooling` | 5000 |

## Configuration

- **Database**: Tools depend on the `mng-db` instance in `04-data`.
- **SSO**: UI services are integrated with Keycloak/DEX for centralized authentication.
- **Persistence**: Data is stored in `${DEFAULT_TOOLING_DIR}`.

## Testing

```bash
# Verify SonarQube Health
curl -f http://sonarqube:9000/api/system/health

# Check Terrakube API
curl -f http://terrakube-api:8080/actuator/health
```

## AI Agent Guidance

1. Terrakube executors use the host's `/var/run/docker.sock` for Terraform runners. Use with caution.
2. Large SonarQube scans should be scheduled during low-traffic periods to avoid DB contention.
3. Access the private registry via `registry.${DEFAULT_URL}` using established credentials.
