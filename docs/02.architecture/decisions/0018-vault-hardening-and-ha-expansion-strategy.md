---
title: "Vault Hardening and HA Expansion Strategy"
version: "1.0.2"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0018"
parent_ids:
- "AD-0018"
created: "2026-03-28"
---
# ADR-0018: Vault Hardening and HA Expansion Strategy

## Context

This document records the decision to prioritize immediate hardening items for the `03-security` Vault layer, while managing auto-unseal/remote audit through a phased transition.

The existing Vault Agent template used placeholder paths, and lacked a `vault-agent` healthcheck, output persistence, and a dedicated CI gate. Auto-unseal and remote audit, on the other hand, require coordinating operational policy, approval, and external dependencies (KMS/HSM, remote storage), so immediate implementation carries high risk.

### Traceability

The verification basis for this decision is limited to the Architecture Description, Spec, and Operations documents linked under `Related Documents`, and the current repository configuration. It does not claim any runtime state without separate execution evidence.

## Decision

- Implement the immediate-application items first.
  - Remove template placeholders and fix the `secret/data/hy-home/...` path contract
  - Add a process-based healthcheck for `vault-agent`
  - Add a persistent `/vault/out` volume
  - Introduce `scripts/hardening/check-all-hardening.sh 03-security` plus the CI `infrastructure-hardening` gate
- At this stage, specify auto-unseal/remote audit ingestion only as a policy/architecture/runbook transition procedure.
- Keep the internal communication model as-is.
  - External TLS termination: Traefik
  - Internal `infra_net`: HTTP
- Restore the existing regression (`scripts/hardening/check-all-hardening.sh 02-auth`) in the same change set.

### Decision Drivers

The decision context above records the applicable drivers and evidence.

## Alternatives

### Alternatives

### Options Considered

### Implement auto-unseal/remote audit at the same time, immediately

- Good:
  - Can quickly raise security maturity.
- Bad:
  - Change risk is high while operational approval/external dependencies are undecided.
  - Harder to isolate root cause during a failure.

### Update documentation only and hold off on infrastructure changes

- Good:
  - Short-term change risk is low.
- Bad:
  - Placeholder/healthcheck/CI regressions remain.

## Consequences

- **Positive**:
  - Operating contracts (paths/health/verification) become clear immediately.
  - CI can preemptively block 03-security regressions.
  - The transition context needed for HA expansion is documented.
- **Trade-offs**:
  - Realizing the value of auto-unseal/remote audit is deferred to the next stage.
  - The single-node raft operating risk remains for the time being.

### Explicit Non-goals

- Implementing KMS/HSM auto-unseal in this change
- Implementing a remote audit sink in this change
- Changing the Vault API/protocol

### Agent-related Example Decisions

- Tool gating: Enforce `check-all-hardening.sh 03-security` as a CI merge gate
- Guardrail strategy: Prohibit placeholder paths, prohibit plaintext secrets

## Related Documents

- **PRD**: [../01.requirements/0003-security.md](../../01.requirements/0003-security.md)
- **Architecture Description**: [../02.architecture/descriptions/0018-security-optimization-hardening-architecture.md](../descriptions/0018-security-optimization-hardening-architecture.md)
- **Spec**: [../03.specs/003-security/spec.md](../descriptions/0003-security-architecture.md)
- **Related ADR**: [ADR-0003](0003-vault-as-secrets-manager.md)
