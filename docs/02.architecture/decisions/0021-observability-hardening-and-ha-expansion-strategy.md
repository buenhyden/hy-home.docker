---
title: "Observability Hardening and HA Expansion Strategy"
version: "1.0.2"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0021"
parent_ids:
- "AD-0021"
created: "2026-03-28"
---
# ADR-0021: Observability Hardening and HA Expansion Strategy

## Context

This document records the decision to first apply immediately applicable hardening (gateway chain + SSO, strengthened health dependencies, container runtime hardening, CI baseline) for the `06-observability` layer, while pursuing catalog-based HA expansion in phases.

The observability layer provides many management paths, and failures can spread easily if the security chain is missing, startup order is unstable, or runtime hardening is insufficient. Layer-specific verification automation is needed to block operational regressions at the PR stage.

## Decision

- Perform immediate hardening.
  - Apply `gateway-standard-chain@file` plus `sso-errors@file,sso-auth@file` to the observability public router.
  - Raise the Loki/Tempo dependency for Alloy/Grafana to `service_healthy`.
  - Add a cAdvisor healthcheck.
  - Specify non-root execution/secret guard for the Loki/Tempo custom images.
  - Introduce `check-all-hardening.sh 06-observability` and the CI `infrastructure-hardening` job.
  - Create the PRD-through-Runbook document set to secure bidirectional traceability.
- Introduce catalog expansion (sampling/long-term retention/modularization) in phases through a policy approval procedure.

## Consequences

- **Positive**:
  - The management path security boundary strengthens.
  - Startup stability and operational regression detection improve.
  - The single contract (SSoT) across documents/configuration/CI strengthens.
- **Trade-offs**:
  - Some automated access may need adjustment due to strengthened SSO.
  - Catalog expansion is applied in phases, so short-term visible effect is centered on hardening.

### Explicit Non-goals

- Immediately switching to a multi-region observability cluster
- A wholesale overhaul of application code instrumentation logic

### Agent-related Example Decisions

- Tool gating: Use `check-all-hardening.sh 06-observability` as a required PR gate
- Guardrail strategy: Require a security chain on public routers, require non-root/secret guard

## Options Considered

### Implement all catalog expansion immediately

- Good:
  - Short-term functional expansion effect
- Bad:
  - Increased change scope raises failure isolation/rollback difficulty

### Update documentation only, keep runtime/CI unchanged

- Good:
  - Reduces short-term implementation burden
- Bad:
  - Lacks the ability to actually block regressions

## Traceability

The verification basis for this decision is limited to the Architecture Description, Spec, and Operations documents linked under `Related Documents`, and the current repository configuration. It does not claim any runtime state without separate execution evidence.

## Decision Drivers

The decision context above records the applicable drivers and evidence.

## Related Documents

- **PRD**: [../01.requirements/0007-observability.md](../../01.requirements/0007-observability.md)
- **Architecture Description**: [../02.architecture/descriptions/0021-observability-optimization-hardening-architecture.md](../descriptions/0021-observability-optimization-hardening-architecture.md)
- **Spec**: [../03.specs/007-observability/spec.md](../descriptions/0006-observability-architecture.md)
- **Related ADR**: [ADR-0006](0006-lgtm-stack-selection.md)
