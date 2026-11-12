---
title: "Compose Network Segmentation Requirements"
version: "1.4.2"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-12"
layer: "requirements"
artifact_id: "REQ-0023"
created: "2026-04-01"
---

# Compose Network Segmentation Requirements

## Overview

### Problem and Outcome

All services once shared one `infra_net` mesh and could reach each other, and
some had no declared network or an ambiguous subnet. That made inter-service
communication hard to reason about and to troubleshoot. This package requires
that the HOME composition split network membership by traffic flow and give
each repository-owned network a predictable address block.

### Stakeholders

- **Infrastructure engineer**: needs each service limited to the peers it uses,
  to keep the structure clear and resolve communication issues.
- **DevOps engineer**: needs a standard network and a predictable address block
  when adding a service.
- **Operator**: needs removed external integrations (k3d) kept off every
  service.

The owner, @buenhyden, writes, reviews and accepts this package.

## Scope

### In Scope

- Every service in the root composition and its included service
  files; the subnets of repository-owned networks.

### Constraints and Exclusions

- **Out of scope**: networks the repository does not own (for example
  `project_net`); each LAB's own isolated network, which follows the LAB
  isolation requirement in REQ-0012; service logic inside containers.

**Assumptions.**

- The root composition merges every included service file into one model.

**Risks.**

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
- **REQ-0023-FR-0004**: A secondary listener without its own authentication
  (metrics, management, profiling or broker) accepts connections only from its
  declared consumers, on an internal network that only those consumers share.
  Exception: a listener that is not yet bound to a consumer-only address stays
  as it is and is recorded here with its owner, until it is bound. The
  recorded exceptions, owned by @buenhyden, are the Registry debug listener
  `:5001`, reachable by every `obs_net` peer, and the SeaweedFS master, volume
  and filer metrics on `9324` to `9326`, reachable by `seaweed_internal` peers.

## Acceptance Criteria

### Acceptance Conditions

- **REQ-0023-FR-0001**: In the rendered root composition, each service's
  networks match its declared traffic flow.
- **REQ-0023-FR-0002**: Each repository-owned network's address setting is its
  declared `10.250.x.0/24` block, or, for the named exception, the subnet its
  service file declares.
- **REQ-0023-FR-0003**: No service in the rendered root composition lists
  `k3d-hyhome`.
- **REQ-0023-FR-0004**: In the rendered root composition, each such listener
  binds to a fixed address on an internal network whose members are only the
  listener's service and its declared consumers, and a peer outside that
  network is refused. The recorded exceptions are excluded.

### Verification Method

Each condition is judged by reviewing the rendered root composition, as the criteria state; the recorded exceptions in REQ-0023-FR-0004 are excluded from that judgment. SPEC-0255 cites REQ-0023 in its body only; its Task evidence rows record the review result. The owner named in the frontmatter, @buenhyden, judges each condition from that evidence. The same owner accepts the requirement once every condition is judged met.

## Traceability

### Source and Constraints

This package records the owner's requirements for standardized infrastructure networks; no upstream document governs it.

### Downstream Links

- **Architecture Description**: [Compose network segmentation](../02.architecture/descriptions/0026-standardize-infra-net.md)
- **ADR**: [ADR-0055 Segmented Per-Flow Networks](../02.architecture/decisions/0055-segmented-per-flow-networks.md)
