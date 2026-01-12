---
trigger: always_on
glob: "**/*.{py,md}"
description: "Documentation Tools: Best practices for pdoc and automated docs."
---
# Documentation Tools Standards

## 1. Python (`pdoc`)

- **Docstrings**: Use Google Style docstrings.
- **Type Hints**: Mandatory for `pdoc` to generate accurate API signatures.
- **`__all__`**: Use `__all__` to explicitly control public API exposure.

## 2. Automation

- **CI/CD**: Generate docs on merge to main.
- **Formats**: Create LLM-friendly documentation (concise, minimal, reference-heavy) alongside human docs.

### Example: Docstring

#### Good

```python
def fn(x: int) -> int:
    """Calculates square.
    
    Args:
        x (int): Input.
    
    Returns:
        int: Squared value.
    """
    return x * x
```
