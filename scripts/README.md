# Utilities & Automation Scripts (`scripts/`)

> Repository maintenance, utility scripts, and automation triggers.

## Overview

**KR**: 빌드, 테스트, 환경 구성 등에 필요한 보조 스크립트와 자동화 툴을 포함하는 디렉토리입니다.
**EN**: Directory containing helper scripts and automation tools for build, test, and environment setup.

## Navigation / Inventory

| Component | Path | Purpose |
| :--- | :--- | :--- |
| Secrets Bootstrap | [bootstrap-secrets.sh](bootstrap-secrets.sh) | Create file-based secrets |
| Docker Validation | [validate-docker-compose.sh](validate-docker-compose.sh) | Validate root compose config |
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

# Bootstrap secrets
./scripts/bootstrap-secrets.sh --force
```

---

## Extensibility & References

- [🤖 Agent Governance](/AGENTS.md)
- [⚙️ Operations Baseline](/OPERATION.md)

---
*Maintained by DevOps & Automation Team*
