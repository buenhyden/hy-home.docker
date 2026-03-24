---
layer: agentic
---

# Infrastructure Workflow Rule

> **Authority**: `instructions.md`

## Rules

1. **Validation First**: Run `scripts/validate-docker-compose.sh` before applying changes.
2. **Secrets Hygiene**: Use Docker Secrets, never `.env` for plain-text credentials.
3. **Connectivity**: All inter-service traffic must use `infra_net`.
4. **Permissions**: Enforce `no-new-privileges:true`.
