---
title: "02-Auth Runtime Hardening and Fail-closed Policy"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0017"
parent_ids:
- "AD-0002"
created: "2026-03-28"
---
# ADR-0017: 02-Auth Runtime Hardening and Fail-closed Policy

## Context

This document records the decision on the `02-auth` layer's runtime hardening approach and the fail-closed policy for authentication failures.

The OAuth2 Proxy in `infra/02-auth` handled secret injection through an inline Compose shell. This approach had low change traceability and reusability, and did not align with operating standards (minimal-privilege runtime, a clear entrypoint contract). Also, whether bypass is allowed during an authentication failure was not clearly fixed in documentation.

### Traceability

The verification basis for this decision is limited to the Architecture Description, Spec, and Operations documents linked under `Related Documents`, and the current repository configuration. It does not claim any runtime state without separate execution evidence.

## Decision

- Unify OAuth2 Proxy secret injection into `docker-entrypoint.sh`.
- Run the OAuth2 Proxy container as a non-root user (`oauth2proxy`).
- Keep fail-closed as the default behavior for authentication failures.
- Perform degraded-mode only in a limited way, per policy/runbook procedure, and require restoring the prior state afterward.
- Keep Keycloak on `template-infra-high`, given its stateful characteristics and current resource baseline (do not force a switch to readonly).

### Decision Drivers

The decision context above records the applicable drivers and evidence.

## Alternatives

### Alternatives

### Options Considered

### Keep the Compose inline shell

- Good:
  - Easy to apply immediately.
- Bad:
  - Secret handling logic is mixed into a declarative file, giving low traceability.
  - Hard to separate reuse/test points.

### Adopt a fail-open exception as the default

- Good:
  - Short-term availability may rise during an IdP failure.
- Bad:
  - Authentication bypass risk grows and the security boundary collapses.

## Consequences

- **Positive**:
  - The secret injection path becomes unified, making audit and verification easier.
  - Minimal-privilege execution reduces the container runtime attack surface.
  - Operators can respond consistently to failures according to policy/procedure.
- **Trade-offs**:
  - Creates a maintenance responsibility for the entrypoint script.
  - Fail-closed means user impact can surface immediately during an IdP failure.

### Explicit Non-goals

- Adding or replacing an authentication stack beyond Keycloak/OAuth2 Proxy
- Introducing fail-open as the default policy
- Introducing a new secret backend (forced migration to Vault)

### Agent-related Example Decisions

- Tool gating: Use `scripts/hardening/check-all-hardening.sh 02-auth` as a required CI gate
- Guardrail strategy: Prohibit plaintext secrets and bypass policies

## Related Documents

- **Requirement Package**: [REQ-0002 Auth requirements](../../01.requirements/0002-auth.md)
- **Architecture Description**: [AD-0002 Auth architecture](../descriptions/0002-auth-architecture.md)
- **Related ADR**: [ADR-0002](0002-keycloak-oauth2-proxy-choice.md)
