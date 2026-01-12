---
description: Run Database Migrations (Alembic/Prisma/TypeORM)
---

1. **Identify Migration Tool**

    Check `alembic.ini`, `schema.prisma`, or `package.json` to determine the ORM.

2. **Generate Migration**

    Create a new migration file based on schema changes.

    - **Alembic**: `alembic revision --autogenerate -m "description"`
    - **Prisma**: `npx prisma migrate dev --name description`
    - **TypeORM**: `npm run typeorm migration:generate -- -n Description`

// turbo
3. **Apply Migration**

    Apply the migrations to the local database.

    ```bash
    # Auto-detect and run

    if [ -f "alembic.ini" ]; then
        alembic upgrade head
    elif [ -f "schema.prisma" ]; then
        npx prisma migrate deploy
    fi
    ```

4. **Verify Database**

    Check if the tables are updated correctly.
