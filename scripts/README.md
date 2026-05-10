# Utilities & Automation Scripts (`scripts/`)

> Repository maintenance, utility scripts, and automation triggers.

## Overview

**KR**: 빌드, 테스트, 환경 구성 등에 필요한 보조 스크립트와 자동화 툴을 포함하는 디렉토리입니다.
**EN**: Directory containing helper scripts and automation tools for build, test, and environment setup.

## Audience

이 README의 주요 독자:

- Operators
- Developers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Repository validation, contract checks, and post-edit automation scripts.
- Tier hardening checks and their shared helper library.
- Local manual utility scripts for preflight checks, safe secret file generation, local certificate generation, and Vault AppRole bootstrap.
- Script inventory and lifecycle ownership rules for root-level `scripts/*.sh` files.

### Out of Scope

- Plaintext secret values, credentials, tokens, private keys, and generated certificate contents.
- Long-form operating procedures that belong in `docs/07.operations/`.
- Generated Graphify output under `graphify-out/`.
- Service-specific Docker Compose source files under `infra/`.

## Structure

```text
scripts/
├── *.sh                 # Root validation, hook, hardening, and manual utility entrypoints
├── lib/
│   └── hardening-lib.sh # Shared implementation for tier hardening checks
└── README.md            # This file
```

## How to Work in This Area

1. Read this README before adding, renaming, or removing a root script.
2. Keep every root `scripts/*.sh` file listed in the inventory below.
3. Reference non-standalone root scripts from a repository entrypoint, stage document, runtime hook, or CI workflow.
4. Use `scripts/check-repo-contracts.sh` to verify script inventory, external references, and library usage.
5. Keep secret-related examples procedural only; do not print or document generated secret values.

## Navigation / Inventory

| Component | Path | Purpose |
| :--- | :--- | :--- |
| Docker Validation | [validate-docker-compose.sh](validate-docker-compose.sh) | Validate root compose config |
| Repo Contract Check | [check-repo-contracts.sh](check-repo-contracts.sh) | Enforce docs, GitHub, script, image, and runtime governance contracts |
| QuickWin Baseline Check | [check-quickwin-baseline.sh](check-quickwin-baseline.sh) | Enforce PLN-QW-001~005 baseline controls |
| Template & Security Baseline Check | [check-template-security-baseline.sh](check-template-security-baseline.sh) | Enforce template adoption and required security controls |
| Documentation Traceability Check | [check-doc-traceability.sh](check-doc-traceability.sh) | Enforce sync links across 05.plans ↔ 07.operations |
| Graphify Health Report | [report-graphify-health.sh](report-graphify-health.sh) | Report advisory health of generated Graphify corpus without blocking validation |
| Post Tool Validation | [post-tool-validate.sh](post-tool-validate.sh) | Run path-aware validation after Claude/Codex file edits |
| Unified Hardening Check | [check-all-hardening.sh](check-all-hardening.sh) | Run all tier hardening checks, or one selected tier |
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
| Secret Generation | [gen-secrets.sh](gen-secrets.sh) | Generate local Docker secret files from `.env` defaults |
| Cert Generation | [generate-local-certs.sh](generate-local-certs.sh) | Generate local TLS files |
| Vault AppRole Bootstrap | [bootstrap-vault-approle.sh](bootstrap-vault-approle.sh) | Configure Vault Agent AppRole credentials after Vault is running and unsealed |

## Script Lifecycle

| Lifecycle | Scripts |
| :--- | :--- |
| CI / quality gate | `check-repo-contracts.sh`, `validate-docker-compose.sh`, `check-doc-traceability.sh`, `check-quickwin-baseline.sh`, `check-template-security-baseline.sh`, `check-all-hardening.sh` |
| Advisory evidence | `report-graphify-health.sh` |
| Runtime hook | `post-tool-validate.sh` |
| Tier wrapper | `check-gateway-hardening.sh`, `check-auth-hardening.sh`, `check-security-hardening.sh`, `check-data-hardening.sh`, `check-messaging-hardening.sh`, `check-observability-hardening.sh`, `check-workflow-hardening.sh`, `check-ai-hardening.sh`, `check-tooling-hardening.sh`, `check-laboratory-hardening.sh` |
| Manual operations | `preflight-compose.sh`, `gen-secrets.sh`, `generate-local-certs.sh`, `bootstrap-vault-approle.sh` |
| Internal library | `scripts/lib/hardening-lib.sh` |

Root scripts must stay listed in this README. A root script that is intended to
remain standalone without an external repository reference must be explicitly
listed in the external-reference exemption set in `check-repo-contracts.sh`.
All other root scripts must be referenced by a repository entrypoint, stage
document, runtime hook, or CI workflow.

---

## 🛠️ Utilities & Automation

### Standard Rules

- **Idempotency**: All scripts MUST be safe to run multiple times without causing corrupted state.
- **No Secrets**: Scripts must fetch credentials from environment variables; never hardcode them.
- **Deterministic**: Any automation added must comply with repository governance in `../docs/00.agent-governance/rules/`.

### Usage Examples

```bash
# Run preflight check
./scripts/preflight-compose.sh

# Enforce repository contracts
./scripts/check-repo-contracts.sh

# Enforce Quick Win baseline
./scripts/check-quickwin-baseline.sh

# Enforce Quick Win baseline for an explicit compose profile set
# Fails when any selected profile has baseline violations.
HYHOME_COMPOSE_PROFILES="core dev" ./scripts/check-quickwin-baseline.sh

# Enforce template + security baseline
./scripts/check-template-security-baseline.sh

# Enforce documentation traceability sync
./scripts/check-doc-traceability.sh

# Report advisory Graphify corpus health
./scripts/report-graphify-health.sh

# Run provider-neutral post-edit validation from hook payload
./scripts/post-tool-validate.sh

# Enforce all tier hardening baselines
./scripts/check-all-hardening.sh

# Enforce one selected tier
./scripts/check-all-hardening.sh 01-gateway

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

# Generate local TLS certificates
bash scripts/generate-local-certs.sh

```

---

## Related References

- [🤖 Agent Governance](../AGENTS.md)
- [⚙️ Operations Baseline](../docs/07.operations/README.md)
- [📘 Runbooks](../docs/07.operations/README.md)
- [Scripts Lifecycle Contract Cleanup Plan](../docs/05.plans/2026-05-09-scripts-lifecycle-contract-cleanup.md)

Note: QuickWin baseline exceptions are sourced from `infra/common-optimizations.exceptions.json`.
