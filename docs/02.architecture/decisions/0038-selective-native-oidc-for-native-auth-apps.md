---
title: "Selective Native OIDC for Applications with Built-in Authentication"
version: "0.1.1"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0038"
parent_ids:
- "AD-0002"
created: "2026-09-18"
---

# ADR-0038: Selective Native OIDC for Applications with Built-in Authentication

## Context

`ADR-0002` selected Keycloak as the central Identity Provider and OAuth2 Proxy
as the Traefik ForwardAuth provider. This pattern suits services without their
own authentication, but for services with their own OIDC and application-level
RBAC it can cause double-auth, `Authorization` header conflicts, and
responsibility duplication.

Airflow 3.3.1's Keycloak Auth Manager and Kafbat UI v1.5.0 provide the <!-- runtime-version-exception: history — the decision records the versions it evaluated -->
application's own OIDC and authorization features.

### Rationale

- Keeps Keycloak as the central IAM.
- Uses Airflow's Keycloak Authorization Services as-is.
- Uses Kafbat's native OAuth2/RBAC as-is.
- Prevents conflicts between the `Authorization` the proxy injects and the
  application's own token.
- Keeps ForwardAuth's simplicity for services without their own
  authentication.

### Guardrails

- Do not apply ForwardAuth redundantly to native OIDC services by default.
- Inject OIDC client secrets as Docker Secrets.
- Add the local mkcert CA while preserving system/JDK public root trust.
- Verify that gateway `Authorization` forwarding does not conflict with the
  upstream token scheme.
- Document new Native OIDC services in the architecture/operations documents.

### Traceability

- [ADR-0002](0002-keycloak-oauth2-proxy-choice.md)
- [Auth Architecture](../descriptions/0002-auth-architecture.md)
- [Application Auth Integration Policy](../../05.operations/policies/0079-application-auth-integration.md)
- [Application Auth Integration Guide](../../05.operations/guides/0079-application-auth-integration.md)

## Decision

Keycloak stays the central IdP.

Service authentication paths are split into two patterns.

### Gateway ForwardAuth

```text
Browser -> Traefik -> OAuth2 Proxy -> Keycloak -> Service
```

Used for services that have no OIDC of their own, or for which gateway SSO is
suitable.

### Application-native OIDC

```text
Browser -> Traefik -> Application -> Keycloak
```

Used for approved services that provide their own OIDC/RBAC.

Currently approved:

- Apache Airflow
- Kafbat UI

Only `gateway-standard-chain@file` applies to the Airflow and Kafbat UI
routers; OAuth2 Proxy's `sso-auth@file`/`sso-errors@file` is not applied
redundantly.

## Alternatives

### Alternatives

### Options Considered

### ForwardAuth-only

Pros:

- Gateway policy is simple.

Cons:

- Causes double-auth in native OIDC apps.
- Duplicates responsibility between application-level RBAC and gateway auth.
- Actual Bearer/JWT conflicts observed in Airflow.

### Native OIDC-only

Pros:

- Each application's authorization model can be used directly.

Cons:

- Cannot be applied to services without OIDC.
- Increases per-service Keycloak client management cost.

## Consequences

### Positive

- Authentication/authorization ownership becomes clear.
- Keeps Airflow/Kafbat application RBAC.
- Avoids conflicts between OAuth2 Proxy header injection and application JWT.

### Negative

- Auth pattern must be explicitly chosen during service onboarding.
- The number of Keycloak clients increases.

## Related Documents

- [ADR-0002](0002-keycloak-oauth2-proxy-choice.md)
- [AD-0002](../descriptions/0002-auth-architecture.md)
