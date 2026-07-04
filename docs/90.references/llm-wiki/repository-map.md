---
status: active
---
<!-- Target: docs/90.references/llm-wiki/repository-map.md -->

# Reference: LLM Wiki Repository Map

## Overview

This reference lists the canonical tracked source files that LLM agents should check first when reading `hy-home.docker`. It helps agents quickly find repository documentation, governance, infrastructure, script, and secret-handling boundaries.

## Purpose

Provide a repo-local exploration order so LLM agents do not confuse runtime truth with reference context. Root [`llms.txt`](../../../llms.txt) is a thin entrypoint to this document, and this document does not replace active policy or original runtime configuration.

## Repository Role

This reference is the curated repository map for the LLM Wiki. It provides exploration paths based on tracked files. Policy decisions are checked in `docs/00.agent-governance/`, operations decisions in `docs/05.operations/`, and latest runtime truth in `infra/`, `scripts/`, registry JSON files, and Docker Compose files.

Graphify output is only a navigation aid. Even when `graphify-out/` exists, do not treat it as an authoritative source. If `bash scripts/knowledge/report-graphify-health.sh` reports `status=advisory`, recheck all structural judgments against canonical tracked source files.

## Scope

### In Scope

- tracked source files that LLM agents should read first
- docs taxonomy, agent governance, infrastructure, scripts, and secret-handling entrypoints
- boundaries for `secrets/`, `volumes/`, and `graphify-out/`
- maintenance rules for repo-local LLM Wiki outputs

### Out of Scope

- public wiki site, deployed wiki, full-content bundle, `llms-full.txt`
- Graphify publication wiring or regeneration policy
- Docker Compose runtime changes
- external model calls, network publishing, deployment workflows
- secret values, credentials, private keys, tokens, shell history, raw logs

## Definitions / Facts

- **LLM Wiki**: Repo-local exploration reference made of root `llms.txt` and `docs/90.references/llm-wiki/`.
- **Generated tracked repo-local index**: Path-only index refreshed by `scripts/knowledge/generate-llm-wiki-index.sh`.
- **Tracked source files**: README files, governance docs, operations docs, Compose files, scripts, and registry JSON files tracked by Git.
- **Runtime truth**: `infra/`, `scripts/`, registry JSON files, Docker Compose files, and `docs/00.agent-governance/` documents that directly define current runtime configuration and validation criteria.
- **Advisory graph context**: Supporting material such as `graphify-out/` output that may be used only as exploration hints and must not be promoted to canonical evidence.

## Repository Map

| Need | Canonical Source | Notes |
| --- | --- | --- |
| Repository overview | [README.md](../../../README.md) | human-facing root hub |
| Agent execution rules | [AGENTS.md](../../../AGENTS.md) | provider-neutral entry shim |
| Documentation taxonomy | [docs/README.md](../../README.md) | active stage routing |
| Agent governance | [docs/00.agent-governance/README.md](../../00.agent-governance/README.md) | repo-local governance SSOT |
| Infrastructure layout | [infra/README.md](../../../infra/README.md) | Compose tier and service map |
| Script inventory | [scripts/README.md](../../../scripts/README.md) | validator and automation map |
| Secret handling | [secrets/README.md](../../../secrets/README.md) | path and policy context only |
| Docker reference context | [docs/90.references/data/docker/README.md](../data/docker/README.md) | stable Docker interpretation rules |
| LLM entrypoint | [llms.txt](../../../llms.txt) | thin machine-readable entrypoint |
| LLM generated index | [llm-wiki-index.md](./llm-wiki-index.md) | generated tracked repo-local path index |
| LLM maintenance guide | [docs/05.operations/guides/00-workspace/llm-wiki-maintenance.md](../../05.operations/guides/00-workspace/llm-wiki-maintenance.md) | refresh and validation procedure |

## Source Rules

- Prefer tracked source files over generated artifacts.
- Use repo-relative links for local files.
- Do not quote or summarize secret values, credentials, private keys, tokens, shell history, or raw logs.
- Treat `secrets/` paths as policy context only unless the user explicitly asks for a task that requires more.
- Exclude `volumes/`, dependency trees, generated/minified artifacts, and `graphify-out/` from authoritative evidence.
- Re-run repository validators after changing this reference or the root LLM entrypoint.

## Sources

- [README.md](../../../README.md) - repository purpose, map, verification entrypoints
- [AGENTS.md](../../../AGENTS.md) - agent bootstrap, Graphify boundary, verification contract
- [docs/README.md](../../README.md) - docs taxonomy, template mapping, contract validation
- [docs/90.references/README.md](../README.md) - reference stage role and lifecycle
- [scripts/validation/check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) - repository contract validation
- [scripts/knowledge/report-graphify-health.sh](../../../scripts/knowledge/report-graphify-health.sh) - advisory Graphify health reporting

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when root README, docs taxonomy, agent governance, script inventory, or secret-handling docs change
- **Update Trigger**: Update when canonical entrypoints move, new tracked-source evidence boundaries are added, or LLM Wiki contract validation changes

## Related Documents

- [LLM Wiki references](./README.md)
- [LLM Wiki generated index](./llm-wiki-index.md)
- [LLM Wiki maintenance guide](../../05.operations/guides/00-workspace/llm-wiki-maintenance.md)
- [LLM entrypoint](../../../llms.txt)
- [90.references](../README.md)
- [docs index](../../README.md)
- [agent governance hub](../../00.agent-governance/README.md)
