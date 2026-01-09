---
trigger: always_on
glob: "**/*.py"
description: "Pytest: Fixtures, Parametrization, Mocking, and Async testing."
---
# Pytest Standards

## 1. Fixtures & Scope

- **Pattern**: Use `conftest.py` for shared fixtures.
- **Scope**: Use `function` (default), `module`, or `session` appropriately.
- **Cleanup**: Use `yield` pattern for teardown.

### Example: Fixture

**Good**

```python
@pytest.fixture
def db_session():
    session = create_session()
    yield session
    session.rollback()
```

**Bad**

```python
# Creating DB connection inline in every test
def test_user():
    session = create_session()
    # ...
    session.rollback() # Manual cleanup, error-prone
```

## 2. Parametrization

- **Data-Driven**: Use `@pytest.mark.parametrize` to test multiple inputs.
- **IDs**: Provide `ids=` for readable failure reports.

### Example: Parametrize

**Good**

```python
@pytest.mark.parametrize("x, expected", [(1, 2), (2, 4)], ids=["one", "two"])
def test_double(x, expected):
    assert x * 2 == expected
```

**Bad**

```python
def test_double_1(): assert 1 * 2 == 2
def test_double_2(): assert 2 * 2 == 4 # Duplication
```

## 3. Mocking (`pytest-mock`)

- **Fixture**: Use `mocker` fixture from `pytest-mock`.
- **Pattern**: `mocker.patch("path.to.class.method", return_value=...)`.

## 4. Async Testing

- **Asyncio**: Use `pytest-asyncio`. Mark tests with `@pytest.mark.asyncio`.
