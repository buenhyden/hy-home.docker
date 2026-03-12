# Hy-Home Docker Infrastructure

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

> A modular, production-ready Docker Compose infrastructure for professional-grade home labs.

`hy-home.docker` is a comprehensive infrastructure-as-code repository designed to deploy and manage a multi-tier service ecosystem consistently. It leverages Docker Compose's `include` feature and profiles to assemble a tailored stack—ranging from core identity management and security to advanced AI inference and observability.

## Overview

This project solves the complexity of maintaining a consistent, secure, and observable infrastructure in local or home-lab environments.

- **Modular Orchestration:** Services are grouped by tiers (Gateway, Auth, Data, etc.) and can be selectively enabled via profiles.
- **Production Alignment:** Implements production-grade patterns like Docker Secrets, non-root users, and centralized observability (LGTM stack).
- **Extensible Architecture:** Designed as a foundational blueprint for developers, data engineers, and AI researchers to build upon.

## Tech Stack

| Category | Technology |
| :--- | :--- |
| **Orchestration** | Docker Engine 24+, Docker Compose v2 |
| **Ingress/Edge** | Traefik, OAuth2-Proxy |
| **Identity/Auth** | Keycloak |
| **Storage/DB** | PostgreSQL (HA), Valkey (Cluster), MinIO, Neo4j, CouchDB |
| **Observability** | LGTM Stack (Grafana, Loki, Tempo, Prometheus), Alloy, Pyroscope |
| **Messaging** | Kafka (KRaft mode), ksqlDB, Schema Registry |
| **AI/ML** | Ollama, Open-WebUI, Qdrant |
| **Workflow/CI** | Airflow, n8n, SonarQube |

## Prerequisites

Ensure your host environment meets these requirements before starting:

- **Docker Engine:** v24.0.0 or higher
- **Docker Compose:** v2.20.0 or higher
- **System Utilities:** `bash`, `rg` (ripgrep)
- **Memory:** Minimum 16GB RAM recommended for the "Core + Data + Obs" stack.
- **Platform Notes:**
  - **Linux:** Native Docker is recommended.
  - **WSL2 (Windows):** Highly recommended to keep the repository within the WSL filesystem (e.g., `/home/<user>/`) rather than `/mnt/c/` for performance and file permission consistency.

## Quick Start

Follow these steps to initialize your local environment and spin up the core infrastructure.

### 1. Repository Setup

Clone the repository and enter the directory:

```bash
git clone https://github.com/organization/hy-home.docker.git
cd hy-home.docker
```

### 2. Environment Configuration

Create your local environment file from the template:

```bash
cp .env.example .env
```

Open `.env` and adjust variables like `DEFAULT_URL` (e.g., `127.0.0.1.nip.io`) and `DEFAULT_MOUNT_VOLUME_PATH` to suit your system.

### 3. Initialize Security Assets

Generate local TLS certificates and bootstrap the mandatory secrets store:

```bash
# Generate mkcert-based local TLS certificates
bash scripts/generate-local-certs.sh

# Bootstrap file-based secrets (referenced by Docker Compose)
bash scripts/bootstrap-secrets.sh --env-file .env.example
```

> [!NOTE]
> `bootstrap-secrets.sh` creates placeholders (`CHANGE_ME_*`) for external integrations like Slack Webhooks and SMTP. You must fill these in `secrets/` before those services will function correctly.

### 4. Validation & Pre-flight

Validate that your Compose configuration is syntactically correct and all prerequisites are met:

```bash
# Static validation of the composed stack
bash scripts/validate-docker-compose.sh

# Runtime pre-flight check (requires Docker daemon)
bash scripts/preflight-compose.sh
```

### 5. Launch the Stack

You can start the default stack (Core + Data + Obs) or use specific profiles:

**Default Stack:**

```bash
docker compose up -d
```

**Profile-based Launch:**

```bash
# Only start core gateway and observability tools
docker compose --profile core --profile obs up -d
```

### Accessing Services

Once the containers are running, you can access the primary dashboards through your configured `DEFAULT_URL`:

- **Traefik Dashboard:** `https://dashboard.127.0.0.1.nip.io`
- **Grafana:** `https://grafana.127.0.0.1.nip.io`
- **Keycloak:** `https://keycloak.127.0.0.1.nip.io`

## System Architecture

This project follows a modular, profile-driven infrastructure pattern. The goal is to provide a single entry point for a complex, multi-tier ecosystem.

### Project Structure

```text
hy-home.docker/
├── .agent/             # AI Agent rules, workflows, and prompts
├── .github/            # CI/CD workflows and repository templates
├── infra/              # Service-specific Compose definitions (Tier 01-10)
│   ├── 01-gateway/      # Ingress (Traefik, OAuth2-Proxy)
│   ├── 02-auth/         # Identity (Keycloak)
│   ├── 04-data/         # Databases (Postgres, Valkey, MinIO)
│   └── ...              # Other tiers (Obs, Messaging, AI)
├── docs/               # Architecture, PRDs, and technical blueprints
├── operations/         # Incident history and postmortems
├── runbooks/           # Executable manual procedures
├── scripts/            # Environment validation and bootstrap tools
├── secrets/            # Local secret store (Docker secrets compatible)
├── specs/              # Implementation plans and feature specs
├── ARCHITECTURE.md     # Global architectural invariants
├── OPERATIONS.md       # Operational index and lifecycle
└── docker-compose.yml  # Main entry point (includes and orchestrates)
```

