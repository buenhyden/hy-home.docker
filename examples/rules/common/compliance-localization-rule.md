---
layer: common
description: "Rule for cross-scope compliance and localization-ready defaults."
---

# Common — Compliance & Localization Rule

## Case
- **[REQ-COM-06]** Keep compliance-sensitive behavior explicit and auditable.
- **[REQ-LOC-01]** Prepare user-facing content for localization.
- **[REQ-LOC-03]** Use consistent internationalization patterns for string management.

## Style
- **[PROC-LOC-01]** Define language/locale ownership boundaries clearly.
- **[REQ-LOC-05]** Preserve translation safety in workflow updates.
- **[BAN-LOC-01]** Avoid hardcoded user-facing locale content where translation is expected.

## Validation
- [ ] Compliance-critical references are traceable.
- [ ] Localization assumptions are explicit.
- [ ] No locale-sensitive regressions are introduced by rule changes.
