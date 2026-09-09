---
title: "Reference: LLM Wiki Repository Map"
version: "1.1.0"
type: "reference/data-pack"
status: "published"
owner: "@buenhyden"
updated: "2026-09-09"
layer: "references"
artifact_id: "DATA-0083"
parent_ids: []
created: "2026-08-23"
observed_at: "2026-08-23"
---

# Reference: LLM Wiki Repository Map

## Overview

This reference describes the repo-local LLM Wiki: which files make it up, which of them are generated, and which document owns each question it used to answer itself.

## Purpose

Describe what the repo-local LLM Wiki consists of and how its members relate, so a reader knows which file to open for which question.

This package is not the entry-point list and not the rule set. Root [`llms.txt`](../../../../llms.txt) owns the canonical entry points and the evidence boundaries an LLM agent must respect, and the agent knowledge category owns surface-to-authority routing with the approval and proving check for each surface. Both were previously restated here, and each restatement was one more place to drift.

Nothing in this package is an obligation. The entry-point list and the evidence
boundaries are in `llms.txt`. Surface ownership, the approval boundary and the
proving check for each surface are in `.agents/knowledge/repository-map.md`.
Document authoring and retirement rules are in
`.agents/governance/documentation-protocol.md`.

## Repository Role

This reference describes the LLM Wiki package set. Exploration order comes from `llms.txt`; surface ownership comes from the agent knowledge repository map; policy stays in `.agents/`, operations in Stage 05, and runtime truth in `infra/`, `scripts/`, registry JSON files, and Docker Compose files.

Graphify output is only a navigation aid. Even when `graphify-out/` exists, do not treat it as an authoritative source. If `bash scripts/knowledge/report-graphify-health.sh` reports `status=advisory`, recheck all structural judgments against canonical tracked source files.

## Scope

### In Scope

- the LLM Wiki member list and how each member is refreshed
- the routing from a wiki question to the document that owns its answer

### Out of Scope

- the canonical entry-point list and evidence boundaries, owned by `llms.txt`
- surface ownership, approval boundaries and proving checks, owned by
  `.agents/knowledge/repository-map.md`
- public wiki site, deployed wiki, full-content bundle, `llms-full.txt`
- Graphify publication wiring or regeneration policy
- Docker Compose runtime changes
- external model calls, network publishing, deployment workflows
- secret values, credentials, private keys, tokens, shell history, raw logs

## Definitions / Facts

- **LLM Wiki**: Repo-local exploration reference made of root `llms.txt`, the generated index, its coverage report, and this description.
- **Generated tracked repo-local index**: Path-only index refreshed by `scripts/knowledge/generate-llm-wiki.py`.
- **Tracked source files**: README files, governance docs, operations docs, Compose files, scripts, and registry JSON files tracked by Git.
- **Runtime truth**: `infra/`, `scripts/`, registry JSON files, Docker Compose files, and `.agents/` documents that directly define current runtime configuration and validation criteria.
- **Advisory graph context**: Supporting material such as `graphify-out/` output that may be used only as exploration hints and must not be promoted to canonical evidence.

## Sources

- [README.md](../../../../README.md) - repository purpose, map, verification entrypoints
- [AGENTS.md](../../../../AGENTS.md) - agent bootstrap, Graphify boundary, verification contract
- [docs/README.md](../../../README.md) - docs taxonomy, template mapping, contract validation
- [docs/90.references/README.md](../../README.md) - reference stage role and lifecycle
- [scripts/validation/run-ci-gate.py](../../../../scripts/validation/run-ci-gate.py) - public repository contract validation across six suites
- [scripts/knowledge/report-graphify-health.sh](../../../../scripts/knowledge/report-graphify-health.sh) - advisory Graphify health reporting

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when root README, docs taxonomy, agent governance, script inventory, or secret-handling docs change
- **Update Trigger**: Update when canonical entrypoints move, new tracked-source evidence boundaries are added, or LLM Wiki contract validation changes

## Related Documents

- [Reference Data index](../README.md)
- [LLM Wiki generated index](../0082-llm-wiki-index/README.md)
- [LLM Wiki maintenance guide](../../../05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/guide.md)
- [LLM entrypoint](../../../../llms.txt)
- [90.references](../../README.md)
- [docs index](../../../README.md)
- [agent governance hub](../../../../.agents/README.md)

## Schema

This package preserves its existing data evidence under the Stage 99 `data` contract.

## Provenance

This package preserves its existing data evidence under the Stage 99 `data` contract.

## Inventory

This package preserves its existing data evidence under the Stage 99 `data` contract.

| Member | Kind | Refreshed by |
| --- | --- | --- |
| `llms.txt` | root machine entrypoint; owns entry points and boundaries | authored |
| `docs/90.references/data/0082-llm-wiki-index/` | tracked path index | `scripts/knowledge/generate-llm-wiki.py` |
| `docs/90.references/data/0076-llm-wiki-stage-category-coverage/` | stage and category coverage of the same candidate set | the same generator |
| this package | what the wiki is and how its members relate | authored |

The maintenance procedure is a Stage 05 subject: `docs/05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/`.

## Refresh

This package preserves its existing data evidence under the Stage 99 `data` contract.

## Consumers

This package preserves its existing data evidence under the Stage 99 `data` contract.

## Traceability

This package preserves its existing data evidence under the Stage 99 `data` contract.
