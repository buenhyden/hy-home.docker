# Tooling (09-tooling)

This category manages developer tools, code quality analyzers, load testing, file synchronization, and infrastructure automation.

## Services

| Service   | Profile   | Path          | Purpose                                      |
| --------- | --------- | ------------- | -------------------------------------------- |
| SonarQube | `tooling` | `./sonarqube` | Continuous code quality inspection           |
| Terrakube | `tooling` | `./terrakube` | Self-hosted Terraform automation (3 nodes)   |
| Terraform | `tooling` | `./terraform` | Containerized Terraform CLI runner           |
| Locust    | `tooling` | `./locust`    | Distributed load testing (master + workers)  |
| Syncthing | `tooling` | `./syncthing` | Peer-to-peer file synchronization            |
| Registry  | `tooling` | `./registry`  | Private Docker container image registry      |

## File Map

| Path           | Description                                                        |
| -------------- | ------------------------------------------------------------------ |
| `sonarqube/`   | SonarQube server connected to management PostgreSQL.               |
| `terrakube/`   | Terrakube API, UI, and Executor nodes (Keycloak + MinIO + Valkey). |
| `terraform/`   | Containerized Terraform CLI with workspace and credential mounts.  |
| `locust/`      | Locust master-worker load tester with InfluxDB metrics output.     |
| `syncthing/`   | Syncthing continuous sync server with resource directory mount.    |
| `registry/`    | Docker Distribution v2 private container image registry.          |
| `README.md`    | Category overview (this file).                                     |

## Guides

| Guide | Purpose |
| ----- | ------- |
| [DevOps Tooling Guide](../../docs/guides/09-tooling/devops-tooling-guide.md) | Service overview and access details |
| [Tooling Operations](../../docs/guides/09-tooling/tooling-operations.md) | Operations and troubleshooting |
| [Tooling Context](../../docs/guides/09-tooling/tooling-context.md) | Service inventory, dependencies, secrets |
| [Tooling Lifecycle](../../docs/guides/09-tooling/tooling-lifecycle.md) | Startup procedures, initial setup, secret rotation |
