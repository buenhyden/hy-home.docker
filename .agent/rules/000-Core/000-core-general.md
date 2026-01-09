---
trigger: always_on
glob: "*"
description: "Core Code Guidelines: Clean Code, SOLID, Testing Mindset, and Error Handling."
---
# Core Code Guidelines: General Standards

## 1. Clean Code Philosophy

- **Intent-Revealing**: Code must be self-documenting. Use variable names that describe *what* they hold.
- **Functions**: Should be small, strictly focused (SRP), and have no side effects (Pure) where possible.
- **Comments**: Code explains *how*; Comments explain *why*. Delete commented-out code immediately (Git has history).

### Example: Intent

**Good**

```python
def calculate_monthly_revenue(bookings: List[Booking]):
    """Calculates total revenue from a list of bookings."""
    return sum(b.price for b in bookings if b.is_confirmed)
```

**Bad**

```python
def calc(b):
    # This function calculates revenue
    s = 0
    for x in b:
        if x.c: s += x.p
    return s
```

## 2. SOLID & Architecture

- **SRP (Single Responsibility)**: A class/function should have only one reason to change.
- **Open/Closed**: Open for extension (interfaces/plugins), closed for modification.
- **Composition over Inheritance**: Prefer building behavior by combining small objects rather than deep inheritance chains.

### Example: Composition

**Good**

```typescript
class User {
    constructor(private auth: AuthMethod) {} // Inject behavior
}
```

**Bad**

```typescript
class GoogleUser extends User { ... } // Fragile hierarchy
class FacebookUser extends User { ... }
```

## 3. Testability & Dependency Injection

- **Inversion of Control**: Never instantiate heavy dependencies (Database, API Client) inside a class. Pass them in constructor/arguments.
- **Determinism**: Logic should not depend on global state (`Date.now()`, `Math.random()`) directly. Pass values or providers.

### Example: DI

**Good**

```javascript
// Easy to test - pass a mock date
function isExpired(date, now = new Date()) {
    return date < now;
}
```

**Bad**

```javascript
// Hard to test - depends on system time
function isExpired(date) {
    return date < new Date();
}
```

## 4. Error Handling

- **Exceptions**: Use Exceptions for exceptional states (Disk full, Network down), NOT for control flow.
- **Fail Fast**: Validate inputs immediately. Don't process half the data then crash.
- **Safe Defaults**: Return "Null Object" or empty collections (`[]`, `""`) instead of `null` when valid.

## 5. Naming High-Level

*(See `005-core-naming-specific.md` for detailed syntax rules)*

- **No Magic**: Avoid magic numbers/strings. specialized constants over literals (`MAX_RETRIES` vs `5`).

## 6. Language-Specific Quality Standards

### Python

- **Formatter**: `Black` (line length 88).
- **Sorter**: `Isort` (profile black).
- **Linter**: `Flake8` or `Ruff`.
- **Typing**: `Mypy` (strict mode).

### JavaScript/TypeScript

- **Formatter**: `Prettier`.
- **Linter**: `ESLint`.
- **Check**: `tsc --noEmit`.

## 7. Quality Process

1. **Format First**: Run automated formatters (Prettier/Black) to fix style.
2. **Lint Second**: Fix logical issues caught by linters.
3. **Type Check**: Ensure type safety (Mypy/TSC).
4. **Review**: Self-review for readability, variable naming, and function size.
