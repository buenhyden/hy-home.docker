---
layer: agentic
---

# Infrastructure Operational Scope

**Boundaries and permissions for agents interacting with infrastructure.**

## 1. Domain Boundaries

- **Primary Surfaces**: `docker-compose*.yml`, `infra/`, `scripts/`, `secrets/`.
- **Secondary Surfaces**: Environment files (`.env`), TLS certs, configuration mounts.

## 2. Operational Permissions

- **READ**: Full read access to all infrastructure configurations.
- **WRITE**: 
  - Allowed for non-destructive changes (e.g., adding labels, updating images).
  - **ASK FIRST** for major structural changes or deleting services.
- **EXECUTE**:
  - `bash scripts/validate-docker-compose.sh`: MANDATORY before any infra change.
  - `docker compose config`: Recommended for syntax validation.
  - `docker system prune`: PROHIBITED without explicit User consent.

## 3. Verification Requirement

All infrastructure changes MUST be verified via `validate-docker-compose.sh` or `preflight-compose.sh`.
