---
layer: infra
---

# Technical Context Documentation Hub (`docs/context/`)

This directory serves as the **authoritative hub for service-specific operational architecture** and technical blueprints.

## Navigation Index

### 🌐 Gateway & Auth

- [**Traefik Ingress Guide**](traefik-ingress-guide.md)
- [**Gateway Operations**](gateway-operations.md)
- [**Keycloak IDP Guide**](keycloak-idp-guide.md)
- [**SSO & Proxy Guide**](sso-oauth2-proxy-guide.md)
- [**Mail Server & Relay**](mail-server-operations.md) | [**Relay Guide**](mail-relay-operations.md) | [**Auth & Mail**](auth-and-mail-operations.md)

### 💾 Data & Storage

- [**Postgres HA (Patroni)**](postgres-patroni-ha-guide.md) | [**Cluster Ops**](postgres-cluster-operations.md) | [**Router**](postgres-router-guide.md) | [**Operations**](postgresql-operations.md)
- [**Valkey Cluster**](valkey-cluster-guide.md) | [**Operations**](valkey-cluster-operations.md)
- [**MinIO Object Storage**](minio-s3-guide.md) | [**Operations**](minio-operations.md)
- [**CouchDB Blueprint**](couchdb-blueprint.md) | [**Operations**](couchdb-operations.md)

### 📊 Messaging & Observability

- [**Kafka KRaft**](kafka-kraft-guide.md) | [**Operations**](kafka-operations.md)
- [**RabbitMQ Guide**](rabbitmq-guide.md) | [**Operations**](rabbitmq-operations.md)
- [**LGTM Stack Blueprint**](lgtm-stack-blueprint.md)
- [**OpenSearch Guide**](opensearch-log-search-guide.md) | [**Operations**](opensearch-operations.md)
- [**InfluxDB TSDB**](influxdb-tsdb-guide.md) | [**Operations**](influxdb-operations.md)

### 🤖 AI & Automation

- [**AI Inference Guide**](ai-inference-guide.md)
- [**Qdrant Context**](qdrant-vector-db-context.md) | [**Qdrant Ops**](ai-qdrant-operations.md)
- [**n8n Automation**](n8n-automation-context.md) | [**n8n Ops**](workflow-n8n-operations.md)
- [**Airflow Blueprint**](airflow-orchestration-blueprint.md) | [**Guide**](airflow-orchestration-guide.md)
- [**Workflow Operations**](workflow-operations.md)

### 🛠️ Tooling & Core

- [**DevOps Tooling Guide**](devops-tooling-guide.md) | [**Operations**](tooling-operations.md)
- [**Infra Lifecycle & Ops**](infra-lifecycle-ops.md) | [**Lifecycle Docs**](infra-lifecycle.md)
- [**Infra Optimization**](infra-optimization-analysis.md) | [**Audit Report**](infra-compose-optimization-audit.md)
