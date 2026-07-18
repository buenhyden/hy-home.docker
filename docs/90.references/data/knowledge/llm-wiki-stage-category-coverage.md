---
status: active
generated_by: scripts/knowledge/generate-llm-wiki-coverage.sh
---

<!-- Target: docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md -->

# Reference: LLM Wiki Stage Category Coverage

## Overview

This generated reference summarizes the safe tracked source paths that feed the repo-local LLM Wiki index by source bucket, LLM Wiki category, and path role.

## Purpose

Provide audit consumers with a compact coverage snapshot without duplicating the full generated index or changing canonical source ownership.

## Repository Role

This file is generated reference data. Runtime truth remains in tracked source files such as `docs/00.agent-governance/`, `infra/`, `scripts/`, Docker Compose files, and registry JSON files.

## Scope

### In Scope

- Counts by source bucket, LLM Wiki category, and path role.
- Representative links for each category.
- Deterministic freshness through `bash scripts/knowledge/generate-llm-wiki-coverage.sh --check`.

### Out of Scope

- Full-content export or public website generation.
- Runtime behavior, deployment workflow, network publishing, or external model calls.
- Secret contents, credentials, private keys, tokens, shell history, raw logs, `volumes/`, dependency trees, generated/minified artifacts, and `graphify-out/` as evidence.

## Definitions / Facts

- **Safe tracked source path**: a `git ls-files` path that passes the LLM Wiki allowlist and exclusion rules.
- **Source bucket**: the top-level repository surface or docs stage that owns a path.
- **LLM Wiki category**: the navigation category used by the generated LLM Wiki index.
- **Path role**: a lightweight type label derived from file name or suffix.

## Source Rules

- This snapshot excludes itself and the generated LLM Wiki index from coverage counts.
- `secrets/README.md` is counted as policy context; secret content paths are excluded.
- `graphify-out/`, `volumes/`, dependency trees, generated/minified artifacts, and lockfiles are excluded.
- Use this file as coverage/navigation evidence only; read canonical source files for implementation truth.

## Coverage Summary

- Safe tracked source paths: `1290`
- Source buckets: `17`
- LLM Wiki categories: `12`
- Path roles: `7`

## Source Bucket Coverage

