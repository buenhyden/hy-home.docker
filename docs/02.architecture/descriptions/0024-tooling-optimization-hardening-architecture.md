---
title: "Platform Operations and Quality Optimization Hardening Architecture Description"
version: "2.2.1"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "architecture"
artifact_id: "AD-0024"
parent_ids:
- "REQ-0010"
created: "2026-03-28"
---

# Platform Operations and Quality Optimization Hardening Architecture Description

## Overview

### Purpose and Readers

This Description records the hardening structure of the `09-platform-ops` and
`11-quality` tiers: the gateway and SSO boundary of their management routes,
their network membership, test-tool runtime stability and the hardening gate.
These are control-plane services for platform operational quality. Requirement
owners, implementers and operators share these concerns; the tier structure
itself is in [AD-0009](0009-tooling-architecture.md).

### System Boundary

- **Owns**: the gateway and SSO contract of the tooling routes, tooling network
  membership, the k6 runtime contract and the `09-platform-ops` and
  `11-quality` checks of the hardening gate.
- **Consumes**: the `01-gateway` middleware chain, the `02-auth` SSO
  middleware, and `04-data` management PostgreSQL, Valkey and SeaweedFS.
- **Does not own**: each tool's domain logic, and the standalone LABs
  SonarQube (`labs/sonarqube/`) and Locust (`labs/locust/`), which run outside
  the root Compose project.
- **Non-goals**: a multi-cluster toolchain and adopting a replacement
  toolchain.

## Context and Constraints

### Context

The Description consumes the `01-gateway` middleware chain, the `02-auth` SSO middleware, and `04-data` management PostgreSQL, Valkey and SeaweedFS. Traefik `websecure` routes the Terrakube and Mailpit UIs, and Keycloak serves them through the SSO middleware.

### Constraints

Every routed tooling UI passes the gateway chain and SSO, and the registry stays loopback-only. The tooling tiers own operational tool metadata and execution policy, not application data, and the hardening checks are static, so they prove no running service.

## Current Structure

### Building Blocks

- **Platform operations** (`infra/09-platform-ops/`): OpenTofu and Terrakube
  (`iac` profile), the image registry (`tooling` profile), Renovate
  (`dependency-update`), restic backup (`backup`), and the project-registration,
  resource-optimization, security-updates and service-integration packages.
- **Quality** (`infra/11-quality/`): k6 (`testing`), Pact Broker
  (`contract-testing`), WireMock (`api-mock`), Conftest (`policy-check`) and
  Mailpit (`dev`).
- **Ingress**: Traefik `websecure` routes the Terrakube API, UI and executor
  and the Mailpit UI through `gateway-standard-chain`, `sso-errors` and
  `sso-auth` (`infra/09-platform-ops/terrakube/docker-compose.yml:65,101,183`,
  `infra/11-quality/mailpit/docker-compose.yml:53`). The registry has no
  Traefik route; it publishes only on loopback
  (`infra/09-platform-ops/registry/docker-compose.yml:29`).
- **Shared dependencies**: management PostgreSQL and Valkey on `mng_data_net`,
  SeaweedFS on `object_net`, and Keycloak through the SSO middleware.

### Runtime and Deployment

#### Runtime View

- **Entities**: OpenTofu state and Terrakube workspace metadata, contract and
  test results, performance metrics and image artifacts.
- **Storage**: Terrakube keeps metadata in management PostgreSQL and objects in
  SeaweedFS; the registry keeps images in its own volume.
- **Boundary**: the tooling tiers own operational tool metadata and execution
  policy, not application data.

#### Deployment View

- **Platform**: Docker Compose packages under `infra/09-platform-ops/` and
  `infra/11-quality/`, included by the root `docker-compose.yml` and selected
  by profile; job-style tools run only for a named operation.
- **Evidence**: `scripts/hardening/check-all-hardening.sh 09-platform-ops
  11-quality` and the CI `infrastructure-hardening` job. Root-context Compose
  rendering runs only when runtime evidence is approved. These are static
  checks; they prove no running service.

## Interfaces

### Contracts

- Traefik `websecure` routes the Terrakube API, UI and executor and the Mailpit UI through `gateway-standard-chain`, `sso-errors` and `sso-auth`, per the Ingress item in Building Blocks.
- The registry has no Traefik route and publishes only on loopback.
- Management PostgreSQL and Valkey are reached on `mng_data_net`, SeaweedFS on `object_net`.

### Failure Boundaries

Healthchecks and the Compose contract order startup. Job-style tools without a peer share the project default network, which is their trust boundary, and the registry's loopback publication is acceptable only while the host is trusted. Change and recovery follow the guide, policy and runbook linked under Currentness and Lineage.

## Decisions

### Decision Links

- **ADR**: [ADR-0062](../decisions/0062-home-lab-membership.md)

### Quality and Risks

#### Quality Attributes

- **Security**: every routed tooling UI passes the gateway chain and SSO; the
  registry stays loopback-only.
- **Reliability**: healthchecks and the Compose contract order startup.
- **Observability**: the hardening script and CI gate detect contract drift.
- **Operability**: change and recovery follow the linked guide, policy and
  runbook.

#### Risks

- The registry's loopback publication is a host exposure outside the gateway;
  it is acceptable only while the host itself is trusted.
- Job-style tools share the project default network when they have no peer, so
  that network is their trust boundary.

## Traceability

### Requirement Mapping

- **PRD**: [REQ-0010](../../01.requirements/0010-tooling.md)

### Currentness and Lineage

- **Tier Architecture Description**: [AD-0009 Platform Operations and Software Verification Architecture Description](0009-tooling-architecture.md)
- **Guide**: [Tooling optimization hardening guide](../../05.operations/guides/10-platform-and-backup/0063-tooling-optimization-hardening.md)
- **Policy**: [Tooling optimization hardening policy](../../05.operations/policies/10-platform-and-backup/0063-tooling-optimization-hardening.md)
- **Runbook**: [Tooling optimization hardening runbook](../../05.operations/runbooks/10-platform-and-backup/0063-tooling-optimization-hardening.md)

#### Evolution

- **OpenTofu**: a plan/apply approval gate, state locking and backup, drift
  detection.
- **Terrakube**: workspace separation, execution permissions and audit logs.
- **Registry**: cosign signing and verification, blocking on scan failure.
- **k6**: storing and comparing performance baselines, standard scenario tags.

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.
