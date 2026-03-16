---
title: 'Documentation and Agent Instruction Refactor PRD'
status: 'Approved'
version: 'v1.0.0'
owner: 'buenhyden'
stakeholders: ['buenhyden']
scope: 'master'
parent_epic: 'N/A'
tags: ['prd', 'requirements', 'agentic', 'documentation']
layer: 'product'
---

# Documentation and Agent Instruction Refactor PRD

> **Status**: Approved
> **Target Version**: v1.0.0
> **Owner**: buenhyden
> **Stakeholders**: buenhyden
> **Scope**: master
> **layer:** product

**Overview (KR):** 본 문서는 `hy-home.docker` 저장소의 문서 구조와 AI Agent 지침을 리팩토링하여 문서의 발견 가능성을 높이고, 필요한 정보만 선택적으로 로드(Lazy Loading)하는 체계를 구축하기 위한 요구사항을 정의합니다.

## Vision

To create a highly discoverable, structured, and efficient documentation system that enables both humans and AI agents to find and utilize relevant information with minimal context overhead.

## Requirements

- **[REQ-PRD-DR-01] Flat Taxonomy**: All management documents must reside in specific subdirectories under `docs/` (e.g., `docs/adr/`, `docs/prd/`) without deep nesting.
- **[REQ-PRD-DR-02] Metadata Requirements**: Every Markdown file must include a `layer:` key in its YAML frontmatter.
- **[REQ-PRD-DR-03] Template Consistency**: All new ADR, ARD, PRD, Spec, Plan, Runbook, Incident, and Postmortem files must use repository-defined templates.
- **[REQ-PRD-DR-04] Lazy Loading Protocol**: AI agents must be guided to load only the necessary context based on their current intent.
- **[REQ-PRD-DR-05] Central Gateway**: `docs/agentic/gateway.md` must serve as the primary entry point for agent discovery.
- **[REQ-PRD-DR-06] Skill Autonomy**: Agents must be explicitly allowed to use any relevant skill from their toolkit without restriction.

## Success Criteria

- All core root files (`ARCHITECTURE.md`, `README.md`, etc.) have correct `layer:` metadata and up-to-date links.
- `docs/agentic/gateway.md` correctly maps intents to rule files and doc categories.
- New management documents for this refactoring cycle are created and valid.
- Agents can successfully follow the discovery protocol to load relevant rules.

## Related

- `[../ard/doc-refactor-ard.md]`
- `[../specs/doc-refactor-spec.md]`
- `[../plans/doc-refactor-plan.md]`
- `[../adr/lazy-loading-adr.md]`
