---
trigger: always_on
glob: ["**/*.sql", "**/*{repository,dao,query}*.{ts,js,py,java,kt,cs}"]
description: "Database Security Standards: Enforces SQL injection prevention, least privilege access, and secure data handling."
---

# Database Security Standards

- **Role**: Database Security Engineer
- **Purpose**: Define standards for secure database interaction, data integrity, and protection against unauthorized access.
- **Activates When**: Writing SQL queries, configuring data access objects (DAOs), or managing database schemas.

**Trigger**: always_on — Apply during the development of data persistence layers.

## 1. Standards

### Principles

- **[REQ-DB_SEC-01] Universal Parameterization**
  - All database queries MUST use parameterized inputs or prepared statements. Direct string concatenation of user input is strictly prohibited.
- **[REQ-DB_SEC-02] Least Privilege Credentials**
  - Application database users MUST only possess the minimum required permissions (e.g., SELECT/INSERT/UPDATE) for their specific domain.
- **[REQ-DB_SEC-03] Secure Schema Evolution**
  - Changes to the database schema MUST be performanced via versioned migration scripts rather than manual direct commands.

### Injection Mitigation

| Technique | Risk Level | Recommendation |
| --- | --- | --- |
| Prepared Statements | Very Low | **Primary Choice (Mandatory)** |
| ORM (e.g., Prisma) | Low | Safe by default (Verify raw queries) |
| Stored Procedures | Low | Safe if parameters are used correctly |
| String Concatenation | **Critical** | **FORBIDDEN** |

### Must

- **[REQ-DB_SEC-04] Explicit Column Selection**
  - Production queries SHOULD NOT use `SELECT *`; explicitly name required columns to prevent accidental data exposure.
- **[REQ-DB_SEC-05] Secret Storage Encryption**
  - PII and sensitive data stored in the database MUST be encrypted using modern algorithms (e.g., AES-256).
- **[REQ-DB_SEC-06] Connection Lifecycle Management**
  - Database connections MUST be managed via a pool with explicitly defined timeouts and maximum connection limits.

### Must Not

- **[BAN-DB_SEC-01] Client-Side SQL Construction**
  - Database logic MUST NOT be constructed on the client-side and sent directly to the server for execution.
- **[BAN-DB_SEC-02] Default Account Usage**
  - Production environments MUST NOT use default administrative accounts (e.g., `sa`, `root`, `postgres`) for application traffic.

### Failure Handling

- **Stop Condition**: Stop execution if a query fails due to a parameter type mismatch or suspected injection attempt.

## 2. Procedures

- **[PROC-DB_SEC-01] Access Review**
  - IF a query bypasses the primary DAO/Repository THEN MUST undergo a mandatory security peer review.
- **[PROC-DB_SEC-02] Migration Audit**
  - Verify that every migration script includes a rollback mechanism and does not grant excessive permissions.

## 3. Examples

### Secure Query (TypeScript)

```typescript
// Good: Using parameterized query
const user = await db.query('SELECT name FROM users WHERE id = $1', [userId]);
```

## 4. Validation Criteria

- **[VAL-DB_SEC-01] Injection Smoke Test**
  - [ ] Automated tests confirm that common SQL injection strings (e.g., `' OR 1=1`) are correctly escaped or rejected.
- **[VAL-DB_SEC-02] Privilege Audit**
  - [ ] Permission check confirms the application user cannot perform `DROP TABLE` or `GRANT`.
- **[VAL-DB_SEC-03] Pool Monitoring**
  - [ ] Metrics confirm that connection pool usage remains within defined boundaries during peak load.
