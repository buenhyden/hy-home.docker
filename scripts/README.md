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

- Repository validation, contract checks, and agent event hook automation scripts.
- Repo-local LLM Wiki index generation and freshness checks.
- Tier hardening checks and their shared helper library.
- Local manual utility scripts for preflight checks, safe secret file generation, local certificate generation, and Vault AppRole bootstrap.
- Script inventory and lifecycle ownership rules for canonical purpose-folder paths.

### Out of Scope

- Plaintext secret values, credentials, tokens, private keys, and generated certificate contents.
- Long-form operating procedures that belong in `docs/05.operations/`.
- Generated Graphify output under `graphify-out/`.
- Service-specific Docker Compose source files under `infra/`.

## Structure

```text
scripts/
├── validation/          # Compose, repo, docs, template, quickwin, and preflight checks
├── hardening/           # Unified and tier-specific hardening checks
├── hooks/               # Provider-neutral hook dispatcher and post-tool validation
├── knowledge/           # LLM Wiki and Graphify advisory utilities
├── operations/          # Manual local cert, Vault AppRole, and secret-generation utilities
├── lib/
│   └── hardening-lib.sh # Shared implementation for tier hardening checks
└── README.md            # This file
```

## Purpose Folder Implementation

The canonical script surface is the purpose-folder path. Root-level
`scripts/*.sh` duplicates were removed after docs, CI, hooks, and pre-commit
references moved to purpose-folder paths. Do not recreate root duplicate
wrappers unless a future approved compatibility plan explicitly requires them.

| Purpose | Canonical paths |
| :--- | :--- |
| Validation | `scripts/validation/validate-docker-compose.sh`, `scripts/validation/check-repo-contracts.sh`, `scripts/validation/check-doc-traceability.sh`, `scripts/validation/check-quickwin-baseline.sh`, `scripts/validation/check-template-security-baseline.sh`, `scripts/validation/preflight-compose.sh` |
| Hardening | `scripts/hardening/check-all-hardening.sh`, `scripts/hardening/check-gateway-hardening.sh`, `scripts/hardening/check-auth-hardening.sh`, `scripts/hardening/check-security-hardening.sh`, `scripts/hardening/check-data-hardening.sh`, `scripts/hardening/check-messaging-hardening.sh`, `scripts/hardening/check-observability-hardening.sh`, `scripts/hardening/check-workflow-hardening.sh`, `scripts/hardening/check-ai-hardening.sh`, `scripts/hardening/check-tooling-hardening.sh`, `scripts/hardening/check-laboratory-hardening.sh` |
| Hooks | `scripts/hooks/agent-event-hook.sh`, `scripts/hooks/post-tool-validate.sh` |
| Knowledge | `scripts/knowledge/generate-llm-wiki-index.sh`, `scripts/knowledge/report-graphify-health.sh` |
| Operations | `scripts/operations/generate-local-certs.sh`, `scripts/operations/bootstrap-vault-approle.sh`, `scripts/operations/gen-secrets.sh` |
| Libraries | `scripts/lib/hardening-lib.sh` |

## How to Work in This Area

1. Read this README before adding, renaming, or removing a script.
2. Place new scripts under the existing purpose folder that owns the behavior.
3. Do not add root-level `scripts/*.sh` duplicates for purpose-folder scripts.
4. Reference canonical purpose-folder paths from docs, CI, hooks, and pre-commit entries.
5. Use `scripts/validation/check-repo-contracts.sh` to verify script inventory, references, and library usage.
6. Keep secret-related examples procedural only; do not print or document generated secret values.

## Navigation / Inventory

