---
status: active
generated_by: scripts/knowledge/generate-llm-wiki.py
---

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
- Deterministic freshness through `python3 scripts/knowledge/generate-llm-wiki.py --check`.

### Out of Scope

- Full-content export or public website generation.
- Runtime behavior, deployment workflow, network publishing, or external model calls.
- Secret contents, credentials, private keys, tokens, shell history, raw logs, `volumes/`, dependency trees, generated/minified artifacts, and `graphify-out/` as evidence.

## Definitions / Facts

- **Safe tracked source path**: a repository path that passes the LLM Wiki allowlist and exclusion rules.
- **Source bucket**: the top-level repository surface or docs stage that owns a path.
- **LLM Wiki category**: the navigation category used by the generated LLM Wiki index.
- **Path role**: a lightweight type label derived from file name or suffix.

## Source Rules

- This snapshot and the generated LLM Wiki index are excluded from coverage counts.
- `secrets/README.md` is counted as policy context; secret content paths are excluded.
- `graphify-out/`, `volumes/`, dependency trees, generated/minified artifacts, and lockfiles are excluded.
- Use this file as coverage/navigation evidence only; read canonical source files for implementation truth.

## Coverage Summary

- Safe tracked source paths: `1258`
- Source buckets: `17`
- LLM Wiki categories: `12`
- Path roles: `7`

## Source Bucket Coverage

| Source Bucket | Paths | Representative Paths |
| --- | ---: | --- |
| `.claude` | 48 | [.claude/CLAUDE.md](../../../../.claude/CLAUDE.md)<br>[.claude/agents/ci-cd-engineer.md](../../../../.claude/agents/ci-cd-engineer.md)<br>[.claude/agents/code-reviewer.md](../../../../.claude/agents/code-reviewer.md) |
| `.codex` | 16 | [.codex/README.md](../../../../.codex/README.md)<br>[.codex/agents/ci-cd-engineer.toml](../../../../.codex/agents/ci-cd-engineer.toml)<br>[.codex/agents/code-reviewer.toml](../../../../.codex/agents/code-reviewer.toml) |
| `.github` | 17 | [.github/CODEOWNERS](../../../../.github/CODEOWNERS)<br>[.github/INDEX.md](../../../../.github/INDEX.md)<br>[.github/ISSUE_TEMPLATE/bug_report.yml](../../../../.github/ISSUE_TEMPLATE/bug_report.yml) |
| `docs/00.agent-governance` | 111 | [docs/00.agent-governance/README.md](../../../00.agent-governance/README.md)<br>[docs/00.agent-governance/agents/README.md](../../../00.agent-governance/agents/README.md)<br>[docs/00.agent-governance/agents/agents/ci-cd-engineer.md](../../../00.agent-governance/agents/agents/ci-cd-engineer.md) |
| `docs/01.requirements` | 26 | [docs/01.requirements/README.md](../../../01.requirements/README.md)<br>[docs/01.requirements/0001-gateway.md](../../../01.requirements/0001-gateway.md)<br>[docs/01.requirements/0002-auth.md](../../../01.requirements/0002-auth.md) |
| `docs/02.architecture` | 53 | [docs/02.architecture/README.md](../../../02.architecture/README.md)<br>[docs/02.architecture/decisions/README.md](../../../02.architecture/decisions/README.md)<br>[docs/02.architecture/decisions/0001-traefik-nginx-hybrid.md](../../../02.architecture/decisions/0001-traefik-nginx-hybrid.md) |
| `docs/03.specs` | 43 | [docs/03.specs/137-agentic-research-pack-rebuild/spec.md](../../../03.specs/137-agentic-research-pack-rebuild/spec.md)<br>[docs/03.specs/README.md](../../../03.specs/README.md)<br>[docs/03.specs/spec-0001-gateway/spec.md](../../../03.specs/spec-0001-gateway/spec.md) |
| `docs/04.execution` | 7 | [docs/04.execution/README.md](../../../04.execution/README.md)<br>[docs/04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md](../../../04.execution/plans/2026-08-08-agentic-research-pack-rebuild.md)<br>[docs/04.execution/plans/README.md](../../../04.execution/plans/README.md) |
| `docs/05.operations` | 209 | [docs/05.operations/README.md](../../../05.operations/README.md)<br>[docs/05.operations/catalog/00-workspace/README.md](../../../05.operations/catalog/00-workspace/README.md)<br>[docs/05.operations/catalog/00-workspace/ops-0001-common-optimizations-template-exceptions/policy.md](../../../05.operations/catalog/00-workspace/ops-0001-common-optimizations-template-exceptions/policy.md) |
| `docs/90.references` | 99 | [docs/90.references/README.md](../../README.md)<br>[docs/90.references/audits/README.md](../../audits/README.md)<br>[docs/90.references/audits/ref-0001-readme.md](../../audits/ref-0001-readme.md) |
| `docs/98.archive` | 275 | [docs/98.archive/README.md](../../../98.archive/README.md)<br>[docs/98.archive/changes/chg-0002-01-gateway-standardization/plan.md](../../../98.archive/changes/chg-0002-01-gateway-standardization/plan.md)<br>[docs/98.archive/changes/chg-0003-02-auth-standardization/plan.md](../../../98.archive/changes/chg-0003-02-auth-standardization/plan.md) |
| `docs/99.templates` | 49 | [docs/99.templates/README.md](../../../99.templates/README.md)<br>[docs/99.templates/support/README.md](../../../99.templates/support/README.md)<br>[docs/99.templates/support/archive-retention-contract.md](../../../99.templates/support/archive-retention-contract.md) |
| `docs/README.md` | 1 | [docs/README.md](../../../README.md) |
| `infra` | 250 | [infra/01-gateway/README.md](../../../../infra/01-gateway/README.md)<br>[infra/01-gateway/nginx/README.md](../../../../infra/01-gateway/nginx/README.md)<br>[infra/01-gateway/nginx/config/nginx.conf](../../../../infra/01-gateway/nginx/config/nginx.conf) |
| `root` | 8 | [.pre-commit-config.yaml](../../../../.pre-commit-config.yaml)<br>[AGENTS.md](../../../../AGENTS.md)<br>[CLAUDE.md](../../../../CLAUDE.md) |
| `scripts` | 45 | [scripts/README.md](../../../../scripts/README.md)<br>[scripts/hardening/check-all-hardening.sh](../../../../scripts/hardening/check-all-hardening.sh)<br>[scripts/hooks/agent-event-hook.sh](../../../../scripts/hooks/agent-event-hook.sh) |
| `secrets` | 1 | [secrets/README.md](../../../../secrets/README.md) |

