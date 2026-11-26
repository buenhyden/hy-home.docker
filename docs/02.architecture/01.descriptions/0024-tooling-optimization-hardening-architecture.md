---
title: "Platform Operations and Quality Optimization Hardening Architecture Description"
version: "3.1.0"
type: "sdlc/architecture-description"
status: "approved"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-26"
layer: "architecture"
artifact_id: "AD-0024"
parent_ids:
- "REQ-0010"
created: "2026-03-28"
---

# Platform Operations and Quality Optimization Hardening Architecture Description

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the architecture-description payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Context and Boundaries

##### System Boundary

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

###### Purpose and Readers
<!-- core-payload-level:4 -->

This Description records the hardening structure of the `09-platform-ops` and
`11-quality` tiers: the gateway and SSO boundary of their management routes,
their network membership, test-tool runtime stability and the hardening gate.
These are control-plane services for platform operational quality. Requirement
owners, implementers and operators share these concerns; the tier structure
itself is in [AD-0009](0009-tooling-architecture.md).

###### Context
<!-- core-payload-level:4 -->

The Description consumes the `01-gateway` middleware chain, the `02-auth` SSO middleware, and `04-data` management PostgreSQL, Valkey and SeaweedFS. Traefik `websecure` routes the Mailpit UI, and Keycloak serves it through the SSO middleware.

##### Constraints

Every routed tooling UI passes the gateway chain and SSO, and the registry stays loopback-only. The tooling tiers own operational tool metadata and execution policy, not application data, and the hardening checks are static, so they prove no running service.

#### Structure

##### Building Blocks

- **Platform operations** (`infra/09-platform-ops/`): OpenTofu
  (`iac` profile), the image registry (`tooling` profile), Renovate
  (`dependency-update`), restic backup (`backup`), and the project-registration,
  resource-optimization, security-updates and service-integration packages.
- **Quality** (`infra/11-quality/`): k6 (`testing`), Pact Broker
  (`contract-testing`), WireMock (`api-mock`), Conftest (`policy-check`) and
  Mailpit (`dev`).
- **Ingress**: Traefik `websecure` routes the Mailpit UI through
  `gateway-standard-chain`, `sso-errors` and `sso-auth`
  (`infra/11-quality/mailpit/docker-compose.yml:53`). The registry has no
  Traefik route; it publishes only on loopback
  (`infra/09-platform-ops/registry/docker-compose.yml:29`).
- **Shared dependencies**: management PostgreSQL and Valkey on `mng_data_net`,
  SeaweedFS on `object_net`, and Keycloak through the SSO middleware.

##### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| Mailpit UI route (Traefik `websecure`) | Mailpit | The description names no consumer for this interface. | `gateway-standard-chain`, `sso-errors` and `sso-auth` (`infra/11-quality/mailpit/docker-compose.yml:53`) | The description records no failure handling for this interface. |
| Registry loopback publication | Image registry | The description names no consumer for this interface. | `infra/09-platform-ops/registry/docker-compose.yml:29` | The description records no failure handling for this interface. |
| Management PostgreSQL and Valkey on `mng_data_net` | `04-data` management PostgreSQL and Valkey | The `09-platform-ops` and `11-quality` tooling | The description links no contract for this interface. | The description records no failure handling for this interface. |
| SSO middleware | `02-auth` SSO middleware and Keycloak | Routed tooling UIs | The description links no contract for this interface. | The description records no failure handling for this interface. |

- Traefik `websecure` routes the Mailpit UI through `gateway-standard-chain`, `sso-errors` and `sso-auth`, per the Ingress item in Building Blocks.
- The registry has no Traefik route and publishes only on loopback.
- Management PostgreSQL and Valkey are reached on `mng_data_net`, SeaweedFS on `object_net`.

#### Runtime Behavior

##### Normal Flow

###### Runtime View
<!-- core-payload-level:4 -->

- **Entities**: OpenTofu state, contract and
  test results, performance metrics and image artifacts.
- **Storage**: the registry keeps images in its own volume.
- **Boundary**: the tooling tiers own operational tool metadata and execution
  policy, not application data.

###### Deployment View
<!-- core-payload-level:4 -->

- **Platform**: Docker Compose packages under `infra/09-platform-ops/` and
  `infra/11-quality/`, included by the root `docker-compose.yml` and selected
  by profile; job-style tools run only for a named operation.
- **Evidence**: `scripts/hardening/check-all-hardening.sh 09-platform-ops
  11-quality` and the CI `infrastructure-hardening` job. Root-context Compose
  rendering runs only when runtime evidence is approved. These are static
  checks; they prove no running service.

##### Failure and Recovery

Healthchecks and the Compose contract order startup. Job-style tools without a peer share the project default network, which is their trust boundary, and the registry's loopback publication is acceptable only while the host is trusted. Change and recovery follow the guide, policy and runbook linked under Currentness and Lineage.

#### Quality Scenarios

##### Scenarios

###### Quality Attributes
<!-- core-payload-level:4 -->

- **Security**: every routed tooling UI passes the gateway chain and SSO; the
  registry stays loopback-only.
- **Reliability**: healthchecks and the Compose contract order startup.
- **Observability**: the hardening script and CI gate detect contract drift.
- **Operability**: change and recovery follow the linked guide, policy and
  runbook.

###### Risks
<!-- core-payload-level:4 -->

- The registry's loopback publication is a host exposure outside the gateway;
  it is acceptable only while the host itself is trusted.
- Job-style tools share the project default network when they have no peer, so
  that network is their trust boundary.

##### Trade-offs

- The registry publishes only on loopback instead of through the gateway;
  this host exposure outside the gateway is acceptable only while the host
  itself is trusted (Risks).
- Job-style tools without a peer share the project default network, so that
  network is their trust boundary (Risks).
- The hardening checks are static and prove no running service; root-context
  Compose rendering runs only when runtime evidence is approved (Constraints,
  Deployment View).

#### Decisions and Adoption

##### Decisions

- **ADR**: [ADR-0062](../02.decisions/0062-home-lab-membership.md)

##### Adoption Boundaries

###### Requirement Mapping
<!-- core-payload-level:4 -->

- **PRD**: [REQ-0010](../../01.requirements/0010-tooling.md)

###### Currentness and Lineage
<!-- core-payload-level:4 -->

- **Tier Architecture Description**: [AD-0009 Platform Operations and Software Verification Architecture Description](0009-tooling-architecture.md)
- **Guide**: [Tooling optimization hardening guide](../../05.operations/01.guides/10.platform-and-backup/0063-tooling-optimization-hardening.md)
- **Policy**: [Tooling optimization hardening policy](../../05.operations/02.policies/10.platform-and-backup/0063-tooling-optimization-hardening.md)
- **Runbook**: [Tooling optimization hardening runbook](../../05.operations/03.runbooks/10.platform-and-backup/0063-tooling-optimization-hardening.md)

###### Evolution
<!-- core-payload-level:4 -->

- **OpenTofu**: a plan/apply approval gate, state locking and backup, drift
  detection.
- **Registry**: cosign signing and verification, blocking on scan failure.
- **k6**: storing and comparing performance baselines, standard scenario tags.

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
