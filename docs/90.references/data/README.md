---
status: active
---

<!-- Target: docs/90.references/data/README.md -->

# Reference Data

> stable reference data, profiles, inventories, and glossary material

## Overview

`docs/90.references/data`는 active stage 문서가 반복해서 참조하는 stable data와 interpretation context를 관리합니다. 이 category는 glossary, HADS profile, Docker/Kubernetes 해석 규칙처럼 느리게 변하는 reference material을 담습니다.

이 category는 runtime source of truth가 아닙니다. 최신 Compose, registry, validator, script, secret-handling 원문은 `infra/`, `scripts/`, `secrets/`, `docs/00.agent-governance/`가 담당합니다.

## Category Role

`docs/90.references/data`는 Stage 90의 안정 데이터 축입니다. 구조화된 reference data와 interpretation profile을 모으되, 학습 로드맵은 [learning](../learning/README.md), LLM 탐색 인덱스는 [llm-wiki](../llm-wiki/README.md), 연구 분석은 [research](../research/README.md), 감사·비교 보고서는 [audits](../audits/README.md)에 둡니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Docker image/version interpretation references
- Generated Docker Compose profile/service coverage inventory
- Stable governance routing reference data
- Stable agent-output eval fixture reference data
- Stable glossary and stage-boundary vocabulary
- HADS profile and validation boundary
- Generated LLM Wiki coverage and knowledge-index reference data
- Kubernetes/k3s/k3d migration reference context

### Out of Scope

- Source-backed research packs
- Audit reports and implementation-status comparison reports
- Learning roadmap and theory references
- Repo-local LLM Wiki generated index and repository map
- Active policy, plan, task evidence, runbook, incident, or postmortem
- Runtime configuration source files or secret values

## Structure

```text
data/
├── README.md      # This file
├── docker/        # Docker image/version and registry interpretation
├── glossary/      # Stable vocabulary and stage-boundary terms
├── governance/    # Governance routing and validation reference data
├── hads/          # HADS reference profile and validator boundary
├── knowledge/     # Generated LLM Wiki coverage and knowledge-index data
└── kubernetes/    # Kubernetes and k3s/k3d migration reference context
```

## Current References

- [docker/README.md](./docker/README.md) - Docker image/version drift, registry, and runtime reference rules
- [docker/compose-profile-service-coverage.md](./docker/compose-profile-service-coverage.md) - generated Docker Compose profile/service coverage snapshot
- [docker/image-version-interpretation.md](./docker/image-version-interpretation.md) - Docker image/version source interpretation rules
- [glossary/README.md](./glossary/README.md) - stable reference terminology category
- [glossary/stable-reference-terms.md](./glossary/stable-reference-terms.md) - shared terms for reference-stage boundaries
- [governance/README.md](./governance/README.md) - governance routing reference data category
- [governance/agent-output-eval-fixtures.md](./governance/agent-output-eval-fixtures.md) - agent-output eval fixture catalog for docs, provider, and infra tasks
- [governance/gap-to-stage-routing.md](./governance/gap-to-stage-routing.md) - Stage 00 gap-to-stage routing advisory reference
- [hads/README.md](./hads/README.md) - HADS profile category
- [hads/profile.md](./hads/profile.md) - HADS profile and validation contract
- [knowledge/README.md](./knowledge/README.md) - generated LLM Wiki coverage and knowledge-index data category
- [knowledge/llm-wiki-stage-category-coverage.md](./knowledge/llm-wiki-stage-category-coverage.md) - generated LLM Wiki source-bucket/category coverage snapshot
- [kubernetes/README.md](./kubernetes/README.md) - Kubernetes and k3s/k3d migration reference context
- [kubernetes/docker-compose-to-k3s-migration.md](./kubernetes/docker-compose-to-k3s-migration.md) - Docker Compose to k3s/k3d migration suitability snapshot

## How to Work in This Area

1. Use this category for stable data or interpretation material only.
2. Put learning roadmaps under [learning](../learning/README.md).
3. Put LLM navigation output under [llm-wiki](../llm-wiki/README.md).
4. Put research analysis under [research](../research/README.md).
5. Put stable audit reports under [audits](../audits/README.md).
6. New non-README reference docs must follow [reference.template.md](../../99.templates/templates/common/reference.template.md).
7. Update this README and [90.references](../README.md) when adding, moving, or deleting data references.
8. Run `bash scripts/validation/check-repo-contracts.sh` after changing reference data docs or generated-index paths.

## Related Documents

- [90.references](../README.md)
- [audit references](../audits/README.md)
- [learning references](../learning/README.md)
- [LLM Wiki references](../llm-wiki/README.md)
- [research references](../research/README.md)
- [reference template](../../99.templates/templates/common/reference.template.md)
- [documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
