---
trigger: always_on (during analysis phases)
glob: "*"
description: Methodology for analyzing and maintaining code style consistency.
---

# Code Style Consistency Rules

## 1. Analysis Methodology

Before writing new code, analyze 3-5 existing files to establish the **Style Profile**:

### Style Profile Checklist

1. **Naming**: `camelCase` vs `snake_case` for variables, functions, files.
2. **Formatting**: Indentation (Spaces/Tabs), Line length, Brackets.
3. **Patterns**: Functional vs OOP, Error handling (try/catch vs Result), Async patterns.
4. **Documentation**: Comment density, Docstring format.
5. **Testing**: Framework, naming convention (`should_` vs `test_`).

## 2. Adaptation Principles

- **No Inventions**: Do not introduce new libraries or paradigms unless necessary.
- **Consisteny > Perfection**: It is better to be consistent with a "okay" pattern than to introduce a "perfect" but alien pattern (Local Consistency).
- **Pattern Mirroring**: Structure new modules exactly like existing similar modules.

## 3. Adaptation Techniques

- **Import Order**: Replicate the grouping and sorting of imports.
- **Error Pattern**: Use the same error classes and handling structure.
- **State Management**: strict adherence to existing stores (Redux, Zustand, Context).

## 4. Verification

- Verify that the new code "looks like" it was written by the original author.
- Ensure no linting errors are introduced based on project config.
