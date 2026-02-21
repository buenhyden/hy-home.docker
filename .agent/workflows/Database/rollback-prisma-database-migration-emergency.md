---
description: Revert the last database migration if something goes wrong
---

1. **Identify Migration**:
   - Check migration status.
   // turbo
   - Run `npx prisma migrate status`

2. **Resolve Migration**:
   - Mark a failed migration as resolved (if stuck).
   // turbo
   - Run `npx prisma migrate resolve --rolled-back "migration_name"`

3. **Down Migration (Manual)**:
   - Prisma doesn't support auto-down. You must manually execute SQL to revert changes.
   // turbo
   - Run `psql -d mydb -f ./migrations/down.sql`

4. **Pro Tips**:
   - Always test migrations on a copy of production data first.
