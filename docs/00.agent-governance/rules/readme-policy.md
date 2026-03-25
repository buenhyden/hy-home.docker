---
layer: agentic
---

# README Update & Maintenance Policy

This document defines the mandatory protocol for maintaining `README.md` files across the `hy-home.docker` ecosystem. It enforces **Spec-Driven Documentation** and ensures that entry points remain synchronized with technical reality.

## 1. The "TDD for Docs" Principle

All significant technical changes MUST follow a **Red-Green-Refactor for Documentation** cycle:

1. **RED**: Update the relevant `README.md` (or Tier-level Map) *before* implementation to define the intent and expected structure.
2. **GREEN**: Implement the change as specified in the updated README or Spec.
3. **REFACTOR**: Polish the documentation after verification to reflect any implementation-specific details (e.g., exact port numbers or volume paths).

## 2. Maintenance Triggers

A `README.md` update is MANDATORY when:

- **New Service added**: Must be added to the tier-level service map.
- **Port/Volume change**: Must be updated in the "Setup" and "Usage" sections.
- **Dependency change**: Update any required environmental variables or upstream services.
- **Scope shift**: If the purpose of a directory or module changes, the high-level description must reflect it.

## 3. Structural Standards (Golden 5)

Every `README.md` MUST adhere to the **Golden 5 Header Pattern**:

1. `## 1. Context & Objective`: High-level purpose and system placement.
2. `## 2. Requirements & Constraints`: Dependencies, secrets, and limitations.
3. `## 3. Setup & Installation`: Step-by-step commands (validated).
4. `## 4. Usage & Integration`: How to use it and how other services link to it.
5. `## 5. Maintenance & Safety`: Healthchecks, backup notes, and safety warnings.

## 4. Hierarchy of Navigation

- **Global View**: Root `README.md` links to `docs/README.md`.
- **Infrastructure View**: `infra/README.md` maps all tiers (01-11).
- **Service View**: Individual service directories (e.g., `infra/01-gateway/nginx/`) contain local context.

## 5. Verification Gate

Before any PR or task completion:
- [ ] Verify all links in the modified README are valid.
- [ ] Ensure any new `[LOAD:...]` markers are correctly pointed to the governance hub.
- [ ] Confirm no legacy taxonomy references (`01-11`, `01~11`) exist.
