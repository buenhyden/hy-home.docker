---
trigger: model_decision
glob: ["**/*"]
description: "Code Migration Agent Standards: Enforces safe, incremental technology transitions, dependency upgrades, and framework-level modernization."
---

# Code Migration Agent Standards

- **Role**: System Migration Specialist
- **Purpose**: Define standards for the safe, reversible, and incremental migration of codebase components between different versions, frameworks, or architectural patterns.
- **Activates When**: The user requests a major dependency upgrade, language version bump, or structural transition (e.g., JavaScript to TypeScript).

**Trigger**: model_decision — Apply during all architectural transition and major dependency upgrade phases.

## 1. Standards

### Principles

- **[REQ-MGS-01] Safety-First Stability Baseline**
  - System stability MUST supersede migration speed. No transition is complete without a proven, zero-regression verification pass.
- **[REQ-MGS-02] Reversible Incremental Batches**
  - Migrations MUST be executed in small, decoupled batches that can be instantly reverted without impacting other system modules.
- **[REQ-MGS-03] Dual-Run Verification Discipline**
  - For high-risk migrations, the new and old implementation paths SHOULD be verified in parallel (e.g., via Feature Flags) before the final switch.

### Transition Matrix

| phase | Requirement ID | Critical Control |
| --- | --- | --- |
| Analysis | [REQ-MGS-04] | Audit Breaking Changes in changelogs |
| Roadmap | [REQ-MGS-05] | Step-by-step sequential migration plan |
| Isolation | [REQ-MGS-06] | Dedicated feature branches or flags |
| Switch | [REQ-MGS-07] | verifiable health-check before final cutover |

### Must

- **[REQ-MGS-08] Mandatory Roadmap Documentation**
  - Every migration task MUST be preceded by a technical roadmap documenting the order of operations, risks, and rollback strategies.
- **[REQ-MGS-09] Explicit Compatibility Management**
  - The agent MUST ensure backward compatibility with existing data schemas and API consumers throughout the migration lifecycle.
- **[REQ-MGS-10] Automated Regression Suite Pass**
  - 100% of the project's regression test suite MUST pass on both the old and new implementations before a migration is considered successful.

### Must Not

- **[BAN-MGS-01] The "Big Bang" Hazard**
  - DO NOT attempt to migrate the entire system in a single, monolithic PR. break the migration into manageable, atomic work items.
- **[BAN-MGS-02] Silent Contract Modification**
  - Avoid introducing accidental functional changes or side-effects during a technical migration; focus exclusively on the technology shift.

### Failure Handling

- **Stop Condition**: Stop the migration immediately if a critical dependency collision is identified or if the rollback script fails to restore the baseline state.

## 2. Procedures

- **[PROC-MGS-01] Pre-migration Impact audit**
  - IF planning a dependency upgrade THEN MUST verify the transitive dependency tree for potential version conflicts or security vulnerabilities.
- **[PROC-MGS-02] Post-Migration Cleanup**
  - UPON successful cutover THEN MUST remove all deprecated code, feature flags, and temporary shims according to the project's "Cleanup" policy.

## 3. Examples

### compliant roadmap (Good)

1. **Batch 1**: Update Types.
2. **Batch 2**: Migrate Logic (under flag).
3. **Batch 3**: Verify & Cutover.
4. **Batch 4**: Cleanup Legacy.

## 4. Validation Criteria

- **[VAL-MGS-01] Roadmap Integrity**
  - [ ] audit confirms the existence of a version-controlled roadmap file for the migration.
- **[VAL-MGS-02] Regression Pass rate**
  - [ ] build logs confirm 100% test success across both the source and target implementations.
- **[VAL-MGS-03] Rollback verification**
  - [ ] manual verification confirms that the system can be restored to the pre-migration state in < 10 minutes.
