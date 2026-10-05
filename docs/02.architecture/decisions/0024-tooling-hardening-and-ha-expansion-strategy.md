---
title: "Tooling Hardening and HA Expansion Strategy"
version: "2.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0024"
parent_ids:
- "AD-0024"
created: "2026-03-28"
---
# ADR-0024: Tooling Hardening and HA Expansion Strategy

## Context

This document records the decision to first carry out immediately applicable hardening (public path SSO chain alignment, explicit network boundaries, locust/k6 runtime contract reinforcement, CI gate introduction) for the `09-tooling` layer, while pursuing catalog expansion items in phases.

The tooling tier corresponds to the platform's operational control plane, and if the boundaries around security/quality/test tools are weak, this directly affects organization-wide deployment stability. At the same time, the catalog requires expansion/strengthened policy per tool, so separating short-term stabilization from mid-term expansion is needed.

### Traceability

The verification basis for this decision is limited to the Architecture Description, Spec, and Operations documents linked under `Related Documents`, and the current repository configuration. It does not claim any runtime state without separate execution evidence.

## Decision

- Carry out immediate hardening.
  - Align the SonarQube/Terrakube routers to `gateway-standard-chain + sso-errors + sso-auth`.
  - Make the `infra_net` external boundary declaration explicit in the tooling compose.
  - Add a locust-worker healthcheck and align k6 volume reference drift.
  - Introduce `scripts/hardening/check-all-hardening.sh 09-tooling` and the CI `infrastructure-hardening` job.
- Carry out catalog expansion in phases.
  - OpenTofu approval/backup/drift automatic detection
  - Strengthen terrakube permissions/audit log
  - Registry signing/scan blocking policy
  - Redefine sonarqube quality gate
  - Standardize k6/locust tests

### Decision Drivers

The decision context above records the applicable drivers and evidence.

## Alternatives

### Alternatives

### Options Considered

### Implement all catalog expansion immediately

- Good:
  - Fast functional sense of the expansion items
- Bad:
  - Increased change scope raises stabilization/verification complexity

### Update documentation only, hold off on runtime/CI hardening

- Good:
  - Reduces short-term implementation cost
- Bad:
  - Lacks the ability to block regressions

## Consequences

- **Positive**:
  - Access control on the tooling public path becomes consistent.
  - Operational network boundaries and test runtime stability improve.
  - Tooling tier regressions can be automatically blocked at the PR stage.
  - Catalog expansion items become executable at the document/task level.
- **Trade-offs**:
  - Strengthened SSO requires adjusting some existing test access paths.
  - Adding policy gates may increase short-term PR processing time.

### Explicit Non-goals

- Immediately replatforming the entire tooling stack
- Immediately implementing the full runtime of catalog expansion items
- Introducing a new tool chain

### Agent-related Example Decisions

- Guardrail strategy: The tooling public router requires the gateway+SSO chain
- Tool gating: Enforce `check-all-hardening.sh 09-tooling` as a required policy gate before merging

## Related Documents

- **PRD**: [../01.requirements/0010-tooling.md](../../01.requirements/0010-tooling.md)
- **Architecture Description**: [../02.architecture/descriptions/0024-tooling-optimization-hardening-architecture.md](../descriptions/0024-tooling-optimization-hardening-architecture.md)
- **Spec**: [../03.specs/010-tooling/spec.md](../descriptions/0009-tooling-architecture.md)
- **Related ADR**: [ADR-0009](0009-tooling-services.md)