| Component | Path | Purpose |
| :--- | :--- | :--- |
| Docker Validation | [validate-docker-compose.sh](./validation/validate-docker-compose.sh) | Validate root compose config |
| Repo Contract Check | [check-repo-contracts.sh](./validation/check-repo-contracts.sh) | Enforce docs, GitHub, script, image, and runtime governance contracts |
| QuickWin Baseline Check | [check-quickwin-baseline.sh](./validation/check-quickwin-baseline.sh) | Enforce PLN-QW-001~005 baseline controls |
| Template & Security Baseline Check | [check-template-security-baseline.sh](./validation/check-template-security-baseline.sh) | Enforce template adoption and required security controls |
| Documentation Traceability Check | [check-doc-traceability.sh](./validation/check-doc-traceability.sh) | Enforce sync links across 04.execution/plans ↔ 05.operations |
| LLM Wiki Index Generator | [generate-llm-wiki-index.sh](./knowledge/generate-llm-wiki-index.sh) | Generate and check the repo-local LLM Wiki path index |
| Graphify Health Report | [report-graphify-health.sh](./knowledge/report-graphify-health.sh) | Report advisory health of generated Graphify corpus without blocking validation |
| Agent Event Hook | [agent-event-hook.sh](./hooks/agent-event-hook.sh) | Dispatch Claude/Codex hook events to provider-neutral repository behavior |
| Post Tool Validation | [post-tool-validate.sh](./hooks/post-tool-validate.sh) | Run path-aware validation after Claude/Codex file edits |
| Unified Hardening Check | [check-all-hardening.sh](./hardening/check-all-hardening.sh) | Run all tier hardening checks, or one selected tier |
| Gateway Hardening Check | [check-gateway-hardening.sh](./hardening/check-gateway-hardening.sh) | Enforce 01-gateway Traefik/Nginx hardening baseline |
| Auth Hardening Check | [check-auth-hardening.sh](./hardening/check-auth-hardening.sh) | Enforce 02-auth Keycloak/OAuth2 Proxy hardening baseline |
| Security Hardening Check | [check-security-hardening.sh](./hardening/check-security-hardening.sh) | Enforce 03-security Vault hardening baseline |
| Data Hardening Check | [check-data-hardening.sh](./hardening/check-data-hardening.sh) | Enforce 04-data service hardening baseline |
| Messaging Hardening Check | [check-messaging-hardening.sh](./hardening/check-messaging-hardening.sh) | Enforce 05-messaging service hardening baseline |
| Observability Hardening Check | [check-observability-hardening.sh](./hardening/check-observability-hardening.sh) | Enforce 06-observability service hardening baseline |
| Workflow Hardening Check | [check-workflow-hardening.sh](./hardening/check-workflow-hardening.sh) | Enforce 07-workflow service hardening baseline |
| AI Hardening Check | [check-ai-hardening.sh](./hardening/check-ai-hardening.sh) | Enforce 08-ai service hardening baseline |
| Tooling Hardening Check | [check-tooling-hardening.sh](./hardening/check-tooling-hardening.sh) | Enforce 09-tooling service hardening baseline |
| Laboratory Hardening Check | [check-laboratory-hardening.sh](./hardening/check-laboratory-hardening.sh) | Enforce 11-laboratory service hardening baseline |
| Preflight Check | [preflight-compose.sh](./validation/preflight-compose.sh) | Bootstrap prerequisite validation |
| Secret Generation | [gen-secrets.sh](./operations/gen-secrets.sh) | Generate local Docker secret files; use safe modes before default generation |
| Cert Generation | [generate-local-certs.sh](./operations/generate-local-certs.sh) | Generate local TLS files |
| Vault AppRole Bootstrap | [bootstrap-vault-approle.sh](./operations/bootstrap-vault-approle.sh) | Configure Vault Agent AppRole credentials after Vault is running and unsealed |

## Script Lifecycle

| Lifecycle | Scripts |
| :--- | :--- |
| CI / quality gate | `scripts/validation/check-repo-contracts.sh`, `scripts/validation/validate-docker-compose.sh`, `scripts/validation/check-doc-traceability.sh`, `scripts/validation/check-quickwin-baseline.sh`, `scripts/validation/check-template-security-baseline.sh`, `scripts/hardening/check-all-hardening.sh`, `scripts/knowledge/generate-llm-wiki-index.sh --check` |
| Advisory evidence | `scripts/knowledge/report-graphify-health.sh` |
| Runtime hook | `scripts/hooks/agent-event-hook.sh`, `scripts/hooks/post-tool-validate.sh` |
| Tier hardening | `scripts/hardening/check-gateway-hardening.sh`, `scripts/hardening/check-auth-hardening.sh`, `scripts/hardening/check-security-hardening.sh`, `scripts/hardening/check-data-hardening.sh`, `scripts/hardening/check-messaging-hardening.sh`, `scripts/hardening/check-observability-hardening.sh`, `scripts/hardening/check-workflow-hardening.sh`, `scripts/hardening/check-ai-hardening.sh`, `scripts/hardening/check-tooling-hardening.sh`, `scripts/hardening/check-laboratory-hardening.sh` |
| Manual operations | `scripts/validation/preflight-compose.sh`, `scripts/operations/gen-secrets.sh`, `scripts/operations/generate-local-certs.sh`, `scripts/operations/bootstrap-vault-approle.sh` |
| Generated index maintenance | `scripts/knowledge/generate-llm-wiki-index.sh` |
| Internal library | `scripts/lib/hardening-lib.sh` |

