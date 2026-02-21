---
trigger: model_decision
glob: [".agent/rules/**/*.md"]
description: "Master Standard: The authoritative guide for writing and validating Rule files."
---

# 0001-Meta-Rule-Writing

- **Role**: System Architect
- **Purpose**: Define the structure, syntax, and validation rules for all `.md` Rule files in this repository.
- **Activates When**: Creating or modifying any Rule file.

## 1. Standards

### 1.1 Principles

- **[REQ-META-GEN-01] Four Digit Prefix**: All rule files MUST start with a 4-digit ID (e.g., `0100-general.md`).
- **[REQ-META-GEN-02] SSOT**: Duplicate rules MUST be consolidated into a Single Source of Truth.
- **[REQ-META-GEN-03] Deterministic**: Rules MUST use "MUST", "MUST NOT", "DO", "DO NOT".

### 1.2 Scope

- **In-Scope**: All files in `.agent/rules`.
- **Out-of-Scope**: Workflows (see 0002), Documentation (see 0800).

### 1.3 Must / Must Not

- **[REQ-META-FMT-01] Frontmatter**: Files MUST have `trigger`, `glob`, `description` YAML frontmatter.
- **[REQ-META-STR-01] Skeleton**: Files MUST have `1. Standards`, `2. Procedures`, `3. Examples`, `4. Validation`.
- **[BAN-META-VAG-01] No Fluff**: Descriptions MUST be one actionable sentence.

## 2. Procedures

### 2.1 Rule Creation

1. **Name**: `NNNN-topic-slug.md`.
2. **Copy Template**: Use the standard 4-section skeleton.
3. **Define IDs**: Use `[REQ-TOPIC-TYPE-01]` format for rules.
4. **Validate**: Check against this standard.

## 3. Examples

### 3.1 Standard Rule File

```markdown
---
trigger: model_decision
glob: ["**/*.ts"]
description: "TypeScript Standards: strict typing and linting."
---

# 1500-TypeScript

## 1. Standards
### 1.1 Principles
- **[REQ-TS-TYP-01] Strict**: strict: true.
```

## 4. Validation Criteria

- [ ] **[VAL-META-NAM-01]** File name is `DDDD-slug.md`.
- [ ] **[VAL-META-FMT-01]** YAML frontmatter exists.
- [ ] **[VAL-META-ID-01]** Rules use `[REQ-...]` IDs.

## 5. References

- Related: [0002-meta-workflow-writing.md](./0002-meta-workflow-writing.md)
