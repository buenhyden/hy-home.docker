---
layer: mobile
description: "Rule for mobile runtime performance, resource efficiency, and responsiveness safeguards."
---

# Mobile — Performance Rule

## Case
- **[REQ-MOBP-01]** Maintain explicit mobile performance budgets.
- **[REQ-MOBP-02]** Optimize rendering and state updates for constrained devices.
- **[REQ-RN-02]** Reduce unnecessary bridge/render overhead in React Native paths.

## Style
- **[PROC-MOBP-01]** Measure before/after for performance-sensitive changes.
- **[REQ-MOBP-03]** Keep expensive operations off critical interaction paths.
- **[BAN-MOBP-01]** Avoid unmeasured performance regressions.

## Validation
- [ ] Performance-critical flows are measured and within budget.
- [ ] Resource-intensive operations are controlled.
- [ ] No significant responsiveness regressions are introduced.
