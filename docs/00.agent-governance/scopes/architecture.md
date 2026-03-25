---
title: 'Architecture Strategy Scope'
layer: architecture
---

# Architecture Strategy Scope

Guidance for high-level system design, service boundaries, and structural patterns.

## 1. Context & Objective
- **Goal**: Maintain architectural integrity across the distributed stack.
- **Scope**: Service discovery, inter-service communication, and shared state.

## 2. Requirements & Constraints
- **Pattern**: Clean Architecture / Ports & Adapters.
- **Protocol**: gRPC for internal, REST/GraphQL for external.

## 3. Implementation Flow
1. Define entities and invariants in `02.ard`.
2. Map service boundaries in `04.specs`.
3. Validate with `bash scripts/validate-architecture.sh`.

## 4. Operational Procedures
- Refer to `docs/08.ops/` for deployment patterns.

## 5. Maintenance & Safety
- Use `adr` skill to document every structural trade-off.

