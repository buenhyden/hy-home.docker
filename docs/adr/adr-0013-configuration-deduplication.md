# ADR-0013: Configuration Deduplication via YAML Anchors and Global Inheritance

## Status

Proposed

## Context

As the number of microservices increases, managing redundant Docker Compose configurations (security options, logging drivers, common volumes) becomes error-prone and leads to configuration drift. We have established `infra/common-optimizations.yml` as a template file, but we need more granular control over shared structures like complex logging labels and volume sets.

## Decision

1. **Extend Global Templates**: All infrastructure services SHALL use the `extends` directive to inherit baseline security (`no-new-privileges`, `cap_drop`) and resource limits.
2. **YAML Anchors for Metadata**: Standardize labels and logging options using YAML anchors (`&` and `*`) within tier-level or global compose files to ensure metadata consistency.
3. **Internal Path Masking**: Replace host-specific absolute paths in volume definitions with environment-driven variables (`${DEFAULT_MOUNT_VOLUME_PATH}`) defined in `.env.example`.

## Consequences

- **Positive**: Reduced maintenance overhead, unified logging/security auditing, and improved ease of adding new services.
- **Negative**: Increased complexity in debugging "resolved" compose configurations (requires `docker compose config`).
- **Neutral**: Services now have a strict dependency on the existence of `common-optimizations.yml`.
