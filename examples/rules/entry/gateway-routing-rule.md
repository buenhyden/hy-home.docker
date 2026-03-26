---
layer: entry
description: "Rule for gateway routing correctness, boundary control, and safe exposure policy."
---

# Entry — Gateway Routing Rule

## Case
- **[REQ-NS-NET-01]** Keep ingress and internal network boundaries explicit.
- **[REQ-NGX-01]** Apply deterministic host/path routing patterns.
- **[REQ-K8S-CFG-01]** Keep routing configuration declarative and versioned.

## Style
- **[PROC-NGX-01]** Validate routing config before apply/reload.
- **[REQ-OPS-01]** Ensure routing changes emit operationally useful logs.
- **[BAN-NGX-01]** No ambiguous wildcard routing that bypasses intended boundaries.

## Validation
- [ ] Route ownership and destination mapping are explicit.
- [ ] Routing configuration passes syntax and safety checks.
- [ ] Internal-only services are not unintentionally exposed.
