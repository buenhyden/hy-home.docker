---
layer: qa
description: "Rule for layered testing strategy, deterministic validation, and release confidence baselines."
---

# QA — Testing Strategy Rule

## Case
- **[REQ-QA-01]** Define layered test strategy (unit/integration/e2e) for critical paths.
- **[REQ-QA-02]** Tie acceptance criteria to deterministic verification steps.
- **[REQ-PERF-01]** Include performance-sensitive checks where risk warrants.

## Style
- **[PROC-QA-01]** Prefer behavior-level validation over implementation-coupled assertions.
- **[REQ-QA-03]** Keep test scope proportional to change impact.
- **[BAN-QA-01]** Do not mark work complete without required validation evidence.

## Validation
- [ ] Critical behavior is covered by appropriate test layers.
- [ ] Acceptance criteria map to executable checks.
- [ ] Verification evidence exists for completion claims.
