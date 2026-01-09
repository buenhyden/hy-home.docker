---
trigger: always_on
glob: "**/*.{test,spec}.{js,ts,py}"
description: "API Testing: Contract testing, Integration, and Mocking."
---
# API Testing Standards

## 1. Contract Testing

- **Validation**: Ensure response schema matches the documentation (OpenAPI/Swagger).
- **Types**: Use tools like `supertest` (Node.js), `tavern` (Python), or `RestAssured` (Java).

### Example: Contract Check

**Good (Supertest)**

```javascript
const response = await request(app).get('/api/users/1');
expect(response.status).toBe(200);
expect(response.body).toMatchSchema(userSchema);
```

**Bad**

```javascript
const response = await fetch('/api/users/1');
// No schema validation, only checking status
expect(response.status).toBe(200);
```

## 2. Statelessness

- **Isolation**: Each test should create its own data or reset the database.
- **Order**: Tests must pass regardless of execution order.

### Example: Setup

**Good**

```python
def test_get_user(client):
    user = create_dummy_user() # Unique user for this test
    response = client.get(f"/users/{user.id}")
```

**Bad**

```python
def test_get_user(client):
    # Relies on user with ID 1 already existing in DB
    response = client.get("/users/1")
```

## 3. Negative Testing

- **Error Cases**: Explicitly test `401`, `403`, `404`, and `422` (Validation) responses.
- **Edge cases**: Test empty payloads, long strings, and invalid types.
