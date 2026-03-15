---
title: '2026-03 Documentation Refactor PRD'
status: 'Approved'
version: 'v1.0.0'
owner: 'buenhyden'
layer: 'product'
---

# 2026-03 Documentation Refactor PRD

**Overview (KR):** 본 문서는 저장소의 문서 구조와 에이전트 규칙을 리팩토링하기 위한 제품 요구사항을 정의합니다. 사용자 경험(UX) 관점에서 문서 탐색 효율성을 극대화하는 것이 목표입니다.

## 1. Vision

Provide a seamless onboarding and operational experience for both AI agents and human collaborators through standardized documentation paths and rule loading protocols.

## 2. Requirements

- **[REQ-PRD-REF-01]** Root redirection files (`CONTRIBUTING.md`, `COLLABORATING.md`) must be reviewed and their essential content integrated into agent entrypoints.
- **[REQ-PRD-REF-02]** Every document must have a `layer` key indicating its tier (e.g., `core`, `ops`, `agentic`, `meta`).
- **[REQ-PRD-REF-03]** Agent entrypoints must use lazy loading to minimize context window usage.

## 3. Success Criteria

- All files in `docs/` follow the plural taxonomy.
- `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` are unified in logic but specialized in triggers.
- Clear path for "Refactoring", "Documentation", "Infrastructure", and "Operations" intents.
