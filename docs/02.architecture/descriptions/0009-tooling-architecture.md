---
title: "Platform Operations and Software Verification Architecture Description"
version: "2.5.0"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "architecture"
artifact_id: "AD-0009"
parent_ids:
- "REQ-0010"
created: "2026-03-26"
---

# Platform Operations and Software Verification Architecture Description

## Overview

This description covers platform operations in `09-platform-ops` and software
verification in `11-quality`: infrastructure automation, backup orchestration,
image storage, dependency updates, load, contract, API-mock and policy tests,
and development mail capture. Public admin UIs sit behind the gateway SSO
boundary, and only services that need it use the data tier.

## Scope

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

## Structure

### Architecture

- **Management services** keep central state while their profile is selected:
  the Terrakube API and UI, Pact Broker and Registry.
- **Execution services** run per job: the Terrakube executor, OpenTofu,
  Renovate, Restic, k6, Conftest and WireMock.

Directories under `infra/09-platform-ops/` without a Compose file
(`project-registration`, `resource-optimization`, `security-updates`,
`service-integration`) hold no service.

## Runtime and Deployment

### Runtime View

```text
IaC configuration -> OpenTofu or Terrakube plan -> approved apply
k6 run -> per-run OTLP ingress -> authenticated Alloy receiver -> Prometheus
contract test -> Pact Broker (mng-pg)
```

Terrakube state and objects use the SeaweedFS S3 backend and its metadata
`mng-pg`; Pact Broker provisions its own `mng-pg` database. Registry and the
OpenTofu workspace use local persistence. Each tool uses its own database or
schema.

### Deployment View

The root `docker-compose.yml` includes every leaf; a profile selects the
service. `tooling` and `registry` select Registry, published only on
`127.0.0.1:${REGISTRY_PORT:-5000}`; `iac` selects OpenTofu and the Terrakube
API, UI and executor; `dependency-update` selects Renovate; `backup` selects
Restic, `restic-offsite` and the SQLite export job; `testing` selects k6;
`contract-testing` selects Pact Broker and its provisioning job; `api-mock`
selects WireMock; `policy-check` selects Conftest; `dev`, `local` and
`mail-dev` select Mailpit. Registry is HOME; the other capabilities are not
activated implicitly.

## Quality and Risks

### Quality Attributes

- **Security:** the Terrakube API, UI and executor routes and the Mailpit UI
  use the ForwardAuth chain. Registry has no gateway route.
- **Reliability:** IaC state stays in the declared backend. SeaweedFS and
  PostgreSQL on one host are not independent failure domains, so a host failure
  breaks continuity; backup and isolated recovery need separate evidence.
- **Scalability:** Terrakube execution capacity changes only through approved
  configuration; no auto-scaling is implemented.

### Risks

Restic, the only cross-platform backup path, runs only when `backup` is
selected; Compose declares no schedule for it.

### Evolution

Promoting SonarQube, Locust or dbt back into a root tier is an owner decision
under the LAB promotion contract.

## Related Documents

- [REQ-0010 Tooling requirements](../../01.requirements/0010-tooling.md)
- [ADR-0009 Tooling services](../decisions/0009-tooling-services.md)
- [OpenTofu operations](../../05.operations/guides/10-platform-and-backup/0082-opentofu.md)
- [Pact Broker operations](../../05.operations/guides/12-testing-and-quality/0093-pact-broker.md)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
