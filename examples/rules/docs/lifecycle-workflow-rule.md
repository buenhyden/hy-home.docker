---
layer: docs
description: "Rule for documentation lifecycle updates and workflow-coupled maintenance."
---

# Docs — Lifecycle Workflow Rule

## Case
- **[REQ-DOC-IDX-03]** Update lifecycle docs when behavior or policy changes.
- **[REQ-DOC-IDX-04]** Keep PR/workflow docs aligned with real execution patterns.
- **[REQ-DOC-ADR-01]** Reflect major decision changes in linked documentation.

## Style
- **[PROC-WKF-01]** Update docs atomically with code/policy changes when coupled.
- **[PROC-WKF-02]** Record unresolved documentation debt explicitly.
- **[BAN-WKF-CMP-01]** Do not mark docs complete without validation.

## Validation
- [ ] Lifecycle state reflects current project reality.
- [ ] Workflow documentation matches executable paths.
- [ ] Documentation debt is explicit when not resolved.
