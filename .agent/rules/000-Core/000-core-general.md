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
- **Consistency**: Match existing project patterns (tab/space, naming, structure) even if they differ from personal preference.
- **DRY (Don't Repeat Yourself)**: Abstract repeated logic into functions or constants.

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
- **Liskov Substitution**: Subtypes must be substitutable.
- **Interface Segregation**: Specific interfaces > General ones.
- **Dependency Inversion**: Depend on abstractions.

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
- **Determinism**: Logic should not depend on global state (Date.now(), Math.random()) directly. Pass values or providers.

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
- **Safe Defaults**: Return "Null Object" or empty collections ([], "") instead of null when valid.

### Assertions

- **Use Assertions Liberally**: Include assertions wherever possible to validate assumptions and catch errors early
- **Document Preconditions**: Assertions serve as executable documentation of function preconditions and invariants
- **Fail Fast with Clear Messages**: Provide descriptive assertion messages to aid debugging

**Example: Assertions**

```python
def process_order(order: Order, user: User):
    assert order is not None, "Order cannot be None"
    assert order.total > 0, f"Order total must be positive, got {order.total}"
    assert user.is_authenticated, "User must be authenticated to process order"
    
    # Process order with confidence in preconditions
    ...
```

```typescript
function calculateDiscount(price: number, discountPercent: number): number {
    console.assert(price >= 0, 'Price must be non-negative');
    console.assert(discountPercent >= 0 && discountPercent <= 100, 'Discount must be 0-100%');
    
    return price * (discountPercent / 100);
}
```

## 5. Naming High-Level

*(See 005-core-naming-specific.md for detailed syntax rules)*

## 6. Language-Specific Quality Standards

### Python

- **Formatter**: Ruff (Primary) + Black.
- **Sorter**: Ruff.
- **Linter**: Ruff (Primary) + Flake8.
- **Typing**: Mypy + ty (Parallel).

### JavaScript/TypeScript

- **Formatter**: Prettier.
- **Linter**: ESLint.
- **Check**:  sc --noEmit.

## 7. Quality Process

1. **Format First**: Run automated formatters (Prettier/Black) to fix style.
2. **Lint Second**: Fix logical issues caught by linters.
3. **Type Check**: Ensure type safety (Mypy/TSC).
4. **Review**: Self-review for readability, variable naming, and function size.

## See Also

- [005-core-naming-specific.md](./005-core-naming-specific.md) - Naming conventions
- [040-core-code-generation-specific.md](./040-core-code-generation-specific.md) - Code generation standards
- [050-core-debugging-specific.md](./050-core-debugging-specific.md) - Debugging and logging
- [091-core-optimization-general.md](./091-core-optimization-general.md) - Performance optimization
