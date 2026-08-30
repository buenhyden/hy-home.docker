---
profile_id: data
status: active
artifact_id: DATA-0076
artifact_type: data
parent_ids: []
created: 2026-08-19
updated: 2026-08-23
observed_at: 2026-08-23
generated_by: scripts/knowledge/generate-llm-wiki.py
---

# LLM Wiki Stage Category Coverage

## Purpose

This generated reference summarizes the safe tracked source paths that feed the repo-local LLM Wiki index by source bucket, LLM Wiki category, and path role.

Provide audit consumers with a compact coverage snapshot without duplicating the full generated index or changing canonical source ownership.

## Schema

Counts are grouped by source bucket, navigation category, and derived path role, with representative repository-relative links.

## Provenance

This package is generated from the same safe tracked candidate set as DATA-0082. Runtime truth remains in canonical tracked sources.

### In Scope

- Counts by source bucket, LLM Wiki category, and path role.
- Representative links for each category.
- Deterministic freshness through `python3 scripts/knowledge/generate-llm-wiki.py --check`.

### Out of Scope

- Full-content export or public website generation.
- Runtime behavior, deployment workflow, network publishing, or external model calls.
- Secret contents, credentials, private keys, tokens, shell history, raw logs, `volumes/`, dependency trees, generated/minified artifacts, and `graphify-out/` as evidence.

## Inventory

- Safe tracked source paths: `929`
- Source buckets: `16`
- LLM Wiki categories: `12`
- Path roles: `7`

## Source Bucket Coverage

| Source Bucket | Paths | Representative Paths |
| --- | ---: | --- |
| `.claude` | 47 | [.claude/CLAUDE.md](../../../../.claude/CLAUDE.md)<br>[.claude/agents/ci-cd-engineer.md](../../../../.claude/agents/ci-cd-engineer.md)<br>[.claude/agents/code-reviewer.md](../../../../.claude/agents/code-reviewer.md) |
| `.codex` | 16 | [.codex/README.md](../../../../.codex/README.md)<br>[.codex/agents/ci-cd-engineer.toml](../../../../.codex/agents/ci-cd-engineer.toml)<br>[.codex/agents/code-reviewer.toml](../../../../.codex/agents/code-reviewer.toml) |
| `.github` | 17 | [.github/CODEOWNERS](../../../../.github/CODEOWNERS)<br>[.github/INDEX.md](../../../../.github/INDEX.md)<br>[.github/ISSUE_TEMPLATE/bug_report.yml](../../../../.github/ISSUE_TEMPLATE/bug_report.yml) |
| `docs/00.agent-governance` | 77 | [docs/00.agent-governance/README.md](../../../00.agent-governance/README.md)<br>[docs/00.agent-governance/policies/agentic.md](../../../00.agent-governance/policies/agentic.md)<br>[docs/00.agent-governance/policies/approval-boundaries.md](../../../00.agent-governance/policies/approval-boundaries.md) |
| `docs/01.requirements` | 26 | [docs/01.requirements/0001-gateway.md](../../../01.requirements/0001-gateway.md)<br>[docs/01.requirements/0002-auth.md](../../../01.requirements/0002-auth.md)<br>[docs/01.requirements/0003-security.md](../../../01.requirements/0003-security.md) |
| `docs/02.architecture` | 54 | [docs/02.architecture/README.md](../../../02.architecture/README.md)<br>[docs/02.architecture/decisions/0001-traefik-nginx-hybrid.md](../../../02.architecture/decisions/0001-traefik-nginx-hybrid.md)<br>[docs/02.architecture/decisions/0002-keycloak-oauth2-proxy-choice.md](../../../02.architecture/decisions/0002-keycloak-oauth2-proxy-choice.md) |
| `docs/03.specs` | 61 | [docs/03.specs/0001-gateway/spec.md](../../../03.specs/0001-gateway/spec.md)<br>[docs/03.specs/0002-auth/spec.md](../../../03.specs/0002-auth/spec.md)<br>[docs/03.specs/0003-security/spec.md](../../../03.specs/0003-security/spec.md) |
| `docs/05.operations` | 208 | [docs/05.operations/README.md](../../../05.operations/README.md)<br>[docs/05.operations/catalog/00-workspace/0001-common-optimizations-template-exceptions/policy.md](../../../05.operations/catalog/00-workspace/0001-common-optimizations-template-exceptions/policy.md)<br>[docs/05.operations/catalog/00-workspace/0002-developer-environment/guide.md](../../../05.operations/catalog/00-workspace/0002-developer-environment/guide.md) |
| `docs/90.references` | 92 | [docs/90.references/README.md](../../README.md)<br>[docs/90.references/audits/0001-readme/README.md](../../audits/0001-readme/README.md)<br>[docs/90.references/audits/0002-automation-coverage-map/README.md](../../audits/0002-automation-coverage-map/README.md) |
| `docs/98.archive` | 4 | [docs/98.archive/README.md](../../../98.archive/README.md)<br>[docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md](../../../98.archive/migrations/0001-sdlc-taxonomy-convergence.md)<br>[docs/98.archive/migrations/0002-operations-catalog-convergence.md](../../../98.archive/migrations/0002-operations-catalog-convergence.md) |
| `docs/99.templates` | 28 | [docs/99.templates/README.md](../../../99.templates/README.md)<br>[docs/99.templates/contracts/document-profile.schema.json](../../../99.templates/contracts/document-profile.schema.json)<br>[docs/99.templates/contracts/frontmatter.schema.json](../../../99.templates/contracts/frontmatter.schema.json) |
| `docs/README.md` | 1 | [docs/README.md](../../../README.md) |
| `infra` | 251 | [infra/01-gateway/README.md](../../../../infra/01-gateway/README.md)<br>[infra/01-gateway/nginx/README.md](../../../../infra/01-gateway/nginx/README.md)<br>[infra/01-gateway/nginx/config/nginx.conf](../../../../infra/01-gateway/nginx/config/nginx.conf) |
| `root` | 7 | [.pre-commit-config.yaml](../../../../.pre-commit-config.yaml)<br>[AGENTS.md](../../../../AGENTS.md)<br>[CLAUDE.md](../../../../CLAUDE.md) |
| `scripts` | 39 | [scripts/README.md](../../../../scripts/README.md)<br>[scripts/hardening/check-all-hardening.sh](../../../../scripts/hardening/check-all-hardening.sh)<br>[scripts/hooks/agent-event-hook.sh](../../../../scripts/hooks/agent-event-hook.sh) |
| `secrets` | 1 | [secrets/README.md](../../../../secrets/README.md) |

