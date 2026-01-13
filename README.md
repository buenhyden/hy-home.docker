# hy-home.docker

[![Infrastructure](https://img.shields.io/badge/Infrastructure-Docker%20Compose-blue)](./infra)
[![License](https://img.shields.io/badge/License-MIT-green)](./LICENSE)

**Home Lab Infrastructure & Enterprise Playground**

This repository is a comprehensive monorepo for hosting a local Home Lab environment using Docker Compose. It features a modern tech stack centered around High Availability, Observability, and Developer Experience.

## 🌟 Key Features

- **Layered Infrastructure**: organized into Edge, Identity, Data, AI, and Observability layers.
- **Enterprise-Grade**: Includes Patroni for PostgreSQL HA, Kafka for streaming, and Keycloak for IAM.
- **AI-Ready**: Integrated Ollama and Qdrant for local LLM and RAG experiments.
- **Full Observability**: Pre-configured LGTM stack (Loki, Grafana, Tempo, Mimir/Prometheus).
- **Agent-Augmented**: Structured specifically for collaboration with AI Agents (Cursor, Windsurf).

## 📂 Repository Structure

```text
hy-home.docker/
├── .agent/             # AI Agent Rules & Workflows (Brain)
├── .github/            # GitHub Templates & CI/CD Config
├── docs/               # Architecture & Operational Documentation
├── infra/              # Core Infrastructure Services (Docker Compose)
│   ├── observability/  # LGTM Stack
│   ├── postgresql/     # DB Clusters
│   └── ...             # 20+ other services
├── scripts/            # Automation & Maintenance Scripts
└── secrets/            # Docker Secrets (Git Ignored)
```

## 🚀 Quick Start

### Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Git
- 16GB+ RAM recommended

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

3. **Launch**

   ```bash
   cd infra
   docker compose up -d
   ```

## 🤖 AI Agent Collaboration

This project follows the **Context-First** approach for AI Agents.

- **Rules**: See [.agent/rules](./.agent/rules) for coding standards.
- **Workflows**: See [.agent/workflows](./.agent/workflows) for standard operating procedures.

## 📚 Documentation

- [Infrastructure Details](./infra/README.md)
- [System Architecture](./docs/architecture/system-architecture.md)
- [Network Topology](./docs/architecture/network-topology.md)
- [Service Catalog](./docs/reference/service-catalog.md)

## 📄 License

This project is licensed under the [MIT License](./LICENSE).