| Source Bucket | Paths | Representative Paths |
| --- | ---: | --- |
| `.claude` | 46 | [.claude/CLAUDE.md](../../../../.claude/CLAUDE.md)<br>[.claude/agents/ci-cd-engineer.md](../../../../.claude/agents/ci-cd-engineer.md)<br>[.claude/agents/code-reviewer.md](../../../../.claude/agents/code-reviewer.md) |
| `.codex` | 16 | [.codex/README.md](../../../../.codex/README.md)<br>[.codex/agents/ci-cd-engineer.toml](../../../../.codex/agents/ci-cd-engineer.toml)<br>[.codex/agents/code-reviewer.toml](../../../../.codex/agents/code-reviewer.toml) |
| `.github` | 15 | [.github/CODEOWNERS](../../../../.github/CODEOWNERS)<br>[.github/ISSUE_TEMPLATE/bug_report.yml](../../../../.github/ISSUE_TEMPLATE/bug_report.yml)<br>[.github/ISSUE_TEMPLATE/feature_request.yml](../../../../.github/ISSUE_TEMPLATE/feature_request.yml) |
| `docs/00.agent-governance` | 107 | [docs/00.agent-governance/README.md](../../../00.agent-governance/README.md)<br>[docs/00.agent-governance/agents/README.md](../../../00.agent-governance/agents/README.md)<br>[docs/00.agent-governance/agents/agents/ci-cd-engineer.md](../../../00.agent-governance/agents/agents/ci-cd-engineer.md) |
| `docs/01.requirements` | 25 | [docs/01.requirements/001-gateway.md](../../../01.requirements/001-gateway.md)<br>[docs/01.requirements/002-auth.md](../../../01.requirements/002-auth.md)<br>[docs/01.requirements/003-security.md](../../../01.requirements/003-security.md) |
| `docs/02.architecture` | 51 | [docs/02.architecture/README.md](../../../02.architecture/README.md)<br>[docs/02.architecture/decisions/0001-traefik-nginx-hybrid.md](../../../02.architecture/decisions/0001-traefik-nginx-hybrid.md)<br>[docs/02.architecture/decisions/0002-keycloak-oauth2-proxy-choice.md](../../../02.architecture/decisions/0002-keycloak-oauth2-proxy-choice.md) |
| `docs/03.specs` | 97 | [docs/03.specs/001-gateway/README.md](../../../03.specs/001-gateway/README.md)<br>[docs/03.specs/001-gateway/spec.md](../../../03.specs/001-gateway/spec.md)<br>[docs/03.specs/002-auth/README.md](../../../03.specs/002-auth/README.md) |
| `docs/04.execution` | 221 | [docs/04.execution/README.md](../../../04.execution/README.md)<br>[docs/04.execution/plans/2026-03-26-01-gateway-standardization.md](../../../04.execution/plans/2026-03-26-01-gateway-standardization.md)<br>[docs/04.execution/plans/2026-03-26-02-auth-standardization.md](../../../04.execution/plans/2026-03-26-02-auth-standardization.md) |
| `docs/05.operations` | 262 | [docs/05.operations/README.md](../../../05.operations/README.md)<br>[docs/05.operations/guides/00-workspace/README.md](../../../05.operations/guides/00-workspace/README.md)<br>[docs/05.operations/guides/00-workspace/developer-setup.md](../../../05.operations/guides/00-workspace/developer-setup.md) |
| `docs/90.references` | 92 | [docs/90.references/README.md](../../README.md)<br>[docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/README.md](../../audits/2026-07-03-workspace-document-contract-audit-pack/README.md)<br>[docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/automation-coverage-map.md](../../audits/2026-07-03-workspace-document-contract-audit-pack/automation-coverage-map.md) |
| `docs/98.archive` | 21 | [docs/98.archive/04.execution/plans/2026-05-30-ai-governance-reorg.md](../../../98.archive/04.execution/plans/2026-05-30-ai-governance-reorg.md)<br>[docs/98.archive/04.execution/plans/2026-05-30-standardizing-agent-governance.md](../../../98.archive/04.execution/plans/2026-05-30-standardizing-agent-governance.md)<br>[docs/98.archive/04.execution/plans/2026-06-01-agent-governance-phase1-diagnostic.md](../../../98.archive/04.execution/plans/2026-06-01-agent-governance-phase1-diagnostic.md) |
| `docs/99.templates` | 48 | [docs/99.templates/README.md](../../../99.templates/README.md)<br>[docs/99.templates/support/README.md](../../../99.templates/support/README.md)<br>[docs/99.templates/support/archive-retention-contract.md](../../../99.templates/support/archive-retention-contract.md) |
| `docs/README.md` | 1 | [docs/README.md](../../../README.md) |
| `infra` | 245 | [infra/01-gateway/README.md](../../../../infra/01-gateway/README.md)<br>[infra/01-gateway/nginx/README.md](../../../../infra/01-gateway/nginx/README.md)<br>[infra/01-gateway/nginx/config/nginx.conf](../../../../infra/01-gateway/nginx/config/nginx.conf) |
| `root` | 8 | [.pre-commit-config.yaml](../../../../.pre-commit-config.yaml)<br>[AGENTS.md](../../../../AGENTS.md)<br>[CLAUDE.md](../../../../CLAUDE.md) |
| `scripts` | 34 | [scripts/README.md](../../../../scripts/README.md)<br>[scripts/hardening/check-all-hardening.sh](../../../../scripts/hardening/check-all-hardening.sh)<br>[scripts/hooks/agent-event-hook.sh](../../../../scripts/hooks/agent-event-hook.sh) |
| `secrets` | 1 | [secrets/README.md](../../../../secrets/README.md) |

## LLM Wiki Category Coverage

