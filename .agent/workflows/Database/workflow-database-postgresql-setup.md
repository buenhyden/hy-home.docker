---
description: Setup PostgreSQL database with migrations, indexes, and connection pooling
---

1. **Install PostgreSQL client libraries**

    Install the necessary PostgreSQL driver for your language/framework.

    For Python (using psycopg2 or asyncpg):

    ```bash
    # Sync driver
    uv pip install psycopg2-binary
    # or async driver
    uv pip install asyncpg
    ```

    For Node.js (using pg):

    ```bash
    npm install pg
    npm install -D @types/pg  # TypeScript
    ```

    For Go:

    ```bash
    go get github.com/lib/pq
    ```

2. **Setup database connection**

    Create database connection configuration with environment variables.

    **Python (SQLAlchemy) example:**

    Create `database.py`:

    ```python
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    import os

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/mydb"
    )

    engine = create_engine(
        DATABASE_URL,
        pool_size=20,
        max_overflow=0,
        pool_pre_ping=True,  # Verify connections before use
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()


    def get_db():
        """Dependency injection for database sessions."""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    ```

    **Node.js (pg) example:**

    Create `database.ts`:

    ```typescript
    import { Pool } from 'pg';

    const pool = new Pool({
      connectionString: process.env.DATABASE_URL,
      max: 20,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
    });

    pool.on('error', (err) => {
      console.error('Unexpected error on idle PostgreSQL client', err);
      process.exit(-1);
    });

    export default pool;
    ```

3. **Create environment configuration**

    Create `.env` file with database credentials.

    ```bash
    # .env
    DATABASE_URL=postgresql://username:password@localhost:5432/dbname

    # Development
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=myapp_dev
    DB_USER=dev_user
    DB_PASSWORD=dev_password

    # Connection pool
    DB_POOL_SIZE=20
    DB_POOL_MAX_OVERFLOW=10
    ```

    **Important**: Add `.env` to `.gitignore`.

4. **Initialize migration tool**

    Setup database migration management.

    **For Python (Alembic):**

    ```bash
    uv pip install alembic
    alembic init migrations
    ```

    Update `alembic.ini`:

    ```ini
    sqlalchemy.url = postgresql://user:password@localhost:5432/mydb
    ```

    Better: Use environment variable in `migrations/env.py`:

    ```python
    from os import getenv
    config.set_main_option('sqlalchemy.url', getenv('DATABASE_URL'))
    ```

    **For Node.js (TypeORM):**

    ```bash
    npm install typeorm reflect-metadata
    npx typeorm init --database postgres
    ```

    **For Go (golang-migrate):**

    ```bash
    go install -tags 'postgres' github.com/golang-migrate/migrate/v4/cmd/migrate@latest
    migrate create -ext sql -dir migrations create_users_table
    ```

5. **Create initial migration**

    Create first database schema migration.

    **Python (Alembic):**

    ```bash
    alembic revision -m "create users table"
    ```

    Edit the generated migration file in `migrations/versions/`:

    ```python
    from alembic import op
    import sqlalchemy as sa
    from sqlalchemy.dialects.postgresql import UUID
    import uuid


    def upgrade():
        op.create_table(
            'users',
            sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
            sa.Column('email', sa.String(255), unique=True, nullable=False, index=True),
            sa.Column('username', sa.String(50), unique=True, nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        )

        # Create index
        op.create_index('idx_users_email', 'users', ['email'])


    def downgrade():
        op.drop_index('idx_users_email')
        op.drop_table('users')
    ```

    **Node.js (TypeORM):**

    ```typescript
    // src/migrations/1234567890-CreateUsers.ts
    import { MigrationInterface, QueryRunner, Table, TableIndex } from "typeorm";

    export class CreateUsers1234567890 implements MigrationInterface {
      public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.createTable(
          new Table({
            name: "users",
            columns: [
              {
                name: "id",
                type: "uuid",
                isPrimary: true,
                default: "uuid_generate_v4()",
              },
              {
                name: "email",
                type: "varchar",
                length: "255",
                isUnique: true,
                isNullable: false,
              },
              {
                name: "username",
                type: "varchar",
                length: "50",
                isUnique: true,
              },
              {
                name: "created_at",
                type: "timestamp with time zone",
                default: "CURRENT_TIMESTAMP",
              },
            ],
          }),
          true
        );

        await queryRunner.createIndex(
          "users",
          new TableIndex({
            name: "idx_users_email",
            columnNames: ["email"],
          })
        );
      }

      public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.dropTable("users");
      }
    }
    ```

