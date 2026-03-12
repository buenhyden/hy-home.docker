# Technical Specifications Hub (`specs/`)

This directory is the tactical source of truth for active implementation contracts. Read this index before opening spec subdirectories.

## Specification Families

### Shared And Cross-Cutting Specs

- [Agent Instruction Refactor Specification](agent-instructions/spec.md)

### Infrastructure Specs

- [Infrastructure Specs Index](infra/README.md)
- [Global Baseline](infra/global-baseline/spec.md)
- [Implementation Baseline](infra/baseline/spec.md)
- [Automation Logic](infra/automation/spec.md)
- [Hardening & Density](infra/system-optimization/spec.md)

## Compliance Baseline

Every specification in this directory MUST contain:

- **Identifier**: Machine-readable coded ID (e.g., `[SPEC-INFRA-NNN]`).
- **Persona**: Mandatory framing from an engineering persona perspective.
- **Components**: NFR, Storage, Interfaces, Verification, Security, and Ops sections.
- **Verification**: At least 3 testable Given-When-Then Acceptance Criteria [REQ-SPT-10].

## Related Tactical Docs

- [Plans Index](../plans/README.md)
- [Documentation Index](../README.md)

---
> [!IMPORTANT]
> **NO SPEC, NO CODE.** All infrastructure modifications MUST BE grounded in an approved specification.