## LLM Wiki Category Coverage

| Category | Paths | Representative Paths |
| --- | ---: | --- |
| Root entrypoints | 7 | [.pre-commit-config.yaml](../../../../.pre-commit-config.yaml)<br>[AGENTS.md](../../../../AGENTS.md)<br>[CLAUDE.md](../../../../CLAUDE.md) |
| LLM Wiki reference | 1 | [docs/90.references/data/0083-repository-map/README.md](../0083-repository-map/README.md) |
| Agent governance | 77 | [docs/00.agent-governance/README.md](../../../00.agent-governance/README.md)<br>[docs/00.agent-governance/policies/agentic.md](../../../00.agent-governance/policies/agentic.md)<br>[docs/00.agent-governance/policies/approval-boundaries.md](../../../00.agent-governance/policies/approval-boundaries.md) |
| Runtime surfaces | 63 | [.claude/CLAUDE.md](../../../../.claude/CLAUDE.md)<br>[.claude/agents/ci-cd-engineer.md](../../../../.claude/agents/ci-cd-engineer.md)<br>[.claude/agents/code-reviewer.md](../../../../.claude/agents/code-reviewer.md) |
| Active stage docs | 141 | [docs/01.requirements/0001-gateway.md](../../../01.requirements/0001-gateway.md)<br>[docs/01.requirements/0002-auth.md](../../../01.requirements/0002-auth.md)<br>[docs/01.requirements/0003-security.md](../../../01.requirements/0003-security.md) |
| Operations docs | 208 | [docs/05.operations/README.md](../../../05.operations/README.md)<br>[docs/05.operations/catalog/00-workspace/0001-common-optimizations-template-exceptions/policy.md](../../../05.operations/catalog/00-workspace/0001-common-optimizations-template-exceptions/policy.md)<br>[docs/05.operations/catalog/00-workspace/0002-developer-environment/guide.md](../../../05.operations/catalog/00-workspace/0002-developer-environment/guide.md) |
| Reference and template docs | 120 | [docs/90.references/README.md](../../README.md)<br>[docs/90.references/audits/0001-readme/README.md](../../audits/0001-readme/README.md)<br>[docs/90.references/audits/0002-automation-coverage-map/README.md](../../audits/0002-automation-coverage-map/README.md) |
| Infrastructure source | 251 | [infra/01-gateway/README.md](../../../../infra/01-gateway/README.md)<br>[infra/01-gateway/nginx/README.md](../../../../infra/01-gateway/nginx/README.md)<br>[infra/01-gateway/nginx/config/nginx.conf](../../../../infra/01-gateway/nginx/config/nginx.conf) |
| Scripts and validators | 39 | [scripts/README.md](../../../../scripts/README.md)<br>[scripts/hardening/check-all-hardening.sh](../../../../scripts/hardening/check-all-hardening.sh)<br>[scripts/hooks/agent-event-hook.sh](../../../../scripts/hooks/agent-event-hook.sh) |
| GitHub workflow surface | 17 | [.github/CODEOWNERS](../../../../.github/CODEOWNERS)<br>[.github/INDEX.md](../../../../.github/INDEX.md)<br>[.github/ISSUE_TEMPLATE/bug_report.yml](../../../../.github/ISSUE_TEMPLATE/bug_report.yml) |
| Secret-handling policy | 1 | [secrets/README.md](../../../../secrets/README.md) |
| Other tracked source | 4 | [docs/98.archive/README.md](../../../98.archive/README.md)<br>[docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md](../../../98.archive/migrations/0001-sdlc-taxonomy-convergence.md)<br>[docs/98.archive/migrations/0002-operations-catalog-convergence.md](../../../98.archive/migrations/0002-operations-catalog-convergence.md) |

## Path Role Coverage

| Role | Paths |
| --- | ---: |
| JSON registry | 77 |
| Markdown reference | 489 |
| YAML config | 110 |
| folder index | 169 |
| script | 53 |
| source path | 27 |
| text entrypoint | 4 |

## Refresh

- **Owner**: `doc-writer` using the `knowledge-map-agent` function.
- **Review Cadence**: Review after root entrypoint, governance, operations, script inventory, infrastructure index, or LLM Wiki path changes.
- **Update Trigger**: Run `python3 scripts/knowledge/generate-llm-wiki.py --write` after in-scope path changes and `python3 scripts/knowledge/generate-llm-wiki.py --check` during validation.

## Consumers

Audit tooling, documentation validators, and AI agents consume this package as coverage evidence only.

## Traceability

- [LLM Wiki generated index](../0082-llm-wiki-index/README.md)
- [LLM Wiki repository map](../0083-repository-map/README.md)
- [generate-llm-wiki.py](../../../../scripts/knowledge/generate-llm-wiki.py)
- [Reference data](../README.md)
- [Reference index](../../README.md)
- [LLM Wiki maintenance guide](../../../05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/guide.md)
