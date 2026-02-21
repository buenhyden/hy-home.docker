---
trigger: model_decision
glob: ["**/*.ts", "**/*.tsx"]
description: "TypeScript Standards: Enforces strict type safety, runtime validation (Zod), and modern ESM patterns."
---

# TypeScript Development Standards

- **Role**: TypeScript Architecture Lead
- **Purpose**: Define standards for writing type-safe, maintainable, and highly efficient TypeScript code that bridges the gap between static analysis and runtime safety.
- **Activates When**: Developing TypeScript-based modules, defining complex data schemas, or managing type-level infrastructure.

**Trigger**: model_decision — Apply during all TypeScript development activities.

## 1. Standards

### Principles

- **[REQ-TS-01] Strict Totality**
  - All projects MUST enable `strict: true` in `tsconfig.json`. The use of `any` is strictly PROHIBITED; use `unknown` for indeterminate types.
- **[REQ-TS-02] Contract-First Validation**
  - All external data (API responses, File I/O) MUST be validated at the system boundary using `Zod` or an equivalent schema library.
- **[REQ-TS-03] Modern ESM Patterns**
  - Favor ES6 modules (import/export) and top-level await where supported. Avoid namespaces and legacy CommonJS patterns.

### Type System Baseline

| Category | Requirement ID | Critical Application |
| --- | --- | --- |
| Validation | [REQ-TS-04] | `z.parse()` for all external inputs |
| Safety | [REQ-TS-05] | Type narrowing for `unknown` types |
| Immutability | [REQ-TS-06] | `readonly` for interfaces & arrays |
| Async | [REQ-TS-07] | `async/await` over `.then()` chains |

### Must

- **[REQ-TS-08] Interface Primacy**
  - Prefer `interface` over `type` for defining public object shapes to leverage declaration merging and better IDE diagnostics.
- **[REQ-TS-09] Explicit Return Types**
  - High-level exports and complex functions MUST have explicit return type annotations to prevent unintentional type leakage.
- **[REQ-TS-10] Constant Assertions**
  - Use `as const` assertions for literal objects and arrays to ensure they are treated as immutable literal types.

### Must Not

- **[BAN-TS-01] Enum Usage**
  - Do NOT use TypeScript `enums`; utilize String Unions or `const` objects with `typeof` for better tree-shaking and safety.
- **[BAN-TS-02] Casting via 'as'**
  - Avoid brute-force type casting (e.g., `x as T`) unless interacting with non-typed external libraries or during unit tests.

### Failure Handling

- **Stop Condition**: Stop feature execution if the TypeScript compiler (`tsc`) emits any errors or if `Zod` identifies a schema mismatch at a runtime boundary.

## 2. Procedures

- **[PROC-TS-01] Schema-to-Type Flow**
  - IF defining a new data model THEN MUST define the `Zod` schema first and derive the TypeScript type using `z.infer`.
- **[PROC-TS-02] Type Audit**
  - Perform a monthly audit of the codebase to identify and eliminate any instances of `any` that may have been introduced as placeholders.

## 3. Examples

### Safe Schema Inference (Good)

```typescript
const UserSchema = z.object({ id: z.string().uuid() });
type User = z.infer<typeof UserSchema>;
```

## 4. Validation Criteria

- **[VAL-TS-01] Strict Mode Verification**
  - [ ] `tsconfig.json` confirms `strict: true` is active across the entire project.
- **[VAL-TS-02] Zero-Any Policy**
  - [ ] Automated code audit confirms zero occurrences of the `any` keyword in application-level code.
- **[VAL-TS-03] Validation Presence**
  - [ ] Every entry point for external data is protected by a verified `Zod` schema.
