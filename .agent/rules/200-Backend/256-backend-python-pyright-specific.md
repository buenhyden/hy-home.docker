---
trigger: always_on
glob: "**/*.py"
description: "Pyright/BasedPyright Standards: Strict typing layout and configuration."
---
# Pyright & Type Checking Standards

## 1. Configuration

- **File**: `pyrightconfig.json` or `[tool.pyright]`.
- **Strictness**: Enable `strict` mode for new code.
- **BasedPyright**: Preferred over standard Pyright for stricter defaults (`reportAny`, `reportExplicitAny`).

## 2. Strict Rules (Essential)

- `"reportAny": "error"`: Ban implicit `Any`.
- `"reportExplicitAny": "error"`: Ban explicit `Any` unless strictly necessary.
- `"reportMissingTypeStubs": "error"`: Ensure all dependencies are typed.

## 3. Type Patterns

- **Aliases**: Use `TypeAlias` (Python 3.10+) for clarity.
- **Unions**: Use `X | Y` syntax (Python 3.10+).
- **Protocols**: Prefer `Iterable`, `Sequence`, `Mapping` for arguments (Duck Typing).
- **Concrete Returns**: Return concrete types (`list`, `dict`) unless abstractness is required.

## 4. Ignores

- **Specific**: Use specific error codes for ignores: `# pyright: ignore[reportGeneralTypeIssues]`.
- **Comment**: Explain *why* the ignore is safe.

## 5. CI/CD

- **Gate**: Type checking must pass in CI/CD pipeline.
- **Stubs**: Maintain a `stubs/` folder for untyped libraries.
