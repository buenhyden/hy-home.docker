---
title: "Traefik & Nginx Hybrid Gateway Architecture"
version: "1.2.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "architecture"
artifact_id: "ADR-0001"
parent_ids:
- "AD-0001"
created: "2026-03-26"
---
# ADR-0001: Traefik & Nginx Hybrid Gateway Architecture

## Context

### Problem and Drivers

This document is the architecture decision record for the decision to use a hybrid of Traefik and Nginx as the ingress for `hy-home.docker`.

- The system has many microservices whose count changes dynamically on a Docker container basis.
- At the same time, infrastructure services such as Keycloak and MinIO exist that need specific path rewrites and complex header manipulation.
- Traefik is very strong at Docker Label based automatic service discovery (Dynamic Discovery), but configuring fine-grained, Nginx-level path control can be somewhat cumbersome.
- Nginx, on the other hand, supports elaborate configuration, but upstream management in a dynamically changing Docker virtual IP environment is manual or needs a separate solution.

### Decision Scope

Explicit non-goals:

- Placing Nginx in front of every internal service (avoids unnecessary hop growth).
- Exposing Nginx directly as the external edge.

## Decision

### Chosen Option

- **Primary Edge Router**: use Traefik v3.
  - Handles the initial receipt of all external traffic (80, 443) and TLS termination.
  - Handles automatic routing for most services through the Docker Provider.
- **Secondary Path Proxy**: keep the Nginx Alpine leaf.
  - It is not included by default in the current root compose; it is registered as a Traefik backend service only under an explicit profile/runtime context.

    At the time this sentence was written, the Nginx leaf was outside the root
    include. After SPEC-0156 and SPEC-0171, the root `docker-compose.yml`
    unconditionally includes all 41 compose files and a profile decides
    startup. Nginx is included, and a dedicated `nginx` profile selects the
    service. Traefik is the same in that it also does not start without a
    profile (`core`, `dev`). The boundary the decision set — Nginx only for
    specialized paths, by explicit selection — remains valid, and only the
    mechanism for drawing that boundary changed from include status to
    profile. The decision sentence is preserved as a record of its time.
    Recorded by SPEC-0176.
  - Nginx handles detailed proxy pass, header manipulation, and buffering configuration internally.

    Amended 2026-11-10: the owner retired the Nginx leaf
    (`infra/01-gateway/nginx/`) and its `nginx` profile. It was an alternative
    gateway selected only by that profile, no Nginx container existed in HOME,
    and the seven-day Traefik router metrics showed every live route on
    Traefik. Traefik is now the only gateway; the Secondary Path Proxy
    decision above is preserved as a record of its time and no longer applies.
- **Service Flow**: default root flow is `Client -> Traefik (Edge) -> Backend Service`; specialized flow is `Client -> Traefik (Edge) -> Nginx (Specialized) -> Backend Service` only when the Nginx leaf is explicitly deployed.

### Authority and Effect

Decided by the owner, @buenhyden; status `accepted`. No separate approval record is linked. Effective from 2026-03-26. The 2026-11-10 amendment above is recorded as an owner decision in the text.

## Alternatives

### Considered Options

#### Alternative 1: Traefik Only

- Good: The architecture becomes simpler and there are fewer management points.
- Bad: Implementing Keycloak's redirect loop issue or MinIO's special header handling with Traefik middleware alone is relatively complex, with few proven cases.

#### Alternative 2: Nginx Only (with Nginx Proxy Manager, etc.)

- Good: Configuration is very powerful and familiar.
- Bad: With plain Nginx, detecting dynamic changes in Docker containers needs an extra tool such as `jwilder/nginx-proxy`, or manual management.

### Trade-offs

Traefik only was not chosen because Keycloak and MinIO path and header handling is relatively complex with Traefik middleware alone. Nginx only was not chosen because detecting dynamic Docker container changes needs an extra tool or manual management.

## Consequences

### Impacts

- **Positive**:
  - Adding a new service can be routed with only Docker Labels, no extra configuration (Traefik's strength).
  - A stable Nginx configuration can be applied to services with tricky proxy needs, such as Keycloak.
  - Visibility is secured through an integrated dashboard.
- **Trade-offs**:
  - One extra network hop is added for certain services (Traefik -> Nginx).
  - Operational burden of managing two different proxy configuration syntaxes.

### Follow-up

No follow-up work is recorded in this decision.

## Traceability

### Sources

The confirming evidence for this decision is limited to the Architecture Description, Spec, and Operations documents linked below, and the current repository configuration. It makes no claim about runtime state without separate execution evidence.

- **PRD**: [../../01.requirements/0001-gateway.md](../../01.requirements/0001-gateway.md)
- **Architecture Description**: [../descriptions/0001-gateway-architecture.md](../descriptions/0001-gateway-architecture.md)
