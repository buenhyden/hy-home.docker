---
layer: qa
description: "Rule for regression prevention, failure triage, and quality-gate enforcement."
---

# QA — Regression Quality Gate Rule

## Case
- **[REQ-QA-04]** Add regression protection for every production-impacting defect fix.
- **[REQ-QA-05]** Use failure triage paths that preserve root-cause visibility.
- **[REQ-PERF-02]** Prevent performance regressions in critical workflows.

## Style
- **[PROC-QA-02]** Group failures by root-cause class before remediation.
- **[VAL-QA-01]** Require evidence-backed gate pass before release-readiness claim.
- **[BAN-QA-02]** Avoid bypassing quality gates for schedule pressure.

## Validation
- [ ] Regression tests exist for fixed high-impact defects.
- [ ] Failure triage output is documented and actionable.
- [ ] Quality gate pass criteria are met with evidence.
