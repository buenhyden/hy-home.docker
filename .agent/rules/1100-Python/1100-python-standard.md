---
trigger: model_decision
glob: ["**/*.py"]
description: "Python Standards: Enforces PEP 8, strict type hints, async-first I/O, and idiomatic project structures."
---

# Python Development Standards

- **Role**: Senior Python Engineer
- **Purpose**: Define standards for writing idiomatic, maintainable, and highly performant Python code across the application stack.
- **Activates When**: Developing Python backend services, writing automation scripts, or managing Python library dependencies.

**Trigger**: model_decision — Apply during the design and implementation of Python-based logic.

## 1. Standards

### Principles

- **[REQ-PY-01] Type-Hinted Totality (PEP 484)**
  - All public function signatures and complex class attributes MUST include explicit type hints. Use `mypy` or `pyright` for static verification.
- **[REQ-PY-02] Async-First Concurrency**
  - Network-bound and I/O operations MUST utilize `asyncio` (async/await) to ensure non-blocking execution and high throughput.
- **[REQ-PY-03] Idiomatic Modernity (3.10+)**
  - Leverage modern Python features such as structural pattern matching (`match`), union types (`|`), and parenthesized context managers.

### Python Stack Baseline

| Category | Requirement ID | Critical Tooling |
| --- | --- | --- |
| Linting | [REQ-PY-04] | `Ruff` (Performance-first) |
| Formatting | [REQ-PY-05] | `Black` / `Ruff format` |
| Testing | [REQ-PY-06] | `pytest` with `pytest-asyncio` |
| Typing | [REQ-PY-07] | `mypy` (Strict mode) |

### Must

- **[REQ-PY-08] Google-Style Docstrings**
  - All public modules, classes, and functions MUST include Google-style docstrings describing parameters, return types, and exceptions.
- **[REQ-PY-09] Explicit Error Propagation**
  - Avoid generic `Exception` catches. Catch specific error types and utilize custom exception hierarchies for domain-specific faults.
- **[REQ-PY-10] Standardized Virtualization**
  - Every project MUST utilize a dependency management tool (e.g., `Poetry`, `uv`, or `pipenv`) with a checked-in lockfile.

### Must Not

- **[BAN-PY-01] Wildcard Imports**
  - The use of `from module import *` is STRICTLY PROHIBITED as it pollutes the namespace and prevents static analysis.
- **[BAN-PY-02] Blocking I/O in Async**
  - Do NOT call synchronous blocking functions (e.g., `time.sleep`, `requests.get`) inside an `async def` function; use `asyncio.sleep` or `httpx`.

### Failure Handling

- **Stop Condition**: Stop feature execution if `mypy` or `ruff` returns "Critical" level errors during the pre-commit or CI phase.

## 2. Procedures

- **[PROC-PY-01] Type Coverage Check**
  - IF adding a new module THEN MUST verify that its type hint coverage is > 95% using `mypy`.
- **[PROC-PY-02] Linting Lifecycle**
  - Automatically run the `ruff check --fix` command before every commit to maintain consistent code style.

## 3. Examples

### Typed Async Function (Good)

```python
async def fetch_item(item_id: int) -> dict | None:
    """Fetch item by ID from the remote repository.
    Args:
        item_id: Primary key of the item.
    Returns:
        The item dictionary or None if not found.
    """
    return {"id": item_id}
```

## 4. Validation Criteria

- **[VAL-PY-01] Mypy Integrity**
  - [ ] Static analysis verifies that all function signatures align with their respective call-sites.
- **[VAL-PY-02] Formatter Pass**
  - [ ] `Black` or `Ruff` confirms zero formatting diffs in the current workspace.
- **[VAL-PY-03] Async Throughput**
  - [ ] Concurrent tests verify that the event loop is not blocked by synchronous implementation details.
