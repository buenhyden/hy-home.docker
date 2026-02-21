---
trigger: model_decision
glob: ["**/*.{ts,tsx,py,go}"]
description: "Tech Stack Standards: Enforces strict typing, interface-first design, and project-specific technical stack integrity."
---

# Tech Stack Standards

- **Role**: Technical Stack Lead
- **Purpose**: Define standards for maintaining the integrity, type-safety, and consistency of the project's specific technical stack and coding patterns.
- **Activates When**: Writing new source code, refactoring existing functional logic, or conducting technical stack reviews.

**Trigger**: model_decision — Apply during every code development and architectural integration task.

## 1. Standards

### Principles

- **[REQ-TCH-01] Strict Type Integrity**
  - All source code MUST utilize strict typing. The use of `any` or implicit types is PROHIBITED unless strictly required by external library constraints.
- **[REQ-TCH-02] Interface-First Architecture**
  - Public interfaces and data models MUST be defined before implementing functional logic to ensure consistent contract enforcement.
- **[REQ-TCH-03] Stack-Native Pattern Adherence**
  - Code MUST align with the project's canonical patterns (e.g., Hooks for React, Context for Go) as defined in the master technical blueprint.

### Coded ID Matrix

| Domain | Requirement ID | Critical Action |
| --- | --- | --- |
| Types | [REQ-TCH-04] | Zero implicit `any` policy |
| Interoperability| [REQ-TCH-05] | Explicit interface declarations |
| Casing | [REQ-TCH-06] | Alignment with project style guide |
| Modeling | [REQ-TCH-07] | Centralized data model definition |

### Must

- **[REQ-TCH-08] Static Analysis Purity**
  - No code MUST be committed that fails the project's mandatory static analysis checks (e.g., `tsc`, `lint`, `type-check`).
- **[REQ-TCH-09] Narrative Function Decomposition**
  - Complex logic MUST be decomposed into a series of small, intent-revealing functions that follow the project's storytelling pattern.
- **[REQ-TCH-10] Explicit Context Injection**
  - Internal dependencies SHOULD be injected via context or providers rather than being hardcoded inside the functional logic.

### Must Not

- **[BAN-TCH-01] Implicit Global Dependecies**
  - Do NOT rely on undocumented global states or environmental variables; utilize explicit configuration injection.
- **[BAN-TCH-02] Prototype Pollution**
  - Avoid modifying native prototypes or adding global side-effects that could impact the stability of the overall tech stack.

### Failure Handling

- **Stop Condition**: Stop feature development if a new component is identified as introducing a "Type Hole" (using `any`) in a critical data path.

## 2. Procedures

- **[PROC-TCH-01] Type-Safety Audit**
  - IF adding a new library THEN MUST verify that its type definitions align with the project's strictness requirements.
- **[PROC-TCH-02] Pattern Verification**
  - Conduct a manual pattern review for all major feature additions to ensure adherence to the project's established technical blueprints.

## 3. Examples

### compliant Interface (Good)

```typescript
interface UserProfile {
  id: string;
  email: string; // Explicit type
  isActive: boolean;
}
```

## 4. Validation Criteria

- **[VAL-TCH-01] Zero-Any Policy Pass**
  - [ ] build scripts confirm that 100% of the project's TypeScript files pass the `noImplicitAny` check.
- **[VAL-TCH-02] Interface Accuracy**
  - [ ] audit confirms that all external-facing modules possess explicit, documented interfaces.
- **[VAL-TCH-03] Pattern Consistency**
  - [ ] Review confirms that > 95% of new code aligns with the established technical stack patterns.
