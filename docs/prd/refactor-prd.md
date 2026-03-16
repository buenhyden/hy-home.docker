---
layer: agentic
---
# PRD-0001: Documentation Taxonomy and Agentic Refactor

- **Status**: Canonical
- **Owner**: buenhyden
- **layer:** product

**Overview (KR):** 인프라 리포지토리의 문서 유발성(Discoverability)을 높이고 AI Agent의 컨텍스트 비대화를 방지하기 위해 평탄화된 문서 구조와 지능형 레이지 로딩 시스템을 구축합니다.

## 1. Product Context

The `hy-home.docker` repository suffers from minor path inconsistencies and context bloat during AI agent sessions. To improve developer experience and agent reliability, we need a strict, type-first hierarchy.

## 2. User Stories

- **Developer**: I want a predictable document pathing system so I can find specs and plans immediately.
- **AI Agent**: I want to trigger task-specific rules without loading the entire instruction set, saving context tokens.

## 3. Functional Requirements

- **[REQ-FUN-01] Path Pluralization**: implementation artifacts (`plans`, `specs`) and operations (`runbooks`) must use plural names.
- **[REQ-FUN-02] Flat Hierarchy**: strictly one level of categorization under `docs/`.
- **[REQ-FUN-03] Lazy-Loading Hub**: `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` must be trigger-based shims.
- **[REQ-FUN-04] Metadata Enforcement**: `layer:` must be present in every Markdown file.

## 4. Non-Functional Requirements

- **[REQ-NFR-01] Backward Compatibility**: Critical links in `README.md` and `ARCHITECTURE.md` must be updated to prevent 404s.
- **[REQ-NFR-02] Performance**: Gateway files must stay compact for near-instant loading.
