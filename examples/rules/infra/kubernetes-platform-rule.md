---
layer: infra
description: "Rule for Kubernetes platform policy, tenancy boundaries, and resource governance."
---

# Infra — Kubernetes Platform Rule

## Case
- **[REQ-K8S-CFG-01]** Keep Kubernetes configuration deterministic and reviewable.
- **[REQ-NS-NET-01]** Enforce namespace/network boundary policy.
- **[REQ-NS-RBAC-01]** Apply least-privilege access in tenancy-sensitive areas.
- **[REQ-RSRC-01]** Declare resource quotas/limits for predictable scheduling.

## Style
- **[PROC-K8S-CFG-01]** Validate manifests/policies before apply.
- **[REQ-K8S-TENANCY-01]** Keep tenancy ownership and separation explicit.
- **[BAN-K8S-CFG-01]** Avoid implicit defaults for critical security/availability controls.

## Validation
- [ ] Resource, tenancy, and access policies are explicit.
- [ ] Manifest validation passes before rollout.
- [ ] Multi-tenant boundaries remain intact.
