---
trigger: always_on
glob: "**/*.{py,js,ts,java,go}"
description: "Backend Structure: Layered, DDD, DTOs, and Dependency Injection."
---
# Backend Project Structure Standards

## 1. Architecture Patterns

- **Layered (Simple)**: Controller -> Service -> Repository. Okay for small CRUD apps.
- **Domain-Driven (DDD)**: Group by *feature/domain*, not file type. Recommended for complex domains.

### Example: DDD Layout

**Good**

```text
src/
  ├── users/
  │   ├── user.controller.ts
  │   ├── user.service.ts
  │   ├── user.repository.ts
  │   └── user.types.ts
  ├── orders/
  │   └── ...
  └── shared/
```

**Bad**

```text
src/
  ├── controllers/ # Grouped by technical layer
  ├── services/
  └── repositories/
```

## 2. API Boundaries & DTOs

- **DTOs**: STRICT separation between DB Entities (internal) and API Schemas (external).
- **Rule**: Never return a DB model directly from an endpoint.

### Example: Separation

**Good**

```python
class UserResponse(BaseModel): # External
    id: UUID
    username: str

# Internal (DB Model)
class User(Base):
    password_hash = Column(String) # Never exposed
```

**Bad**

```python
return db.query(User).get(id) # Leaks password_hash
```

## 3. Dependency Injection

- **Principle**: Services should receive their dependencies (DB, Clients) via constructor, not instantiate them.
- **Testing**: This makes unit testing trivial (inject mocks).

### Example: DI

**Good**

```typescript
class UserService {
  constructor(private userRepo: UserRepository) {}
}
```

**Bad**

```typescript
class UserService {
  private userRepo = new UserRepository(); // Hardcoded
}
```
