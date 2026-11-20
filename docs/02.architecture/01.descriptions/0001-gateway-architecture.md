---
title: "Gateway Tier Architecture Description"
version: "2.0.0"
type: "sdlc/architecture-description"
status: "approved"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "architecture"
artifact_id: "AD-0001"
parent_ids:
- "REQ-0001"
created: "2026-03-26"
---

# Gateway Tier Architecture Description

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the architecture-description payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Context and Boundaries

##### System Boundary

- **Owns:** the `web` (80), `websecure` (443) and `metrics` (8082) entrypoints;
  TLS termination with the local certificate; routing to internal services; the
  file-provided middleware (rate limit, security headers, request buffering,
  ForwardAuth wiring). Admin IP allow lists are per-service Docker labels.
- **Consumes:** the Docker socket (read-only) for discovery, the local
  certificate files, OAuth2 Proxy for ForwardAuth, and Tempo for traces.
- **Does not own:** application logic, database connections, or Keycloak
  identity management.
- **Non-goals:** full payload logging and service-mesh control.

###### Purpose and Readers
<!-- core-payload-level:4 -->

The Gateway tier is the single ingress of `hy-home.docker`. Traefik provides
Docker-label service discovery, TLS termination and shared middleware. The
former alternative Nginx leaf was retired on 2026-11-10. Requirement owners,
implementers and operators share this view.

###### Context
<!-- core-payload-level:4 -->

Clients reach the tier over HTTPS from the internet. Traefik discovers services through the read-only Docker socket, calls OAuth2 Proxy for ForwardAuth, and sends traces to Tempo.

##### Constraints

The tier is the only ingress and has no state of its own. Traefik sets no TLS minimum version, so Go defaults apply; changing it is covered under Evolution. Full payload logging and service-mesh control are non-goals.

#### Structure

##### Building Blocks

- `traefik` (`infra/01-gateway/traefik/`) joins `edge_net`, `obs_net` and the
  dedicated ingress networks; its static config is `config/traefik.yml` and its
  file provider loads `dynamic/` (middleware, TLS, file routes).

Traefik is the only gateway leaf. The alternative Nginx leaf (selected only by
the `nginx` profile; `/oauth2/`, `/keycloak/` and SeaweedFS `/cdn/` paths) was
retired on 2026-11-10 by owner decision: no Nginx container existed in HOME and
the seven-day Traefik router metrics showed every live route on Traefik.

##### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| `web` (80) and `websecure` (443) entrypoints | Traefik | Internet clients over HTTPS | `config/traefik.yml` static config and Docker labels with the file-provided middleware under `dynamic/` | A Traefik outage affects every routed UI; the description records no other failure handling for this interface. |
| `metrics` (8082) entrypoint | Traefik | Prometheus | Prometheus metrics with router and service labels | The description records no failure handling for this interface. |
| OTLP traces to `tempo:4317` | Traefik | Tempo | OTLP | The description records no failure handling for this interface. |
| Docker socket (read-only) discovery | The description names no producer for this interface. | Traefik | Docker labels | The Docker provider adds and removes routes as containers change health and state. |
| ForwardAuth call | OAuth2 Proxy | Traefik | File-provided ForwardAuth middleware under `dynamic/` | The description records no failure handling for this interface. |
| Local certificate files | Local certificate mounts | Traefik | TLS configuration loaded by the file provider from `dynamic/` | The description records no failure handling for this interface. |

Traefik exposes the `web` (80), `websecure` (443) and `metrics` (8082) entrypoints. Routes come from Docker labels and the file-provided middleware under `dynamic/`; metrics go to Prometheus and OTLP traces to `tempo:4317`.

#### Runtime Behavior

##### Normal Flow

###### Runtime View
<!-- core-payload-level:4 -->

```text
Internet -> Traefik (TLS termination, middleware) -> service container
```

The gateway forwards or rewrites request metadata (headers, path) and does not
persist request bodies. Configuration and certificates arrive through mounts;
the gateway keeps no state of its own.

###### Deployment View
<!-- core-payload-level:4 -->

The root Compose includes the Traefik leaf unconditionally; a profile decides
whether it starts. `traefik` is selected by `core`, `dev` or `local` and
publishes host ports 80/443. The Traefik image is pinned by digest.

##### Failure and Recovery

A Traefik outage affects every routed UI (see Risks below). The Docker provider adds and removes routes as containers change health and state; the description records no other failure boundary.

#### Quality Scenarios

##### Scenarios

###### Quality Attributes
<!-- core-payload-level:4 -->

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

###### Risks
<!-- core-payload-level:4 -->

- Traefik is the single ingress, so a Traefik outage affects every routed UI.

##### Trade-offs

- Traefik is the single ingress and keeps no state of its own; the accepted cost
  (Risks) is that a Traefik outage affects every routed UI.
- Traefik sets no TLS minimum version, so Go defaults apply (Constraints,
  Quality Attributes); setting one needs a Stage 03 change (Evolution).
- Full payload logging and service-mesh control are non-goals (Constraints).

#### Decisions and Adoption

##### Decisions

- [ADR-0001 Traefik and Nginx hybrid](../02.decisions/0001-traefik-nginx-hybrid.md) (Nginx half retired 2026-11-10)

##### Adoption Boundaries

###### Requirement Mapping
<!-- core-payload-level:4 -->

- [REQ-0001 Gateway requirements](../../01.requirements/0001-gateway.md)

###### Currentness and Lineage
<!-- core-payload-level:4 -->

- [Derived Compose image projection](../../../infra/tech-stack.versions.json)

###### Evolution
<!-- core-payload-level:4 -->

A Traefik TLS minimum version needs a Stage 03 change.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
