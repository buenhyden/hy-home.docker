---
trigger: always
glob: ["**/*"]
description: "Unified Master Standard. The Constitution of the Rule System, defining hierarchy, conflict resolution, and governance."
---

# 0100-Unified-Master-Standard

- **Role**: Rule System Governor
- **Purpose**: Maintain integrity, consistency, and discoverability of the Agentic Rule System.
- **Activates When**: Creating rules, resolving conflicts, or navigating the system.

## 1. Standards

### 1.1 The Rule Hierarchy

- **Tier 0 (Core)**: Behavior (`0000`), Governance (`0100`), Workflows (`0200`).
- **Tier 1 (Domain)**: Cloud (`0400`), AI (`0500`), Data (`0600`), Web (`0800`).
- **Tier 2 (Tech)**: Python (`1100`), Next.js (`1200`), Go (`1300`), TS (`1500`).
- **Tier 3 (Cross)**: Security (`2200`), Docs (`2100`).

### 1.2 Principles

- **[REQ-GOV-SPEC-01] Specificity Wins**: Specific rules override general ones (e.g., Python > Backend).
- **[REQ-GOV-SEC-01] Security Supreme**: Security rules (`2200`) override ALL others.
- **[REQ-GOV-SSOT-01] Single Truth**: Duplicate rules are FORBIDDEN.

### 1.3 Scope

- **In-Scope**: Rule creation, ID generation, Conflict resolution.
- **Out-of-Scope**: Individual rule content (unless violating governance).

### 1.4 Must / Must Not

- **[REQ-WRITE-FMT-01] Frontmatter**: All rules MUST have YAML frontmatter.
- **[REQ-WRITE-ID-01] Unique IDs**: All requirements MUST have unique IDs.
- **[BAN-WRITE-VAG-01] No Ambiguity**: Avoid "maybe" or "try". Use "MUST".

## 2. Procedures

### 2.1 New Rule Protocol

1. **Search**: Check `0100-Unified-Master` for correct Pillar.
2. **Verify**: Ensure no duplicates exist.
3. **Draft**: Follow 8-Section Skeleton.
4. **Review**: Validate IDs and Formatting.

## 3. Examples

### 3.1 Conflict Resolution

```text
Conflict: "Use innerHTML" (Perf) vs "No innerHTML" (Sec).
Resolution: Security (Tier 3 Cross-Cutting) overrides Performance.
Result: Ban innerHTML.
```

## 4. Validation Criteria

- [ ] **[VAL-GOV-YML-01]** Valid YAML frontmatter present.
- [ ] **[VAL-GOV-ID-01]** All REQ IDs are unique.
- [ ] **[VAL-GOV-SSOT-01]** Topic exists in exactly one file.