## LLM Wiki Category Coverage

| Category | Paths | Representative Paths |
| --- | ---: | --- |
| Root entrypoints | 8 | [.pre-commit-config.yaml](../../../../.pre-commit-config.yaml)<br>[AGENTS.md](../../../../AGENTS.md)<br>[CLAUDE.md](../../../../CLAUDE.md) |
| LLM Wiki reference | 3 | [docs/90.references/llm-wiki/README.md](../../llm-wiki/README.md)<br>[docs/90.references/llm-wiki/llm-wiki-index.md](../../llm-wiki/llm-wiki-index.md)<br>[docs/90.references/llm-wiki/ref-0083-repository-map.md](../../llm-wiki/ref-0083-repository-map.md) |
| Agent governance | 111 | [docs/00.agent-governance/README.md](../../../00.agent-governance/README.md)<br>[docs/00.agent-governance/agents/README.md](../../../00.agent-governance/agents/README.md)<br>[docs/00.agent-governance/agents/agents/ci-cd-engineer.md](../../../00.agent-governance/agents/agents/ci-cd-engineer.md) |
| Runtime surfaces | 64 | [.claude/CLAUDE.md](../../../../.claude/CLAUDE.md)<br>[.claude/agents/ci-cd-engineer.md](../../../../.claude/agents/ci-cd-engineer.md)<br>[.claude/agents/code-reviewer.md](../../../../.claude/agents/code-reviewer.md) |
| Active stage docs | 129 | [docs/01.requirements/README.md](../../../01.requirements/README.md)<br>[docs/01.requirements/0001-gateway.md](../../../01.requirements/0001-gateway.md)<br>[docs/01.requirements/0002-auth.md](../../../01.requirements/0002-auth.md) |
| Operations docs | 209 | [docs/05.operations/README.md](../../../05.operations/README.md)<br>[docs/05.operations/catalog/00-workspace/README.md](../../../05.operations/catalog/00-workspace/README.md)<br>[docs/05.operations/catalog/00-workspace/ops-0001-common-optimizations-template-exceptions/policy.md](../../../05.operations/catalog/00-workspace/ops-0001-common-optimizations-template-exceptions/policy.md) |
| Reference and template docs | 146 | [docs/90.references/README.md](../../README.md)<br>[docs/90.references/audits/README.md](../../audits/README.md)<br>[docs/90.references/audits/ref-0001-readme.md](../../audits/ref-0001-readme.md) |
| Infrastructure source | 250 | [infra/01-gateway/README.md](../../../../infra/01-gateway/README.md)<br>[infra/01-gateway/nginx/README.md](../../../../infra/01-gateway/nginx/README.md)<br>[infra/01-gateway/nginx/config/nginx.conf](../../../../infra/01-gateway/nginx/config/nginx.conf) |
| Scripts and validators | 45 | [scripts/README.md](../../../../scripts/README.md)<br>[scripts/hardening/check-all-hardening.sh](../../../../scripts/hardening/check-all-hardening.sh)<br>[scripts/hooks/agent-event-hook.sh](../../../../scripts/hooks/agent-event-hook.sh) |
| GitHub workflow surface | 17 | [.github/CODEOWNERS](../../../../.github/CODEOWNERS)<br>[.github/INDEX.md](../../../../.github/INDEX.md)<br>[.github/ISSUE_TEMPLATE/bug_report.yml](../../../../.github/ISSUE_TEMPLATE/bug_report.yml) |
| Secret-handling policy | 1 | [secrets/README.md](../../../../secrets/README.md) |
| Other tracked source | 275 | [docs/98.archive/README.md](../../../98.archive/README.md)<br>[docs/98.archive/changes/chg-0002-01-gateway-standardization/plan.md](../../../98.archive/changes/chg-0002-01-gateway-standardization/plan.md)<br>[docs/98.archive/changes/chg-0003-02-auth-standardization/plan.md](../../../98.archive/changes/chg-0003-02-auth-standardization/plan.md) |

