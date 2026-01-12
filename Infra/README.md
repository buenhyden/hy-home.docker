# Infrastructure Services

This directory contains the Docker Compose configurations for the project's infrastructure services. Each service is isolated in its own subdirectory.

## Service Directory

| Service | Description | Status |
| :--- | :--- | :--- |
| **Airflow** | Workflow orchestration for data engineering pipelines. | [Optional](./airflow) |
| **CouchDB** | NoSQL database cluster. | [Optional](./couchdb) |
| **Harbor** | Private container registry. | [Optional](./harbor) |
| **InfluxDB** | Time-series database. | [Active](./influxdb) |
| **Kafka** | Event streaming platform (KRaft mode). | [Active](./kafka) |
| **Keycloak** | Identity and Access Management (IAM). | [Active](./keycloak) |
| **ksqlDB** | Database purpose-built for stream processing applications. | [Active](./ksql) |
| **MailHog** | Email testing tool (`infra/mail`). | [Optional](./mail) |
| **MinIO** | High-performance, S3 compatible object storage. | [Active](./minio) |
| **Management DB** | Shared Valkey and PostgreSQL for management tools. | [Active](./mng-db) |
| **n8n** | Workflow automation tool. | [Active](./n8n) |
| **Nginx** | Web server and reverse proxy. | [Optional](./nginx) |
| **OAuth2 Proxy** | Authentication proxy for services. | [Active](./oauth2-proxy) |
| **Observability** | LGTM stack (Loki, Grafana, Tempo, Mimir/Prometheus) + Alloy. | [Active](./observability) |
| **Ollama** | Local LLM inference engine. | [Active](./ollama) |
| **OpenSearch** | Search and analytics engine. | [Optional](./opensearch) |
| **PostgreSQL HA** | High Availability PostgreSQL cluster (Patroni). | [Active](./postgresql-cluster) |
| **Qdrant** | Vector database for AI applications. | [Active](./qdrant) |
| **Redis Cluster** | Distributed Redis cache/store (Legacy). | [Optional](./redis-cluster) |
| **SonarQube** | Code quality and security scanning. | [Active](./sonarqube) |
| **Storybook** | UI component documentation and testing. | [Optional](./storybook) |
| **Terrakube** | Infrastructure as Code (IaC) platform (Terraform alternative). | [Optional](./Terrakube) |
| **Traefik** | Cloud-native application proxy and edge router. | [Active](./traefik) |
| **Valkey Cluster** | Distributed Valkey (Redis fork) cluster. | [Active](./valkey-cluster) |

For complete service details including images, versions, and port mappings, see the [Service Catalog](../docs/reference/service-catalog.md).

## Network

All services communicate via the external Docker network `infra_net` (Subnet: `172.19.0.0/16`). Specific services are assigned static IPs to facilitate stable internal communication.

## Environment Variables

A shared `.env` file (located in `infra/.env`) is used to manage configuration across all services, including:

- **Ports**: `${HTTP_PORT}`, `${HTTPS_PORT}`, `${POSTGRES_PORT}`, etc.
- **Domains**: `${DEFAULT_URL}` (Base domain for all services).
- **Credentials**: Database passwords, API keys, etc.

For complete environment variable reference, see [Environment Variables Documentation](../docs/reference/environment-variables.md) (WIP).

## Quick Links

- **[System Architecture](../docs/architecture/system-architecture.md)**: Layered architecture and service dependencies
- **[Network Topology](../docs/architecture/network-topology.md)**: Network configuration and routing
- **[Deployment Guide](../docs/guides/deployment-guide.md)**: Installation and setup instructions
- **[Troubleshooting](../docs/guides/troubleshooting.md)**: Common issues and solutions
