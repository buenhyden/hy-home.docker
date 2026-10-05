---
title: "Gateway Tier Architecture Description"
version: "1.2.3"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "AD-0001"
parent_ids:
- "REQ-0001"
created: "2026-03-26"
---
# Gateway Tier Architecture Description

## Overview

### Overview

## Scope

### Scope

### Context and Stakeholders

This document defines the architecture of the Gateway tier, the unified entry point for the `hy-home.docker` system. It describes a structure that achieves dynamic service discovery and fine-grained path routing at the same time through a hybrid Traefik and Nginx configuration.

### Stakeholders and Concerns

Requirement owners, implementers, and operators share the concerns recorded in this section and the following views. Only concerns confirmed in the existing document are covered here.

The Gateway tier acts as the primary passage between the external network and the internal service network. The root compose includes both leaves unconditionally, and a profile decides which starts. `traefik` belongs to `core` and `dev`, and `nginx` belongs only to the dedicated `nginx` profile, so neither starts without a profile. Nginx remains as an auxiliary proxy leaf for specific legacy compatibility and special-path handling.

### System Boundaries

This section preserves the system boundaries, consumption relationships, non-goals, and constraints the current document already records.

- **Owns**:
  - Receiving external ingress traffic (`web` 80, `websecure` 443) and the metrics/ping entrypoint (`metrics` 8082).
  - Applying and terminating TLS/SSL certificates.
  - Routing and load-balancing traffic to internal services.
  - Security middleware (rate limit, IP allow list, auth integration).
- **Consumes**:
  - Docker Socket (Service Discovery).
  - Local Certificates (SSL/TLS).
  - OAuth2 Proxy (Authentication request).
- **Does Not Own**:
  - Internal business logic of individual microservices.
  - Direct database connections and management.
  - Identity Provide (internal Keycloak management).
- **Non-goals**:
  - Detailed payload logging for all traffic (handled as sampling in the observability tier).
  - Service Mesh-level complex dynamic control (currently focused on simple Ingress).

### Traceability

The disposition of the upstream requirement and the related decision/implementation specs are owned by the PRD, ADR, and Spec links in `Related Documents`. This description does not replace the role of those documents.

## Architecture

### Architecture

### Components

### Viewpoints and Views

This section uses the context, component, or deployment representation as the view for the relevant concern.

Gateway leaves join `edge_net`, but they are alternative host listeners. Normal
HOME traffic enters Traefik. The `nginx` profile instead selects Nginx for its
special-path routes; Nginx is not chained behind Traefik in the current Compose.

### Data Flow

### Data and Control Flows

Data and control flows include only the interactions specified in this section and the existing infrastructure/deployment description.

- **Key Entities / Flows**:
  - `Internet -> Traefik (TLS Term) -> Service Container`
  - `Internet -> Nginx (TLS Term + Path Rewrite) -> Keycloak/SeaweedFS CDN` when the
    alternative `nginx` profile is selected
- **Storage Strategy**: Targets a stateless architecture; configuration files and certificates are supplied through volume mounts.
- **Data Boundaries**: The gateway only modifies or forwards request metadata (header, path); it does not persist the request body.

### Deployment View

- **Runtime / Platform**: Docker Compose / Linux Alpine-based container.
- **Deployment Model**: the root compose includes both leaves. `traefik` is selected
  by `core`, `dev`, or `local`; `nginx` is selected only by `nginx`. Both publish
  host ports 80/443, so they must not be selected together. Nginx also requires
  the root network and healthy SeaweedFS S3 dependency context.
- **Operational Evidence**: root `core` profile compose validation, `check-all-hardening.sh 01-gateway`, Traefik Dashboard (`dashboard.DEFAULT_URL`) and sanitized runtime logs when the approved stack is running.

## Quality Attributes

### Quality Scenarios

Quality scenarios point to the existing configuration these attributes apply to and the verification expectations tied to the failure boundary. Concrete execution evidence belongs to the related Spec and Operations documents.

- **Performance**: Guarantees low latency through Traefik's Go-based asynchronous processing. Optimizes static assets using Nginx's caching capability.
- **Security**: Prioritizes TLS 1.3, enforces HSTS, limits request size, integrates authentication (SSO).
- **Reliability**: Automatically excludes unhealthy targets through Health Check. Self-healing routing based on the Docker Provider.
- **Scalability**: Adds new service horizontal scaling and routing using only Docker labels.
- **Observability**: Exposes Prometheus metrics, integrates distributed tracing through OpenTelemetry (Tempo).
- **Operability**: Secures real-time routing visibility through the Traefik Dashboard. Supports file-based dynamic configuration.

## Related Documents

- **PRD**: [../../01.requirements/0001-gateway.md](../../01.requirements/0001-gateway.md)
- **Spec**: [../../03.specs/001-gateway/spec.md](0001-gateway-architecture.md)
- **ADR**: [../decisions/0001-traefik-nginx-hybrid.md](../decisions/0001-traefik-nginx-hybrid.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies drift verification.
