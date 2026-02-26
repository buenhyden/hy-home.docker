# ADR-001: System Optimization and Hardening Strategies

## Status

Approved

## Context

The previous Hy-Home infrastructure integrated multiple Docker Compose sub-stacks via the `include` directive. However, it lacked standardization in security capabilities, observability drivers, and resource boundaries, leading to inconsistent security postures across tiers.

## Decision [REQ-SPT-09]

We SHALL implement the following optimization strategies to fulfill **[REQ-SYS-01]** and **[REQ-SYS-02]**:

1. **Local YAML Anchors**: Every tier-specific `docker-compose.yml` SHALL define a local `x-optimizations` block with anchors for `&security-baseline` and `&logging-loki` to ensure reliable expansion.
2. **Minimal Capabilities Policy**: All infrastructure services MUST explicitly drop all capabilities (`cap_drop: ALL`) and utilize `no-new-privileges: true`.
3. **Loki-Integrated Logging**: The `loki` logging driver MUST be the primary telemetry channel for all containers, providing unified metadata via `hy-home.tier` labels.
4. **Deterministic Orchestration**: Service dependencies SHALL be enforced via `service_healthy` conditions to ensure reliable startup order.

## Consequences [REQ-SPT-05]

- **Positive**: Uniform security across all tiers, predictable resource consumption, and simplified log aggregation.
- **Negative**: Increased YAML boilerplate in localized compose files to overcome Docker Compose scoping limitations.
