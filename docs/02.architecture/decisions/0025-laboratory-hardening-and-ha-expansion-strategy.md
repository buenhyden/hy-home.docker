---
title: "Laboratory Hardening and HA Expansion Strategy"
version: "1.0.2"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0025"
parent_ids:
- "AD-0025"
created: "2026-03-28"
---
# ADR-0025: Laboratory Hardening and HA Expansion Strategy

## Context

This document records the decision to first apply immediately applicable hardening (ingress boundary strengthening, removal of direct exposure, network contract alignment, minimal-privilege improvements, CI gate introduction) for the `11-laboratory` layer, while introducing catalog expansion items in phases.

The laboratory tier greatly affects operator productivity but provides UIs with strong privileges. Therefore, loose security/operating standards can create bypass paths into the entire core tier. Boundary hardening is needed in the short term, and strengthened experimental-service operating governance (expiration/approval/audit) is needed in the mid term.

### Traceability

The verification basis for this decision is limited to the Architecture Description, Spec, and Operations documents linked under `Related Documents`, and the current repository configuration. It does not claim any runtime state without separate execution evidence.

## Decision

- Apply immediate hardening.
  - Remove the dashboard's direct host `ports` exposure and allow only exposure via Traefik.
  - Apply `gateway-standard-chain + service ipAllowList + sso-errors + sso-auth` to all laboratory routers.
  - Keep the service network block that joins the root `infra_net` context.
  - Restrict the dozzle docker socket to read-only.
  - Protect the open-notebook UI route with an allowlist+large-body+SSO boundary and keep Docker Secret-based credential injection.
  - Introduce `check-all-hardening.sh 11-laboratory` and the CI `infrastructure-hardening` job.
- Apply catalog expansion in phases.
  - Dashboard expiration policy
  - Dozzle log access scope restriction
  - Portainer session/approval policy
  - RedisInsight minimal-privilege/audit log policy
  - open-notebook notebook data retention/expiration and direct API/DB host-port exposure review

### Decision Drivers

The decision context above records the applicable drivers and evidence.

## Alternatives

### Alternatives

### Options Considered

### Implement all catalog items immediately

- Good:
  - Fast rise in policy maturity
- Bad:
  - Expanded change scope can reduce short-term stability

### Update documentation only, hold off on runtime/CI hardening

- Good:
  - Reduces short-term change volume
- Bad:
  - Lacks the ability to actually block regressions

## Consequences

- **Positive**:
  - Management UIs sit behind a consistent security boundary.
  - Removes direct-exposure bypass paths and blocks operational drift in CI.
  - Catalog expansion items become executable in Plan/Tasks/Operations.
- **Trade-offs**:
  - The allowlist default may require environment variable adjustment for remote operator access.
  - Adding the CI gate slightly increases PR processing time.

### Explicit Non-goals

- Immediately replatforming the laboratory service group
- A full redesign of core Keycloak/Traefik policy
- Immediately automating the runtime of all catalog expansion items

## Related Documents

- **PRD**: [../01.requirements/0012-laboratory.md](../../01.requirements/0012-laboratory.md)
- **Architecture Description**: [../02.architecture/descriptions/0025-laboratory-optimization-hardening-architecture.md](../descriptions/0025-laboratory-optimization-hardening-architecture.md)
- **Spec**: [../03.specs/012-laboratory/spec.md](../descriptions/0011-laboratory-architecture.md)
- **Related ADR**: [ADR-0011](0011-laboratory-services.md)
