---
title: "Choice of Keycloak and OAuth2 Proxy for IAM and SSO"
version: "1.0.4"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "architecture"
artifact_id: "ADR-0002"
parent_ids:
- "AD-0002"
created: "2026-03-26"
---
# ADR-0002: Choice of Keycloak and OAuth2 Proxy for IAM and SSO

## Context

### Problem and Drivers

This document covers the technical background for choosing Keycloak and OAuth2 Proxy as the authentication scheme for `hy-home.docker`. It is a choice made for standard OIDC protocol compliance, support for various authentication methods, and implementation of a ForwardAuth architecture that protects existing services without client-side code changes.

We need an authentication system that is:

1. Centrally managed.
2. Protocol-standard (OIDC, SAML).
3. Easily integrable with Traefik.
4. Capable of protecting "dumb" upstream services that don't have built-in auth.

### Decision Scope

Explicit non-goals:

- This ADR does not change runtime behavior.
- This ADR does not rewrite historical decision evidence.
- Implementation details remain in linked specs, plans, and tasks.

## Decision

### Chosen Option

We decided to use:

- **Keycloak**: As the primary Identity/OIDC Provider.
- **OAuth2 Proxy**: As the ForwardAuth middleware provider.

#### Rationale

- **Keycloak** is the industry standard for open-source IAM, offering rich features like SSO, Identity Brokering, and MFA out of the box.
- **OAuth2 Proxy** allows us to enforce authentication at the ingress layer (Traefik) without modifying the source code of internal applications.
- This combination is well-supported, highly configurable, and integrates natively with our Traefik gateway via the ForwardAuth middleware pattern.

### Authority and Effect

Decided by the owner, @buenhyden; status `accepted`. No separate approval record is linked. Effective from 2026-03-26.

## Alternatives

### Considered Options

- **Authelia**: A lightweight alternative. While good, it lacks the advanced identity provider features and wide community support of Keycloak.
- **Casdoor**: Another IAM. Less "enterprise-proven" compared to Keycloak in our assessment.
- **App-level Auth**: Implementing auth in each app. Rejected due to high maintenance and lack of unified security policy.

### Trade-offs

Authelia lacks the advanced identity provider features and wide community support of Keycloak. Casdoor is less enterprise-proven in our assessment. App-level auth was rejected due to high maintenance and lack of unified security policy.

## Consequences

### Impacts

- **Pros**: Robust, standard-based, zero-trust ready, unified UI for users.
- **Cons**: higher resource consumption (Keycloak is Java/Quarkus-based), increased complexity in managing realms and clients.

#### AI Agent Guidance

Agents must use the OIDC discovery endpoint provided by Keycloak (`/realms/hy-home.realm/.well-known/openid-configuration`) to obtain token information.

### Follow-up

No follow-up work is recorded in this decision; implementation details remain in linked specs, plans, and tasks.

## Traceability

### Sources

The confirming evidence for this decision is limited to the Architecture Description, Spec, and Operations documents linked below, and the current repository configuration. It makes no claim about runtime state without separate execution evidence.

- **PRD**: [../../01.requirements/0002-auth.md](../../01.requirements/0002-auth.md)
- **Architecture Description**: [../descriptions/0002-auth-architecture.md](../descriptions/0002-auth-architecture.md)
