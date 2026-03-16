---
title: '2026-03 Documentation & Agent Rule Alignment PRD'
status: 'Approved'
version: 'v1.1.0'
owner: 'buenhyden'
tags: ['prd', 'requirements', 'agentic']
layer: product
---

# 2026-03 Documentation & Agent Rule Alignment PRD

**Overview (KR):** 2026년 3월 최신 기준에 따라 에이전트 지침 및 문서 구조를 정렬하여 지능형 자동화 효율성을 극대화합니다.

## Requirements

- **[REQ-ALGN-01] Path Perfect Linkage**: All root links must point to specific categories (`docs/plans/`, `docs/runbooks/`, etc.).
- **[REQ-ALGN-02] Intent Trigger Matrix**: Implement `[LOAD:RULES:*]` in `AGENTS.md` and `GEMINI.md`.
- **[REQ-ALGN-03] Persona Guidance**: Direct Gemini to use higher-intelligence profiles (Reasoner) for spec/plan tasks.
- **[REQ-ALGN-04] Skill Autonomy Clause**: "No restricted skills" must be explicitly stated in all root instruction shims.
- **[REQ-ALGN-05] Template Consistency**: Every document must use the exact filenames specified in `templates/`.

## Success Criteria

- Grep for `[LOAD:RULES:` returns results in both `AGENTS.md` and `GEMINI.md`.
- No broken relative links in the `docs/` index.
- 100% metadata coverage.
