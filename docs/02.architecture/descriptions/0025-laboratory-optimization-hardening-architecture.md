---
title: "Admin and Experiment Tools Hardening Architecture Description"
version: "1.3.1"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "architecture"
artifact_id: "AD-0025"
parent_ids:
- "REQ-0012"
created: "2026-03-28"
---

# Admin and Experiment Tools Hardening Architecture Description

## Overview

### Purpose and Readers

This Description records the hardening structure of the administration and
experimentation tools spread across the Data, Observability and AI tiers, and
of the standalone LABs. These tools expose high-privilege UIs, so the design
puts the security boundary first. Each tool keeps its own authentication:
RedisInsight uses ForwardAuth, Dozzle native OIDC, and Open Notebook a
password file with a gateway CIDR allowlist. These exceptions predate the
relocation recorded in POL-0073, and the move grants no new exemption. The
tier structure is in [AD-0011](0011-laboratory-architecture.md).

### System Boundary

- **Owns**: the per-tool ingress contract (gateway chain, authentication and
  allowlist), the no-direct-host-exposure rule with Open Notebook's loopback
  API as its one exception, Dozzle's read-only Docker socket, Open Notebook's
  password, allowlist, large-body and Docker Secret contract, and the checks
  of the hardening gate for these tools.
- **Consumes**: the `01-gateway` Traefik middleware, the `02-auth` SSO
  middleware and Keycloak, the Docker Engine, and the Valkey/Redis endpoints.
- **Does not own**: Keycloak realm policy, Traefik global entrypoints, and the
  LAB promotion contract, which SPEC-0263 owns.
- **Non-goals**: promoting an experimental service to the HOME tier and
  replatforming the management tools.

## Context and Constraints

### Context

The tools consume the `01-gateway` Traefik middleware, the `02-auth` SSO middleware and Keycloak, the Docker Engine, and the Valkey/Redis endpoints. Dozzle reads the Docker socket, RedisInsight reaches Valkey and Redis, and Open Notebook reaches SurrealDB.

### Constraints

Each tool keeps its own authentication, and no tool is exposed on a host port except Open Notebook's loopback API. The LAB promotion contract is owned by SPEC-0263, and the hardening checks are static source-drift checks, not live access acceptance.

## Current Structure

### Building Blocks

| Tool | Package | Ingress chain | Authentication |
| --- | --- | --- | --- |
| Dozzle | `infra/06-observability/dozzle` (`admin`) | `gateway-standard-chain`, `dozzle-admin-ip` | native Keycloak OIDC; Docker socket read-only |
| RedisInsight | `infra/04-data/redisinsight` (`admin`) | `gateway-standard-chain`, `redisinsight-admin-ip`, `sso-errors`, `sso-auth` | ForwardAuth |
| Open Notebook and SurrealDB | `infra/08-ai/open-notebook` (`notebook`) | `gateway-standard-chain`, `open-notebook-admin-ip`, `large-body` | password file; API on `127.0.0.1` only |
| MLflow | `infra/08-ai/mlflow` (`mlops`) | `gateway-standard-chain`, `sso-errors`, `sso-auth` | ForwardAuth |

Sources: `infra/06-observability/dozzle/docker-compose.yml:35,48,74`,
`infra/04-data/redisinsight/docker-compose.yml:74`,
`infra/08-ai/open-notebook/docker-compose.yml:33,101`,
`infra/08-ai/mlflow/docker-compose.yml:141`.

Control paths: Dozzle reads the Docker socket, RedisInsight reaches the Valkey
and Redis endpoints on `dev_data_net` and `mng_data_net`, and Open Notebook
reaches SurrealDB on `ai_net`; SurrealDB publishes no host port.

**LABs**: each LAB is one folder `labs/<name>/` with its `docker-compose.yml`,
`README.md` and `promotion.yaml`, run as a standalone project outside the root
Compose project, with secrets under `secrets/labs/<name>/` (SPEC-0263);
`labs/README.md` lists the current LABs. No LAB is promoted; the owner
decides promotion.

### Runtime and Deployment

#### Runtime View

This architecture introduces no production data ownership. Data access is
limited to management metadata, Docker socket visibility, log streams,
Valkey/Redis inspection, MLflow tracking metadata and Open Notebook's local
state.

#### Deployment View

- **Platform**: the root `docker-compose.yml` includes the four packages
  above under their own profiles; `infra/common-optimizations.yml` supplies the
  shared template. LABs start only through their own project.
- **Evidence**: `scripts/hardening/check-all-hardening.sh 04-data
  06-observability 08-ai` and the CI `infrastructure-hardening` job. These are
  static source-drift checks, not live access acceptance.

## Interfaces

### Contracts

- The per-tool ingress chain and authentication are tabulated in Building Blocks.
- Open Notebook's API is published on `127.0.0.1` only, and SurrealDB publishes no host port.
- Each LAB is one folder `labs/<name>/` with `docker-compose.yml`, `README.md` and `promotion.yaml` (SPEC-0263).

### Failure Boundaries

Peer services on a shared network can reach a tool without the gateway, and Dozzle and Open Notebook rely on their own authentication. Regression recovery follows the CI gate and the runbook linked under Currentness and Lineage.

## Decisions

### Decision Links

- **ADR**: [ADR-0062](../decisions/0062-home-lab-membership.md)

### Quality and Risks

#### Quality Attributes

- **Security**: each declared gateway and authentication boundary holds, with
  the Open Notebook loopback API as the only host publication.
- **Reliability**: the Compose contract and healthchecks give minimum runtime
  stability.
- **Operability**: regression recovery follows the CI gate and the runbook.

#### Risks

- Peer services on a shared network can reach a tool without the gateway;
  proving no bypass needs separate runtime evidence.
- Dozzle and Open Notebook do not use gateway ForwardAuth, so their own
  authentication configuration is their access boundary.

## Traceability

### Requirement Mapping

- **PRD**: [REQ-0012](../../01.requirements/0012-laboratory.md)
- **Spec**: [SPEC-0263 LAB promotion contract](../../03.specs/0263-lab-promotion-contract/spec.md)

### Currentness and Lineage

- **Tier Architecture Description**: [AD-0011 Administration and Experimentation Architecture Description](0011-laboratory-architecture.md)
- **Guide**: [Laboratory optimization hardening guide](../../05.operations/guides/10-platform-and-backup/0074-laboratory-optimization-hardening.md)
- **Policy**: [Laboratory optimization hardening policy](../../05.operations/policies/10-platform-and-backup/0074-laboratory-optimization-hardening.md)
- **Runbook**: [Laboratory optimization hardening runbook](../../05.operations/runbooks/10-platform-and-backup/0074-laboratory-optimization-hardening.md)

#### Evolution

- **Management UIs**: an expiry policy for experimental services.
- **Dozzle**: narrowing the visible log scope and reviewing least privilege.
- **RedisInsight**: minimal access, no direct production cache change, and an
  audit-log policy.
- **Open Notebook**: notebook data retention and a host-exposure review before
  any promotion.

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.
