# Infrastructure Services

This directory contains the Docker Compose configurations for the project's infrastructure services. Each service is isolated in its own subdirectory.

## Service Directory

| Service | Description | Status |
| :--- | :--- | :--- |
| **Airflow** | Workflow orchestration for data engineering pipelines. | [View Details](./airflow) |
| **CouchDB** | NoSQL database cluster. | [View Details](./couchdb) |
| **Harbor** | Private container registry. | [View Details](./harbor) |
| **InfluxDB** | Time-series database. | [View Details](./influxdb) |
| **Kafka** | Event streaming platform (KRaft mode). | [View Details](./kafka) |
| **Keycloak** | Identity and Access Management (IAM). | [View Details](./keycloak) |
| **ksqlDB** | Database purpose-built for stream processing applications. | [View Details](./ksql) |
| **MailHog** | Email testing tool (`infra/mail`). | [View Details](./mail) |
| **MinIO** | High-performance, S3 compatible object storage. | [View Details](./minio) |
| **Management DB** | Shared Valkey and PostgreSQL for management tools. | [View Details](./mng-db) |
| **n8n** | Workflow automation tool. | [View Details](./n8n) |
| **Nginx** | Web server and reverse proxy. | [View Details](./nginx) |
| **OAuth2 Proxy** | Authentication proxy for services. | [View Details](./oauth2-proxy) |
| **Observability** | LGTM stack (Loki, Grafana, Tempo, Mimir/Prometheus) + Alloy. | [View Details](./observability) |
| **Ollama** | Local LLM inference engine. | [View Details](./ollama) |
| **OpenSearch** | Search and analytics engine. | [View Details](./opensearch) |
| **PostgreSQL HA** | High Availability PostgreSQL cluster (Patroni). | [View Details](./postgresql-cluster) |
| **Qdrant** | Vector database for AI applications. | [View Details](./qdrant) |
| **Redis Cluster** | Distributed Redis cache/store. | [View Details](./redis-cluster) |
| **SonarQube** | Code quality and security scanning. | [View Details](./sonarqube) |
| **Storybook** | UI component documentation and testing. | [View Details](./storybook) |
| **Terrakube** | Infrastructure as Code (IaC) platform (Terraform alternative). | [View Details](./Terrakube) |
| **Traefik** | Cloud-native application proxy and edge router. | [View Details](./traefik) |
| **Valkey Cluster** | Distributed Valkey (Redis fork) cluster. | [View Details](./valkey-cluster) |

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
