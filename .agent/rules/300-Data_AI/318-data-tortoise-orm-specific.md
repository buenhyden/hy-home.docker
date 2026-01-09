---
trigger: always_on
glob: "**/*.py"
description: "Tortoise ORM: Model Definition, Queries, Async, and Best Practices."
---
# Tortoise ORM Standards

## 1. Model Definition

- **Fields**: Use explicit field types with constraints.
- **Meta**: Define `table` name and `unique_together`.
- **Relationships**: Use `ForeignKeyField`, `ManyToManyField`.

### Example: Model

**Good**

```python
from tortoise import fields, Model

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "users"
```

**Bad**

```python
class User(Model):
    username = fields.CharField()  # No max_length, no constraints
```

## 2. Async Queries

- **await**: Always await query operations.
- **Prefetch**: Use `prefetch_related()` to avoid N+1.
- **Select**: Use `select_related()` for FK joins.

### Example: Queries

**Good**

```python
# Avoid N+1 with prefetch
users = await User.all().prefetch_related('posts')
for user in users:
    print(user.posts)  # Already loaded
```

**Bad**

```python
users = await User.all()
for user in users:
    posts = await user.posts.all()  # N+1 queries!
```

## 3. Transactions

- **atomic()**: Use for multiple operations.
- **Rollback**: Automatic on exception.

### Example: Transaction

**Good**

```python
async with in_transaction():
    user = await User.create(username="alice")
    await Profile.create(user=user, bio="Hello")
```

## 4. Initialization

- **Tortoise.init()**: Call once at startup.
- **Aerich**: Use for migrations.
