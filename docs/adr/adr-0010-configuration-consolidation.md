# ADR-0010: Configuration Consolidation via Templates

## Status

Proposed

## Context

Infrastructure service definitions in Docker Compose were becoming redundant, repeating security baselines, logging drivers, and restart policies across multiple files. This fragmentation makes global updates (e.g., changing the Loki URL or updating security options) difficult and error-prone.

## Decision

We will consolidate all common infrastructure "anchors" into a single file: `infra/common-optimizations.yml`.
This file will define:

- `&security-baseline`: `no-new-privileges` and `cap_drop`.
- `&logging-loki`: Standardized Loki driver configuration.
- `&default-restart`: Default `unless-stopped` policy.
- `&resource-low/med/high`: Standardized CPU/Memory quotas.

Service definitions will `include` or reference this file to apply these templates.

## Consequences

- **Positive**: Single point of truth for infrastructure standards.
- **Positive**: Reduced boilerplate in service-specific compose files.
- **Negative**: Increased dependency on the `include` feature of Docker Compose.
- **Negative**: Slight complexity in understanding anchor resolution across files.
