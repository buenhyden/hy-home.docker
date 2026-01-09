---
trigger: always_on
glob: "**/*.ts,schema.prisma"
description: "Prisma: Modern DB Toolkit Guidelines."
---
# Prisma ORM Standards

## 1. Schema Design

- **Naming**: Use camelCase for fields and PascalCase for models (e.g., `model UserProfile`).
- **Composite Keys**: Use `@@id` for composite primary keys.
- **Indexes**: Explicitly define indexes (`@@index`) for fields used in `where`, `orderBy`, or join conditions.

### Example: Schema

**Good**

```prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  posts     Post[]
  @@index([email])
}
```

## 2. Client Management

- **Singleton Pattern**: Instantiate `PrismaClient` once and reuse it across the application to prevent connection pool exhaustion.

### Example: Singleton

**Good**

```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = global as unknown as { prisma: PrismaClient }

export const prisma = globalForPrisma.prisma || new PrismaClient()

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma
```

## 3. Query Optimization

- **Select Fields**: Always use `select` to fetch only necessary fields. Avoid `include` unless relations are strictly needed.
- **Bulk Operations**: Use `createMany`, `updateMany`, and `deleteMany` for batch operations instead of loops.
- **N+1 Problem**: Be cautious with nested reads in loops. Use fluent API or batching.

## 4. Migrations

- **Version Control**: Commit `migrations/` folder.
- **Development**: Use `prisma migrate dev`.
- **Production**: Use `prisma migrate deploy` in CI/CD pipelines.
