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

- Repository validation, implementation-alignment checks, contract checks, local QA gate orchestration, and agent event hook automation scripts.
- Repo-local LLM Wiki index generation and freshness checks.
- Tier hardening checks and their shared helper library.
- Local preflight validation mode and safe secret file generation utility.
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
├── hardening/           # Unified hardening check with tier arguments
├── hooks/               # Provider-neutral hook dispatcher and post-tool validation
├── knowledge/           # LLM Wiki and Graphify advisory utilities
├── operations/          # Safe secret-generation utility
├── requirements.txt     # Python modules required by repository validation scripts
├── lib/
│   └── hardening-lib.sh # Shared implementation for tier hardening checks
└── README.md            # This file
```

## Purpose Folder Implementation

The canonical script surface is the purpose-folder path. Root-level
`scripts/*.sh` duplicates were removed after docs, CI, hooks, and pre-commit
references moved to purpose-folder paths. Do not recreate root duplicate
wrappers unless a future approved compatibility plan explicitly requires them.

The hardening surface is intentionally consolidated into
`scripts/hardening/check-all-hardening.sh`. Tier-specific wrapper entrypoints
were removed by the 2026-05-17 cleanup; use tier arguments instead.

| Purpose    | Canonical paths                                                                                                                                                                                                                                                                                                                                                                                                    |
| :--------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Validation | `scripts/validation/validate-docker-compose.sh`, `scripts/validation/validate-harness.sh`, `scripts/validation/check-repo-contracts.sh`, `scripts/validation/check-doc-implementation-alignment.sh`, `scripts/validation/check-storybook-contract.sh`, `scripts/validation/check-doc-traceability.sh`, `scripts/validation/check-quickwin-baseline.sh`, `scripts/validation/check-template-security-baseline.sh`, `scripts/validation/run-local-qa-gates.sh` |
| Hardening  | `scripts/hardening/check-all-hardening.sh`                                                                                                                                                                                                                                                                                                                                                                         |
| Hooks      | `scripts/hooks/agent-event-hook.sh`, `scripts/hooks/patch-graphify-post-commit.sh`, `scripts/hooks/post-tool-validate.sh`                                                                                                                                                                                                                                                                                          |
| Knowledge  | `scripts/knowledge/generate-llm-wiki-index.sh`, `scripts/knowledge/report-graphify-health.sh`                                                                                                                                                                                                                                                                                                                      |
| Operations | `scripts/operations/gen-secrets.sh`, `scripts/operations/use-qa-ci-tools.sh`, `scripts/operations/sync-provider-surfaces.sh`, `scripts/operations/sync-tech-stack-versions.sh`                                                                                                                                                                                                                                     |
| Libraries  | `scripts/lib/hardening-lib.sh`, `scripts/requirements.txt`                                                                                                                                                                                                                                                                                                                                                         |

## How to Work in This Area

1. Read this README before adding, renaming, or removing a script.
2. Place new scripts under the existing purpose folder that owns the behavior.
3. Do not add root-level `scripts/*.sh` duplicates for purpose-folder scripts.
4. Reference canonical purpose-folder paths from docs, CI, hooks, and pre-commit entries.
5. Use `scripts/validation/check-repo-contracts.sh` to verify script inventory, references, and library usage.
6. Keep secret-related examples procedural only; do not print or document generated secret values.
7. Keep Python module dependencies for repository validation scripts in `scripts/requirements.txt`.

## Active Surface Retention Rules

Keep a root `scripts/` implementation when any active surface uses it:

- GitHub Actions, pre-commit, Claude/Codex hooks, root README files, active
  specs, active operations docs, or `infra/**/README.md` reference the script.
- Another implementation script sources it as a library.
- The script is the single canonical entrypoint for a manual operation, such as
  local preflight checks or local secret file generation.

Remove or reject a script when it is only a duplicate wrapper, a one-off operation
captured by active documentation, or a deleted entrypoint reintroduced without an
approved compatibility plan. Historical references under completed requirements,
architecture decisions, execution evidence, governance memory, or generated
reference artifacts are audit evidence and do not by themselves justify keeping a
script.

## Navigation / Inventory

| Component                              | Path                                                                                        | Purpose                                                                                                                                                                                                         |
| :------------------------------------- | :------------------------------------------------------------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Docker Validation                      | [validate-docker-compose.sh](./validation/validate-docker-compose.sh)                       | Validate root compose config                                                                                                                                                                                    |
| Harness Validation                     | [validate-harness.sh](./validation/validate-harness.sh)                                     | Run the harness-surface validation wrapper without duplicating local QA gate logic                                                                                                                               |
| Repo Contract Check                    | [check-repo-contracts.sh](./validation/check-repo-contracts.sh)                             | Enforce docs, GitHub, script, image, runtime governance, Hookify metadata, and execution evidence status contracts                                                                                              |
| Storybook Contract Check               | [check-storybook-contract.sh](./validation/check-storybook-contract.sh)                     | Enforce Storybook CI scripts, workflow wiring, and 90% coverage threshold metadata                                                                                                                              |
| QuickWin Baseline Check                | [check-quickwin-baseline.sh](./validation/check-quickwin-baseline.sh)                       | Enforce PLN-QW-001~005 baseline controls                                                                                                                                                                        |
| Template & Security Baseline Check     | [check-template-security-baseline.sh](./validation/check-template-security-baseline.sh)     | Enforce template adoption and required security controls                                                                                                                                                        |
| Documentation Implementation Alignment | [check-doc-implementation-alignment.sh](./validation/check-doc-implementation-alignment.sh) | Validate active Stage 01-05 docs against tracked implementation surfaces, removed template names, archive index-only links, operations service coverage, scripts, and workflow paths                            |
| Documentation Traceability Check       | [check-doc-traceability.sh](./validation/check-doc-traceability.sh)                         | Enforce sync links across 04.execution/plans ↔ 05.operations                                                                                                                                                    |
| Local QA Gate Runner                   | [run-local-qa-gates.sh](./validation/run-local-qa-gates.sh)                                 | Run locally reproducible script-backed QA/CI gates and list remote-only CI responsibilities                                                                                                                     |
| LLM Wiki Index Generator               | [generate-llm-wiki-index.sh](./knowledge/generate-llm-wiki-index.sh)                        | Generate and check the repo-local LLM Wiki path index                                                                                                                                                           |
| Graphify Health Report                 | [report-graphify-health.sh](./knowledge/report-graphify-health.sh)                          | Report advisory health of generated Graphify corpus without blocking validation                                                                                                                                 |
| Agent Event Hook                       | [agent-event-hook.sh](./hooks/agent-event-hook.sh)                                          | Dispatch Claude/Codex hook events, including template-first target-stage docs guidance, governance memory guidance, post-edit style validation/formatting, logical commit completion reminders, and Stop gating |
| Post Tool Validation                   | [post-tool-validate.sh](./hooks/post-tool-validate.sh)                                      | Run path-aware validation, including changed-doc template enforcement, after Claude/Codex file edits                                                                                                            |
| Graphify Post-commit Patcher           | [patch-graphify-post-commit.sh](./hooks/patch-graphify-post-commit.sh)                      | Re-apply the graphify-out filter to `.git/hooks/post-commit` after hook resets                                                                                                                                  |
| Unified Hardening Check                | [check-all-hardening.sh](./hardening/check-all-hardening.sh)                                | Run all tier hardening checks, or one selected tier                                                                                                                                                             |
| QA/CI Tooling Environment              | [use-qa-ci-tools.sh](./operations/use-qa-ci-tools.sh)                                       | Expose user-global QA/CI tools to restricted agent shells                                                                                                                                                       |
| Docker Preflight Mode                  | [validate-docker-compose.sh](./validation/validate-docker-compose.sh) `--preflight`         | Real local prerequisite validation without dummy file creation                                                                                                                                                  |
| Secret Generation                      | [gen-secrets.sh](./operations/gen-secrets.sh)                                               | Generate local Docker secret files; use `--check` or `--dry-run` before default generation                                                                                                                      |
| Provider Surface Sync                  | [sync-provider-surfaces.sh](./operations/sync-provider-surfaces.sh)                         | Regenerate the Codex mirror and Gemini reference index from the canonical Claude runtime; default verifies, `--write` applies                                                                                   |
| Tech-Stack Version Sync                | [sync-tech-stack-versions.sh](./operations/sync-tech-stack-versions.sh)                     | Re-point curated `infra/tech-stack.versions.json` images to declared compose tags; default writes, `--check` verifies, `--dry-run` previews                                                                     |

## Hardening Tier Arguments

Use `bash scripts/hardening/check-all-hardening.sh <tier>` for a selected
tier. Without arguments, all supported tiers are checked.

| Tier          | Accepted arguments                         |
| :------------ | :----------------------------------------- |
| Gateway       | `01-gateway`, `gateway`                    |
| Auth          | `02-auth`, `auth`                          |
| Security      | `03-security`, `security`                  |
| Data          | `04-data`, `data`                          |
| Messaging     | `05-messaging`, `messaging`                |
| Observability | `06-observability`, `observability`, `obs` |
| Workflow      | `07-workflow`, `workflow`                  |
| AI            | `08-ai`, `ai`                              |
| Tooling       | `09-tooling`, `tooling`                    |
| Laboratory    | `11-laboratory`, `laboratory`, `lab`       |

## Script Lifecycle

| Lifecycle                   | Scripts                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :-------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CI / quality gate           | `scripts/validation/validate-harness.sh`, `scripts/validation/run-local-qa-gates.sh`, `scripts/validation/check-repo-contracts.sh`, `scripts/validation/check-doc-implementation-alignment.sh`, `scripts/validation/validate-docker-compose.sh`, `scripts/validation/check-doc-traceability.sh`, `scripts/validation/check-storybook-contract.sh`, `scripts/validation/check-quickwin-baseline.sh`, `scripts/validation/check-template-security-baseline.sh`, `scripts/hardening/check-all-hardening.sh`, `scripts/knowledge/generate-llm-wiki-index.sh --check` |
| Advisory evidence           | `scripts/knowledge/report-graphify-health.sh`                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| Runtime hook                | `scripts/hooks/agent-event-hook.sh`, `scripts/hooks/post-tool-validate.sh`                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Tier hardening              | `scripts/hardening/check-all-hardening.sh <tier>`                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Manual operations           | `scripts/validation/validate-docker-compose.sh --preflight`, `scripts/operations/gen-secrets.sh`                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Agent QA/CI environment     | `source scripts/operations/use-qa-ci-tools.sh`                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Generated index maintenance | `scripts/knowledge/generate-llm-wiki-index.sh`                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Internal library            | `scripts/lib/hardening-lib.sh`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

`scripts/operations/gen-secrets.sh` is a manual operation entrypoint. Its
no-argument mode may read or write local secret registry and secret files; use
`--check` for readiness checks and `--dry-run` for ID/path-only action previews
before running the default mode.

`scripts/hooks/post-tool-validate.sh` is a hook payload consumer. With no JSON
payload or no changed paths, it exits successfully without running validators.
Use `--check` or `POST_TOOL_VALIDATE_CHECK_ONLY=1` to run non-mutating
validation; check-only mode disables whitespace writes and `shfmt -w` while
preserving diff, syntax, and repo checks.

`scripts/validation/run-local-qa-gates.sh` is the local script-backed QA/CI
orchestrator. Default mode runs only checks that are safe to execute locally.
Use `--list` to see local, CI/local-tooling, and remote-only responsibilities.
Use `--all-profiles` to run the same local gates with the governed all-profile
Compose set unless `HYHOME_COMPOSE_PROFILES` is already set.

Repo-local Hookify metadata validation currently supports only `bash`, `file`,
and `stop` events, as enforced by
`scripts/validation/check-repo-contracts.sh`. External Hookify event names are
not automatically accepted by this repository.

---

## Utilities & Automation

### Standard Rules

- **Idempotency**: All scripts MUST be safe to run multiple times without causing corrupted state.
- **No Secrets**: Scripts must fetch credentials from environment variables; never hardcode them.
- **Deterministic**: Any automation added must comply with repository governance in `../docs/00.agent-governance/rules/`.

### Usage Examples

```bash
# Run real local preflight checks without creating dummy files
./scripts/validation/validate-docker-compose.sh --preflight

