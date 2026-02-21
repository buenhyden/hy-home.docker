---
trigger: model_decision
glob: ["**/*.sql", "**/prisma/**", "**/migrations/**"]
description: "Database Design Agent Standards: Enforces 3NF normalization, efficient indexing strategies, and reversible schema migration protocols."
---

# Database Design Agent Standards

- **Role**: Principal Data Architect
- **Purpose**: Define standards for the design, modeling, and evolution of scalable, performant, and normalized relational and non-relational data schemas.
- **Activates When**: The user requests new table structures, schema modifications (DDL), index optimizations, or data migration scripts.

**Trigger**: model_decision — Apply during all data modeling, schema design, and query optimization phases.

## 1. Standards

### Principles

- **[REQ-DBA-01] Normalized Baseline (3NF)**
  - All relational schemas MUST default to Third Normal Form (3NF) to ensure data integrity. Denormalization MUST be explicitly justified by Read-Heavy performance requirements.
- **[REQ-DBA-02] Mandatory Primary Key Casing**
  - Every table MUST possess a primary key utilizing standard types (UUID or BigInt). Composite keys SHOULD be avoided in favor of a unique surrogate key where applicable.
- **[REQ-DBA-03] Reversible Migration Integrity**
  - All schema modifications MUST be deployed via versioned migration scripts that include balanced `UP` and `DOWN` logic for instant rollbacks.

### Modeling Matrix

| Category | Requirement ID | Mandatory Standard |
| --- | --- | --- |
| Keys | [REQ-DBA-04] | Foreign Keys MUST have associated indexes |
| Deletion | [REQ-DBA-05] | Soft Deletes (`deleted_at`) for critical data |
| Data Types | [REQ-DBA-06] | Match types to precision needs (e.g. JSONB for props) |
| Performance | [REQ-DBA-07] | explain Analyze for query optimization |

### Must

- **[REQ-DBA-08] Explicit Foreign Key Constraints**
  - Relations MUST be enforced at the database level using Foreign Key constraints with appropriate `ON DELETE` referential actions.
- **[REQ-DBA-09] Narrative Migration Naming**
  - Migration files MUST follow a chronological, narrative naming pattern (e.g., `20240101_add_user_auth_fields.sql`) for auditability.
- **[REQ-DBA-10] Documented Access Patterns**
  - Architecture blueprints MUST document the primary read/write access patterns that influenced the final schema and indexing decisions.

### Must Not

- **[BAN-DBA-01] Opaque Magic IDs**
  - Avoid using non-deterministic or non-unique identifier patterns for primary keys that could cause collisions during data synchronization.
- **[BAN-DBA-02] Direct Production DDL**
  - DO NOT execute manual, ad-hoc DDL commands directly on production clusters; all changes MUST flow through the versioned migration pipeline.

### Failure Handling

- **Stop Condition**: Stop schema implementation if a proposed change identifies a circular relationship or lacks a clear, reversible migration path.

## 2. Procedures

- **[PROC-DBA-01] Index Efficiency review**
  - IF adding a new query-heavy column THEN MUST verify the performance impact using `EXPLAIN ANALYZE` before finalizing the index strategy.
- **[PROC-DBA-02] Migration Pre-Flight Check**
  - Before applying a migration, verify against a representative data set in the staging environment to ensure zero locking of mission-critical tables.

## 3. Examples

### Clean Junction Table (Good)

```sql
CREATE TABLE user_roles (
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
  PRIMARY KEY (user_id, role_id)
);
```

## 4. Validation Criteria

- **[VAL-DBA-01] Normalization Pass**
  - [ ] audit confirms that 100% of new schemas adhere to the 3NF baseline unless denormalization is documented.
- **[VAL-DBA-02] Reversibility verification**
  - [ ] manual verification confirms that the `DOWN` script successfully restores the previous schema state without data loss.
- **[VAL-DBA-03] Constraint Audit**
  - [ ] audit confirms that zero orphaned records are possible due to correctly implemented Foreign Key constraints.
