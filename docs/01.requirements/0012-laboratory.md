---
title: "Administration and Experimentation Requirements"
version: "1.6.0"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "requirements"
artifact_id: "REQ-0012"
created: "2026-03-26"
---

# Administration and Experimentation Requirements

## Overview

### Problem and Outcome

When service access points, container state, data store debugging tools and
notebook-style experiment tools are scattered, operators waste time on status
checks and incident response. This package keeps the former Laboratory
obligations across capability tiers: RedisInsight (data), Dozzle
(observability), Open Notebook with SurrealDB and MLflow (AI), and JupyterLab
as an isolated LAB. It states how administrators, developers and AI agents find
and safely use these tools, and how an isolated LAB is kept apart from HOME
until the owner promotes it. The retired Laboratory directory does not retire
these requirements.

### Stakeholders

- **System administrator**: monitors container state and logs (Dozzle).
- **Backend developer**: inspects and debugs Redis data (RedisInsight).
- **AI agent**: finds service access points and configuration.
- **Researcher**: runs notebook-style work and experiments (Open Notebook,
  JupyterLab) and tracks models (MLflow).

The owner, @buenhyden, writes, reviews and accepts this package.

## Scope

### In Scope

- RedisInsight, Dozzle, Open Notebook with SurrealDB, MLflow and
  JupyterLab; the isolation and promotion readiness of every LAB.

### Constraints and Exclusions

- **Out of scope**: admin UIs of individual business applications.
- **Non-goals**: hardware-level monitoring, owned by the observability tier;
  one aggregated dashboard, which is not provided.

**Assumptions.**

- The shared SSO (Keycloak) is available for SSO-protected routes.
- No LAB is promoted now; each promotion is a separate, owner-approved change.

**Risks.**

- Dozzle reads the Docker socket. A read-only mount does not restrict Docker
  API reads, so native OIDC and the gateway allowlist are its boundary.
- These tools see Docker, Redis/Valkey, provider APIs and notebook content, so
  a weak boundary exposes the whole host.

## Requirements

| Requirement ID | Statement | Rationale | Acceptance | Priority |
| --- | --- | --- | --- | --- |
| REQ-0012-FR-0001 | Every administration and experimentation tool has one documented access point that an operator or agent can find from the shared operations navigation. | Scattered access points waste operators' time on status checks and incident response; an AI agent finds service access points and configuration. | Each tool in scope has a guide in the operations catalog that names its access point. | must |
| REQ-0012-FR-0002 | Every admin tool route keeps its approved gateway, authentication and allowlist boundary (RedisInsight SSO and allowlist, Dozzle native OIDC and allowlist, Open Notebook password and allowlist, MLflow SSO); JupyterLab has no gateway route, is reachable only on the LAB host address (loopback by default) and always requires its server token. | These tools see Docker, Redis/Valkey, provider APIs and notebook content, so a weak boundary exposes the whole host. | RedisInsight, Dozzle, Open Notebook and MLflow keep their declared gateway and authentication controls, and JupyterLab refuses to start with a missing or short token; a gateway check does not prove that peer-network access is denied. | must |
| REQ-0012-FR-0004 | Root composition validation covers the selections `admin`, `notebook`, `surrealdb`, `mlops` and `data-science`; JupyterLab is outside root validation, renders on its own and selects no root service. | This package records no rationale for this requirement. | Root validation renders each listed selection without failure, and the JupyterLab LAB renders alone; this is not evidence of a running service. | must |
| REQ-0012-FR-0005 | These optional capabilities stay outside the always-on HOME set and their absence must not affect core traffic; each LAB keeps its own project, network, endpoint inputs, data root and secret copies, declares its promotion path, and is promoted only with owner approval and a passing fail-closed readiness report. | The package states how an isolated LAB is kept apart from HOME until the owner promotes it; each promotion is a separate, owner-approved change. | Every LAB passes the LAB isolation check, and no LAB is promoted without an owner-approved readiness report whose criteria all pass. | must |

### Functional Requirements

- **REQ-0012-FR-0001**: Every administration and experimentation tool must have
  one documented access point that an operator or agent can find from the
  shared operations navigation.
- **REQ-0012-FR-0002**: Every admin tool route must keep its approved gateway,
  authentication and allowlist boundary: RedisInsight uses SSO with a gateway
  allowlist; Dozzle uses native OIDC with a gateway allowlist; Open Notebook
  uses its own password with a gateway allowlist; the MLflow browser route uses
  SSO. Direct network and API paths need separate access evidence. JupyterLab,
  as a LAB, has no gateway route; it is reachable only on the LAB host address (loopback by default)
  and always requires its server token.
- **REQ-0012-FR-0004**: Root composition validation must cover the selections
  `admin` (Dozzle and RedisInsight), `notebook` (Open Notebook and SurrealDB),
  `surrealdb`, and `mlops` and `data-science` (each MLflow and its database
  provisioner). JupyterLab is outside root validation; it renders on its own
  and selects no root service.
- **REQ-0012-FR-0005**: These capabilities are optional and outside the
  always-on HOME set; their absence must not affect core traffic. Each LAB keeps
  its own project, network, endpoint inputs, data root and secret copies, and
  declares where and how it would be promoted. A LAB is promoted only when the
  owner approves it and a fail-closed readiness report passes, judged on
  declared resource reservations; an unmeasured value is not a pass.

### Quality Requirements

This package declares no quality requirement.

## Traceability

### Sources

This package records the owner's requirements for the laboratory tier; no upstream
document governs it.

### Verification Links

#### Acceptance Conditions

- **REQ-0012-FR-0001**: Each tool in scope has a guide in the operations catalog
  that names its access point.
- **REQ-0012-FR-0002**: RedisInsight, Dozzle, Open Notebook and MLflow keep their
  declared gateway and authentication controls, and JupyterLab refuses to start
  with a missing or short token. A gateway check does not prove that
  peer-network access is denied.
- **REQ-0012-FR-0004**: Root validation renders each listed selection without
  failure, and the JupyterLab LAB renders alone; this is not evidence of a
  running service.
- **REQ-0012-FR-0005**: Every LAB passes the LAB isolation check, and no LAB is
  promoted without an owner-approved readiness report whose criteria all pass.

#### Verification Method

Review the catalog guides, the named root selections and the standalone LAB
isolation checks. Use SPEC-0262 Task evidence for the migration or rendering
results it records. Verify each running access control in an authorized
observation of the named target. Record a promotion's reservation-based
readiness result and owner approval in its applicable Task under the
SPEC-0263 contract. @buenhyden judges the conditions and accepts the
requirement once they are met.

#### Downstream Links

- **Architecture Description**: [Laboratory architecture](../02.architecture/descriptions/0011-laboratory-architecture.md)
- **Spec**: [SPEC-0262 LAB migration](../03.specs/0262-analytics-labs-migration/spec.md)
  and [SPEC-0263 LAB promotion contract](../03.specs/0263-lab-promotion-contract/spec.md)
- **Policy**: [LAB promotion](../05.operations/policies/15-labs/0107-lab-promotion.md)
- **Retired ADR-0011** (laboratory services): deleted on 2026-11-04; its
  surviving tool selection is summarized in AD-0011 Traceability.
- **Retired domain Spec SPEC-0012** (laboratory): replaced by the laboratory
  guides, policies and runbooks in the operations catalog under
  `docs/05.operations/`.
- **Retired requirement REQ-0022** (laboratory optimization hardening): retired
  under SPEC-0169 because every clause named an implementation artifact; its
  contract lives in the laboratory operations policy, and its documentation
  traceability clause moved to REQ-0026-FR-0011.
