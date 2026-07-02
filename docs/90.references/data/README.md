---
status: active
---

<!-- Target: docs/90.references/data/README.md -->

# Reference Data

> stable reference data, profiles, generated indexes, inventories, and glossary material

## Overview

`docs/90.references/data`는 active stage 문서가 반복해서 참조하는 stable data와 interpretation context를 관리합니다. 이 category는 glossary, HADS profile, LLM Wiki index, Docker/Kubernetes 해석 규칙, 학습 로드맵처럼 느리게 변하는 reference material을 담습니다.

이 category는 runtime source of truth가 아닙니다. 최신 Compose, registry, validator, script, secret-handling 원문은 `infra/`, `scripts/`, `secrets/`, `docs/00.agent-governance/`가 담당합니다.

## Category Role

`docs/90.references/data`는 Stage 90의 안정 데이터 축입니다. 구조화된 reference data와 machine-readable 성격의 generated index를 모으되, 연구 분석은 [research](../research/README.md), 감사·비교 보고서는 [audits](../audits/README.md)에 둡니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Docker image/version interpretation references
- Stable glossary and stage-boundary vocabulary
- HADS profile and validation boundary
- Kubernetes/k3s/k3d migration reference context
- CS/CE/SE learning roadmap references
- Repo-local LLM Wiki generated index and repository map

### Out of Scope

- Source-backed research packs
- Audit reports and implementation-status comparison reports
- Active policy, plan, task evidence, runbook, incident, or postmortem
- Runtime configuration source files or secret values

## Structure

```text
data/
├── README.md      # This file
├── docker/        # Docker image/version and registry interpretation
├── glossary/      # Stable vocabulary and stage-boundary terms
├── hads/          # HADS reference profile and validator boundary
├── kubernetes/    # Kubernetes and k3s/k3d migration reference context
├── learning/      # Learning roadmap and theory references
└── llm-wiki/      # Repo-local LLM navigation map and generated path index
```

## Current References

- [docker/README.md](./docker/README.md) - Docker image/version drift, registry, and runtime reference rules
- [docker/image-version-interpretation.md](./docker/image-version-interpretation.md) - Docker image/version source interpretation rules
- [glossary/README.md](./glossary/README.md) - stable reference terminology category
- [glossary/stable-reference-terms.md](./glossary/stable-reference-terms.md) - shared terms for reference-stage boundaries
- [hads/README.md](./hads/README.md) - HADS profile category
- [hads/profile.md](./hads/profile.md) - HADS profile and validation contract
- [kubernetes/README.md](./kubernetes/README.md) - Kubernetes and k3s/k3d migration reference context
- [kubernetes/docker-compose-to-k3s-migration.md](./kubernetes/docker-compose-to-k3s-migration.md) - Docker Compose to k3s/k3d migration suitability snapshot
- [learning/README.md](./learning/README.md) - Docker-based infrastructure learning roadmap and theory references
- [llm-wiki/README.md](./llm-wiki/README.md) - repo-local LLM Wiki entrypoint and tracked-source repository map
- [llm-wiki/repository-map.md](./llm-wiki/repository-map.md) - curated tracked-source repository map
- [llm-wiki/index.md](./llm-wiki/index.md) - generated tracked repo-local path index

## How to Work in This Area

1. Use this category for stable data or interpretation material only.
2. Put research analysis under [research](../research/README.md).
3. Put stable audit reports under [audits](../audits/README.md).
4. New non-README reference docs must follow [reference.template.md](../../99.templates/templates/common/reference.template.md).
5. Update this README and [90.references](../README.md) when adding, moving, or deleting data references.
6. Run `bash scripts/validation/check-repo-contracts.sh` after changing reference data docs or generated-index paths.

## Related Documents

- [90.references](../README.md)
- [audit references](../audits/README.md)
- [research references](../research/README.md)
- [reference template](../../99.templates/templates/common/reference.template.md)
- [documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
