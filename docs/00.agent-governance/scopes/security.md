---
layer: security
title: 'Security Enforcement Scope'
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
- Network hardening:
  - isolate traffic on intended networks,
  - enforce TLS at ingress boundaries.

## 3. Implementation Flow

1. Perform lightweight threat modeling for new/changed services.
2. Run security checks defined in active scope plus `rules/task-checklists.md`.
3. Apply static analysis and dependency risk checks where available.

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
| `scripts/check-all-hardening.sh` | `security-auditor` | all other agents                                 |
| `scripts/check-*-baseline.sh`    | `security-auditor` | all other agents                                 |
| `docs/10.incidents/`             | `security-auditor` | `incident-responder` (read)                      |
| `infra/*/`                       | read-only          | audit only; changes owned by `infra-implementer` |

## 7. Subagent Bridge

```text
# security-auditor agent preamble
@import docs/00.agent-governance/scopes/security.md
# H100:28 Audit pattern — threat-model → scan → report
# OWASP Top 10 · ASVS L2 · Docker Secrets mandatory
```

Spawn via Task tool. Do not embed security policy inline in agent files.
