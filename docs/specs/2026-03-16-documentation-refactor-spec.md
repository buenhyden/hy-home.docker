---
title: 'Documentation and Agent Instruction Refactor Specification'
status: 'Canonical'
version: '1.0'
owner: 'buenhyden'
scope: 'master'
prd_reference: '../prd/2026-03-16-documentation-standardization-prd.md'
arch_reference: '../ard/documentation-system-ard.md'
decision_reference: '../adr/0026-documentation-structure-and-lazy-loading.md'
tags: ['spec','implementation']
layer: 'specs'
---

# Documentation and Agent Instruction Refactor Specification

> **Status**: Canonical
> **Scope**: master
> **layer:** specs
> **Related PRD**: [2026-03-16-documentation-standardization-prd.md](../prd/2026-03-16-documentation-standardization-prd.md)
> **Related Architecture**: [2026-03-15-doc-taxonomy-ard.md](../ard/2026-03-15-doc-taxonomy-ard.md)
> **Decision Record**: [0026-documentation-structure-and-lazy-loading.md](../adr/0026-documentation-structure-and-lazy-loading.md)

**Overview (KR):** 에이전트 지침 최적화 및 문서 구조 표준화를 위한 기술적 명세를 정의합니다. Lazy Loading 구현 방식과 디렉토리 구조 변경 계획을 포함합니다.

## Technical or Platform Baseline

This spec operates on the `hy-home.docker` repository's documentation directory (`docs/`) and the root management files. It leverages agent-driven markers for conditional context loading.

## Contracts

- **[REQ-SPC-FUN-01] Agent Metadata Contract**: All markdown files MUST have YAML frontmatter with `layer: <category>`.
- **[REQ-SPC-FUN-02] Naming Contract**: Plans must use `YYYY-MM-DD-feature.md` format.
- **[REQ-SPC-FUN-03] Lazy Loading Contract**: Rule files in `docs/agentic/rules/` are excluded from the default prompt and only included when a `[LOAD:RULES:<NAME>]` trigger is matched.

## 5. Component Breakdown

- **`docs/agentic/gateway.md`**: Updated to serve as the routing table for rules and category indexes.
- **`docs/agentic/instructions.md`**: Stripped of specialized logic; contains only cross-cutting behavioral standards.
- **`docs/agentic/rules/*.md`**: Granular, single-responsibility rule files with explicit markers.
- **`ARCHITECTURE.md`**: Updated with correct links and `layer: core` metadata.
- **`README.md`**: Links to promoted `CONTRIBUTING.md` and `COLLABORATING.md`.

## Verification

```bash
# Verify layer metadata presence
grep -r "layer:" docs/ | head -n 20

# Verify Lazy Loading markers
grep -r "\[LOAD:RULES:" docs/agentic/gateway.md
```