## Path Role Coverage

| Role | Paths |
| --- | ---: |
| JSON registry | 74 |
| Markdown reference | 854 |
| YAML config | 115 |
| folder index | 125 |
| script | 59 |
| source path | 27 |
| text entrypoint | 4 |

## Sources

- [LLM Wiki generated index](../../llm-wiki/ref-0082-llm-wiki-index.md) - full safe path index
- [LLM Wiki repository map](../../llm-wiki/ref-0083-repository-map.md) - curated canonical source map
- [generate-llm-wiki.py](../../../../scripts/knowledge/generate-llm-wiki.py) - deterministic two-output generator
- [script manifest checker](../../../../scripts/validation/check-script-manifest.py) - aggregate generated-output freshness gate

## Maintenance

- **Owner**: `doc-writer` using the `knowledge-map-agent` function.
- **Review Cadence**: Review after root entrypoint, governance, operations, script inventory, infrastructure index, or LLM Wiki path changes.
- **Update Trigger**: Run `python3 scripts/knowledge/generate-llm-wiki.py --write` after in-scope path changes and `python3 scripts/knowledge/generate-llm-wiki.py --check` during validation.

## Related Documents

- [Knowledge reference data](./README.md)
- [Reference data](../README.md)
- [LLM Wiki references](../../llm-wiki/README.md)
- [LLM Wiki maintenance guide](../../../05.operations/catalog/00-workspace/ops-0007-llm-wiki-maintenance/guide.md)
