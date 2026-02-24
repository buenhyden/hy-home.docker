# Technical Context Documentation Hub (`docs/context/`)

This directory serves as the **authoritative hub for service-specific operational architecture** and technical blueprints. It integrates design-time context with bootstrapping and initialization logic.

## Navigation Index

### 01-Gateway

- [**Traefik Ingress Guide**](01-gateway/traefik-ingress-guide.md): Router rules, SSL termination, and labels.

### 02-Authentication & Communication

- [**Keycloak Identity Provider Guide**](02-auth/keycloak-idp-guide.md): Realm setup, OIDC clients, and user provisioning.
- [**SSO & OAuth2 Proxy Blueprint**](02-auth/sso-oauth2-proxy-guide.md): Centralized auth flow and cache.
- [**SMTP Mail Relay Guide**](02-auth/mail-relay-operations.md): Internal mail trapping and testing.

### 03-Security Tier

- [**HashiCorp Vault Security Guide**](03-security/vault-cluster-guide.md): Secret initialization, unsealing, and integration.

### 04-Data Storage

- [**CouchDB Cluster Blueprint**](04-data/couchdb-blueprint.md): HA configurations and API patterns.
- [**MinIO Object Storage Guide**](04-data/minio-s3-guide.md): S3 compatibility and CLI management.
- [**PostgreSQL HA Guide**](04-data/postgres-patroni-ha-guide.md): Patroni topology and switchover logic.
- [**PostgreSQL Router Guide**](04-data/postgres-router-guide.md): HAProxy load balancing for SQL.
- [**Valkey Memory Store Guide**](04-data/valkey-cluster-guide.md): 6-node cluster topology and connectivity.

### 05-Messaging

- [**Kafka KRaft Guide**](05-messaging/kafka-kraft-guide.md): Zookeeper-less streaming architecture.
- [**RabbitMQ Operational Blueprint**](05-messaging/rabbitmq-guide.md): AMQP queues and management.

### 06-Observability

- [**LGTM Stack Blueprint**](06-observability/lgtm-stack-blueprint.md): Loki, Grafana, Tempo, and Alloy metrics flow.
- [**InfluxDB TSDB Guide**](06-observability/influxdb-tsdb-guide.md): Time-series metrics and data retention.
- [**OpenSearch Log Analytics Guide**](06-observability/opensearch-log-search-guide.md): Centralized searching and indexing.

### 07-Workflow Automation

- [**n8n Automation Context**](07-workflow/n8n-automation-context.md): Low-code queue-based execution.
- [**Airflow Orchestration Blueprint**](07-workflow/airflow-orchestration-guide.md): Complex DAG management.

### 08-AI Infrastructure

- [**AI Inferencing & UI Guide**](08-ai/ai-inference-guide.md): Ollama, Open-WebUI, and GPU acceleration.
- [**Qdrant Vector DB Context**](08-ai/qdrant-vector-db-context.md): RAG memory and HNSW optimization.

### 09-DevOps Tooling

- [**Tooling & Static Analysis Guide**](09-tooling/devops-tooling-guide.md): SonarQube, Terraform, and Terrakube.

### Core Foundation

- [**Infra Lifecycle & Core Operations**](core/infra-lifecycle-ops.md): Global stack management and startup order.
