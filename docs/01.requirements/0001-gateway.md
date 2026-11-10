---
title: "Gateway Tier (01-gateway) Requirements"
version: "1.3.2"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-10"
layer: "requirements"
artifact_id: "REQ-0001"
created: "2026-03-26"
---

# Gateway Tier (01-gateway) Requirements

## Overview

The `01-gateway` tier is the single entry point for external traffic into
`hy-home.docker`. It must terminate TLS, route requests to services that opt in
to exposure, and apply a shared access-control and traffic-protection chain, so
that no service has to manage its own TLS or authentication front door.

Without it, each service carries its own TLS and authentication settings,
exposure needs manual configuration, and there is no central view of what is
reachable from outside.

## Scope

- **In scope**: the edge router for all external HTTP and HTTPS traffic, TLS
  termination, automatic route discovery for opted-in services, the shared
  middleware chain.
- **Out of scope**: business logic inside services, long-term log storage
  (Observability tier) and the authentication server itself (Auth tier).

### Assumptions

- The operator provides the TLS certificate and key before the gateway starts;
  the gateway does not issue certificates.
- A service is exposed only when it declares its own route; nothing is exposed
  by default.

### Risks

- Route discovery needs read access to the container runtime, which is a
  privileged interface.
- The gateway is a single point of entry: when it is down, every external route
  is down.

## Requirements

### Functional Requirements

- **REQ-0001-FR-0001**: Plain HTTP requests must be permanently redirected to
  HTTPS.
- **REQ-0001-FR-0002**: The gateway must discover a service that declares a
  route and activate that route without a manual gateway configuration edit;
  a service that declares no route must stay unexposed.
- **REQ-0001-FR-0003**: The gateway must terminate external TLS with the
  operator-provided certificate and must not accept a protocol version below
  TLS 1.2.
- **REQ-0001-FR-0004**: The gateway must offer a reusable single sign-on
  access-control step, backed by the Auth tier, that a route can require.

### Stakeholders and User Needs

- **Infrastructure engineer**: controls traffic flow, TLS and the shared
  security chain in one place.
- **Service developer**: exposes a service safely by declaring a route,
  without building TLS or login handling.
- **Security auditor**: checks which routes require which access control.
- **Administrator**: views current routes and their status through an
  authenticated gateway dashboard.

### Non-functional Requirements

No separately numbered non-functional requirement is defined.

### Interface Requirements

No separately numbered solution-independent external interface requirement is
defined.

## Acceptance Criteria

- **REQ-0001-FR-0001**: An HTTP request to any external host receives a
  permanent redirect to the HTTPS URL; every external route is served over TLS.
- **REQ-0001-FR-0002**: A newly started service that declares a route is
  reachable within 60 seconds without editing gateway configuration, and a
  service without a declared route is not reachable.
- **REQ-0001-FR-0003**: A TLS 1.0 or 1.1 handshake is refused, and a TLS 1.2 or
  1.3 handshake presents the operator-provided certificate.
- **REQ-0001-FR-0004**: A route that requires single sign-on sends an
  unauthenticated browser to the sign-in flow and admits the request only after
  a valid session.

## Related Documents

- [Gateway architecture description](../02.architecture/descriptions/0001-gateway-architecture.md)
- [ADR-0001: Traefik and Nginx hybrid gateway](../02.architecture/decisions/0001-traefik-nginx-hybrid.md)
- [Traefik policy](../05.operations/policies/02-gateway-and-networking/0013-traefik.md)
- Retired domain Spec SPEC-0001 (gateway): replaced by the gateway guides,
  policies and runbooks under `docs/05.operations/`.
