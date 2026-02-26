# ADR-001: System Optimization and Hardening Strategies

## Status

Proposed

## Context

The current Hy-Home infrastructure consists of multiple Docker Compose sub-stacks integrated via the `include` directive. While functional, there is a lack of standardization in security (caps/privileges), observability (logging drivers), and resource limits.

## Decision [REQ-SPT-09]

We SHALL implement the following optimization strategies:

1. **YAML Anchors for Standardization**: Use YAML anchors/aliases in the root `docker-compose.yml` or shared configuration files to define `x-logging`, `x-security`, and `x-resource` templates.
2. **Minimal Capabilities Policy**: Every service MUST explicitly drop all capabilities and only add required ones (e.g., `NET_BIND_SERVICE`).
3. **Loki-First Logging**: The `loki` logging driver SHALL be the primary driver for all services, with a `json-file` fallback where necessary.
4. **Deterministic Healthchecks**: Refine `depends_on` conditions to use `service_healthy` to ensure ordered startup and reduce initial failure noise.

## Consequences

- **Positive**: Improved security posture, centralized log management, better resource predictability.
- **Negative**: Increased complexity in template management, potential for service-specific capability issues during initial rollout.
