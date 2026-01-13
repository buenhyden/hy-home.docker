# hy-home.docker

[![Infrastructure](https://img.shields.io/badge/Infrastructure-Docker%20Compose-blue)](./infra)
[![License](https://img.shields.io/badge/License-MIT-green)](./LICENSE)

**Home Lab Infrastructure & Enterprise Playground**

This repository is a comprehensive monorepo for hosting a local Home Lab environment using Docker Compose. It features a modern tech stack centered around **High Availability**, **Observability**, and **Developer Experience**.

## 🌟 Key Features

- **Layered Infrastructure**: Organized into Edge, Identity, Data, AI, and Observability layers.
- **Enterprise-Grade**: Includes Patroni for PostgreSQL HA, Kafka for streaming, and Keycloak for IAM.
- **AI-Ready**: Integrated Ollama and Qdrant for local LLM and RAG experiments.
- **Full Observability**: Pre-configured **LGTM Stack** (Loki, Grafana, Tempo, Mimir/Prometheus) with Alloy.
- **Agent-Augmented**: Structured specifically for collaboration with AI Agents (Cursor, Windsurf) using the Context-First approach.

## 📂 Repository Structure

| Path | Description |
| :--- | :--- |
| **[.agent/](./.agent)** | **AI Brain**: Agent Rules, Workflows, and Memory. |
| **[.github/](./.github)** | **CI/CD**: Workflows, Issue Templates, and Policy. |
| **[docs/](./docs)** | **Knowledge Base**: Architecture diagrams, detailed guides, and API specs. |
| **[examples/](./examples)** | **Samples**: Grafana dashboards, `.env` examples, and host configurations. |
| **[infra/](./infra)** | **Core Infrastructure**: 26+ Docker Compose services (The heart of the repo). |
| **[projects/](./projects)** | **Sub-Projects**: Independent modules (e.g., Terraform labs, specialized apps). |
| **[scripts/](./scripts)** | **Automation**: PowerShell/Bash scripts for management and validation. |
| **[secrets/](./secrets)** | **Security**: Local secrets storage (Git Ignored). |

## 🚀 Quick Start

### Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Git
- 16GB+ RAM recommended (32GB for full stack)

### Setup

1. **Clone & Prepare**

   ```bash
   git clone https://github.com/buenhyden/hy-home.docker.git
   cd hy-home.docker
   ```

2. **Secrets Initialization**
   Create the necessary secret files (avoiding hardcoded credentials).

   ```bash
   mkdir -p secrets
   echo "my-secure-password" > secrets/postgres_password.txt
   echo "my-secure-password" > secrets/valkey_password.txt
   # See infra/README.md for full list
   ```

3. **Launch Infrastructure**

   ```bash
   cd infra
   docker compose up -d
   ```

## 🛠️ Utilities & Scripts

Automate common tasks using the provided scripts in `scripts/`.

| Script | description | Usage |
| :--- | :--- | :--- |
| `new_infra_service` | Scaffolds a new Docker Compose service folder. | `./scripts/new_infra_service.sh <service_name>` |
| `validate_compose_change` | Validates `docker-compose.yml` syntax. | `./scripts/validate_compose_change.sh` |
| `fix_grafana_dashboards` | Normalizes Grafana dashboard JSONs. | `python scripts/fix_grafana_dashboards.py` |

## 🤖 AI Agent Collaboration

This project allows you to pair program with AI Agents effectively.

- **Rules**: See [.agent/rules](./.agent/rules) for coding standards.
- **Workflows**: See [.agent/workflows](./.agent/workflows) for standard operating procedures.

## 📚 Documentation Index

- **Architecture**: [System Architecture](./docs/architecture/system-architecture.md)
- **Networking**: [Network Topology](./docs/architecture/network-topology.md)
- **Operations**: [Maintenance Guide](./docs/guides/maintenance.md)
- **Services**: [Service Catalog](./docs/reference/service-catalog.md)

## 📄 License

This project is licensed under the [MIT License](./LICENSE).