---

## 🛠️ Utilities & Automation

### Standard Rules

- **Idempotency**: All scripts MUST be safe to run multiple times without causing corrupted state.
- **No Secrets**: Scripts must fetch credentials from environment variables; never hardcode them.
- **Deterministic**: Any automation added must comply with repository governance in `../docs/00.agent-governance/rules/`.

### Usage Examples

```bash
# Run preflight check
./scripts/validation/preflight-compose.sh

# Enforce repository contracts
./scripts/validation/check-repo-contracts.sh

# Enforce Quick Win baseline
./scripts/validation/check-quickwin-baseline.sh

# Enforce Quick Win baseline for an explicit compose profile set
# Fails when any selected profile has baseline violations.
HYHOME_COMPOSE_PROFILES="core dev" ./scripts/validation/check-quickwin-baseline.sh

# Enforce template + security baseline
./scripts/validation/check-template-security-baseline.sh

# Enforce documentation traceability sync
./scripts/validation/check-doc-traceability.sh

# Generate the repo-local LLM Wiki path index
bash scripts/knowledge/generate-llm-wiki-index.sh

# Verify the repo-local LLM Wiki path index is fresh
bash scripts/knowledge/generate-llm-wiki-index.sh --check

# Report advisory Graphify corpus health
./scripts/knowledge/report-graphify-health.sh

# Dispatch a provider-neutral PreToolUse hook event
printf '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"rg hook"}}' | bash scripts/hooks/agent-event-hook.sh PreToolUse

# Run provider-neutral post-edit validation from hook payload
./scripts/hooks/post-tool-validate.sh

# Enforce all tier hardening baselines
./scripts/hardening/check-all-hardening.sh

# Enforce one selected tier
./scripts/hardening/check-all-hardening.sh 01-gateway

# Enforce 01-gateway hardening baseline
./scripts/hardening/check-gateway-hardening.sh

# Enforce 02-auth hardening baseline
./scripts/hardening/check-auth-hardening.sh

# Enforce 03-security hardening baseline
./scripts/hardening/check-security-hardening.sh

# Enforce 04-data hardening baseline
./scripts/hardening/check-data-hardening.sh

# Enforce 05-messaging hardening baseline
./scripts/hardening/check-messaging-hardening.sh

# Enforce 06-observability hardening baseline
./scripts/hardening/check-observability-hardening.sh

# Enforce 07-workflow hardening baseline
./scripts/hardening/check-workflow-hardening.sh

# Enforce 08-ai hardening baseline
./scripts/hardening/check-ai-hardening.sh

# Enforce 09-tooling hardening baseline
./scripts/hardening/check-tooling-hardening.sh

# Enforce 11-laboratory hardening baseline
./scripts/hardening/check-laboratory-hardening.sh

# Inspect secret-generation readiness without reading or writing secret values
./scripts/operations/gen-secrets.sh --check

# Preview secret-generation actions by ID/path only
./scripts/operations/gen-secrets.sh --dry-run

# Generate local TLS certificates
bash scripts/operations/generate-local-certs.sh

```

---

## Related Documents

- [🤖 Agent Governance](../AGENTS.md)
- [⚙️ Operations Baseline](../docs/05.operations/README.md)
- [📘 Runbooks](../docs/05.operations/README.md)
- [LLM Wiki Maintenance](../docs/05.operations/guides/llm-wiki-maintenance.md)
- [LLM Wiki Generated Index](../docs/90.references/llm-wiki/index.md)
- [Scripts Lifecycle Contract Cleanup Plan](../docs/04.execution/plans/2026-05-09-scripts-lifecycle-contract-cleanup.md)

Note: QuickWin baseline exceptions are sourced from `infra/common-optimizations.exceptions.json`.
