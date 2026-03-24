---
title: 'Meta-Documentation & Agentic Framework PRD'
status: 'Draft'
version: 'v1.1.0'
owner: 'Antigravity'
stakeholders: ['buenhyden']
scope: 'repository-wide'
tags: ['prd', 'agentic', 'meta']
layer: 'meta'
---

# Meta-Documentation & Agentic Framework PRD

**Overview (KR):** 문서 자체를 실행 가능한 지침으로 활용하는 "Doc-as-Instruction" 시스템을 구축하여 에이전트의 수행 능력을 극대화하기 위한 프레임워크 요구사항입니다.

## 1. Vision

To create a "Doc-as-Instruction" system where the repository's documentation is not just human-readable, but explicitly structured to guide AI Agents with minimal context overhead via lazy loading and intent-based discovery.

## 2. Requirements

- **[REQ-META-01] Content Decomposition**: Root-level files (`README`, `ARCHITECTURE`) should be stripped of process/procedural details. Those details must move to `docs/guides/` or `docs/manuals/`.
- **[REQ-META-02] Intent-Based Discovery**: The `gateway.md` must provide clear entry points for specific *tasks* (e.g., "Refactoring", "Debugging", "Infrastructure Deploy").
- **[REQ-META-03] Lazy Loading Implementation**: Agent rules must be modular. Each rule should be a distinct file in `docs/agentic/rules/`.
- **[REQ-META-04] Universal Metadata**: Every documentation file in the repository must include a `layer` key in its frontmatter.

## 3. Success Criteria

- Root `README.md` is reduced to < 300 lines.
- AI Agents can perform a task by loading only the `gateway.md` and one task-specific `rule.md`.
- 100% compliance with `layer:` metadata.
