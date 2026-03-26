---
layer: infra
description: "Rule for cloud/governance alignment, CI/CD safety, and GitOps operational discipline."
---

# Infra — Cloud & GitOps Rule

## Case
- **[REQ-CICD-01]** Use automated pipelines for reproducible infra delivery.
- **[REQ-GITOPS-01]** Keep desired state in version control as source of truth.
- **[REQ-CLOUD-GOV-01]** Align cloud changes with governance/security baselines.

## Style
- **[PROC-CICD-01]** Gate delivery with validation and rollback paths.
- **[REQ-PD-STR-01]** Use progressive delivery where risk warrants staged rollout.
- **[BAN-CICD-SEC-01]** Block insecure bypasses around deployment controls.

## Validation
- [ ] CI/CD and GitOps flows remain consistent with declared process.
- [ ] Rollback strategy exists for high-impact infra changes.
- [ ] Governance constraints are enforced in delivery path.
