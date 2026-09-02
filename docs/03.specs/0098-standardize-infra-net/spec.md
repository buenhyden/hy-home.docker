---
title: infra_net Standardization Outcome
version: 1.0.0
type: sdlc/spec
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0098
parent_ids:
  - AD-0026
created: 2026-07-05
updated: 2026-09-01
---
# infra_net Standardization Outcome

## Overview

This completed change standardized the shared infra_net definition and service
membership. Current network structure and address allocation now belong to
AD-0026 and the IP address management Operations subject.

## Boundaries and Inputs

The change covered the root Compose IPAM definition, service network
membership, static address preservation, and validation. Other external
networks and host networking were not redefined.

## Behavior Contract

- Root Compose defines infra_net with the approved subnet and gateway defaults.
- Services use the tracked dictionary network form when a static address is
  required.
- Existing k3d-hyhome or other approved network membership is preserved.
- Individual addresses and grouped allocation are current only in AD-0026 and
  tracked Compose, not in this completed change record.

## Technical Approach

The implementation updated root and service Compose files and verified the
merged configuration. Current changes use the Architecture allocation view and
Stage 05 procedure rather than replaying the original migration steps.

## Interfaces and Data

The durable interfaces are docker-compose.yml, infra/** Compose files,
AD-0026, and OPS-0077 Guide/Policy/Runbook.

## Failure Modes and Guardrails

Duplicate addresses, out-of-subnet assignments, lost network membership, or a
change that updates only documentation fails validation. A topology change
requires a new active change packet.

## Acceptance Contract

The root network renders with the approved IPAM contract, tracked services
preserve their required memberships, and AD-0026 matches current static
addresses.

## Traceability

- [REQ-0023](../../01.requirements/0023-standardize-infra-net.md)
- [AD-0026 current network architecture](../../02.architecture/descriptions/0026-standardize-infra-net.md)
- [ADR-0026](../../02.architecture/decisions/0026-standardize-infra-net.md)
- [IP address management guide](../../05.operations/catalog/12-infra-net/0077-ip-address-management/guide.md)
- [IP address management policy](../../05.operations/catalog/12-infra-net/0077-ip-address-management/policy.md)
- [IP address management runbook](../../05.operations/catalog/12-infra-net/0077-ip-address-management/runbook.md)
