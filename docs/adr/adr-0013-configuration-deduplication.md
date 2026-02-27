# ADR-0013: Configuration Deduplication and Consolidation

- **Status**: Proposed
- **Date**: 2026-02-27
- **Authors**: Platform Architect

## 1. Context

As the number of infrastructure services in the Hy-Home ecosystem increases, managing redundant Docker Compose configurations (security options, logging drivers, common volumes, and restart policies) across 30+ service definitions has become error-prone and leads to configuration drift. We need a uniform, template-driven approach to minimize boilerplate and ensure architectural invariants.

## 2. Decision

We SHALL utilize a two-tier configuration management strategy:

1. **Global Inheritance (`extends`)**: Consolidate all common infrastructure "anchors" and composite profiles into `infra/common-optimizations.yml`. All services MUST extend from these global templates.
2. **YAML Anchors for Metadata**: Utilize YAML anchors (`&` and `*`) within tier-level or global files to maintain consistent metadata (e.g., complex logging labels) that cannot be fully captured in static global templates.
3. **Path Abstraction**: 100% of host-specific absolute paths in volume definitions SHALL be replaced by environment variables (e.g., `${DEFAULT_DATA_DIR}`) defined in `.env.example`.

### 2.1 Defined Templates

In `infra/common-optimizations.yml`:

- `base-security`: Core isolation (`no-new-privileges`, `cap_drop: ALL`).
- `logging-loki`: Standardized Loki driver configuration.
- `resource-low/med/high`: Standardized CPU/Memory quotas.
- `template-infra-low/med/high`: Composite templates combining security, logs, and resources.

## 3. Consequences

- **Positive**: Uniform security posture and observability across all stacks.
- **Positive**: Drastic reduction in YAML boilerplate and maintenance toil.
- **Negative**: Increased dependency on Docker Compose v2.20+ and the `include`/`extends` features.
- **Negative**: Resolved configurations are more complex to debug (requires `docker compose config`).
