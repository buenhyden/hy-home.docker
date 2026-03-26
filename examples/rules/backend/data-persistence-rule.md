---
layer: backend
description: "Rule for storage safety, schema integrity, and durable persistence behavior."
---

# Backend — Data Persistence Rule

## Case
- **[REQ-DAT-01]** Define persistence models with explicit ownership and lifecycle.
- **[REQ-DBA-01]** Keep migrations safe, reversible, and operationally planned.
- **[REQ-KAF-01]** Preserve event/schema consistency for async data contracts.

## Style
- **[PROC-DAT-MIG-FAIL]** Include rollback/failure handling for data migration operations.
- **[REQ-DATE-01]** Use explicit temporal handling for date/time sensitive data paths.
- **[BAN-DB-MUT-01]** Avoid uncontrolled destructive schema/data mutation.
- **[BAN-DAT-LOG-01]** Do not log sensitive persisted data content.

## Validation
- [ ] Data model changes include migration and rollback strategy.
- [ ] Event/schema compatibility checks pass for contract-sensitive updates.
- [ ] Persistence-layer operations meet safety and audit constraints.
