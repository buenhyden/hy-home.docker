---
layer: infra
description: "Rule for Docker-based infrastructure composition, isolation, and safe operational change."
---

# Infra — Docker Rule

## Case
- **[RULE-INF-001]** Run plan/validation before infra mutation.
- **[RULE-INF-002]** Preserve intended network isolation boundaries.
- **[REQ-INF-DOCKER-01]** Keep container runtime configuration explicit and versioned.

## Style
- **[RULE-INF-003]** Prefer declarative config over click-ops changes.
- **[RULE-INF-004]** Use multi-stage build patterns where images are built.
- **[BAN-OPS-01]** Avoid ad-hoc destructive operations without explicit approval.

## Validation
- [ ] Compose/runtime configuration passes validation checks.
- [ ] Internal services remain isolated as intended.
- [ ] Changed services are observable after rollout.
