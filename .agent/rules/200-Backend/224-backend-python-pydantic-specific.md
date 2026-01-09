---
trigger: always_on
glob: "**/*.py"
description: "Pydantic V2 Best Practices: Strict validation, settings management, and model organization."
---
# Pydantic Standards

## 1. Validation & Types

- **Strict Types**: Use `StrictInt`, `StrictFloat`, etc., where coercion is unwanted.
- **Immutability**: Prefer `ConfigDict(frozen=True)` for data models to prevent side effects.

### Example: Configuration

**Good**

```python
from pydantic import BaseModel, ConfigDict, EmailStr

class User(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: int
    email: EmailStr
```

## 2. Settings Management

- **BaseSettings**: Use `pydantic_settings.BaseSettings` for app configuration. Store secrets in `SecretStr`.

### Example: Settings

**Good**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url: str
    api_key: SecretStr
```

## 3. Validation Logic

- **Validators**: Use `@field_validator` for single fields and `@model_validator` for cross-field validation. Keep logic concise.

## 4. Performance

- **V2 Core**: Leverage Pydantic V2's Rust core. Avoid defining custom `__init__` if possible; let Pydantic handle initialization.