# Enforce repository contracts
./scripts/validation/check-repo-contracts.sh

# Enforce active docs to tracked implementation alignment
bash scripts/validation/check-doc-implementation-alignment.sh

# Enforce Quick Win baseline
./scripts/validation/check-quickwin-baseline.sh

# Enforce Quick Win baseline for an explicit compose profile set
# Fails when any selected profile has baseline violations.
HYHOME_COMPOSE_PROFILES="core dev" ./scripts/validation/check-quickwin-baseline.sh

# Enforce template + security baseline
./scripts/validation/check-template-security-baseline.sh

# Enforce documentation traceability sync
./scripts/validation/check-doc-traceability.sh

# Run locally reproducible QA/CI gates
./scripts/validation/run-local-qa-gates.sh

# Show local vs remote-only QA/CI responsibilities
./scripts/validation/run-local-qa-gates.sh --list

# Run the harness-change-scoped fast gate
./scripts/validation/validate-harness.sh

# Run the same harness subset through the local QA gate runner
./scripts/validation/run-local-qa-gates.sh --harness

# Generate the repo-local LLM Wiki path index
bash scripts/knowledge/generate-llm-wiki-index.sh

# Verify the repo-local LLM Wiki path index is fresh
bash scripts/knowledge/generate-llm-wiki-index.sh --check

