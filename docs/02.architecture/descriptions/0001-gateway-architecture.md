---
title: "Gateway Tier Architecture Description"
version: "1.4.0"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-11-10"
layer: "architecture"
artifact_id: "AD-0001"
parent_ids:
- "REQ-0001"
created: "2026-03-26"
---

# Gateway Tier Architecture Description

## Overview

The Gateway tier is the single ingress of `hy-home.docker`. Traefik provides
Docker-label service discovery, TLS termination and shared middleware. The
former alternative Nginx leaf was retired on 2026-11-10. Requirement owners,
implementers and operators share this view.

## Scope

- **Owns:** the `web` (80), `websecure` (443) and `metrics` (8082) entrypoints;
  TLS termination with the local certificate; routing to internal services; the
  file-provided middleware (rate limit, security headers, request buffering,
  ForwardAuth wiring). Admin IP allow lists are per-service Docker labels.
- **Consumes:** the Docker socket (read-only) for discovery, the local
  certificate files, OAuth2 Proxy for ForwardAuth, and Tempo for traces.
- **Does not own:** application logic, database connections, or Keycloak
  identity management.
- **Non-goals:** full payload logging and service-mesh control.

## Structure

### Architecture

- `traefik` (`infra/01-gateway/traefik/`) joins `edge_net`, `obs_net` and the
  dedicated ingress networks; its static config is `config/traefik.yml` and its
  file provider loads `dynamic/` (middleware, TLS, file routes).

Traefik is the only gateway leaf. The alternative Nginx leaf (selected only by
the `nginx` profile; `/oauth2/`, `/keycloak/` and SeaweedFS `/cdn/` paths) was
retired on 2026-11-10 by owner decision: no Nginx container existed in HOME and
the seven-day Traefik router metrics showed every live route on Traefik. The
SeaweedFS `cdn-bucket` and its anonymous read identity remain defined and have
no gateway consumer.

## Runtime and Deployment

### Runtime View

```text
Internet -> Traefik (TLS termination, middleware) -> service container
```

The gateway forwards or rewrites request metadata (headers, path) and does not
persist request bodies. Configuration and certificates arrive through mounts;
the gateway keeps no state of its own.

### Deployment View

The root Compose includes the Traefik leaf unconditionally; a profile decides
whether it starts. `traefik` is selected by `core`, `dev` or `local` and
publishes host ports 80/443. The Traefik image is pinned by digest.

## Quality and Risks

### Quality Attributes

- **Security:** HSTS (`stsSeconds: 31536000`), rate limiting and request
  buffering come from `dynamic/middleware.yml`. Traefik sets no TLS minimum
  version, so Go defaults apply.
- **Reliability:** the Docker provider adds and removes routes as containers
  change health and state.
- **Scalability:** a new service is routed by Docker labels only.
- **Observability:** Prometheus metrics on `metrics` with router and service
  labels; OTLP traces go directly to `tempo:4317`.
- **Operability:** the Traefik dashboard (`dashboard.${DEFAULT_URL}`) is behind
  `dashboard-auth@file`.

### Risks

- Traefik is the single ingress, so a Traefik outage affects every routed UI.

### Evolution

A Traefik TLS minimum version needs a Stage 03 change.

## Related Documents

- [REQ-0001 Gateway requirements](../../01.requirements/0001-gateway.md)
- [ADR-0001 Traefik and Nginx hybrid](../decisions/0001-traefik-nginx-hybrid.md) (Nginx half retired 2026-11-10)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
