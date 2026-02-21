---
trigger: model_decision
glob: ["docs/**"]
description: "Lifecycle Standards: Creation, Review, Deprecation, and Archival of documentation."
---

# 0820-Documentation-Lifecycle

- **Role**: Documentation Manager
- **Purpose**: Manage the full lifecycle of documentation from creation to archival.
- **Activates When**: Creating new docs, reviewing existing docs, or deprecating features.

## 1. Standards

### 1.1 Principles

- **[REQ-LIF-GEN-01] Freshness**: Documentation MUST be kept current with code.
- **[REQ-LIF-GEN-02] Review**: All docs MUST be reviewed before merging.
- **[REQ-LIF-GEN-03] Cleanup**: Obsolete docs MUST be archived or removed.

### 1.2 Scope

- **In-Scope**: All project documentation.
- **Out-of-Scope**: Ephemeral notes.

### 1.3 Inputs & Outputs

- **Inputs**: Feature lifecycle events.
- **Outputs**: Up-to-date documentation repository.

### 1.4 Must / Must Not

- **[REQ-LIF-CRE-01] Definition of Done**: Features are not "Done" until documented.
- **[REQ-LIF-REV-01] Peer Review**: Docs change requires 1 approval.
- **[REQ-LIF-DEP-01] Deprecation Notice**: Deprecated docs MUST have a warning callout at the top.

## 2. Procedures

### 2.1 Deprecation Workflow

1. **Mark**: Add `> [!WARNING] This document is deprecated.` to the top.
2. **Redirect**: Link to the new standard/doc.
3. **Archive**: Move to `_archive/` after set period (e.g., 6 months) or delete.

## 3. Examples

### 3.1 Deprecation Banner

```markdown
> [!WARNING]
> **Deprecated**: This feature is replaced by API v2.
> See [Introduction to v2](./v2-intro.md).
```

## 4. Validation Criteria

- [ ] **[VAL-LIF-DEP-01]** Deprecated docs have banners.
- [ ] **[VAL-LIF-REV-01]** New docs follow standards and passed review.

## 5. References

- Related: [0800-documentation-content.md](./0800-documentation-content.md)
