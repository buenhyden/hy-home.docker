# ARD: Optimized Home Lab Architecture Review

## Architecture Overview

The system is a multi-tier Docker Compose environment organized into functional clusters (Gateway, Security, Data, Messaging, Observability, AI).

## Optimized Tiers

1. **Tier 1 (Gateway)**: HA Traefik with automatic TLS and internal routing.
2. **Tier 2 (Core Logic)**: Auth (Keycloak) and Security (Vault) isolation.
3. **Tier 3 (Data Persistence)**: Clustered DBs with resource limits and backup schedules.
4. **Tier 4 (Observability)**: LGTM stack with centralized log collection from Tiers 1-3.

## Resource Strategy

- **Limits**: Every container has configured `mem_limit` and `cpu_quota`.
- **Profiles**: `docker compose --profile` used to toggle heavy AI and Tooling services to save idle RAM.

## Security Controls

- **Secrets**: 100% Docker Secrets.
- **Network**: Service isolation via `internal` Docker networks, only exposing Tier 1 Gateway to host.
