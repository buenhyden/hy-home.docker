# Infrastructure Architecture Overview

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![Status](https://img.shields.io/badge/status-active-success)

> A macro-level overview of the `infra` docker-compose stack and its isolated network layout.

## 1. System Context

The `infra` directory hosts the core operational tooling for the platform. It is designed around modular `docker-compose.yml` stacks that integrate via a shared Docker bridge network (`infra_net`).

## 2. Directory Structure

The infrastructure is broken down into tiered capabilities:

- `01-gateway`: Edge routing and load balancing via Traefik.
- `02-auth`: Authentication providers (Keycloak, OAuth2 Proxy).
- `03-security`: Secrets management and hardening (Vault).
- `04-data`: Stateful stores (PostgreSQL Patroni cluster, MinIO, Redis/Valkey, Qdrant).
- `05-messaging`: Async bus and streaming (Kafka).
- `06-observability`: Telemetry (Prometheus, Loki, Tempo, Grafana, Alloy).
- `07-workflow` / `08-ai` / `09-tooling` / `10-communication`: Extension tools for application requirements.

## 3. Network Architecture

The environment relies on the `infra_net` custom bridge network with the IP space defined as `172.19.0.0/16`. Services explicitly define static IPv4 assignments within this subnet for predictability during node recovery.

> [!IMPORTANT]
> Do not expose internal ports directly to the host (`ports: "5432:5432"`) unless absolutely necessary. Inter-service communication MUST occur via the `infra_net` utilizing Docker DNS names (e.g., `pg-router:5000` or `prometheus:9090`).

## 4. Security Principles

- **Rootless Execution**: Where natively supported (e.g., PostgreSQL, Etcd, Prometheus), containers run using restricted users (`1000:1000`).
- **Read-Only Filesystems**: Edge components like Traefik employ `read_only: true` with strict bind mounts.
- **Capabilities**: All extended Docker capabilities are dropped unles explicitly justified.

## 5. Storage

All stateful data relies on local bind mounts originating from the root `$DEFAULT_DATA_DIR` mapping to specific volumes in the `docker-compose.yml` definitions to preserve state across restarts.
