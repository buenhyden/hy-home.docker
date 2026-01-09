---
trigger: always_on
glob: "**/*.py"
description: "Python Documentation: Google-style docstrings and pdoc integration."
---
# Python Documentation Standards (pdoc)

## 1. Docstring Format

- **Style**: ALWAYS use **Google Style** docstrings.
- **Coverage**: All public modules, classes, functions, and methods must be documented.
- **Structure**:
  1. **Summary Line**: Concise command (e.g., "Calculates user retention.").
  2. **Description**: Context and details.
  3. **Args**: Parameters with types.
  4. **Returns**: Return value and type.
  5. **Raises**: Potential exceptions.
  6. **Example**: Doctest-compatible example.

## 2. Type Hints

- **Mandatory**: All function signatures MUST have type hints. `pdoc` uses these for navigation.
- **Specificity**: Use `List[str]` over `list`, `Optional[int]` over `int`.

## 3. Pdoc Integration

- ****all****: Define `__all__` in `__init__.py` to control what `pdoc` generates.
- **Visibility**: Use `_` prefix for internal members to hide them from docs.

### Example: Google Style Docstring

#### Good

```python
from typing import List, Optional

def process_items(items: List[str], retry_count: int = 3) -> Optional[int]:
    """Processes a list of items with retry logic.

    Iterates through items and performs processing. If processing fails,
    it retries up to `retry_count` times.

    Args:
        items (List[str]): List of item IDs to process.
        retry_count (int): Maximum number of retries. Defaults to 3.

    Returns:
        Optional[int]: The number of successfully processed items, 
        or None if critical error occurred.

    Raises:
        ValueError: If `items` is empty.

    Example:
        >>> process_items(["a", "b"])
        2
    """
    if not items:
        raise ValueError("Items list cannot be empty")
    # ... implementation
    return len(items)
```
