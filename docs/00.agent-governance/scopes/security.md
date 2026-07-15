---
layer: security
---

# Security Enforcement Scope

Universal security standards and data protection protocols for `hy-home.docker`.

## 1. Context and Objective

- Goal: zero-trust implementation and continuous security posture management.
- Baseline: OWASP Top 10 and ASVS L2 alignment.
- Governance: follow `docs/00.agent-governance/rules/quality-standards.md`.

## 2. Requirements and Constraints

- Identity and access:
  - centralized authentication via Keycloak (OIDC/SAML),
  - least-privilege RBAC/ABAC at API and data layers.
- Secrets management:
  - prohibited: plaintext credentials in source-controlled configs,
  - mandatory: Docker secrets and/or Vault-backed secret flow.
- Container hardening:
  - mandatory where compatible: non-root runtime, `no-new-privileges`, minimal
    capabilities, read-only mounts for static config, and secret injection by
    file rather than image layer or plaintext environment value,
  - manual review unless an existing validator or hook enforces the specific
    field.
- Network hardening:
  - isolate traffic on intended networks,
  - enforce TLS at ingress boundaries.

## 3. Implementation Flow

1. Perform lightweight threat modeling for new/changed services.
2. Run security checks defined in active scope plus `rules/task-checklists.md`.
3. Apply static analysis and dependency risk checks where available.

### 3.1 Approved Secrets Work Protocol

When the user approves secrets work, agents may inspect repository-local secret
metadata needed for the task, but secret values remain non-output data.
Permitted evidence includes counts, IDs, file paths, key names, registry
metadata, rotation status, and command success/failure. Prohibited evidence
includes plaintext values, private keys, token-bearing logs, shell history, and
full secret file bodies.

Secret value reads, writes, or rotations require a concrete target and task
evidence that records the redaction boundary, validation command, and rollback
or recovery path. Do not commit, print, summarize, or quote secret values.

## 4. Operational Procedures

- Patch critical CVEs in images and dependencies with priority handling.
- Log authentication events and sensitive access operations centrally.
- Ensure incident and postmortem links are captured for high-severity events.

## 5. Maintenance and Safety

- Periodically validate guardrails and access controls through controlled exercises.
- Keep security guidance repository-realistic; remove references to nonexistent local paths.

## 6. File Ownership SSOT

| Path Pattern                     | Owner Agent        | Read-Only For                                    |
| -------------------------------- | ------------------ | ------------------------------------------------ |
| `scripts/hardening/check-all-hardening.sh` | `security-auditor` | all other agents                                 |
| `scripts/hardening/check-all-hardening.sh`, `scripts/validation/check-template-security-baseline.sh`, `scripts/validation/check-quickwin-baseline.sh` | `security-auditor` | all other agents                                 |
| `docs/05.operations/incidents/`             | `security-auditor` | `incident-responder` (read)                      |
| `infra/*/`                       | read-only          | audit only; changes owned by `infra-implementer` |

## 7. Subagent Bridge

```text
# security-auditor agent preamble
@import docs/00.agent-governance/scopes/security.md
# Audit pattern — threat-model → scan → report
# OWASP Top 10 · ASVS L2 · Docker Secrets mandatory
```

Spawn via the active runtime's delegated-agent facility. Do not embed security policy inline in agent files.

## Related Documents

- [Agent governance hub](../README.md)
- [Bootstrap rule](../rules/bootstrap.md)
- [Persona protocol](../rules/persona.md)
- [Task checklists](../rules/task-checklists.md)
- [Agentic rule](../rules/agentic.md)
