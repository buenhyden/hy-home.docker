# Service Catalog

Complete reference of all infrastructure services with access details.

## Core Infrastructure

| Service | URL | Port | Purpose |
| :--- | :--- | :--- | :--- |
| **Traefik** | <https://dashboard.127.0.0.1.nip.io> | 80/443 | Edge Router & Ingress |
| **Vault** | <https://vault.127.0.0.1.nip.io> | 8200 | Secrets Management |
| **Keycloak** | <https://keycloak.127.0.0.1.nip.io> | - | Identity Provider (IAM) |
| **OAuth2 Proxy** | - | 4180 | Auth Gateway |

## Observability (LGTM Stack)

| Service | URL | Port | Purpose |
| :--- | :--- | :--- | :--- |
| **Grafana** | <https://grafana.127.0.0.1.nip.io> | 3000 | Visualization Dashboard |
| **Prometheus** | <https://prometheus.127.0.0.1.nip.io> | 9090 | Metrics Database |
| **Alertmanager** | <https://alertmanager.127.0.0.1.nip.io> | 9093 | Alerting |
| **Loki** | - | 3100 | Log Aggregation |
| **Tempo** | - | 3200 | Distributed Tracing |
| **Alloy** | <https://alloy.127.0.0.1.nip.io> | 12345 | OTel Collector |

## Data & Persistence

| Service | connection | Port | Purpose |
| :--- | :--- | :--- | :--- |
| **PostgreSQL HA** | `localhost:5000` (Write), `5001` (Read) | 5432 | Relational Database |
| **Valkey Cluster** | `localhost:6379-6384` | 6379+ | Distributed Cache |
| **MinIO** | <https://minio-console.127.0.0.1.nip.io> | 9000/9001 | Object Storage (S3) |
| **InfluxDB** | <https://influxdb.127.0.0.1.nip.io> | 8086 | Time Series Database |
| **MongoDB** | `localhost:27017` | 27017 | NoSQL Database |
| **CouchDB** | `localhost:5984` | 5984 | NoSQL Document Store |
| **Qdrant** | `localhost:6333` | 6333 | Vector Database |
| **OpenSearch** | <https://opensearch.127.0.0.1.nip.io> | 9200 | Search Engine |

## Messaging & Streaming

| Service | Connection | Port | Purpose |
| :--- | :--- | :--- | :--- |
| **Kafka** | `localhost:9092-9094` | 9092+ | Event Streaming |
| **Kafka UI** | <https://kafka-ui.127.0.0.1.nip.io> | 8080 | Kafka Management UI |
| **KSQL** | `localhost:8088` | 8088 | Streaming SQL |

## Application & DevOps

| Service | URL | Port | Purpose |
| :--- | :--- | :--- | :--- |
| **n8n** | <https://n8n.127.0.0.1.nip.io> | 5678 | Workflow Automation |
| **Ollama** | `localhost:11434` | 11434 | LLM Inference API |
| **Open WebUI** | <https://chat.127.0.0.1.nip.io> | 3000 | LLM Chat Interface |
| **SonarQube** | <https://sonarqube.127.0.0.1.nip.io> | 9000 | Code Quality |
| **Harbor** | <https://harbor.127.0.0.1.nip.io> | 80/443 | Container Registry |
| **Terrakube** | <https://terrakube.127.0.0.1.nip.io> | 8080 | IaC Platform |
| **Storybook** | <https://storybook.127.0.0.1.nip.io> | 6006 | Component Documentation |
| **Terraform** | Docker CLI | - | Infrastructure as Code |
| **Airflow** | <https://airflow.127.0.0.1.nip.io> | 8080 | Data Orchestration |

## Utilities

| Service | URL | Port | Purpose |
| :--- | :--- | :--- | :--- |
| **MailHog/Stalwart** | <https://mail.127.0.0.1.nip.io> | 8025 | Email Testing/Relay |
| **Nginx** | `localhost:80` | 80 | Static Web Server |

## Redis Cluster (Legacy)

| Service | Connection | Port | Purpose |
| :--- | :--- | :--- | :--- |
| **Redis** | `localhost:7000-7005` | 7000+ | Legacy Redis Cluster |
