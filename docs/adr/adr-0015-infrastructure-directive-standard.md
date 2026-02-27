# ADR-0015: Mandatory Infrastructure Directives

## Status

Proposed

## Context

The infrastructure audit revealed inconsistencies in healthcheck coverage, hardcoded IPs in `extra_hosts`, and varied volume path patterns. To ensure 100% portability and operational reliability, we need a strict directive standard.

## Decision

All services participating in the `hy-home` infrastructure MUST adhere to the following directive schema:

1. **Healthchecks**: Mandatory for all "Tier 1" and "Tier 2" services. Must use internal loopback URLs (`localhost`) and respect `${SERVICE_PORT}` variables where available.
2. **Zero Hardcoding**:
    - IP addresses in `extra_hosts` or `environment` are PROHIBITED. Use service names or variables.
    - Credentials MUST be injected via Docker Secrets (`/run/secrets/`).
3. **Volume Variable Primacy**: All host-path volumes MUST use the `${DEFAULT_*_DIR}` variable hierarchy defined in `.env.example`.
4. **Resource Caps**: All services must extend a resource profile (`template-infra-*`) or define explicit `deploy.resources.limits`.

## Consequences

- Improved portability across different host environments.
- Faster detection of service failures via standardized healthchecks.
- Enhanced security via enforced secret mapping.
- Simplified maintenance through variable inheritance.
