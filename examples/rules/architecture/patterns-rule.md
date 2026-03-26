---
layer: architecture
description: "Rule for architecture patterns, dependency direction, and structural integrity."
---

# Architecture — Patterns Rule

## Case
- **[REQ-ARCH-01]** Define component/service boundaries explicitly.
- **[REQ-ARCH-02]** Keep dependency flow directional and reviewable.
- **[REQ-ARC-03]** Prevent circular dependencies in architecture and implementation.

## Style
- **[REQ-ARC-06]** Prefer clean or hexagonal boundary patterns where applicable.
- **[REQ-ARC-09]** Document public interfaces at boundary seams.
- **[BAN-ARCH-01]** Avoid opaque coupling that hides side effects.

## Validation
- [ ] Boundaries and interactions are explicitly documented.
- [ ] No circular dependency paths remain.
- [ ] Structural choices are consistent with chosen architecture pattern.
