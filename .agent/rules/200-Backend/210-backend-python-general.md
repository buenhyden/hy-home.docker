---
trigger: always_on
glob: "**/*.py"
description: "Python General: Type Hints, Modern Tooling (uv/ruff), and Testing."
---
# Python General Standards

## 1. Type Hints (Strict)

- **Signatures**: ALL functions must have typed arguments and return types.
- **No Any**: Use `object` if you really mean "anything", or `TypeVar` for generics. Avoid `Any`.

### Example: Typing

**Good**

```python
def process_items(items: list[str]) -> int:
    return len(items)
```

**Bad**

```python
def process_items(items): # Missing types
    return len(items)
```

## 2. Code Style

- **Explicit**: Avoid "magic" context locals (like Flask's global `request`). Pass dependencies explicitly.
- **Exceptions**: Catch specific errors. Never `except:`.

### Example: Exceptions

**Good**

```python
try:
    data = json.loads(payload)
except json.JSONDecodeError:
    logger.error("Invalid JSON")
```

**Bad**

```python
try:
    data = json.loads(payload)
except: # Catches KeyboardInterrupt too!
    pass
```

## 3. Toolchain & Quality Standards

- **Black**: Uncompromising code formatter.
- **Isort**: Import sorter.
- **Pylint**: Semantic analysis and code smells.
- **Pyright**: Strict static type checking.

## 4. Configuration (pyproject.toml)

- **Centralized**: ALL tools configured in `pyproject.toml`.
- **Strictness**: Enable explicit `Any` reporting and strict mode.

### Example: pyproject.toml

```toml
[tool.black]
line-length = 88

[tool.isort]
profile = "black"

[tool.pyright]
typeCheckingMode = "strict"
reportAny = true
reportExplicitAny = true
```

## 5. Coding Standards

- **Formatting**: Run `black` and `isort` pre-commit.
- **Type Aliases**: Use `TypeAlias` for complex types.
- **Casting**: Use `cast()` carefully.
