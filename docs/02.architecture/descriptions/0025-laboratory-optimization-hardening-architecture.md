---
title: "11-Laboratory Optimization Hardening Architecture Description"
version: "1.1.2"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "AD-0025"
parent_ids:
- "REQ-0012"
created: "2026-03-28"
---
# 11-Laboratory Optimization Hardening Architecture Description

## Context and Stakeholders

This document defines the optimization/hardening reference architecture of
the `11-laboratory` layer. It specifies the architecture contract that places
the management UI behind the gateway security chain, SSO authentication, and
the IP allowlist boundary, and controls experimental service operational
drift with a CI gate.

### Stakeholders and Concerns

Requirement owners, implementers, and operators share the concerns recorded
in this section and the following views. Only concerns confirmed in the
existing document are covered here.

The laboratory tier is a management tool layer for operator productivity,
but a "security boundary first" design is needed because it handles
high-privilege UIs.

- Container/Log Admin UI: dozzle
- Data Admin UI: redisinsight
- Local notebook lab: open-notebook, surrealdb

## System Boundaries

This section preserves the system boundary, consumption relationships,
non-goals, and constraints already recorded in the current document.

- **Owns**:
  - Laboratory UI ingress boundary contract (gateway chain + SSO + allowlist)
  - network boundary contract
  - management UI direct host exposure prohibition contract
  - dozzle least-privilege (socket read-only) contract
  - open-notebook UI route SSO/allowlist/large-body boundary and Docker
    Secret injection contract
  - laboratory hardening CI policy gate
- **Consumes**:
  - `01-gateway` Traefik middleware
  - `02-auth` SSO middleware
  - Docker Engine / Valkey-Redis endpoints
- **Does Not Own**:
  - Keycloak realm detailed policy
  - Traefik global entrypoints
- **Non-goals**:
  - promoting an experimental service to the production workload tier
  - a full replatform of the management tools

## Quality Attributes

### Quality Scenarios

The quality scenarios point to the existing configuration, failure boundary,
and verification expectation to which the attributes below apply. Concrete
execution evidence is owned by the related Spec and Operations documents.

- **Security**: removes direct host exposure, applies the dual
  allowlist+SSO boundary
- **Reliability**: secures minimum runtime stability based on the compose
  contract and healthcheck
- **Operability**: standardizes regression recovery based on the CI
  hardening gate and runbook
- **Scalability**: expands the catalog-based policy (expiration/approval/
  audit) in stages

## Components

### Viewpoints and Views

The context, component, or deployment representation in this section serves
as the view for that concern.

- **Ingress path**:
  - Operator -> Traefik(websecure) -> dozzle/redisinsight/open-notebook
- **Control path**:
  - dozzle -> Docker socket
  - redisinsight -> valkey/redis endpoints
  - open-notebook -> surrealdb

## Data Flow

### Data and Control Flows

The data and control flows include only the interactions specified in this
section and the existing infrastructure/deployment descriptions.

This hardening Architecture Description does not introduce production data ownership for the laboratory tier. Data access remains limited to management metadata, Docker socket visibility, log streams, Valkey/Redis endpoint inspection, and Open Notebook local laboratory state described in the control path.

## Deployment View

- **Runtime / Platform**: Docker Compose (`infra/11-laboratory/*`)
- **Deployment Model**:
  - per-service compose + a common template (`infra/common-optimizations.yml`)
- **Operational Evidence**:
  - compose static checks
  - `scripts/hardening/check-all-hardening.sh 11-laboratory`
  - CI `infrastructure-hardening` job

## Evolution

- **Management UI**: keeping SSO+allowlist, applying an automatic
  expiration policy for experimental services
- **dozzle**: restricting the log viewing scope (rule blocking access to
  production logs), ongoing review of least-privilege
- **redisinsight**: minimizing access permission, prohibiting direct
  production cache changes and strengthening the audit log policy
- **open-notebook**: keeping secret-file credential injection, notebook data
  retention/expiration policy, direct API/DB host-port exposure review
  before production promotion

## Traceability

The disposition of the parent requirement and the related decision/implementation specs are owned by the PRD, ADR, and Spec links in `Related Documents`. This description does not replace the role of those documents.

## Related Documents

- **PRD**: [../01.requirements/0012-laboratory.md](../../01.requirements/0012-laboratory.md)
- **Spec**: [../03.specs/012-laboratory/spec.md](0011-laboratory-architecture.md)
- **ADR**: [../02.architecture/decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md](../decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md)
- **Guide**: [../../05.operations/guides/0074-laboratory-optimization-hardening.md](../../05.operations/guides/0074-laboratory-optimization-hardening.md)
- **Operation**: [../../05.operations/policies/0074-laboratory-optimization-hardening.md](../../05.operations/policies/0074-laboratory-optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/0074-laboratory-optimization-hardening.md](../../05.operations/runbooks/0074-laboratory-optimization-hardening.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.
