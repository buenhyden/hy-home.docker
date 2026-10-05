---
title: "Laboratory Services Selection and Configuration"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0011"
parent_ids:
- "AD-0011"
created: "2026-03-26"
---
# ADR-0011: Laboratory Services Selection and Configuration

## Context

This document records the architecture decision for selecting the core management tools of the `11-laboratory` tier.

To raise system operating efficiency, we need to build a container management, database inspection, and service navigation environment. This requires selecting tools that are lightweight, reliable, and integrate smoothly with Traefik and Keycloak.

### Traceability

The verification basis for this decision is limited to the Architecture Description, Spec, and Operations documents linked under `Related Documents`, and the current repository configuration. It does not claim any runtime state without separate execution evidence.

## Decision

We select the following service stack as the standard tooling for `11-laboratory`.

1. **Dashboard (Homer)**: An ultra-lightweight dashboard based on static configuration.
2. **Container Management (Portainer)**: Intuitive container resource control and status monitoring.
3. **Data Inspection (RedisInsight)**: Redis/Valkey data structure visualization and analysis.
4. **Log Viewer (Dozzle)**: Real-time log streaming across multiple containers.
5. **Local Notebook Lab (Open Notebook + SurrealDB)**: Manages local knowledge work and experimental notebook state.

### Decision Drivers

The decision context above records the applicable drivers and evidence.

## Alternatives

### Alternatives

### Options Considered

Existing alternatives, rationale, or rejected options in this ADR remain the alternative analysis. This alignment section does not add new alternatives.

## Consequences

- **Positive**:
  - Substantially improves the operator's infrastructure visibility and debugging speed.
  - Uses SSO unified login without separate account management.
- **Trade-offs**:
  - Exposing `docker.sock` is required, so strong access control through SSO is essential.

### Explicit Non-goals

- This ADR does not change runtime behavior.
- This ADR does not rewrite historical decision evidence.
- Implementation details remain in linked specs, plans, and tasks.

## Related Documents

- **PRD**: [../../01.requirements/0012-laboratory.md](../../01.requirements/0012-laboratory.md)
- **Architecture Description**: [../descriptions/0011-laboratory-architecture.md](../descriptions/0011-laboratory-architecture.md)
- **Spec**: [../../03.specs/012-laboratory/spec.md](../descriptions/0011-laboratory-architecture.md)
