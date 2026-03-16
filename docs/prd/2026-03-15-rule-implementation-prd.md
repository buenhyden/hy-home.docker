---
title: 'Agent Rule Implementation and Document Refinement PRD'
status: 'Approved'
version: 'v1.0.0'
owner: 'buenhyden'
stakeholders: ['buenhyden']
scope: 'master'
tags: ['prd', 'requirements', 'agentic', 'rules']
layer: 'product'
---

# Agent Rule Implementation and Document Refinement PRD

> **Status**: Approved
> **Target Version**: v1.0.0
> **Owner**: buenhyden
> **Stakeholders**: buenhyden
> **Scope**: master
> **layer:** product

**Overview (KR):** AI Agent의 작업 효율성을 극대화하기 위해 루트 지침 파일(`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`)에 의도 기반 규칙 로딩 체계를 구축하고, 저장소의 핵심 문서들을 최신 템플릿과 경로 표준에 맞춰 정제합니다.

## Vision

A seamless AI-collaboration environment where agents automatically load the most relevant rules for any given task, backed by a perfectly structured documentation hierarchy.

## Requirements

- **[REQ-RULE-01] Uniform Rule Triggers**: `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` must share a consistent trigger mechanism (e.g., `[LOAD:RULES:<NAME>]`).
- **[REQ-RULE-02] Lazy Loading Alignment**: Rule triggers must point to modular files in `docs/agentic/rules/`.
- **[REQ-RULE-03] Skill Autonomy Mandate**: Root agent files must explicitly state that no skills are restricted.
- **[REQ-RULE-04] Path Standardization**:
  - ADR: `docs/adr/`
  - ARD: `docs/ard/`
  - Incident: `docs/operations/incidents/`
  - Postmortem: `docs/operations/postmortems/`
  - Plan: `docs/plans/`
  - Spec: `docs/specs/`
  - PRD: `docs/prd/`
  - Runbook: `docs/runbooks/`
- **[REQ-RULE-05] Layer Metadata**: All files must contain `layer:` metadata.

## Success Criteria

- Agents can load specialized rules directly from root-level prompts.
- All core documents are reorganized into the prescribed flattened directory structure.
- Redundant content between root files and `docs/agentic/` is minimized.

## Related

- `[../ard/rule-refactor-ard.md]`
- `[../specs/2026-03-15-rule-refactor-spec.md]`