// turbo
6. **Run migrations**

    Apply migrations to create database schema.

    ```bash
    # Python (Alembic)
    alembic upgrade head

    # Node.js (TypeORM)
    npm run typeorm migration:run

    # Go (golang-migrate)
    migrate -path migrations -database "postgresql://localhost:5432/mydb?sslmode=disable" up
    ```

    Expected: Tables created successfully.

7. **Create database indexes**

    Add indexes for query optimization based on `200-Backend/264-backend-database-optimization-specific.md`.

    **Common indexes to create:**

    - Primary keys (auto-created)
    - Foreign keys
    - Frequently queried columns
    - Columns used in WHERE, JOIN, ORDER BY

    Example migration for indexes:

    ```python
    # Alembic
    def upgrade():
        op.create_index('idx_users_created_at', 'users', ['created_at'])
        op.create_index('idx_users_username_email', 'users', ['username', 'email'])  # Composite
        op.execute('CREATE INDEX idx_users_email_lower ON users (LOWER(email))')  # Case-insensitive
    ```

8. **Setup connection pooling**

    Configure connection pool settings for optimal performance.

    **Recommendations:**

    - Pool size: 20-50 for web apps
    - Max overflow: 10-20
    - Pool timeout: 30 seconds
    - Pool pre-ping: enabled (verify connections)

    Update connection configuration from step 2 with these values.

9. **Create database models/entities**

    Define data models with proper types and constraints.

    **Python (SQLAlchemy):**

    ```python
    from sqlalchemy import Column, String, DateTime
    from sqlalchemy.dialects.postgresql import UUID
    from database import Base
    import uuid
    from datetime import datetime


    class User(Base):
        __tablename__ = "users"

        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        email = Column(String(255), unique=True, nullable=False, index=True)
        username = Column(String(50), unique=True, nullable=False)
        created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
        updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow)
    ```

10. **Implement security best practices**

    Follow database security guidelines from `700-Security`.

    **SQL Injection Prevention:**

    - ✅ Always use parameterized queries
    - ❌ Never concatenate SQL strings

    ```python
    # Good: Parameterized
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))

    # Bad: String concatenation
    cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")  # DON'T DO THIS
    ```

    **Access Control:**

    - Use application-specific DB user (not admin)
    - Grant minimal required permissions
    - Enable SSL for connections in production

11. **Create database backup script**

    Setup automated backup strategy.

    Create `scripts/backup_db.sh`:

    ```bash
    #!/bin/bash
    DATE=$(date +%Y%m%d_%H%M%S)
    BACKUP_DIR="./backups"
    DB_NAME="myapp_db"

    mkdir -p $BACKUP_DIR

    pg_dump $DB_NAME | gzip > $BACKUP_DIR/backup_${DB_NAME}_${DATE}.sql.gz

    # Keep only last 7 days
    find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete

    echo "Backup completed: backup_${DB_NAME}_${DATE}.sql.gz"
    ```

    Make executable:

    ```bash
    chmod +x scripts/backup_db.sh
    ```

// turbo
12. **Verify database setup**

    Test database connection and query execution.

    ```bash
    # PostgreSQL CLI
    psql -U username -d dbname -c "SELECT version();"

    # Check tables
    psql -U username -d dbname -c "\dt"

    # Check indexes
    psql -U username -d dbname -c "\di"
    ```

    **Test in code:**

    Python:

    ```python
    from database import engine, SessionLocal

    # Test connection
    with engine.connect() as connection:
        result = connection.execute("SELECT 1")
        print("Database connected:", result.fetchone())

    # Test ORM
    db = SessionLocal()
    user_count = db.query(User).count()
    print(f"Users in database: {user_count}")
    ```
