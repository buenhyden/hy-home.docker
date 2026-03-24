---
layer: agentic
---
# PRD-0002: Deep Taxonomy Alignment & Agent Optimization

- **Status**: Draft
- **Owner**: buenhyden
- **layer:** product

**Overview (KR):** 리포지토리의 모든 문서를 March 2026 표준에 따라 완전하게 재정렬하고, AI Agent의 스킬 자율성(Autonomy)을 보장하는 지능형 엔트리포인트 시스템을 구축합니다.

## 1. Objectives

- Ensure 100% compliance with "# 필수 사항" directory naming.
- Refactor AGENTS.md, CLAUDE.md, GEMINI.md into lightweight triggers.
- Remove legacy `docs/plan_tmp/` and consolidate implementation plans.
- Explicitly authorize full skill access for all AI personas.

## 2. Success Criteria

- No functional links point to singular `plan` or `spec` directories.
- Every Markdown file in the repo contains `layer:` in its frontmatter.
- Root shims are < 20 lines and effectively trigger gateway routing.
