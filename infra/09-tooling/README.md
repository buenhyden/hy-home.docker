<!-- [ID:09-tooling:root] -->
# Tooling Tier (09-tooling)

> Central repository for developer tools, code quality analyzers, load testing, and IaC automation.

## 1. Context (SSoT)

This tier manages the auxiliary services that support the development lifecycle, infrastructure automation, and peer-to-peer synchronization in the `hy-home.docker` ecosystem.

- **SSoT Documentation**: [docs/07.guides/09-tooling/README.md](../../docs/07.guides/09-tooling/README.md)
- **Governance**: [docs/08.operations/09-tooling/README.md](../../docs/08.operations/09-tooling/README.md)
- **Status**: Operational

## 2. Structure

```text
09-tooling/
├── sonarqube/        # Continuous code quality inspection
├── terrakube/        # Self-hosted Terraform automation (API/UI/Executor)
├── terraform/        # Containerized Terraform CLI runner
├── locust/           # Distributed load testing (Master + Workers)
├── syncthing/        # Peer-to-peer file synchronization
├── registry/         # Private Docker container image registry
└── k6/               # (Planned) Scriptable load testing
```

## 3. Service Matrix

| Service | Category | Profile | Role |
| :--- | :--- | :--- | :--- |
| **sonarqube** | Code Quality | `tooling` | Static analysis and security scanning |
| **terrakube** | IaC Automation | `tooling` | Terraform orchestration and management |
| **terraform** | IaC CLI | `tooling` | Local-compatible IaC execution environment |
| **locust** | Load Testing | `tooling` | User-simulation and performance benchmarking |
| **syncthing** | File Sync | `tooling` | Distributed, encrypted file synchronization |
| **registry** | Image Repo | `tooling` | Private OCI-compliant image registry |

## 4. Tech Stack

- **CI/CD/IaC**: Terrakube 2.29, Terraform 1.14
- **Testing**: Locust (Python-based)
- **Quality**: SonarQube 10.7
- **Sync**: Syncthing 2.0
- **Registry**: Docker Distribution v2

## 5. Governance & Persistence

- **Data Path**: All services MUST store data in `${DEFAULT_TOOLING_DIR}`.
- **Secrets**: Credentials (DB passwords, PATs) MUST be managed via Docker secrets.
- **Dependencies**: Terrakube and SonarQube depend on the `mng-db` (04-data) PostgreSQL instance.

---

Copyright (c) 2026. Licensed under the MIT License.
