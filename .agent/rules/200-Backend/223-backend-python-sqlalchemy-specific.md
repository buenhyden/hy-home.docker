---
trigger: always_on
glob: "**/*.py"
description: "SQLAlchemy 2.x Best Practices: Modern ORM patterns, type safety, and efficient querying."
---
# SQLAlchemy Standards

## 1. Modern API (2.0 Style)

- **DeclarativeBase**: Use `DeclarativeBase` and `Mapped` for model definitions. Avoid legacy `declarative_base()` and untyped `Column`.
- **Select**: ALWAYS use `select()` constructs (`session.execute(select(User))`). Deprecate `session.query()`.

### Example: Model Definition

**Good**

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
```

## 2. Session Management

- **Context Managers**: ALWAYS use `Session` as a context manager.
- **Transactions**: For complex atomic operations, use `with session.begin():`.

### Example: Session

**Good**

```python
with Session(engine) as session:
    user = User(name="Alice")
    session.add(user)
    session.commit()
```

## 3. Query Optimization

- **Eager Loading**: Prevent N+1 issues by using `selectinload` (for collections) or `joinedload` (for many-to-one) in options.

## 4. Migrations

- **Alembic**: Use Alembic for all schema changes (`alembic revision --autogenerate`). Never modify the DB manually in production.
