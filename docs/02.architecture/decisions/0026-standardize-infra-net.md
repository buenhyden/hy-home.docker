---
title: "Standardize infra_net Subnet and Static IP Assignment"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0026"
parent_ids:
- "AD-0026"
created: "2026-04-01"
---
# ADR-0026: Standardize infra_net Subnet and Static IP Assignment

## Context

This document records the decision to standardize the subnet of the network for
all infrastructure services (`infra_net`) to `172.19.0.0/16`, and to manage
`infra_net` connections of Compose services with dictionary-based static IP
assignment.

Several Docker Compose files are currently `include`d, and each could carry its
own separate network configuration. If the range for the `infra_net` used across
the infrastructure is unclear or conflicts, this causes inter-service
communication failures or difficulty managing IPs. Therefore all infrastructure
services need to be forced to run on the same virtual network plane.

## Decision

- **Decision item 1**: Fix the subnet of `infra_net` to `${INFRA_SUBNET:-172.19.0.0/16}`
  in the root `docker-compose.yml`.
- **Decision item 2**: Explicitly declare `infra_net` for services in every
  individual `include`d configuration file.
- **Decision item 3**: If a service is already connected to another network such
  as `k3d-hyhome`, keep that connection and add `infra_net` rather than removing it.
- **Decision item 4**: Write a service's `infra_net` declaration as a dictionary,
  and assign a static IP within `172.19.0.0/16` through `ipv4_address`.

## Consequences

- **Positive**:
  - Predictable IP range management (`172.19.0.0/16`).
  - Stable DNS and IP references between services.
  - Service connectivity survives container restarts.
- **Trade-offs**:
  - A small chance of conflict remains with other local network environments
    that overlap this subnet.
  - Advance range management adds overhead to avoid IP conflicts.

### Explicit Non-goals

- Changing the subnet of the user application network (`project_net`) is out of
  scope.
- Changing the dedicated interconnect network configuration inside the database
  cluster is not covered.

## Options Considered

### Alternative 1: Docker Default Bridge (Automatic CIDR)

- Good: Docker allocates addresses on its own with no separate configuration.
- Bad: IPs change depending on service placement order, making static
  IP-based configuration impossible.

### Alternative 2: External IPAM Service

- Good: A dedicated, independent management tool can automate IP address
  management.
- Bad: Adds excessive configuration and operational complexity for a small
  Docker Compose-based local infrastructure.

## Traceability

The confirmation basis for this decision is limited to the Architecture
Description, Spec, and Operations documents linked in `Related Documents`, and
the current repository configuration. Runtime state without separate execution
evidence is not claimed.

## Decision Drivers

The decision context above records the applicable drivers and evidence.

## Related Documents

- **PRD**: [infra_net product requirements](../../01.requirements/0023-standardize-infra-net.md)
- **Architecture Description**: [infra_net architecture descriptions](../descriptions/0026-standardize-infra-net.md)
- **Spec**: [infra_net technical specification](../../98.archive/completed/03.specs/0098-standardize-infra-net/spec.md)
- **Plan**: infra_net implementation plan
