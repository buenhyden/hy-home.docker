---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-04-01-standardize-infra-net.md -->

# Standardize `infra_net` Implementation Plan

## Overview

This document defines the concrete implementation plan for applying the `infra_net` network to all infrastructure services and standardizing the subnet as `172.19.0.0/16`. Work proceeds in three phases: documentation, implementation, and verification.

## Context

To establish a communication standard between infrastructure services and reduce IP management complexity, previously separate network settings are consolidated into `infra_net`.

## Goals & In-Scope

- **Goals**:
  - Connect all active infrastructure services to `infra_net`.
  - Enforce the `172.19.0.0/16` subnet.
  - Preserve the existing `k3d-hyhome` settings.
- **In Scope**: Modify `docker-compose.yml` and 21 lower-level `include` files.

## Non-Goals & Out-of-Scope

- **Non-goals**: Service port changes or internal logic changes.
- **Out of Scope**: Network setting changes outside the cluster on the host.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Write SSoT documents (9 folders) | `docs/{01.requirements,02.architecture,03.specs,04.execution,05.operations}/` | REQ-GOV | All templates comply and links are complete |
| PLN-002 | Update root Compose network definition | `docker-compose.yml` | REQ-FUN-02 | `docker compose config` confirms the subnet |
| PLN-003 | Update individual service network assignments | `infra/**/docker-compose.yml` | REQ-FUN-01 | Each service has `infra_net` |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Verify merge result | `docker compose config` | Valid YAML output without errors |
| VAL-PLN-002 | Network | Verify subnet/IP | `docker compose config \| grep -E "subnet\|infra_net"` | `172.19.0.0/16` is confirmed |
| VAL-PLN-003 | Persistence | Verify `k3d-hyhome` preservation | `grep "k3d-hyhome" infra/**/docker-compose.yml` | Existing settings are preserved |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| YAML syntax errors | High | Run `docker compose config` individually after editing each file |
| IP range conflicts | Medium | First scan and confirm the list of existing manually assigned IPs |

## Completion Criteria

- [x] Scoped work completed
- [x] Verification passed (`docker compose config` success)
- [x] Required docs updated (9-directory governance)
- [x] Post-hoc IP assignments synced (e.g., oauth2-proxy-valkey: .5)

## Related Documents

- **PRD**: [../../01.requirements/2026-04-01-standardize-infra-net.md](../../01.requirements/2026-04-01-standardize-infra-net.md)
- **ARD**: [../../02.architecture/requirements/0026-standardize-infra-net.md](../../02.architecture/requirements/0026-standardize-infra-net.md)
- **Spec**: [../../03.specs/standardize-infra-net/spec.md](../../03.specs/standardize-infra-net/spec.md)
- **ADR**: [../../02.architecture/decisions/0026-standardize-infra-net.md](../../02.architecture/decisions/0026-standardize-infra-net.md)
- **TASK**: [../tasks/2026-04-01-standardize-infra-net.md](../tasks/2026-04-01-standardize-infra-net.md)
