---
title: "Laboratory Tier (11-laboratory) Product Requirements"
version: "1.1.1"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "requirements"
artifact_id: "REQ-0012"
parent_ids: []
created: "2026-03-26"
---
# Laboratory Tier (11-laboratory) Product Requirements

## Problem and Goals

This document defines the product requirements for the `11-laboratory` tier. It sets out the unified dashboard and admin UI requirements so system administrators, developers, and AI agents can check and manage the access points and state of distributed infrastructure services in one place.

### Problem Statement

When infrastructure service access points, container state, data store debugging tools, and local notebook-style experiment tools are scattered, operators waste time on status checks and incident response. `11-laboratory` must make admin/experiment surfaces such as RedisInsight, Dozzle, and Open Notebook explorable in one place while protecting them with SSO.

## Stakeholders and User Needs

The `11-laboratory` tier provides a unified control center and an isolated experimentation environment for system administrators and developers. It visualizes distributed infrastructure services and builds an intuitive management interface for container and data resources to maximize operational efficiency.

### Personas

- **System Administrator**: monitors overall container state and controls running services.
- **Backend Developer**: visually inspects and debugs data in data stores such as Redis.
- **AI Agent**: understands infrastructure configuration and checks service access points.

### Key Use Cases

- **Checking container logs**: checks approved container logs through Dozzle.
- **Data visualization**: analyzes key distribution and performance of the Redis cluster through RedisInsight.
- **Notebook-style experimentation**: performs local knowledge work and SurrealDB-backed experiments through Open Notebook.

## Functional Requirements

- **REQ-0012-FR-0001**: Every active infrastructure service must be exposed on the dashboard, either automatically or through manual configuration.
- **REQ-0012-FR-0002**: Every admin tool UI route must be protected by the Traefik SSO middleware and allowlist boundary so only authenticated users can access it.
- **REQ-0012-FR-0004**: Laboratory services selected by the `admin` profile (Dozzle, RedisInsight, Open Notebook, SurrealDB) must be included in the root compose `admin` profile static validation.

## Non-functional Requirements

No separately numbered non-functional requirement was identified in the source package.

## Interface Requirements

No separately numbered solution-independent external interface requirement was identified in the source package.

## Acceptance Criteria

- **REQ-0012-FR-0001**: root `admin` profile validation renders active Laboratory services without failure.
- **REQ-0012-FR-0002**: The UI routes of RedisInsight, Dozzle, and Open Notebook are protected by the Traefik gateway+allowlist+SSO boundary.

## Constraints

- **In Scope**: configuring and integrating RedisInsight, Dozzle, Open Notebook/SurrealDB.
- **Out of Scope**: admin UIs of individual business applications.
- **Non-goals**: hardware-level monitoring (owned by 06-observability).

### AI Agent Requirements

N/A

## Risks

- **Dependency**: `02-auth` (Keycloak) availability for SSO.
- **Risk**: Exposing Docker Socket to Dozzle; mitigated by read-only mount and mandatory SSO.

## Traceability

- **Architecture Description**: [Laboratory architecture descriptions](../02.architecture/descriptions/0011-laboratory-architecture.md)
- **Spec**: [Laboratory technical specification](../02.architecture/descriptions/0011-laboratory-architecture.md)
- **Plan**: Laboratory standardization plan
- **ADR**: [Laboratory services decision](../02.architecture/decisions/0011-laboratory-services.md)
