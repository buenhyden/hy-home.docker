---
layer: infra
title: 'Infrastructure Operational Scope'
---

# Infrastructure Operational Scope

**Boundaries, permissions, and performance standards for agents interacting with the `hy-home.docker` infrastructure.**

## 1. Context & Objective

- **Goal**: Maintain a highly available, performant, and secure containerized infrastructure.
- **Service Stack**: Traefik/Nginx, Keycloak, PostgreSQL (Zalando Spilo Cluster), Kafka, OpenSearch, Ollama, MinIO.
- **Performance SLO**: Maintain a gateway-level **LATENCY_SLO < 200ms** for all core service requests.
- **Standard**: Mandatory alignment with `docs/00.agent-governance/rules/quality-standards.md`.

## 2. Requirements & Constraints

- **Networking**: All inter-service traffic MUST use `infra_net`. Direct external exposure is PROHIBITED except via authorized gateways.
- **Storage**: Use named volumes following the `[Service]-[Data]-[Volume]` convention.
- **Security**: Mandatory `no-new-privileges: true` for all containers. Use Docker Secrets for production credentials.
- **Service Integrations**:
  - **Messaging**: Kafka (standard) or RabbitMQ for async events.
  - **AI**: Ollama for local LLM inference, Open-WebUI for interaction.

## 3. Implementation Flow

1. **Pre-flight**: Run `bash scripts/validate-docker-compose.sh` or `compose-preflight.sh` before any change.
2. **Schema**: Verify service dependencies and network isolation in `docker-compose.yml`.
3. **Execution**: Apply smallest correct change (Atomic Infra).
4. **Post-check**: Verify service health via `docker compose ps` and logs.

## 4. Operational Procedures

- **Scalability**: For database scaling, refer to `infra/04-data/postgresql-cluster/` (Patroni/ETCD).
- **Secrets**: Rotate secrets via `scripts/gen-secrets.sh` (referencing `SENSITIVE_ENV_VARS.md.example`).

## 5. Maintenance & Safety

- **Backups**: Ensure automated backup tags are present for all persistent data volumes.
- **Pruning**: `docker system prune` is PROVISIONS-ONLY. Never run without explicit user consent.
