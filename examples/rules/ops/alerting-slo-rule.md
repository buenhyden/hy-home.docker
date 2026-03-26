---
layer: ops
description: "Rule for alerting quality, SLO alignment, and error-budget-aware operations."
---

# Ops — Alerting & SLO Rule

## Case
- **[REQ-ALT-01]** Define alerting based on meaningful operational risk.
- **[REQ-ALT-03]** Tie alerts to service-level objectives and error budgets.
- **[REQ-PERF-01]** Track reliability/performance budget consumption.

## Style
- **[PROC-ALT-01]** Tune thresholds to reduce noisy/non-actionable alerts.
- **[REQ-ALT-05]** Keep escalation paths explicit and documented.
- **[BAN-ALT-01]** Avoid alert floods from low-signal conditions.

## Validation
- [ ] SLO-linked alerts exist for critical services.
- [ ] Alert thresholds are actionable and documented.
- [ ] Error-budget policy is measurable.
