# Operational Runbooks Hub (`runbooks/`)

This directory is the **exclusive, authoritative home** for all executable procedures and incident response guides. Every file here is strictly procedural: "Actionable steps to resolve infrastructure state."

## Documentation Taxonomy

1. **Technical Blueprints** ([`docs/context/`](../docs/context/README.md)): The "Why" and "How it works".
2. **Runbooks** ([`runbooks/`](./README.md)): The "What to type" during an incident.

## Directory Structure

- [**01-Gateway**](01-gateway/): Ingress recovery and routing fixes.
- [**02-Auth**](02-auth/): Identity provider lockout and DB restoration.
- [**03-Security**](03-security/): Vault unsealing and key management.
- [**04-Data**](04-data/): Database HA recovery and sync maintenance.
- [**05-Messaging**](05-messaging/): Kafka/RabbitMQ quorum and maintenance.
- [**06-Observability**](06-observability/): LGTM stack maintenance and storage cleanup.
- [**07-Workflow**](07-workflow/): Automation engine and worker recovery.
- [**Core**](core/): Global incident response and deployment workflows.

## Standards for New Runbooks

- **Given**: The starting state or symptoms.
- **When**: The specific trigger or failure condition.
- **Then**: The exact CLI commands to resolve the issue.

> **DevOps Rule**: No architecture diagrams or background theory in this folder. Use cross-links to `docs/context/` for that purpose.
