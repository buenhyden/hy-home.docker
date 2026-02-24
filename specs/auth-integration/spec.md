---
title: 'Auth Integration (SSO) Implementation Spec'
status: 'Draft'
version: '1.0'
owner: 'Platform/DevOps'
prd_reference: 'N/A'
api_reference: 'N/A'
arch_reference: '../../ARCHITECTURE.md'
tags: ['spec', 'implementation', 'auth', 'infra']
---

# Implementation Specification (Spec)

> **Status**: Draft
> **Related PRD**: N/A
> **Related API Spec**: N/A
> **Related Architecture**: `../../ARCHITECTURE.md`

_Target Directory: `specs/auth-integration/spec.md`_
_Note: This document is the absolute Source of Truth for Coder Agents. NO CODE can be generated without it._

---

## 0. Pre-Implementation Checklist (Governance)

> **Mandatory**: Coder agents MUST verify these checklists before generating code.

### 0.1 Architecture / Tech Stack

| Item               | Check Question                                        | Required | Alignment Notes | Where to document |
| ------------------ | ----------------------------------------------------- | -------- | --------------- | ----------------- |
| Architecture Style | Is the style Monolith/Modular Monolith/Microservices? | Must     | Modular infra services | Section 1 |
| Service Boundaries | Are module boundaries documented (diagram/text)?      | Must     | Traefik, OAuth2-Proxy, Keycloak | Section 1 |
| Domain Model       | Are core domain entities and relationships defined?   | Must     | N/A | Section 3 |
| Backend Stack      | Are language/framework/libs (web, ORM, auth) decided? | Must     | Keycloak + OAuth2-Proxy + Traefik | Section 1 |
| Frontend Stack     | Are framework/state/build tools decided?              | Must     | N/A | Section 1 |

### 0.2 Quality / Testing / Security

| Item            | Check Question                                 | Required | Alignment Notes | Where to document |
| --------------- | ---------------------------------------------- | -------- | --------------- | ----------------- |
| Test Strategy   | Levels (Unit/Integration/E2E/Load) defined?    | Must     | Integration/E2E validation | Section 7 |
| Test Tooling    | Agreed framework/runner and mock strategy?     | Must     | curl + browser-based SSO validation | Section 7 |
| Coverage Policy | Are goals defined as numbers (e.g., 100%)?      | Must     | N/A | Section 7 |
| AuthN/AuthZ     | Is auth approach designed (token/OAuth/RBAC)?  | Must     | OAuth2/OIDC + Keycloak groups | Section 4 |
| Data Protection | Encryption/access policies for sensitive data? | Must     | TLS via Traefik | Section 9 |
| Performance     | Are Core Web Vitals/Latency metrics targeted?  | Must     | N/A | Section 8 |
| Accessibility   | Is WCAG compliance integrated (contrast/ARIA)? | Must     | N/A | Section 8 |

### 0.3 Operations / Deployment / Monitoring

| Item         | Check Question                                           | Required | Alignment Notes | Where to document |
| ------------ | -------------------------------------------------------- | -------- | --------------- | ----------------- |
| Environments | Are tiers (dev/staging/prod) clarified for this feature? | Must     | `OPERATIONS.md` | OPERATIONS.md |
| Logging      | Required structured logs defined (fields, IDs)?          | Must     | OAuth2-Proxy logs only | Section 9 |
| Monitoring   | Metrics and dashboards defined (RED/USE)?                | Must     | N/A | Section 9 |
| Alerts       | Are alert thresholds and routing defined?                | Must     | N/A | Section 9 |
| Backups      | Are backup policies defined for added data?              | Must     | Keycloak DB handled separately | Section 9 |

---

## 1. Technical Overview & Architecture Style

This spec defines the Single Sign-On (SSO) integration for internal services using Traefik, OAuth2-Proxy, and Keycloak. Traefik enforces `ForwardAuth` via middleware, OAuth2-Proxy validates sessions, and Keycloak acts as the IdP.

- **Component Boundary**: `infra/01-gateway/traefik`, `infra/02-auth/keycloak`, `infra/02-auth/oauth2-proxy`.
- **Key Dependencies**: Traefik middleware config, Keycloak realm, OAuth2-Proxy client settings.
- **Tech Stack**: Traefik + OAuth2-Proxy + Keycloak (OIDC).

## 2. Coded Requirements (Traceability)

| ID                | Requirement Description | Priority | Parent PRD REQ |
| ----------------- | ----------------------- | -------- | -------------- |
| **REQ-SPC-001** | Traefik must apply `sso-auth@file` middleware for protected apps | High | N/A |
| **REQ-SPC-002** | OAuth2-Proxy must validate Keycloak sessions and forward identity headers | High | N/A |
| **REQ-SPC-003** | Keycloak realm `hy-home.realm` is the shared IdP realm | High | N/A |
| **REQ-SPC-004** | RBAC mapping relies on Keycloak groups (e.g., `/admins`) | Medium | N/A |

## 3. Data Modeling & Storage Strategy

No new data models. Keycloak stores identity data in its DB as configured in infra.

## 4. Interfaces & Data Structures

### 4.1. Core Interfaces

- **ForwardAuth**: Traefik forwards requests to OAuth2-Proxy (`auth.local.dev`).
- **Identity Headers**: OAuth2-Proxy forwards `X-Forwarded-User` and/or `X-Forwarded-Email`.

### 4.2. AuthN / AuthZ (Required if protected data/actions)

- **Authentication**: OIDC (Keycloak) via OAuth2-Proxy.
- **Authorization**: Keycloak groups mapped to app roles (Grafana uses `contains(groups[*], '/admins')`).
- **Sensitive Endpoints/Actions**: Any protected dashboard or internal admin app.

## 5. Component Breakdown

- **`infra/01-gateway/traefik/docker-compose.yml`**: Traefik routing + middleware usage.
- **`infra/02-auth/oauth2-proxy/docker-compose.yml`**: OAuth2-Proxy client config.
- **`infra/02-auth/keycloak/docker-compose.yml`**: Keycloak IdP realm and endpoints.

## 6. Edge Cases & Error Handling

- **Missing session cookie**: OAuth2-Proxy must redirect to Keycloak login.
- **Invalid group mapping**: App falls back to default (non-admin) permissions.
- **TLS misconfiguration**: Requests must fail closed; no plaintext auth flows.

## 7. Verification Plan (Testing & QA)

- **[VAL-SPC-001] Integration**: Access a protected route without a session -> redirected to Keycloak.
- **[VAL-SPC-002] Integration**: Login via Keycloak -> app receives `X-Forwarded-*` headers.
- **[VAL-SPC-003] RBAC**: User with `/admins` group -> Grafana Admin role applied.

## 8. Non-Functional Requirements (NFR) & Scalability

- **Latency**: Authentication redirect must complete within a reasonable user interaction window (< 2s in local infra).
- **Availability**: Auth stack must survive individual container restarts.

## 9. Operations & Observability

- **Deployment Strategy**: Managed via infra compose stacks; no code changes required.
- **Monitoring & Alerts**: Track OAuth2-Proxy login failures in logs.
- **Logging**: Use OAuth2-Proxy access logs for audit trails.
- **Data Protection**: TLS via Traefik; no plaintext tokens in logs.
- **Sensitive Data Handling**: Do not log full JWTs or secrets.
