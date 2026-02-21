---
trigger: model_decision
glob: ["**/*"]
description: "Architecture Design Principles: Enforces Separation of Concerns, Dependency Inversion, and Modular Evolutions."
---

# Architecture Design Standard

- **Role**: Software Systems Architect
- **Purpose**: Define core design principles and mandatory patterns for building modular, resilient, and maintainable software systems.
- **Activates When**: Designing system boundaries, selecting architectural patterns (Clean, Hexagonal, etc.), or managing cross-service dependencies.

**Trigger**: model_decision — Apply during the conceptual and detailed design phases of software development.

## 1. Standards

### Principles

- **[REQ-ARCH-01] Dependency Inversion Primacy**
  - High-level business policies MUST NOT depend on low-level implementation details (Frameworks, DBs). Dependencies MUST point inward toward the domain.
- **[REQ-ARCH-02] Strict Boundary Isolation (SoC)**
  - Systems MUST maintain a strict Separation of Concerns. Presentation, Application, Domain, and Infrastructure roles MUST be isolated into distinct packages/modules.
- **[REQ-ARCH-03] Contractual Integrity**
  - All inter-module and inter-service communications MUST occur through explicit, versioned interfaces or contracts.

### Design Patterns Baseline

| Pattern | Requirement ID | Application Context |
| --- | --- | --- |
| Clean Architecture | [REQ-ARCH-04] | Core business logic decoupled from UI/IO |
| Hexagonal (Ports/Adapters) | [REQ-ARCH-05] | Isolation from external infrastructure |
| Modular Monolith | [REQ-ARCH-06] | Early-stage development with clear boundaries |
| Event-Driven | [REQ-ARCH-07] | Asynchronous decoupling and resilience |

### Must

- **[REQ-ARCH-08] Domain-Driven Boundaries**
  - Architectural boundaries MUST align with the business domain (Bounded Contexts) rather than technical artifacts.
- **[REQ-ARCH-09] Explicit Reliability Layers**
  - Every remote dependency call MUST be wrapped in a reliability layer (Timeout, Circuit Breaker, Retries).
- **[REQ-ARCH-10] Idempotent Handlers**
  - All asynchronous event handlers and API write operations MUST be idempotent to ensure consistency during retries.
- **[REQ-ARCH-11] Blueprint Alignment**
  - Every technical implementation MUST align with the root `ARCHITECTURE.md` blueprint's defined style and principles.

### Must Not

- **[BAN-ARCH-01] Circular Dependency Chains**
  - The system MUST NOT contain circular references between modules or layers (A -> B -> A).
- **[BAN-ARCH-02] Shared Logic Leakage**
  - Domain invariants and business rules MUST NOT be duplicated or leaked into the Infrastructure or UI layers.

### Failure Handling

- **Stop Condition**: Stop design approval if a "God Component" (> 500 lines or > 10 responsibilities) is identified in the core path.

## 2. Procedures

- **[PROC-ARCH-01] Boundary Verification**
  - IF creating a new module THEN MUST verify its dependency graph against the established layer hierarchy.
- **[PROC-ARCH-02] Acyclic Audit**
  - Run automated dependency analysis monthly to detect and resolve hidden circular references.

## 3. Examples

### Clean Dependency Flow (Good)

```text
[UI/Controllers] -> [Use Cases/Services] -> [Domain Model/Entities]
[Infrastructure/DB] -> [Domain Interfaces/Ports]
```

## 4. Validation Criteria

- **[VAL-ARCH-01] Layer Isolation Pass**
  - [ ] Automated linting rules (e.g., ArchUnit) confirm that zero infrastructure classes are imported into the domain layer.
- **[VAL-ARCH-02] Resilience Verification**
  - [ ] Fault injection tests prove that the system degrades gracefully when an external dependency times out.
- **[VAL-ARCH-03] Contract Compliance**
  - [ ] API audit confirms that 100% of cross-service traffic matches the approved schemas.
