---
description: Workflow for building high-performance APIs with FastAPI
---

1. **Project Scaffolding**

    Initialize project structure and dependencies.

    // turbo

    ```bash
    # Create project directory
    mkdir fastapi-project
    # (User needs to cd in, not safe to auto cd)
    ```

2. **Environment Setup**

    Configure virtual environment and dependencies.

    ```bash
    python -m venv .venv
    # Activate manually: source .venv/bin/activate
    uv pip install fastapi uvicorn[standard] pydantic-settings sqlalchemy alembic
    ```

3. **Create Main Application**

    Set up `app/main.py`.

    ```python
    from fastapi import FastAPI
    from app.routers import users

    app = FastAPI(title="My API")

    app.include_router(users.router)

    @app.get("/health")
    async def health():
        return {"status": "ok"}
    ```

4. **Database Models (SQLAlchemy)**

    Define models in `app/models/user.py`.

    ```python
    from sqlalchemy.orm import Mapped, mapped_column
    from app.db import Base

    class User(Base):
        __tablename__ = "users"
        id: Mapped[int] = mapped_column(primary_key=True)
        email: Mapped[str] = mapped_column(unique=True)
    ```

5. **Pydantic Schemas**

    Define schemas in `app/schemas/user.py`.

    ```python
    from pydantic import BaseModel, EmailStr

    class UserCreate(BaseModel):
        email: EmailStr
        password: str

    class UserResponse(BaseModel):
        id: int
        email: EmailStr

        class Config:
            from_attributes = True
    ```

6. **API Endpoints**

    Implement routers.

    ```python
    from fastapi import APIRouter, Depends
    from sqlalchemy.orm import Session

    router = APIRouter(prefix="/users", tags=["users"])

    @router.post("/", status_code=201)
    async def create_user(user: UserCreate, db: Session = Depends(get_db)):
        # Implementation
        pass
    ```

7. **Run and Test**

    Start server and verify.

    // turbo

    ```bash
    # Start server (dev mode)
    uvicorn app.main:app --reload
    ```

    // turbo

    ```bash
    # Run tests
    pytest
    ```
