---
title: 'Security & Compliance Scope'
layer: security
---

# Security & Compliance Scope

Hardening, secret management, and regulatory compliance.

## 1. Context & Objective
- **Goal**: Protection of user data and infrastructure integrity.

## 2. Requirements & Constraints
- **Secrets**: NEVER commit plain-text secrets. Use `scripts/gen-secrets.sh`.

## 3. Implementation Flow
1. Run `snyk test` / `npm audit`.
2. Validate Docker Compose with `scripts/validate-docker-compose.sh`.
3. Encrypt data at rest and in transit.

## 4. Operational Procedures
- Incident response procedures in `docs/08.ops/incident`.

## 5. Maintenance & Safety
- Monthly security audit with `security-audit` skill.

