---
title: "Tooling Tier Architecture Description"
version: "2.1.1"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "AD-0009"
parent_ids:
- "REQ-0010"
created: "2026-03-26"
---
# Tooling Tier Architecture Description

## Context and Stakeholders

This document defines the reference architecture and quality attributes of the `09-tooling` layer. It provides the system boundary, responsibilities, and integration structure with common infrastructure for infrastructure automation, quality analysis, and performance testing tools.

### Stakeholders and Concerns

Requirement owners, implementers, and operators share the concerns recorded in this section and the following views. Only concerns confirmed in the existing document are covered here.

The `09-tooling` layer is an auxiliary layer responsible for the project's "operational efficiency" and "quality assurance." It consists of an IaC engine, an analysis server, test workers, and similar components; services with a public admin UI use the gateway/SSO boundary, and only the services that need it integrate with data tier backends such as PostgreSQL, SeaweedFS, and Valkey.

## System Boundaries

This section preserves the system boundaries, consumption relationships, non-goals, and constraints the current document already records.

- **Owns**:
  - IaC CLI helper (`OpenTofu`) and automation platform (`Terrakube`)
  - Static code analysis engine (`SonarQube`)
  - Distributed load-testing system (`Locust`) and explicit load-testing jobs (`k6`)
  - Private package/image storage (`Registry`)
  - Manual dependency update jobs (`Renovate`)
- **Consumes**:
  - Data persistence services (`04-data` / PostgreSQL, SeaweedFS, Valkey)
  - Common authentication service (`02-auth` / Keycloak)
  - Network resources (declared Compose network)
- **Does Not Own**:
  - Core business application services
  - The global monitoring and logging stack (06-observability)
- **Non-goals**:
  - Traffic routing and external exposure management for live services (owned by the Gateway layer)

## Quality Attributes

### Quality Scenarios

Quality scenarios point to the existing configuration these attributes apply to and the verification expectations tied to the failure boundary. Concrete execution evidence belongs to the related Spec and Operations documents.

- **Scalability**: Locust worker and Terrakube execution capacity are adjusted through approved configuration changes. This does not mean the current fixed Compose services implement or have verified auto-scaling.
- **Security**: Applies a gateway+SSO chain to public admin UIs such as SonarQube/Terrakube.
- **Reliability**: Keeps IaC state/object persistence in the declared backend. SeaweedFS and PostgreSQL on the same host are not independent failure domains, so continuity is not guaranteed during a host failure. Backup and isolated recovery verification need separate operational evidence.
- **Operability**: Provides a unified control environment through a centralized dashboard and API.

## Components

### Viewpoints and Views

This section uses the context, component, or deployment representation as the view for the relevant concern.

The system is divided into "Managed Tools" and "Execution Tools."

1. **Management**: SonarQube, the Terrakube API, and similar services manage central state in an environment where the matching profile is selected. They are not automatically included as HOME always-on targets.
2. **Execution**: Terrakube Worker, Locust Worker, and similar services occupy resources and perform the actual computation when a job occurs.

## Data Flow

### Data and Control Flows

Data and control flows include only the interactions specified in this section and the existing infrastructure/deployment description.

- **Key Entities / Flows**: Source Code → SonarQube Scan → Quality Result / IaC Configuration → OpenTofu or Terrakube Plan → Approved Apply.
- **Storage Strategy**: Terrakube state/object data uses the SeaweedFS S3 backend, and SonarQube/Terrakube metadata uses the management PostgreSQL. Registry and the OpenTofu workspace currently use bind-mount-based local persistence. The Syncthing runtime has been removed and does not own a file-sync path.
- **Data Boundaries**: Each tool uses a separate database or schema to prevent data interference.

## Deployment View

- **Runtime / Platform**: Docker Compose using the current root Compose include and profile contract.
- **Deployment Model**: The root `docker-compose.yml` includes every leaf, and
  a profile selects the service. `tooling` selects only Registry and
  SonarQube; `testing` selects both k6 and Locust master/worker; `iac`
  selects OpenTofu and the Terrakube API/UI/executor together;
  `dependency-update` selects only Renovate. `registry` and `sast` each
  select that single role. `analytics-engineering` selects dbt and its DB
  provisioning job; `contract-testing` selects Pact Broker and its DB
  provisioning job; `api-mock` selects WireMock; `backup` selects Restic and
  the SQLite export job; `policy-check` selects only the Conftest job. These
  tools are not included in HOME.
- **Operational Evidence**: `bash scripts/hardening/check-all-hardening.sh 09-tooling`, service healthcheck, approved root-context runtime evidence.

## Traceability

The disposition of the upstream requirement and the related decision/implementation specs are owned by the PRD, ADR, and Spec links in `Related Documents`. This description does not replace the role of those documents.

## Related Documents

- **PRD**: [010-tooling.md](../../01.requirements/0010-tooling.md)
- [Current convergence Spec](../../98.archive/completed/03.specs/0180-home-dev-convergence/spec.md)
- [OpenTofu operations](../../05.operations/guides/0082-opentofu.md)
- [Terraform migration handoff](../../05.operations/guides/0068-terraform.md)
- **ADR**: [0009-tooling-services.md](../decisions/0009-tooling-services.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies drift verification.
