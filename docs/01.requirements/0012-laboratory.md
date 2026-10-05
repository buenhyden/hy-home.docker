---
title: "Administration and Experimentation Product Requirements"
version: "1.1.2"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "requirements"
artifact_id: "REQ-0012"
created: "2026-03-26"
---
# Administration and Experimentation Product Requirements

## Overview

### Overview

### Problem and Goals

This document preserves the former Laboratory obligations across capability tiers: RedisInsight in `04-data`, Dozzle in `06-observability`, Open Notebook/SurrealDB and MLflow in `08-ai`, and JupyterLab in `12-analytics`. The retired directory does not retire these requirements. It sets out the unified dashboard and admin UI requirements so system administrators, developers, and AI agents can check and manage the access points and state of distributed infrastructure services in one place.

### Problem Statement

When infrastructure service access points, container state, data store debugging tools, and local notebook-style experiment tools are scattered, operators waste time on status checks and incident response. Shared Operations navigation must make RedisInsight, Dozzle and Open Notebook discoverable while preserving each service's approved authentication and gateway boundary.

## Requirements

### Requirements

### Functional Requirements

- **REQ-0012-FR-0001**: Every active infrastructure service must be exposed on the dashboard, either automatically or through manual configuration.
- **REQ-0012-FR-0002**: Every admin tool UI route must preserve its approved gateway, authentication and allowlist boundary. RedisInsight uses ForwardAuth; Dozzle uses native OIDC with the gateway CIDR control; Open Notebook uses its password-file authentication with the gateway CIDR control. These existing service-specific exceptions are recorded in POL-0073 and the corresponding source, not introduced by relocation. MLflow and JupyterLab browser routes use ForwardAuth; direct network/API paths require separate access evidence.
- **REQ-0012-FR-0004**: Root Compose validation must cover `admin` (Dozzle and RedisInsight), `notebook` (Open Notebook and SurrealDB), `surrealdb`, `mlops` (MLflow and its provisioner), and `data-science` (MLflow, its provisioner and JupyterLab), preserving existing selections.

### Non-functional Requirements

No separately numbered non-functional requirement was identified in the source package.

### Interface Requirements

No separately numbered solution-independent external interface requirement was identified in the source package.

## Acceptance Criteria

- **REQ-0012-FR-0001**: root validation renders the administration and experimentation profile selections without failure; this is not evidence of a running dashboard or live access.
- **REQ-0012-FR-0002**: RedisInsight, Dozzle and Open Notebook retain their declared gateway and service-specific authentication/CIDR controls. Validate direct network access separately; a gateway check does not prove that peer-network access is denied.

## Scope

### Scope

### Stakeholders and User Needs

These capabilities provide shared operational navigation and explicitly selected experimentation surfaces; directory placement does not establish isolation for system administrators and developers. It visualizes distributed infrastructure services and builds an intuitive management interface for container and data resources to maximize operational efficiency.

### Personas

- **System Administrator**: monitors overall container state and controls running services.
- **Backend Developer**: visually inspects and debugs data in data stores such as Redis.
- **AI Agent**: understands infrastructure configuration and checks service access points.

### Key Use Cases

- **Checking container logs**: checks approved container logs through Dozzle.
- **Data visualization**: analyzes key distribution and performance of the Redis cluster through RedisInsight.
- **Notebook-style experimentation**: performs local knowledge work and SurrealDB-backed experiments through Open Notebook.

### Constraints

- **In Scope**: configuring and integrating RedisInsight, Dozzle, Open Notebook/SurrealDB, MLflow and JupyterLab.
- **Out of Scope**: admin UIs of individual business applications.
- **Non-goals**: hardware-level monitoring (owned by 06-observability).

### AI Agent Requirements

N/A

### Risks

- **Dependency**: `02-auth` (Keycloak) availability for SSO.
- **Risk**: Exposing Docker Socket to Dozzle; bounded by the read-only mount and native OIDC; a read-only socket mount does not restrict Docker API reads.

## Related Documents

### Traceability

- **Architecture Description**: [Laboratory architecture descriptions](../02.architecture/descriptions/0011-laboratory-architecture.md)
- **Spec**: [Laboratory technical specification](../02.architecture/descriptions/0011-laboratory-architecture.md)
- **Plan**: Laboratory standardization plan
- **ADR**: [Laboratory services decision](../02.architecture/decisions/0011-laboratory-services.md)