| Category | Paths | Representative Paths |
| --- | ---: | --- |
| Root entrypoints | 8 | [.pre-commit-config.yaml](../../../../.pre-commit-config.yaml)<br>[AGENTS.md](../../../../AGENTS.md)<br>[CLAUDE.md](../../../../CLAUDE.md) |
| LLM Wiki reference | 2 | [docs/90.references/llm-wiki/README.md](../../llm-wiki/README.md)<br>[docs/90.references/llm-wiki/repository-map.md](../../llm-wiki/repository-map.md) |
| Agent governance | 107 | [docs/00.agent-governance/README.md](../../../00.agent-governance/README.md)<br>[docs/00.agent-governance/agents/README.md](../../../00.agent-governance/agents/README.md)<br>[docs/00.agent-governance/agents/agents/ci-cd-engineer.md](../../../00.agent-governance/agents/agents/ci-cd-engineer.md) |
| Runtime surfaces | 62 | [.claude/CLAUDE.md](../../../../.claude/CLAUDE.md)<br>[.claude/agents/ci-cd-engineer.md](../../../../.claude/agents/ci-cd-engineer.md)<br>[.claude/agents/code-reviewer.md](../../../../.claude/agents/code-reviewer.md) |
| Active stage docs | 394 | [docs/01.requirements/001-gateway.md](../../../01.requirements/001-gateway.md)<br>[docs/01.requirements/002-auth.md](../../../01.requirements/002-auth.md)<br>[docs/01.requirements/003-security.md](../../../01.requirements/003-security.md) |
| Operations docs | 262 | [docs/05.operations/README.md](../../../05.operations/README.md)<br>[docs/05.operations/guides/00-workspace/README.md](../../../05.operations/guides/00-workspace/README.md)<br>[docs/05.operations/guides/00-workspace/developer-setup.md](../../../05.operations/guides/00-workspace/developer-setup.md) |
| Reference and template docs | 139 | [docs/90.references/README.md](../../README.md)<br>[docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/README.md](../../audits/2026-07-03-workspace-document-contract-audit-pack/README.md)<br>[docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/automation-coverage-map.md](../../audits/2026-07-03-workspace-document-contract-audit-pack/automation-coverage-map.md) |
| Infrastructure source | 245 | [infra/01-gateway/README.md](../../../../infra/01-gateway/README.md)<br>[infra/01-gateway/nginx/README.md](../../../../infra/01-gateway/nginx/README.md)<br>[infra/01-gateway/nginx/config/nginx.conf](../../../../infra/01-gateway/nginx/config/nginx.conf) |
| Scripts and validators | 34 | [scripts/README.md](../../../../scripts/README.md)<br>[scripts/hardening/check-all-hardening.sh](../../../../scripts/hardening/check-all-hardening.sh)<br>[scripts/hooks/agent-event-hook.sh](../../../../scripts/hooks/agent-event-hook.sh) |
| GitHub workflow surface | 15 | [.github/CODEOWNERS](../../../../.github/CODEOWNERS)<br>[.github/ISSUE_TEMPLATE/bug_report.yml](../../../../.github/ISSUE_TEMPLATE/bug_report.yml)<br>[.github/ISSUE_TEMPLATE/feature_request.yml](../../../../.github/ISSUE_TEMPLATE/feature_request.yml) |
| Secret-handling policy | 1 | [secrets/README.md](../../../../secrets/README.md) |
| Other tracked source | 21 | [docs/98.archive/04.execution/plans/2026-05-30-ai-governance-reorg.md](../../../98.archive/04.execution/plans/2026-05-30-ai-governance-reorg.md)<br>[docs/98.archive/04.execution/plans/2026-05-30-standardizing-agent-governance.md](../../../98.archive/04.execution/plans/2026-05-30-standardizing-agent-governance.md)<br>[docs/98.archive/04.execution/plans/2026-06-01-agent-governance-phase1-diagnostic.md](../../../98.archive/04.execution/plans/2026-06-01-agent-governance-phase1-diagnostic.md) |

## Path Role Coverage

| Role | Paths |
| --- | ---: |
| JSON registry | 69 |
| Markdown reference | 810 |
| YAML config | 109 |
| folder index | 222 |
| script | 50 |
| source path | 27 |
| text entrypoint | 3 |

## Sources

- [LLM Wiki generated index](../../llm-wiki/llm-wiki-index.md) - full safe path index
- [LLM Wiki repository map](../../llm-wiki/repository-map.md) - curated canonical source map
- [generate-llm-wiki-index.sh](../../../../scripts/knowledge/generate-llm-wiki-index.sh) - generated index source
- [generate-llm-wiki-coverage.sh](../../../../scripts/knowledge/generate-llm-wiki-coverage.sh) - this coverage snapshot generator
- [repo contract checker](../../../../scripts/validation/check-repo-contracts.sh) - freshness gate

## Maintenance

- **Owner**: `doc-writer` using the `knowledge-map-agent` function.
- **Review Cadence**: Review after root entrypoint, governance, operations, script inventory, infrastructure index, or LLM Wiki path changes.
- **Update Trigger**: Run `bash scripts/knowledge/generate-llm-wiki-coverage.sh` after in-scope path changes and `bash scripts/knowledge/generate-llm-wiki-coverage.sh --check` during validation.

## Related Documents

- [Knowledge reference data](./README.md)
- [Reference data](../README.md)
- [LLM Wiki references](../../llm-wiki/README.md)
- [LLM Wiki maintenance guide](../../../05.operations/guides/00-workspace/llm-wiki-maintenance.md)
