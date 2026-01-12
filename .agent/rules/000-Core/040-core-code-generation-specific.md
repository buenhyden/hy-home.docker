---
trigger: always_on
glob: "**/*.{php,js,ts,vue,jsx,tsx,py,rb,java}"
description: "Code Generation: Standards for high-quality, executable code generation."
---
# Code Generation Standards

## 1. Completeness

- **No Placeholders**: Never use `// TODO:`, `pass`, or stub methods (e.g., `return null` without logic) unless explicitly requested.
- **Implement Full Logic**: Generated code must be fully functional and handle edge cases.

## 2. Conditionals

- **No Dead Logic**: Remove conditions that are always `false` or unreachable code.
- **Valid Logic**: Ensure `if` statements check for real, possible states.

## 3. Logging & Comments

- **Logging Standards**: See [050-core-debugging-specific.md](./050-core-debugging-specific.md) for comprehensive logging standards including production rules.
- **Type Hints**: In Python, use type annotation syntax (`x: int`) over comment-based annotations (`# type: int`).

### Example: Completeness

#### Good

```javascript
function calculateTotal(items) {
  if (!items || items.length === 0) return 0;
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

#### Bad

```javascript
function calculateTotal(items) {
  // TODO: implement this
  return 0;
}
```

## See Also

- [000-core-general.md](./000-core-general.md) - Core coding standards
- [050-core-debugging-specific.md](./050-core-debugging-specific.md) - Logging and debugging standards
