---
title: "Observability Hardening and HA Expansion Strategy"
version: "1.0.4"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "architecture"
artifact_id: "ADR-0021"
parent_ids:
- "AD-0021"
created: "2026-03-28"
---
# ADR-0021: Observability Hardening and HA Expansion Strategy

## Context

### Problem and Drivers

This document records the decision to first apply immediately applicable hardening (gateway chain + SSO, strengthened health dependencies, container runtime hardening, CI baseline) for the `06-observability` layer, while pursuing catalog-based HA expansion in phases.

The observability layer provides many management paths, and failures can spread easily if the security chain is missing, startup order is unstable, or runtime hardening is insufficient. Layer-specific verification automation is needed to block operational regressions at the PR stage.

### Decision Scope

Explicit non-goals:

- Immediately switching to a multi-region observability cluster
- A wholesale overhaul of application code instrumentation logic

## Decision

### Chosen Option

- Perform immediate hardening.
  - Apply `gateway-standard-chain@file` plus `sso-errors@file,sso-auth@file` to the observability public router.
  - Raise the Loki/Tempo dependency for Alloy/Grafana to `service_healthy`.
  - Add a cAdvisor healthcheck.
  - Specify non-root execution/secret guard for the Loki/Tempo custom images.
  - Introduce `check-all-hardening.sh 06-observability` and the CI `infrastructure-hardening` job.
  - Create the PRD-through-Runbook document set to secure bidirectional traceability.
- Introduce catalog expansion (sampling/long-term retention/modularization) in phases through a policy approval procedure.

### Authority and Effect

Decided by the owner, @buenhyden; status `accepted`. No separate approval record is linked. Effective from 2026-03-28.

## Alternatives

### Considered Options

#### Implement all catalog expansion immediately

- Good:
  - Short-term functional expansion effect
- Bad:
  - Increased change scope raises failure isolation/rollback difficulty

#### Update documentation only, keep runtime/CI unchanged

- Good:
  - Reduces short-term implementation burden
- Bad:
  - Lacks the ability to actually block regressions

### Trade-offs

Immediate full catalog expansion was not chosen because the increased change scope raises failure isolation and rollback difficulty. Documentation-only was not chosen because it lacks the ability to actually block regressions.

## Consequences

### Impacts

- **Positive**:
  - The management path security boundary strengthens.
  - Startup stability and operational regression detection improve.
  - The single contract (SSoT) across documents/configuration/CI strengthens.
- **Trade-offs**:
  - Some automated access may need adjustment due to strengthened SSO.
  - Catalog expansion is applied in phases, so short-term visible effect is centered on hardening.

#### Agent-related Example Decisions

- Tool gating: Use `check-all-hardening.sh 06-observability` as a required PR gate
- Guardrail strategy: Require a security chain on public routers, require non-root/secret guard

### Follow-up

Catalog expansion (sampling/long-term retention/modularization) follows in phases through a policy approval procedure, as decided above.

## Traceability

### Sources

The verification basis for this decision is limited to the Architecture Description, Spec, and Operations documents linked below, and the current repository configuration. It does not claim any runtime state without separate execution evidence.

- **PRD**: [../01.requirements/0007-observability.md](../../01.requirements/0007-observability.md)
- **Architecture Description**: [AD-0021 06-Observability Optimization Hardening Architecture Description](../descriptions/0021-observability-optimization-hardening-architecture.md)
- **Tier Architecture Description**: [AD-0006 Observability Architecture Description](../descriptions/0006-observability-architecture.md)
- **Related ADR**: [ADR-0053](0053-observability-storage-on-seaweedfs.md)
