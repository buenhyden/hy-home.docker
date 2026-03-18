---
title: 'ADR 0017: Flat Documentation Taxonomy and Layer Metadata'
status: 'Accepted'
date: '2026-03-14'
authors: ['Antigravity']
deciders: ['buenhyden']
tags: ['adr', 'documentation', 'taxonomy']
layer: architecture
---

# ADR 0017: Flat Documentation Taxonomy and Layer Metadata

- **Status:** Accepted
- **Date:** 2026-03-14
- **Scope:** master
- **layer:** architecture
- **Authors:** Antigravity

**Overview (KR):** 문서의 복잡도를 낮추고 AI 에이전트의 가독성을 높이기 위해, 깊은 계층 구조 대신 역할 기반의 평탄화된 폴더 구조를 채택하고 모든 파일에 `layer` 메타데이터를 추가하기로 결정했습니다.

## Context

The previous documentation structure was either fragmented or relied on inconsistent nesting. AI agents often struggled to locate related documents (e.g., finding the runbook related to a specific spec) without performing expensive directory scans or broad `grep` operations. Furthermore, there was no standardized way to track which architectural layer a document belonged to.

## Decision

- **[DEC-01]** Adopt a role-based flat taxonomy. All documentation must live in one of the following root folders: `adr, ard, prd, specs, plans, runbooks, operations, context, guides, manuals, agentic`.
- **[DEC-02]** Mandatory `layer` metadata. Every file in the documentation set must include a `layer` key in the YAML frontmatter and a Markdown metadata block.
- **[DEC-03]** Gateway-Based Discovery. Agents must load `docs/agentic/gateway.md` first and use named markers (`[LOAD:CATEGORY]`) instead of path guessing.

## Consequences

- **Positive**: Reduced context window pollution (lazy loading), clear traceability between requirement and implementation, and standardized metadata for future automation.
- **Trade-off**: Requires strict manual or automated enforcement when creating new files.
- **Limitation**: Does not resolve historical inconsistency in legacy document *content* (only structure).

## Related

- `[../specs/2026-03-15-refactor-docs-spec.md]`
- `[../ard/2026-03-15-doc-taxonomy-ard.md]`
- `[../prd/2026-03-15-refactor-docs-prd.md]`
