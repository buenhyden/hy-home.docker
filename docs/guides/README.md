# System and Service Guides (docs/guides/)

This directory contains detailed technical context, blueprints, and operational guides for the various infrastructure tiers and services within the `hy-home.docker` platform.

## Directory Structure

The documentation is organized into tiers matching the [`infra/`](../../infra/) directory:

- [01-gateway/](01-gateway/): Edge routing, ingress (Traefik, Nginx), and TLS management.
- [02-auth/](02-auth/): Identity providers (Keycloak) and access proxies (OAuth2 Proxy).
- [03-security/](03-security/): Secret management and security vault (Vault).
- [04-data/](04-data/): Databases (PostgreSQL, Valkey), object storage (MinIO), and search (OpenSearch).
- [05-messaging/](05-messaging/): Event streaming and message brokers (Kafka, RabbitMQ).
- [06-observability/](06-observability/): Monitoring, logging, and tracing (LGTM stack).
- [07-workflow/](07-workflow/): Workflow orchestration and automation (Airflow, n8n).
- [08-ai/](08-ai/): Local AI inference and interfaces (Ollama, Open WebUI).
- [09-tooling/](09-tooling/): DevOps, QA, and platform engineering tools.
- [10-communication/](10-communication/): Mail servers and relay services.

## Relationship to Architecture

These documents supplement the global invariants defined in [`ARCHITECTURE.md`](../../ARCHITECTURE.md) by providing service-specific implementation details and operational context.
