---
trigger: always_on
glob: "**/*.py"
description: "Unittest Best Practices: Structure, assertions, and mocking."
---
# Unittest Standards

## 1. Structure

- **Naming**: Methods must start with `test_`. Class names must start with `Test`.
- **Main**: Always include `if __name__ == '__main__': unittest.main()` for discoverability.

### Example: Class

**Good**

```python
import unittest

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(1 + 1, 2)
```

## 2. Assertions

- **Specificity**: Use specific assert methods (`assertIn`, `assertIsNone`, `assertRaises`) instead of generic `assertTrue/False` for better failure messages.
- **One Logical Assert**: Each test should verify one logical condition.

## 3. Mocking

- **Patch**: Use `unittest.mock.patch` as a decorator or context manager.
- **Spec**: Prefer `autospec=True` in patches to ensure mocks adhere to the API of the real object.

### Example: Mock

**Good**

```python
@patch('module.external_call', autospec=True)
def test_external(self, mock_call):
    mock_call.return_value = 'mocked'
    # ...
```
