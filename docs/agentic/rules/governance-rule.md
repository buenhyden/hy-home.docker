---
layer: agentic
---

# Architectural Change Governance Rule

This rule defines the mandatory verification checklist for any architectural or cross-cutting structural change.

## Verification Checklist

Every architectural PR or change must satisfy:

1. **Boundary Impact**: Explicitly state which tier/service boundary is changing.
2. **Network Impact**: Analyze effects on `infra_net` or external networks.
3. **Secret Impact**: Define new secret file paths and injection methods (Docker Secrets only).
4. **Port Impact**: Update `*_HOST_PORT` variables and default values in Compose and README.
5. **Security Baseline**: Provide justification for any privilege escalation (cap_add/privileged).
6. **Ops Impact**: Update corresponding `docs/runbooks/` and `OPERATIONS.md`.
7. **Validation**: Must pass `bash scripts/validate-docker-compose.sh`.
8. **Traceability**: Ensure reciprocal links between ADR, Spec, and Runbook.

## Enforcement

- Agents must run this checklist mentally before submitting work involving `docker-compose.yml` includes or global policies.
