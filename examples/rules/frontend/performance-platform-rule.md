---
layer: frontend
description: "Rule for frontend performance budgets, browser/platform compatibility, and resilient delivery."
---

# Frontend — Performance & Platform Rule

## Case
- **[REQ-FND-06]** Maintain frontend performance budgets.
- **[REQ-BRW-01]** Preserve browser API compatibility expectations.
- **[REQ-PWA-01]** Keep platform behavior predictable when progressive enhancement is used.

## Style
- **[PROC-PERF-01]** Measure before optimization and preserve evidence.
- **[REQ-CB-01]** Validate critical paths on supported browser matrix.
- **[BAN-PERF-01]** Avoid unmeasured performance regressions.

## Validation
- [ ] Performance-sensitive paths are measured and within budget.
- [ ] Browser/platform compatibility checks are recorded.
- [ ] No critical rendering regressions are introduced.
