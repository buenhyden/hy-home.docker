---
layer: entry
description: "Rule for edge hardening with TLS, rate limits, and gateway security controls."
---

# Entry — Edge Security Rule

## Case
- **[REQ-EDGE-TLS-01]** Enforce TLS on external entry paths.
- **[REQ-SEC-02]** Verify caller identity where edge auth is applied.
- **[REQ-SEC-03]** Apply least-privilege gateway policies.

## Style
- **[PROC-SEC-GEN-01]** Keep edge security controls observable and testable.
- **[REQ-SEC-10]** Include protections against common edge abuse vectors.
- **[BAN-EDGE-TLS-01]** No insecure TLS downgrade defaults.

## Validation
- [ ] TLS and certificate behavior are explicitly configured.
- [ ] Rate limit and abuse controls are present on sensitive routes.
- [ ] Edge policy behavior is verifiable through logs/metrics.