### Infrastructure Profiles

Services are grouped into logical stacks. You can enable them by setting `COMPOSE_PROFILES` in your `.env` or using the `--profile` flag.

| Profile | Description | Primary Services |
| :--- | :--- | :--- |
| `core` | **Edge & Identity:** Mandatory gateway and auth services. | Traefik, Keycloak, OAuth2-Proxy |
| `data` | **Persistence Layer:** Shared databases and object storage. | Postgres, Valkey, MinIO |
| `obs` | **Observability:** Centralized logging, metrics, and tracing. | Grafana, Prometheus, Loki, Tempo |
| `messaging`| **Event Streaming:** Kafka-based messaging infrastructure. | Kafka, Schema Registry, ksqlDB |
| `workflow` | **Orchestration:** ETL and automation engines. | Airflow, n8n |
| `ai` | **Inference:** Local LLM and Vector search environment. | Ollama, Open-WebUI, Qdrant |
| `tooling` | **Engineering Tools:** Quality and DevOps utilities. | SonarQube, Locust |

### Core Principles

- **Include-based Assembly:** The root `docker-compose.yml` does not define services directly; it `include`s definitions from the `infra/` directory to maintain modularity.
- **Secrets First:** Never pass passwords in `.env`. All sensitive data is injected via Docker Secrets from `secrets/**/*.txt`.
- **Security Baseline:** Services run with `no-new-privileges:true` and dropped capabilities (`cap_drop: [ALL]`) by default.
- **Network Isolation:** All internal traffic flows through `infra_net`. Boundary traffic is handled exclusively by Tier 01 Gateway.

## Configuration & Reference

### Environment Variables

The project uses a comprehensive set of environment variables managed via `.env`. Below are the primary configuration points:

| Variable | Default | Description |
| :--- | :--- | :--- |
| `DEFAULT_URL` | `127.0.0.1.nip.io` | Primary domain for all service ingress. |
| `COMPOSE_PROFILES` | `core,data,obs` | Default profiles to boot on `up`. |
| `HTTP_HOST_PORT` | `80` | Host port for Traefik HTTP entry point. |
| `HTTPS_HOST_PORT` | `443` | Host port for Traefik HTTPS entry point. |
| `DEFAULT_MOUNT_VOLUME_PATH` | `/home/hy/volumes` | Root directory for persistent data mounts. |
| `INFRA_SUBNET` | `172.19.0.0/16` | Subnet range for the internal `infra_net`. |

> [!TIP]
> For a full list of service-specific ports (e.g., `POSTGRES_HOST_PORT`, `KAFKA_UI_HOST_PORT`), refer to the [`.env.example`](.env.example) file.

### Available Scripts (`scripts/`)

Maintenance and bootstrap tasks should be executed through the following scripts:

| Script | Purpose |
| :--- | :--- |
| `bootstrap-secrets.sh` | Generates initial `secrets/**/*.txt` files from placeholders. |
| `generate-local-certs.sh`| Creates mkcert-based TLS certificates for local HTTPS. |
| `validate-docker-compose.sh`| Performs static analysis on the Compose stack. |
| `preflight-compose.sh` | Checks runtime prerequisites (mounts, networks, env). |

### Operational Tiers

This infrastructure is designed to scale across different environments (defined in `OPERATIONS.md`):

- **L1 (Local Dev):** Fast iterations and unit testing on a local machine.
- **L2 (Home-Lab):** 24/7 internal services running on dedicated hardware (e.g., NUC, Server).
- **L3 (Pro-Lab):** High-availability clusters for benchmarking and recovery drills.

### Observability & Backup

- **Centralized Logs:** All logs are routed via the `loki` driver and viewable in Grafana.
- **Backups:** Nightly DB snapshots are stored at `/mnt/backup/db/` (for PostgreSQL and OpenSearch).
- **Secrets Management:** 100% of sensitive data is handled via Docker Secrets at `/run/secrets/`.

## Troubleshooting

### Secret Bootstrapping Issues

- **Error:** `CHANGE_ME_*` placeholders remain in `secrets/*.txt`.
- **Solution:** You must manually edit the files in the `secrets/` directory to replace placeholders with your actual credentials (e.g., SMTP passwords, Slack Webhooks). Use `bash scripts/bootstrap-secrets.sh --strict` to verify.

### Port Conflicts

- **Error:** `Bind for 0.0.0.0:80 failed: port is already allocated`.
- **Solution:** Change `HTTP_HOST_PORT` or `HTTPS_HOST_PORT` in your `.env` file to an available port.

### Directory Permissions

- **Error:** Permission denied when mounting volumes.
- **Solution:** Ensure your `DEFAULT_MOUNT_VOLUME_PATH` exists and is writable by the user running Docker. On WSL2, avoid mounting from `/mnt/c/`.

## Governance & Contributing

This project implements **Spec-Driven Development** managed by AI Agents.

- **Spec Requirement:** All new features must start with a specification in the `specs/` directory.
- **Rule Compliance:** Code and documentation must adhere to the standards defined in `.agent/rules/`.
- **Merge Policy:** Pull Requests require passing all local QA gates (Coverage > 80%, Linting).

For detailed instructions, refer to:

- [🤝 Contributing Guidelines](./CONTRIBUTING.md)
- [🤖 Multi-Agent Governance](./AGENTS.md)
- [🏛️ System Architecture](./ARCHITECTURE.md)
- [⚙️ Operations Baseline](./OPERATIONS.md)

## License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for details.
