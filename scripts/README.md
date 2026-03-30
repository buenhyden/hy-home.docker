# Utilities & Automation Scripts (`scripts/`)

> Repository maintenance, utility scripts, and automation triggers.

## Overview

**KR**: 빌드, 테스트, 환경 구성 등에 필요한 보조 스크립트와 자동화 툴을 포함하는 디렉토리입니다.
**EN**: Directory containing helper scripts and automation tools for build, test, and environment setup.

## Navigation / Inventory

| Component | Path | Purpose |
| :--- | :--- | :--- |
| Docker Validation | [validate-docker-compose.sh](validate-docker-compose.sh) | Validate root compose config |
| QuickWin Baseline Check | [check-quickwin-baseline.sh](check-quickwin-baseline.sh) | Enforce PLN-QW-001~005 baseline controls |
| Template & Security Baseline Check | [check-template-security-baseline.sh](check-template-security-baseline.sh) | Enforce template adoption and required security controls |
| Documentation Traceability Check | [check-doc-traceability.sh](check-doc-traceability.sh) | Enforce sync links across 05.plans ↔ 08.operations ↔ 09.runbooks |
| Gateway Hardening Check | [check-gateway-hardening.sh](check-gateway-hardening.sh) | Enforce 01-gateway Traefik/Nginx hardening baseline |
| Auth Hardening Check | [check-auth-hardening.sh](check-auth-hardening.sh) | Enforce 02-auth Keycloak/OAuth2 Proxy hardening baseline |
| Security Hardening Check | [check-security-hardening.sh](check-security-hardening.sh) | Enforce 03-security Vault hardening baseline |
| Data Hardening Check | [check-data-hardening.sh](check-data-hardening.sh) | Enforce 04-data service hardening baseline |
| Messaging Hardening Check | [check-messaging-hardening.sh](check-messaging-hardening.sh) | Enforce 05-messaging service hardening baseline |
| Observability Hardening Check | [check-observability-hardening.sh](check-observability-hardening.sh) | Enforce 06-observability service hardening baseline |
| Workflow Hardening Check | [check-workflow-hardening.sh](check-workflow-hardening.sh) | Enforce 07-workflow service hardening baseline |
| AI Hardening Check | [check-ai-hardening.sh](check-ai-hardening.sh) | Enforce 08-ai service hardening baseline |
| Tooling Hardening Check | [check-tooling-hardening.sh](check-tooling-hardening.sh) | Enforce 09-tooling service hardening baseline |
| Laboratory Hardening Check | [check-laboratory-hardening.sh](check-laboratory-hardening.sh) | Enforce 11-laboratory service hardening baseline |
| Preflight Check | [preflight-compose.sh](preflight-compose.sh) | Bootstrap prerequisite validation |
| Cert Generation | [generate-local-certs.sh](generate-local-certs.sh) | Generate local TLS files |

---

## 🛠️ Utilities & Automation

### Standard Rules

- **Idempotency**: All scripts MUST be safe to run multiple times without causing corrupted state.
- **No Secrets**: Scripts must fetch credentials from environment variables; never hardcode them.
- **Deterministic**: Any automation added must comply with standard rules in `.agent/rules/0200-workflows-pillar-standard.md`.

### Usage Examples

```bash
# Run preflight check
./scripts/preflight-compose.sh

# Enforce Quick Win baseline
./scripts/check-quickwin-baseline.sh

# Enforce template + security baseline
./scripts/check-template-security-baseline.sh

# Enforce documentation traceability sync
./scripts/check-doc-traceability.sh

# Enforce 01-gateway hardening baseline
./scripts/check-gateway-hardening.sh

# Enforce 02-auth hardening baseline
./scripts/check-auth-hardening.sh

# Enforce 03-security hardening baseline
./scripts/check-security-hardening.sh

# Enforce 04-data hardening baseline
./scripts/check-data-hardening.sh

# Enforce 05-messaging hardening baseline
./scripts/check-messaging-hardening.sh

# Enforce 06-observability hardening baseline
./scripts/check-observability-hardening.sh

# Enforce 07-workflow hardening baseline
./scripts/check-workflow-hardening.sh

# Enforce 08-ai hardening baseline
./scripts/check-ai-hardening.sh

# Enforce 09-tooling hardening baseline
./scripts/check-tooling-hardening.sh

# Enforce 11-laboratory hardening baseline
./scripts/check-laboratory-hardening.sh

```

---

## Extensibility & References

- [🤖 Agent Governance](/AGENTS.md)
- [⚙️ Operations Baseline](/OPERATION.md)

---
*Maintained by DevOps & Automation Team*

Note: QuickWin baseline exceptions are sourced from `infra/common-optimizations.exceptions.json`.
