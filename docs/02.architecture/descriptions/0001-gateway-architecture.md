---
title: "Gateway Tier Architecture Description"
version: "1.3.0"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "architecture"
artifact_id: "AD-0001"
parent_ids:
- "REQ-0001"
created: "2026-03-26"
---

# Gateway Tier Architecture Description

## Overview

The Gateway tier is the single ingress of `hy-home.docker`. Traefik provides
Docker-label service discovery, TLS termination and shared middleware; Nginx is
an alternative leaf for special-path routing. Requirement owners, implementers
and operators share this view.

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
- `nginx` (`infra/01-gateway/nginx/`) joins `edge_net` and `object_net` and
  serves the `/oauth2/`, `/app/`, `/keycloak/` and SeaweedFS `/cdn/` paths with
  a local proxy cache.

The two leaves are alternative host listeners. Nginx is not chained behind
Traefik in the current Compose.

## Runtime and Deployment

### Runtime View

```text
Internet -> Traefik (TLS termination, middleware) -> service container
Internet -> Nginx (TLS termination, path rewrite) -> Keycloak / SeaweedFS CDN   (nginx profile only)
```

The gateway forwards or rewrites request metadata (headers, path) and does not
persist request bodies. Configuration and certificates arrive through mounts;
the gateway keeps no state of its own.

### Deployment View

The root Compose includes both leaves unconditionally; a profile decides which
starts. `traefik` is selected by `core`, `dev` or `local`; `nginx` only by
`nginx`, which also starts SeaweedFS. Both publish host ports 80/443, so they
must not be selected together. The Traefik image is pinned by digest; Nginx uses
`nginx:alpine`.

## Quality and Risks

### Quality Attributes

- **Security:** HSTS (`stsSeconds: 31536000`), rate limiting and request
  buffering come from `dynamic/middleware.yml`. Traefik sets no TLS minimum
  version, so Go defaults apply; Nginx allows TLS 1.2 and 1.3.
- **Reliability:** the Docker provider adds and removes routes as containers
  change health and state.
- **Scalability:** a new service is routed by Docker labels only.
- **Observability:** Prometheus metrics on `metrics` with router and service
  labels; OTLP traces go directly to `tempo:4317`.
- **Operability:** the Traefik dashboard (`dashboard.${DEFAULT_URL}`) is behind
  `dashboard-auth@file`.

### Risks

- Selecting `nginx` and a Traefik profile together collides on host ports
  80/443.
- `nginx:alpine` is an unpinned floating tag, unlike the digest-pinned Traefik
  image.

### Evolution

A Traefik TLS minimum version or an Nginx retirement needs a Stage 03 change
and, for the hybrid itself, a superseding ADR.

## Related Documents

- [REQ-0001 Gateway requirements](../../01.requirements/0001-gateway.md)
- [ADR-0001 Traefik and Nginx hybrid](../decisions/0001-traefik-nginx-hybrid.md)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
