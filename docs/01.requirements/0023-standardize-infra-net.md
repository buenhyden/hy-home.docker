---
title: "Compose Network Segmentation Requirements"
version: "1.3.0"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "requirements"
artifact_id: "REQ-0023"
created: "2026-04-01"
---

# Compose Network Segmentation Requirements

## Overview

All services once shared one `infra_net` mesh and could reach each other, and
some had no declared network or an ambiguous subnet. That made inter-service
communication hard to reason about and to troubleshoot. This package requires
that the HOME composition split network membership by traffic flow and give
each repository-owned network a predictable address block.

## Scope

- **In scope**: every service in the root composition and its included service
  files; the subnets of repository-owned networks.
- **Out of scope**: networks the repository does not own (for example
  `project_net`); each LAB's own isolated network, which follows the LAB
  isolation requirement in REQ-0012; service logic inside containers.

### Assumptions

- The root composition merges every included service file into one model.

### Risks

- A manually assigned address can collide when a subnet changes.

## Requirements

### Functional Requirements

- **REQ-0023-FR-0001**: Every active service connects only to networks with
  peers it actually uses, and uses the composition's default network when it
  has no peer.
- **REQ-0023-FR-0002**: Each repository-owned network declares a
  `10.250.x.0/24` subnet in the root composition. Exception: a small,
  leaf-owned internal network that only isolates one service's egress may
  declare a narrower subnet in its own service file and must be named here.
  The one exception is `crawl4ai_egress_net` (`10.250.200.0/29`).
- **REQ-0023-FR-0003**: No service connects to the `k3d-hyhome` network (k3d
  integration removed by owner decision on 2026-09-23).

### Stakeholders and User Needs

- **Infrastructure engineer**: needs each service limited to the peers it uses,
  to keep the structure clear and resolve communication issues.
- **DevOps engineer**: needs a standard network and a predictable address block
  when adding a service.
- **Operator**: needs removed external integrations (k3d) kept off every
  service.

### Non-functional Requirements

No numbered non-functional requirement is issued.

### Interface Requirements

No numbered interface requirement is issued.

## Acceptance Criteria

- **REQ-0023-FR-0001**: In the rendered root composition, each service's
  networks match its declared traffic flow.
- **REQ-0023-FR-0002**: Each repository-owned network's address setting is its
  declared `10.250.x.0/24` block, or, for the named exception, the subnet its
  service file declares.
- **REQ-0023-FR-0003**: No service in the rendered root composition lists
  `k3d-hyhome`.

## Related Documents

- **Architecture Description**: [Compose network segmentation](../02.architecture/descriptions/0026-standardize-infra-net.md)
- **ADR**: [ADR-0055 Segmented Per-Flow Networks](../02.architecture/decisions/0055-segmented-per-flow-networks.md)
