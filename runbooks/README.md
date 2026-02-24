# Operational Runbooks Hub (`runbooks/`)

This directory is the **exclusive, authoritative home** for all executable procedures and incident response guides. Every file here is strictly procedural: "Actionable steps to resolve infrastructure state."

## Documentation Taxonomy

1. **Technical Blueprints** ([`docs/context/`](../docs/context/README.md)): The "Why" and "How it works".
2. **Runbooks** ([`runbooks/`](./README.md)): The "What to type" during an incident.

## Directory Structure

- [**01-Gateway**](01-gateway/) ([Blueprint](../docs/context/01-gateway/traefik-ingress-guide.md)): Ingress recovery and routing fixes.
- [**02-Auth**](02-auth/) ([Blueprint](../docs/context/02-auth/keycloak-idp-guide.md)): Identity provider lockout and DB restoration.
- [**03-Security**](03-security/) ([Blueprint](../docs/context/03-security/vault-cluster-guide.md)): Vault unsealing and key management.
- [**04-Data**](04-data/) ([Blueprint](../docs/context/04-data/postgres-patroni-ha-guide.md)): Database HA recovery and sync maintenance.
- [**05-Messaging**](05-messaging/) ([Blueprint](../docs/context/05-messaging/kafka-kraft-guide.md)): Kafka/RabbitMQ quorum and maintenance.
- [**06-Observability**](06-observability/) ([Blueprint](../docs/context/06-observability/lgtm-stack-blueprint.md)): LGTM stack maintenance and storage cleanup.
- [**07-Workflow**](07-workflow/) ([Blueprint](../docs/context/07-workflow/n8n-automation-context.md)): Automation engine and worker recovery.
- [**08-AI**](docs/context/08-ai/ai-inference-guide.md) ([Blueprint](../docs/context/08-ai/ai-inference-guide.md)): Model inference and GPU recovery.
- [**Core**](core/) ([Blueprint](../docs/context/core/infra-lifecycle-ops.md)): Global incident response and deployment workflows.

## Standards for New Runbooks

- **Given**: The starting state or symptoms.
- **When**: The specific trigger or failure condition.
- **Then**: The exact CLI commands to resolve the issue.

> **DevOps Rule**: No architecture diagrams or background theory in this folder. Use cross-links to `docs/context/` for that purpose.
