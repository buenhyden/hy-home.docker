---
title: "Gateway Tier (01-gateway) Product Requirements"
version: "1.1.2"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "requirements"
artifact_id: "REQ-0001"
parent_ids: []
created: "2026-03-26"
---
# Gateway Tier (01-gateway) Product Requirements

## Problem and Goals

This document defines the product requirements for the `01-gateway` tier, the unified entry point of the `hy-home.docker` ecosystem. The current implementation consists of the Traefik edge router selected by the `core`/`dev` profiles and the Nginx special-path proxy leaf selected by the dedicated `nginx` profile, orchestrating traffic routing, TLS termination, and the security middleware chain (SSO, rate limit, and so on).

### Problem Statement

- With multiple microservices distributed across the platform, managing individual security settings (TLS, auth) for each service is difficult.
- Without automated service discovery, operational complexity increases.
- Centralized control and visibility (logging/metrics) over externally exposed paths are lacking.

## Stakeholders and User Needs

Provide a unified, secure, and observable entry point for all external traffic to strengthen system security and simplify service exposure.

### Personas

- **Infrastructure Engineer**: Designs the overall traffic flow of the system and manages TLS and network security.
- **Backend Developer**: Wants to expose their own service externally, easily and safely.
- **Security Auditor**: Monitors compliance with authentication and authorization policy for all inbound traffic.

### Key Use Cases

- **STORY-01**: When a user accesses a service through a browser, the connection must be automatically upgraded to HTTPS with a valid certificate.
- **STORY-02**: An administrator must be able to view current routing rules and service status in real time through the Traefik dashboard.
- **STORY-03**: For specific paths (for example, `/keycloak/`, `/cdn/`), the Nginx leaf must support fine-grained path rewriting and header manipulation, and the Nginx runtime must be handled only in an explicit root network/dependency context.

## Functional Requirements

- **REQ-0001-FR-0001**: HTTP(80) traffic must be forcibly redirected to HTTPS(443).
- **REQ-0001-FR-0002**: The system must detect container creation via the Docker Provider and automatically generate routes.
- **REQ-0001-FR-0003**: The system must support TLS 1.2/1.3 and modern cipher suites to guarantee communication security.
- **REQ-0001-FR-0004**: The system must integrate with OAuth2 Proxy to provide authentication (SSO) middleware for specific paths.

## Non-functional Requirements

No separately numbered non-functional requirement was identified in the source package.

## Interface Requirements

No separately numbered solution-independent external interface requirement was identified in the source package.

## Acceptance Criteria

- **REQ-0001-FR-0001**: All externally exposed services must be accessed via TLS 100% of the time.
- **REQ-0001-FR-0002**: When a new container is deployed, routing must become active within 60 seconds without any separate configuration file edits.

## Constraints

- **In Scope**:
  - Root-active dynamic routing based on Traefik (Edge Router).
  - Nginx-based special-path proxying and header manipulation selected by the `nginx` profile.
  - TLS termination and certificate management.
- **Out of Scope**:
  - Business logic internal to individual services.
  - Long-term log storage (owned by the Observability tier).
- **Non-goals**:
  - Implementing a dedicated authentication server (owned by the Auth tier).

### AI Agent Requirements

- **Allowed Actions**: Analyze routing rules, execute health checks, read non-sensitive configuration files.
- **Disallowed Actions**: Accessing or exfiltrating private keys/certificates, modifying global security policies without human approval.
- **Human-in-the-loop Requirement**: Critical security policy changes and certificate renewals.
- **Evaluation Expectation**: 100% routing accuracy for new services within 60 seconds.

## Risks

- **Dependency**: Docker Socket access is required for container discovery.
- **Assumption**: The required certificates and files are prepared in advance via `scripts/operations/gen-secrets.sh`.

## Traceability

- **Architecture Description**: [Gateway architecture descriptions](../02.architecture/descriptions/0001-gateway-architecture.md)
- **Spec**: [Gateway technical specification](../02.architecture/descriptions/0001-gateway-architecture.md)
- **Plan**: Gateway standardization plan
- **ADR**: [Traefik and Nginx hybrid decision](../02.architecture/decisions/0001-traefik-nginx-hybrid.md)
