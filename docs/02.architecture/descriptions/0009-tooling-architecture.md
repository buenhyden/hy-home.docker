---
title: "Platform Operations and Software Verification Architecture Description"
version: "2.6.0"
type: "sdlc/architecture-description"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "architecture"
artifact_id: "AD-0009"
parent_ids:
- "REQ-0010"
created: "2026-03-26"
---

# Platform Operations and Software Verification Architecture Description

## Context and Boundaries

### System Boundary

- **Owns:** OpenTofu (IaC CLI helper) and Terrakube (API, UI, executor);
  Registry (private images); Renovate (manual dependency updates); Restic,
  `restic-offsite` and the SQLite export job (cross-platform backup); k6 (the
  default load tool); Pact Broker, WireMock, Conftest and Mailpit.
- **Consumes:** `04-data` `mng-pg` and SeaweedFS; `02-auth` Keycloak through
  ForwardAuth; `06-observability` for k6 and Registry metrics.
- **Does not own:** business application services, the monitoring stack, or
  live-service routing (Gateway).
- **Not in this tier:** SonarQube (`labs/sonarqube`), Locust (`labs/locust`)
  and dbt (`labs/dbt`) are standalone LABs; dbt belongs to Analytics.

#### Purpose and Readers

This description covers platform operations in `09-platform-ops` and software
verification in `11-quality`: infrastructure automation, backup orchestration,
image storage, dependency updates, load, contract, API-mock and policy tests,
and development mail capture. Public admin UIs sit behind the gateway SSO
boundary, and only services that need it use the data tier.

#### Context

Public admin UIs sit behind the gateway SSO boundary through ForwardAuth. The tier consumes `mng-pg` and SeaweedFS (`04-data`), Keycloak (`02-auth`), and `06-observability` for k6 and Registry metrics.

### Constraints

Only services that need it use the data tier, and each tool uses its own database or schema. Capabilities other than Registry are not activated implicitly, and SonarQube, Locust and dbt remain standalone LABs.

## Structure

### Building Blocks

- **Profile-selected services:** the Terrakube API, UI and executor, Pact
  Broker, Registry, WireMock and Mailpit. WireMock serves requests while its
  profile is active.
- **Job tools:** OpenTofu, Renovate, Restic, k6 and Conftest run for named
  operations.

Directories under `infra/09-platform-ops/` without a Compose file
(`project-registration`, `resource-optimization`, `security-updates`,
`service-integration`) hold no service.

### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| Terrakube API, UI and executor routes | Terrakube | The description names no consumer for this interface. | ForwardAuth chain with Keycloak (`02-auth`) | The description records no failure handling for this interface. |
| Mailpit UI route | Mailpit | The description names no consumer for this interface. | ForwardAuth chain with Keycloak (`02-auth`) | The description records no failure handling for this interface. |
| Registry loopback publication | Registry | The description names no consumer for this interface. | `127.0.0.1:${REGISTRY_PORT:-5000}` with no gateway route | The description records no failure handling for this interface. |
| k6 per-run OTLP | k6 | Authenticated Alloy receiver, then Prometheus (`06-observability`) | OTLP | The description records no failure handling for this interface. |
| Terrakube state S3 backend | SeaweedFS (`04-data`) | Terrakube | The description links no contract for this interface. | A host failure breaks continuity because SeaweedFS and PostgreSQL share one host. |
| `mng-pg` databases | `mng-pg` (`04-data`) | Terrakube metadata and Pact Broker | The description links no contract for this interface. | A host failure breaks continuity because SeaweedFS and PostgreSQL share one host. |

The Terrakube API, UI and executor routes and the Mailpit UI use the ForwardAuth chain; Registry has no gateway route and publishes only on `127.0.0.1:${REGISTRY_PORT:-5000}`. k6 sends per-run OTLP to an authenticated Alloy receiver, and Terrakube state uses the SeaweedFS S3 backend.

## Runtime Behavior

### Normal Flow

#### Runtime View

```text
IaC configuration -> OpenTofu or Terrakube plan -> approved apply
k6 run -> per-run OTLP ingress -> authenticated Alloy receiver -> Prometheus
contract test -> Pact Broker (mng-pg)
```

Terrakube state and objects use the SeaweedFS S3 backend and its metadata
`mng-pg`; Pact Broker provisions its own `mng-pg` database. Registry and the
OpenTofu workspace use local persistence. Each tool uses its own database or
schema.

#### Deployment View

The root `docker-compose.yml` includes every leaf; a profile selects the
service. `tooling` and `registry` select Registry, published only on
`127.0.0.1:${REGISTRY_PORT:-5000}`; `iac` selects OpenTofu and the Terrakube
API, UI and executor; `dependency-update` selects Renovate; `backup` selects
Restic, `restic-offsite` and the SQLite export job; `testing` selects k6;
`contract-testing` selects Pact Broker and its provisioning job; `api-mock`
selects WireMock; `policy-check` selects Conftest; `dev`, `local` and
`mail-dev` select Mailpit. Terrakube, Pact Broker and WireMock are optional root
packages. Their standalone LAB moves are planned in ADR-0062. Registry and
Mailpit remain in root Compose. Membership in the root project does not
indicate which profiles are active.

### Failure and Recovery

SeaweedFS and PostgreSQL on one host are not independent failure domains, so a host failure breaks continuity (see Quality Attributes and Risks below). The description records no failure boundary beyond the linked operations documents.

## Quality Scenarios

### Scenarios

#### Quality Attributes

- **Security:** the Terrakube API, UI and executor routes and the Mailpit UI
  use the ForwardAuth chain. Registry has no gateway route.
- **Reliability:** IaC state stays in the declared backend. SeaweedFS and
  PostgreSQL on one host are not independent failure domains, so a host failure
  breaks continuity; backup and isolated recovery need separate evidence.
- **Scalability:** Terrakube execution capacity changes only through approved
  configuration; no auto-scaling is implemented.

#### Risks

Restic, the only cross-platform backup path, runs only when `backup` is
selected; Compose declares no schedule for it.

### Trade-offs

- SeaweedFS and PostgreSQL run on one host and are not independent failure
  domains, so a host failure breaks continuity; backup and isolated recovery
  need separate evidence (Quality Attributes).
- Restic, the only cross-platform backup path, runs only when `backup` is
  selected and Compose declares no schedule for it (Risks).
- Terrakube execution capacity changes only through approved configuration;
  no auto-scaling is implemented (Quality Attributes).
- Capabilities other than Registry are not activated implicitly, and
  SonarQube, Locust and dbt stay standalone LABs (Constraints).

## Decisions and Adoption

### Decisions

- [ADR-0062 HOME Membership and Planned LABs](../decisions/0062-home-lab-membership.md)

### Adoption Boundaries

#### Requirement Mapping

- [REQ-0010 Tooling requirements](../../01.requirements/0010-tooling.md)

#### Currentness and Lineage

- [OpenTofu operations](../../05.operations/guides/10-platform-and-backup/0082-opentofu.md)
- [Pact Broker operations](../../05.operations/guides/12-testing-and-quality/0093-pact-broker.md)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)

#### Evolution

Promoting SonarQube, Locust or dbt back into a root tier is an owner decision
under the LAB promotion contract.
