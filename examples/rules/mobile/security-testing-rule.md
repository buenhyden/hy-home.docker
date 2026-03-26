---
layer: mobile
description: "Rule for mobile security posture and regression-oriented mobile test discipline."
---

# Mobile — Security & Testing Rule

## Case
- **[REQ-MOBS-01]** Apply mobile-specific security controls for sensitive paths.
- **[REQ-MOBT-01]** Define repeatable mobile testing strategy per platform.
- **[REQ-MOBT-02]** Add regression coverage for fixed mobile defects.

## Style
- **[PROC-MOBS-01]** Validate auth/session/storage behavior under mobile threat assumptions.
- **[PROC-MOBT-01]** Keep test evidence attached to critical mobile changes.
- **[BAN-MOBS-01]** Do not store sensitive mobile secrets insecurely.
- **[BAN-MOBT-01]** Do not claim mobile readiness without cross-platform verification.

## Validation
- [ ] Mobile security controls are explicit and tested.
- [ ] Regression-sensitive mobile paths have repeatable checks.
- [ ] Test evidence exists for critical behavior changes.
