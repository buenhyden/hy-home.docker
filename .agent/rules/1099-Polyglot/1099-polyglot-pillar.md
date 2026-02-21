---
trigger: always
glob: ["**/*"]
description: "Language & Toolset Pillar Standard (Polyglot). Enforces high-performance, type-safe protocols across Python (uv/ruff), TypeScript (Zod/Vitest), Go, and Rust."
---

# 1099-Polyglot-Pillar

- **Role**: Polyglot Quality Architect
- **Purpose**: Enforce unified, type-safe, and high-performance standards across all languages.
- **Activates When**: Writing code in Python, TypeScript, Go, or Rust.

## 1. Standards

### 1.1 Universal Principles

- **[REQ-POLY-FMT-01] Formatting**: You MUST use automated formatters (Prettier, Ruff, gofmt).
- **[REQ-POLY-LINT-01] Zero Tolerance**: Lint errors are build blockers. Fix them immediately.
- **[REQ-POLY-MOD-01] Modularity**: Functions MUST be small and testable (Single Responsibility).

### 1.2 TypeScript/JavaScript (Strict)

- **[REQ-TS-STR-01] Strict Mode**: `strict: true` is MANDATORY.
- **[REQ-TS-NOANY-01] No Any**: Use `unknown` or Zod schemas. `any` is FORBIDDEN.
- **[REQ-TS-TOOL-01] Tooling**: Use **Vitest** for testing and **Zod** for validation.

### 1.3 Python (Modern)

- **[REQ-PY-TYP-01] Type Hints**: All function signatures MUST be typed.
- **[REQ-PY-TOOL-01] Tooling**: Use **uv** for deps, **Ruff** for linting, **Mypy** for typing.

### 1.4 Go & Rust (Systems)

- **[REQ-GO-ERR-01] Error Wrapping**: Wrap errors with context: `fmt.Errorf("...: %w", err)`.
- **[REQ-RS-OWN-01] Safety**: `unwrap()` is FORBIDDEN in production. Handle `Option/Result`.

## 2. Procedures

### 2.1 Quality Gate

1. **Format**: Apply auto-formatting.
2. **Lint**: Check for logic errors.
3. **Type**: Verify strict type safety.
4. **Test**: Run unit tests (Vitest/Pytest).

## 3. Examples

### 3.1 Strict TypeScript

```typescript
// Good
const UserSchema = z.object({ id: z.string().uuid() });
type User = z.infer<typeof UserSchema>;

// Bad
const user: any = { id: "123" };
```

## 4. Validation Criteria

- [ ] **[VAL-POLY-TYP-01]** No missing type signatures.
- [ ] **[VAL-POLY-LINT-01]** Linter passes with 0 warnings.
- [ ] **[VAL-POLY-FMT-01]** Code is auto-formatted.
