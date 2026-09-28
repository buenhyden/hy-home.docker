---
title: "Messaging Hardening and HA Expansion Strategy"
version: "1.0.2"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0020"
parent_ids:
- "AD-0020"
created: "2026-03-28"
---
# ADR-0020: Messaging Hardening and HA Expansion Strategy

## Context

This document records the decision to first introduce immediately applicable hardening (gateway chain, pinned image tags, configuration consistency, CI gate) for the `05-messaging` layer, while proceeding with catalog expansion items (DLQ/reprocessing/quorum queue/HA expansion) in phases.

The messaging layer exposes operationally sensitive management paths externally, and can be vulnerable to traffic spikes/transient failures. Floating-tag images and dev configuration consistency issues also lower reproducibility and stability. Automated baseline verification is needed to block operational regressions at the PR stage.

## Decision

- Reflect the immediate hardening items first.
  - Apply `gateway-standard-chain@file` to the management router
  - Pin `kafka-ui` family image tags to fixed versions
  - Fix `docker-compose.dev.yml` path consistency
  - Add a messaging-hardening-specific check script plus a CI job
  - Create the optimization-hardening Stage 01-05 document set and sync links
- Keep RabbitMQ on its current `messaging-option` operating model (opt-in activation).
- Apply catalog expansion items in phases through a policy/guide/runbook-based approval procedure.

## Consequences

- **Positive**:
  - Gateway boundary quality (traffic control/failure absorption) improves.
  - Reduces image regression risk and raises configuration reproducibility.
  - CI blocks messaging-hardening regressions early.
- **Trade-offs**:
  - Applying the SSO chain may require adjusting some operational automation scripts.
  - Catalog expansion is a phased rollout, so short-term effect stays centered on hardening.

### Explicit Non-goals

- Immediately restructuring the messaging topology itself in this change
- Implementing an application-logic-based reprocessing pipeline
- Switching to a cloud messaging service

### Agent-related Example Decisions

- Tool gating: Enforce `check-all-hardening.sh 05-messaging` as a CI gate
- Guardrail strategy: Prohibit floating tags, enforce the standard middleware chain, maintain document link integrity

## Options Considered

### Implement all catalog expansion items immediately

- Good:
  - Can deliver many functional improvements in the short term
- Bad:
  - Change scope grows, making failure isolation and rollback harder

### Update documentation only and hold off on compose/CI changes

- Good:
  - Reduces short-term implementation burden
- Bad:
  - Cannot automatically block actual operational regressions

## Traceability

The verification basis for this decision is limited to the Architecture Description, Spec, and Operations documents linked under `Related Documents`, and the current repository configuration. It does not claim any runtime state without separate execution evidence.

## Decision Drivers

The decision context above records the applicable drivers and evidence.

## Related Documents

- **PRD**: [../01.requirements/0006-messaging.md](../../01.requirements/0006-messaging.md)
- **Architecture Description**: [../02.architecture/descriptions/0020-messaging-optimization-hardening-architecture.md](../descriptions/0020-messaging-optimization-hardening-architecture.md)
- **Spec**: [../03.specs/006-messaging/spec.md](../descriptions/0005-messaging-architecture.md)
- **Related ADR**: [ADR-0005](0005-kafka-vs-rabbitmq-selection.md)
