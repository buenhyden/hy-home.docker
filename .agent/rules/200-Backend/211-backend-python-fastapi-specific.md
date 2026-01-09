---
trigger: always_on
glob: "**/*.py"
description: "FastAPI: Pydantic V2, Dependency Injection, and Async Patterns."
---
# FastAPI Standards

## 1. Pydantic V2

- **Config**: Use `model_config = ConfigDict(frozen=True)` for immutability.
- **Validation**: Use `Field(..., gt=0)` for declarative validation.

### Example: Schema

**Good**

```python
from pydantic import BaseModel, ConfigDict, Field

class UserCreate(BaseModel):
    model_config = ConfigDict(frozen=True)
    username: str = Field(..., min_length=3)
```

**Bad**

```python
class UserCreate(BaseModel):
    username: str # No validation
```

## 2. Dependency Injection

- **Session**: Always inject DB sessions using `Depends()`. Never create them manually in routes.
- **Annotated**: Use `Annotated` for cleaner signatures.

### Example: Injection

**Good**

```python
@router.get("/users")
async def get_users(db: Annotated[AsyncSession, Depends(get_db)]):
    ...
```

**Bad**

```python
@router.get("/users")
async def get_users():
    db = await get_db() # Hard To Mock
    ...
```

## 3. Async DB

- **I/O**: Use `await db.execute()` for all SQL operations.
- **404**: Raise `HTTPException(404)` explicitly if not found.
