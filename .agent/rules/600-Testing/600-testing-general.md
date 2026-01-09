---
trigger: always_on
glob: "**/*.{test,spec}.*"
description: "QA & Testing Core: Testing Pyramid, AAA Pattern, and Automation."
---
# QA & Testing General Standards

## 1. The Testing Pyramid

- **Unit Tests (Base)**: 70-80% of your tests. Focus on individual functions/logic in isolation. Mock *all* external dependencies.
- **Integration Tests (Middle)**: 15-20% of your tests. Focus on the interaction between components (e.g., Service + DB).
- **E2E Tests (Top)**: 5-10% of your tests. Focus on the full user journey (e.g., Login -> Dashboard).

## 2. Test Separation and Mocking

- **Separation**: Test code MUST be completely separated from production code (e.g., `tests/` vs `src/`). Do not modify production code solely for testing (use Dependency Injection).
- **Mocking**:
  - **External**: Always mock external APIs (Stripe, Twilio) in Unit/Integration tests.
  - **DI**: Use Dependency Injection to swap real implementations with Stubs/Mocks.
  - **Verification**: Verify that mocks are called with expected arguments, not just that they return a value.

## 3. The AAA Pattern

- **Arrange**: Set up the initial state and dependencies.
- **Act**: Execute the function or behavior being tested.
- **Assert**: Verify the actual outcome matches the expected outcome.

### Example: AAA

**Good**

```javascript
test('should add item to cart', () => {
  // Arrange
  const cart = new Cart();
  const item = { id: 1, name: 'Apple' };
  
  // Act
  cart.addItem(item);
  
  // Assert
  expect(cart.items).toHaveLength(1);
  expect(cart.items[0].name).toBe('Apple');
});
```

**Bad**

```javascript
test('test cart', () => {
  const c = new Cart();
  c.addItem({id:1});
  // No assertions? Or mixing Act/Assert.
});
```

## 3. Automation & Quality

- **Deterministic**: Tests must be 100% reliable. "Flaky" tests should be quarantined or fixed immediately.
- **No Side Effects**: Tests should clean up their own data (DB, Mapped files).
- **Independence**: A test failure in Module A should not cause tests in Module B to fail if they are unrelated.

## 4. Coverage vs Quality

- **Focus**: Aim for 100% coverage of *critical business logic*, not just 100% line coverage of boilerplate.
- **Edge Cases**: Always test nulls, empty collections, and boundary values.
- **Mutations**: Periodically use Mutation Testing to ensure your assertions are actually catching bugs.

## 5. Test Naming Standards

- **Pattern**: `should_[expected]_when_[condition]` or `test_[feature]_[scenario]`.
- **Descriptive**: Name must describe variable scenario and expected outcome.

```python
def test_user_creation_returns_201_when_valid_data(): ...
```

## 6. Test Data Management

- **Factories**: Use factories (Factory Boy, Faker) over static JSON fixtures.
- **Isolation**: Each test creates its own data.