# Report advisory Graphify corpus health
./scripts/knowledge/report-graphify-health.sh

# Dispatch a provider-neutral PreToolUse hook event
printf '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"rg hook"}}' | bash scripts/hooks/agent-event-hook.sh PreToolUse

# Run provider-neutral post-edit validation from a file-edit hook payload
printf '{"tool_input":{"file_path":"docs/00.agent-governance/memory/progress.md"}}' | bash scripts/hooks/post-tool-validate.sh

# Run provider-neutral post-edit validation without formatting writes
printf '{"tool_input":{"file_path":"docs/00.agent-governance/memory/progress.md"}}' | bash scripts/hooks/post-tool-validate.sh --check

# Enforce all tier hardening baselines
./scripts/hardening/check-all-hardening.sh

# Enforce one selected tier
./scripts/hardening/check-all-hardening.sh 01-gateway

# Inspect secret-generation readiness without reading or writing secret values
./scripts/operations/gen-secrets.sh --check

# Preview secret-generation actions by ID/path only
./scripts/operations/gen-secrets.sh --dry-run

# Verify the tech-stack version registry is synced to declared compose tags
bash scripts/operations/sync-tech-stack-versions.sh --check

# Preview planned tech-stack registry tag updates without writing
bash scripts/operations/sync-tech-stack-versions.sh --dry-run

# Re-point the tech-stack registry to declared compose tags
bash scripts/operations/sync-tech-stack-versions.sh

# Make globally installed QA/CI tools available in restricted agent shells
source scripts/operations/use-qa-ci-tools.sh

# Verify the agent-visible QA/CI toolchain
./scripts/operations/use-qa-ci-tools.sh

```

---

## Related Documents

- [🤖 Agent Governance](../AGENTS.md)
- [⚙️ Operations Baseline](../docs/05.operations/README.md)
- [📘 Runbooks](../docs/05.operations/README.md)
- [LLM Wiki Maintenance](../docs/05.operations/guides/90-knowledge/llm-wiki-maintenance.md)
- [LLM Wiki Generated Index](../docs/90.references/llm-wiki/index.md)
- [Scripts CI/CD & QA Cleanup Plan](../docs/04.execution/plans/2026-05-17-scripts-ci-qa-cleanup.md)
- [Scripts Lifecycle Contract Cleanup Plan](../docs/04.execution/plans/2026-05-09-scripts-lifecycle-contract-cleanup.md)

Note: QuickWin baseline exceptions are sourced from `infra/common-optimizations.exceptions.json`.
