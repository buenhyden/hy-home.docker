---
title: "Selective Native OIDC for Applications with Built-in Authentication"
version: "0.3.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "architecture"
artifact_id: "ADR-0038"
parent_ids:
- "AD-0002"
created: "2026-09-18"
---

# ADR-0038: Selective Native OIDC for Applications with Built-in Authentication

## Context

### Problem and Drivers

`ADR-0002` selected Keycloak as the central Identity Provider and OAuth2 Proxy
as the Traefik ForwardAuth provider. This pattern suits services without their
own authentication, but for services with their own OIDC and application-level
RBAC it can cause double-auth, `Authorization` header conflicts, and
responsibility duplication.

Airflow 3.3.1's Keycloak Auth Manager and Kafbat UI v1.5.0 provide the <!-- runtime-version-exception: history — the decision records the versions it evaluated -->
application's own OIDC and authorization features.

#### Rationale

- Keeps Keycloak as the central IAM.
- Uses Airflow's Keycloak Authorization Services as-is.
- Uses Kafbat's native OAuth2/RBAC as-is.
- Prevents conflicts between the `Authorization` the proxy injects and the
  application's own token.
- Keeps ForwardAuth's simplicity for services without their own
  authentication.

#### Sources

- [ADR-0002](0002-keycloak-oauth2-proxy-choice.md)
- [Auth Architecture](../01.descriptions/0002-auth-architecture.md)
- [Application Auth Integration Policy](../../05.operations/02.policies/03.identity-and-access/0079-application-auth-integration.md)
- [Application Auth Integration Guide](../../05.operations/01.guides/03.identity-and-access/0079-application-auth-integration.md)

- [ADR-0002](0002-keycloak-oauth2-proxy-choice.md)
- [AD-0002](../01.descriptions/0002-auth-architecture.md)

### Decision Scope

#### Guardrails

- Do not apply ForwardAuth redundantly to native OIDC services by default.
- Inject OIDC client secrets as Docker Secrets.
- Add the local mkcert CA while preserving system/JDK public root trust.
- Verify that gateway `Authorization` forwarding does not conflict with the
  upstream token scheme.
- Document new Native OIDC services in the architecture/operations documents.

## Options

### Considered Options

#### ForwardAuth-only

Pros:

- Gateway policy is simple.

Cons:

- Causes double-auth in native OIDC apps.
- Duplicates responsibility between application-level RBAC and gateway auth.
- Actual Bearer/JWT conflicts observed in Airflow.

#### Native OIDC-only

Pros:

- Each application's authorization model can be used directly.

Cons:

- Cannot be applied to services without OIDC.
- Increases per-service Keycloak client management cost.

### Trade-offs

| Option | Benefit | Cost and Risk | Reason |
| --- | --- | --- | --- |
| ForwardAuth-only | Gateway policy is simple. | Causes double-auth in native OIDC apps, duplicates responsibility between application-level RBAC and gateway auth, and actual Bearer/JWT conflicts were observed in Airflow. | Not chosen because it causes double-auth in native OIDC apps. |
| Native OIDC-only | Each application's authorization model can be used directly. | Cannot be applied to services without OIDC, and increases per-service Keycloak client management cost. | Not chosen because it cannot be applied to services without OIDC and increases per-service Keycloak client management cost. |
| Keycloak as central IdP with Gateway ForwardAuth plus Application-native OIDC for approved services (Apache Airflow, Kafbat UI) | Authentication/authorization ownership becomes clear, Airflow/Kafbat application RBAC is kept, and OAuth2 Proxy header injection no longer conflicts with application JWT. | The auth pattern must be explicitly chosen during service onboarding, and the number of Keycloak clients increases. | Keeps Keycloak as central IAM, uses Airflow's and Kafbat's native authorization as-is, prevents `Authorization` conflicts, and keeps ForwardAuth's simplicity for services without their own authentication. |

The Pros and Cons of each option above carry its benefits and costs. ForwardAuth-only was not chosen because it causes double-auth in native OIDC apps; Native OIDC-only was not chosen because it cannot be applied to services without OIDC and increases per-service Keycloak client management cost.

## Decision

### Chosen Option

Keycloak stays the central IdP.

Service authentication paths are split into two patterns.

#### Gateway ForwardAuth

```text
Browser -> Traefik -> OAuth2 Proxy -> Keycloak -> Service
```

Used for services that have no OIDC of their own, or for which gateway SSO is
suitable.

#### Application-native OIDC

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

### Authority and Effect

Decided by the owner, @buenhyden; status `accepted`. No separate approval record is linked. Effective from 2026-09-18.

## Consequences

### Impacts

#### Positive

- Authentication/authorization ownership becomes clear.
- Keeps Airflow/Kafbat application RBAC.
- Avoids conflicts between OAuth2 Proxy header injection and application JWT.

#### Negative

- Auth pattern must be explicitly chosen during service onboarding.
- The number of Keycloak clients increases.

### Follow-up

On 2026-11-17 the owner, @buenhyden, directed an in-place amendment of this
record: its sections moved line for line to the core decision form, and the
options table under Trade-offs was derived from the options it records. The
decision text is unchanged.

No separate follow-up work is recorded. The guardrails under Decision Scope apply to each new Native OIDC service.
