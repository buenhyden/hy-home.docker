---
layer: ops
description: "Rule for incident handling readiness, runbook quality, and post-incident learning loops."
---

# Ops — Incident & Runbook Rule

## Case
- **[REQ-INC-01]** Maintain explicit incident response workflows.
- **[REQ-RBK-01]** Keep runbooks executable and up to date.
- **[REQ-INC-02]** Capture post-incident learnings for recurrence prevention.

## Style
- **[PROC-INC-01]** Use runbook-first response for recurring failure patterns.
- **[REQ-RBK-03]** Include rollback and verification steps in procedures.
- **[BAN-INC-PM-01]** Avoid ad-hoc incident handling without timeline/evidence capture.

## Validation
- [ ] Critical failure modes have associated runbooks.
- [ ] Incident workflow includes ownership and escalation steps.
- [ ] Post-incident action items are explicit and trackable.
