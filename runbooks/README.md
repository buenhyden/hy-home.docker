# Operational Runbooks Hub (`runbooks/`)

This directory is the **exclusive, authoritative home** for all executable procedures and incident response guides. Every file here is strictly procedural: "Actionable steps to resolve infrastructure state."

## 📚 Documentation Taxonomy

1. **Architecture Reference (ARD)** ([`docs/ard/`](../docs/ard/README.md)): The "How it's built".
2. **Product Requirements (PRD)** ([`docs/prd/`](../docs/prd/README.md)): The "What it should do".
3. **Operational Runbooks** ([`runbooks/`](./README.md)): The "What to type" during an incident.

## 🧭 Operational Navigator (Role-Based)

### 🏗️ For Platform Engineers (Bootstrap & Core)

- [**Core Procedures**](core/) — `make bootstrap`, environment setup, and global incident response.
- [**Gateway Ingress**](01-gateway/) — Traefik routing, 502/504 errors, and middleware fixes.
- [**Security & Vault**](03-security/) — Unsealing Vault, rotated secrets, and TLS certificate generation.

### 💾 For Data & Reliability Engineers

- [**Database HA**](04-data/) — PostgreSQL Patroni recovery, MinIO sync, and OpenSearch shards.
- [**Event Streams**](05-messaging/) — Kafka broker offline recovery and RabbitMQ quorum.
- [**Observability Stack**](06-observability/) — Maintaining the LGTM stack (Loki/Prom/Tempo) and full storage remediation.

### 🤖 For AI & Automation Ops

- [**Workflow Engines**](07-workflow/) — Airflow Celery workers and n8n engine recovery.
- [**Local AI Stack**](docs/ard/ai-ard.md) — GPU passthrough and model pulling procedures.

## 📐 Operational Standards (`0381-runbooks-oncall.md`)

Every runbook MUST follow the 8-section template:

- **Scenario Based**: Uses **Given-When-Then** format for troubleshooting scenarios.
- **Deterministic**: Provides direct CLI commands with expected outcomes.
- **Verification First**: Every fix must be validated via Section 8.

---
> [!IMPORTANT]
> **NO THEORY, ONLY ACTION.** Documentation for architectural background belongs in `docs/ard/`.
