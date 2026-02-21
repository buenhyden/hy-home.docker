---
trigger: always_on
glob: "**/*.{ts,tsx}"
description: "Advanced TypeScript Patterns: Enforces strict type safety, utility types, and advanced generic patterns."
---

# Advanced TypeScript Patterns

- **Role**: TypeScript Language Architect
- **Purpose**: Define standards for high-level type engineering, ensuring maximum safety and reusability through advanced TS features.
- **Activates When**: Developing complex TypeScript libraries, defining application state shapes, or engineering reusable generic utilities.

**Trigger**: always_on — Apply during the design and implementation of TypeScript-based systems.

## 1. Standards

### Principles

- **[REQ-TSAD-01] Strict Type Totality**
  - Applications MUST enable all `strict` compiler flags. The `any` type is strictly PROHIBITED; use `unknown` for truly indeterminate types.
- **[REQ-TSAD-02] Contract-First Interfaces**
  - Prefer `interface` over `type` for defining public object shapes to leverage declaration merging and better error messages.
- **[REQ-TSAD-03] Intentional Immutability**
  - Use `readonly` and `as const` assertions to enforce immutability at the type level for configuration and static data.

### Advanced Type Framework

| Feature | Requirement ID | Use Case |
| --- | --- | --- |
| Utility Types | [REQ-TSAD-04] | `Pick`, `Omit`, `Partial` transformations |
| Discriminated Unions | [REQ-TSAD-05] | Type-safe state management |
| Conditional Types | [REQ-TSAD-06] | Dynamic type resolution based on input |
| Template Literals | [REQ-TSAD-07] | String-based type manipulation |

### Must

- **[REQ-TSAD-08] Satisfies Operator Audit**
  - Use the `satisfies` operator to validate object shapes without losing the specificity of their inferred types.
- **[REQ-TSAD-09] Type Guards & Assertions**
  - Use User-Defined Type Guards (`is` keyword) to narrow types safely at runtime boundaries.
- **[REQ-TSAD-10] Exhaustive Switch Checks**
  - Discriminated union handling MUST include an exhaustive `never` check to ensure all cases are covered.

### Must Not

- **[BAN-TSAD-01] Implicit Any**
  - Logic MUST NOT rely on implicit `any`; every function signature and complex object MUST have an explicit or inferred type.
- **[BAN-TSAD-02] Unsafe Type Assertions**
  - Avoid brute-force type assertions (e.g., `as T`) unless absolutely necessary for external library interop.

### Failure Handling

- **Stop Condition**: Stop the build if the TypeScript compiler emits any type-level errors or unreachable code warnings.

## 2. Procedures

- **[PROC-TSAD-01] Type Documentation**
  - IF defining a complex utility type THEN MUST provide JSDoc examples demonstrating its usage.
- **[PROC-TSAD-02] Version Alignment**
  - Ensure the project utilizes the latest stable TypeScript version to leverage modern features like `satisfies`.

## 3. Examples

### Exhaustive Match (Good)

```typescript
type Shape = { type: 'circle', radius: number } | { type: 'square', size: number };

function getArea(shape: Shape) {
  switch (shape.type) {
    case 'circle': return Math.PI * shape.radius ** 2;
    case 'square': return shape.size ** 2;
    default: const _ex: never = shape; return _ex;
  }
}
```

## 4. Validation Criteria

- **[VAL-TSAD-01] Strict Mode Pass**
  - [ ] `tsconfig.json` verifies that `strict: true` and `noImplicitAny: true` are active.
- **[VAL-TSAD-02] Type Coverage**
  - [ ] Codebase audit confirms zero usage of the `any` type in application-level logic.
- **[VAL-TSAD-03] Generic Resilience**
  - [ ] Reusable utilities pass unit tests with multiple diverse generic inputs.
